# trips/urls.py
from django.urls import path
from . import views
from .views import add_trip,home

urlpatterns = [
    # This line will map the URL "trips/" to the view "home" in views.py
    path('', views.home, name='home'), 
    path('add/', add_trip, name='add_trip'),
    path('edit/<int:trip_id>/', views.edit_trip, name='edit_trip'),
    path('delete/<int:trip_id>/', views.delete_trip, name='delete_trip'),
    path('review/', views.review_page, name='review_page'),
   

    # Path to edit a specific review
    path('review/edit/<int:review_id>/', views.edit_review, name='edit_review'),

    # Path to delete a specific review
    # urls.py
    path('review/delete/confirm/<int:review_id>/', views.delete_review_confirm, name='delete_review_confirm'),

    path('review/add_page/', views.add_review_page, name='add_review_page'),
path('review/add/<int:trip_id>/', views.add_review, name='add_review'),
    ]
