from django.db.models import Count
from django.shortcuts import render

# Create your views here.
# trips/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Trip, Review
from .forms import TripForm, TripYearFilterForm, ReviewForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db import connection

def home(request):
    year_filter_form = TripYearFilterForm(request.GET or None)
    trips = Trip.objects.all()

    # Check if a year has been selected and filter trips accordingly
    if 'year' in request.GET and request.GET['year']:
        trips = trips.filter(start_date__year=request.GET['year'])

    return render(request, 'trip/home.html', {
        'trips': trips,
        'year_filter_form': year_filter_form,  # Pass the form to the template
    })

def add_trip(request):
   
    superuser = User.objects.get(username='chinmay')

    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)  
            trip.user = superuser  
            trip.save()  
            return redirect('home')
    else:
        form = TripForm()
    return render(request, 'trip/add_trip.html', {'form': form})
def edit_trip(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)
    if request.method == 'POST':
        form = TripForm(request.POST, instance=trip)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TripForm(instance=trip)
    return render(request, 'trip/edit_trip.html', {'form': form, 'trip_id': trip.id})



# def delete_trip(request, trip_id):
#     trip = get_object_or_404(Trip, pk=trip_id)
#     if request.method == 'POST':
#         trip.delete()
#         messages.success(request, 'Trip deleted successfully.')
#         return redirect('home')
#     return render(request, 'trip/delete_trip.html', {'trip': trip})

def delete_trip(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)

    if request.method == 'POST':
        with connection.cursor() as cursor:

            cursor.execute("DELETE FROM trip_review WHERE trip_id = %s", [trip_id])
            cursor.execute("DELETE FROM trip_trip WHERE id = %s", [trip_id])
        messages.success(request, 'Trip deleted successfully.')
        return redirect('home')

    return render(request, 'trip/delete_trip.html', {'trip': trip})


def review_page(request):
    year_filter_form = TripYearFilterForm(request.GET or None)
    trips = Trip.objects.all().prefetch_related('reviews')

    if 'year' in request.GET and request.GET['year']:
        trips = trips.filter(start_date__year=request.GET['year'])

    no_trips = not trips.exists()

    return render(request, 'trip/review_page.html', {
        'year_filter_form': year_filter_form,
        'trips': trips,
        'no_trips': no_trips,
    })


def add_review(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)
   
    user = User.objects.get(username='chinmay')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.trip = trip
            review.user = user 
            review.save()
            return redirect('review_page')  
    else:
        form = ReviewForm()

    return render(request, 'trip/add_review_form.html', {'form': form, 'trip_id': trip_id})

def edit_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('review_page')
    else:
        form = ReviewForm(instance=review)

    return render(request, 'trip/edit_review_form.html', {'form': form, 'review': review})


# views.py
def delete_review_confirm(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM trip_review WHERE id = %s", [review_id])
        messages.success(request, 'Review deleted successfully.')
        return redirect('review_page')  
    else:
        return render(request, 'trip/delete_review_confirm.html', {'review': review})






def add_review_page(request):
    
    trips_without_reviews = Trip.objects.annotate(reviews_count=Count('reviews')).filter(reviews_count=0)

    return render(request, 'trip/add_review_page.html', {
        'trips_without_reviews': trips_without_reviews,
    })
