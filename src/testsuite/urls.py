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
from .views import index, Generate, StartRun, CancelRun, get_cbeff, settings, RunStatus, get_sample_settings, get_current_config, UploadOverrideSettings


urlpatterns = [
    path('', index),
    re_path(r'^settings\W?$', settings),
    re_path(r'^test\W?$', StartRun.as_view()),
    re_path(r'^generate\W?$', Generate.as_view()),
    re_path(r'^cancel\W?$', CancelRun.as_view()),
    re_path(r'^status\W?$', RunStatus.as_view()),
    # re_path(r'^produce\W?$', InsertEntry.as_view()),
    # re_path(r'^consume\W?$', GetEntry.as_view()),
    path('test_info/<str:run_id>', StartRun.as_view()),
    path('get_cbeff/<str:reference_id>', get_cbeff),
    re_path(r'^get_current_config\W?$', get_current_config),
    re_path(r'^get_sample_settings\W?$', get_sample_settings),
    re_path(r'^upload_override_settings\W?$', UploadOverrideSettings.as_view())
]
