"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path
from .views import index, StartRun, CancelRun, get_cbeff, settings, testdata, RunStatus, UploadTestData, \
    get_sample_settings, get_current_config, UploadOverrideSettings, get_current_testdata, get_sample_testdata


urlpatterns = [
    path('', index),
    path('abis/cbeff/<str:reference_id>', get_cbeff),

    re_path(r'^abis/test/run\W?$', StartRun.as_view()),
    re_path(r'^abis/test/cancel\W?$', CancelRun.as_view()),
    re_path(r'^abis/test/status\W?$', RunStatus.as_view()),
    path('abis/test/info/<str:run_id>', StartRun.as_view()),

    re_path(r'^abis/settings\W?$', settings),
    re_path(r'^abis/settings/current\W?$', get_current_config),
    re_path(r'^abis/settings/sample\W?$', get_sample_settings),
    re_path(r'^abis/settings/upload\W?$', UploadOverrideSettings.as_view()),

    re_path(r'^abis/testdata\W?$', testdata),
    re_path(r'^abis/testdata/current\W?$', get_current_testdata),
    re_path(r'^abis/testdata/sample\W?$', get_sample_testdata),
    re_path(r'^abis/testdata/upload\W?$', UploadTestData.as_view()),
    re_path(r'^.*/$', index),
]
