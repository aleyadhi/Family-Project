from django.urls import path
from app.views import (
    home_view,
    family_view,
    details_view,
    create_view,
    update_view,
    details_hx_view,
    details_update_hx_view,
)

from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

app_name = 'family'
urlpatterns = [
    path('', home_view, name='home'),
    path('family/', family_view, name='family'),
    path('family/create', create_view, name='create'),
    path('family/<slug:slug>/detail/<int:id>', details_update_hx_view, name='hx-detail-details'),
    path('family/<slug:slug>/detail/', details_update_hx_view, name='hx-detail-create'),
    path('family/hx/<slug:slug>', details_hx_view, name='hx-details'),
    path('family/<slug:slug>', details_view, name='details'),
    path('family/<slug:slug>/update', update_view, name='update'),
    path('hello', login_required(TemplateView.as_view(template_name='hello.html')), name='hello'),
    
]