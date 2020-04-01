#!/bin/bash

job=$$
#source venv/bin/activate
list_descendants ()
{
  local children=$(ps -o pid= --ppid "$1")

  for pid in $children
  do
    list_descendants "$pid"
  done

  echo "$children"
}

cd /opt/abis-testing-kit/src
python3 manage.py runserver 0.0.0.0:8000 --noreload &
P1=$!

python3 orchestration_job.py &
P2=$!

python3 queue_listener_job.py &
P3=$!

python3 dummy_abis.py &
P4=$!

/opt/activemq/bin/activemq start &
P5=$!

PIDs=$(list_descendants $$)

echo "$PIDs" > ./../pid.txt
trap 'kill $PIDs' SIGINT SIGTERM EXIT ERR
#trap 'err=$?; echo >&2 "Exiting on error $err" >> ./../process.log exit $err' ERR

while sleep 5; do
  if ps -p $P1 >/dev/null; then
      echo $P1"Process"
  else
      echo "manage.py runserver failed" >> ./../process.log
      kill "$PIDs" "$$"
  fi
  if ps -p $P2 >/dev/null; then
      echo $P2"Process"
  else
      echo "orchestration_job failed" >> ./../process.log
      kill "$PIDs" "$$"
  fi
  if ps -p $P3 >/dev/null; then
      echo $P3"Process"
  else
      echo "queue_listener_job failed" >> ./../process.log
      kill "$PIDs" "$$"
  fi
  if ps -p $P4 >/dev/null; then
      echo $P4"Process"
  else
      echo "dummy_abis failed" >> ./../process.log
      kill "$PIDs" "$$"
  fi
  if ps -p $P5 >/dev/null; then
      echo $P5"Process"
  else
      echo "activemq crashed" >> ./../process.log
      kill "$PIDs" "$$"
  fi
done