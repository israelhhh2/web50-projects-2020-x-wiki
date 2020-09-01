from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry_name>", views.entry_page, name="entry_title"),
    path("search", views.search, name="search"),
    path("newPage",views.new_page, name="new_page")
]
