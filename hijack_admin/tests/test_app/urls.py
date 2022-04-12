from from django.urls import re_path
from django.views.generic import TemplateView

urlpatterns = [
    re_path(r'^filter/$', TemplateView.as_view(template_name='hello_filter.html'), name='hello_filter'),
    re_path(r'^$', TemplateView.as_view(template_name='hello.html'), name='hello'),
]
