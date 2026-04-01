from django.urls import path
from .views import RoundUpPreviewView

urlpatterns = [
    path('preview-roundup/', RoundUpPreviewView.as_view(), name='preview-roundup'),
]