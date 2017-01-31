from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.ProductListView.as_view(), name='app_home'),
]
