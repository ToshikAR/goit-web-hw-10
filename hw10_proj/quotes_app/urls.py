from django.urls import path

from . import views

app_name = "quotes_app"

urlpatterns = [
    path("", views.main, name="root"),
    path("<int:page>", views.main, name="root_paginate"),
    path("author/<str:id_>", views.author, name="author"),
    path("tag/<str:tag_>", views.tags, name="tags"),
    path("author-add/", views.AuthorView.as_view(), name="author-add"),
    path("quote-add/", views.QuoteView.as_view(), name="quote-add"),
    path("tag-add/", views.TagView.as_view(), name="tag-add"),
    path("fillall/", views.fillAll, name="fillall"),
    path("scrap/", views.scrap, name="scrap"),
]
