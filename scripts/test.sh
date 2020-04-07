#!/bin/bash

job=$$

list_descendants ()
{
  local children=$(ps -o pid= --ppid "$1")

  for pid in $children; do
      if [ "$pid" == "$2" ]; then
          echo "Activemq pid: $pid" > /dev/tty
      else
          list_descendants "$pid"
      fi
  done

  echo "$children"
}

cd ./../src
python3 manage.py runserver 0.0.0.0:8000 --noreload &
P1=$!

python3 orchestration_job.py &
P2=$!

python3 queue_listener_job.py &
P3=$!

python3 dummy_abis.py &
P4=$!

PIDs=$(list_descendants $$)

echo "$PIDs" > ./../pid.txt
trap 'kill $PIDs' SIGINT SIGTERM EXIT ERR
#trap 'err=$?; echo >&2 "Exiting on error $err" >> ./../process.log exit $err' ERR

while sleep 15; do
  if ps -p $P1 >/dev/null; then
      echo $P1": manage.py runserver active"
  else
      echo "manage.py runserver failed"
      kill "$PIDs" "$$"
  fi
  if ps -p $P2 >/dev/null; then
      echo $P2": orchestration_job active"
  else
      echo "orchestration_job failed"
      kill "$PIDs" "$$"
  fi
  if ps -p $P3 >/dev/null; then
      echo $P3": queue_listener_job active"
  else
      echo "queue_listener_job failed"
      kill "$PIDs" "$$"
  fi
  if ps -p $P4 >/dev/null; then
      echo $P4": dummy_abis active"
  else
      echo "dummy_abis failed"
      kill "$PIDs" "$$"
  fi
done