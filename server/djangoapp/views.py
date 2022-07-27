from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.conf import settings
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create an `about` view to render a static about page
def about(request):
    context = {}
    return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    return render(request, 'djangoapp/contact.html', context)

def sign_up(request):
    context = {}
    return render(request, 'djangoapp/registration.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return redirect('djangoapp:index')
    else:
        return redirect('djangoapp:index')

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(username=username, 
                                            first_name=first_name, 
                                            last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://ba61a290.us-south.apigw.appdomain.cloud/bestcars/api/dealership"
        dealerships = get_dealers_from_cf(url)

        context['dealerships'] = dealerships
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context = {}

        dealer_url="https://ba61a290.us-south.apigw.appdomain.cloud/bestcars/api/dealership"
        review_url="https://ba61a290.us-south.apigw.appdomain.cloud/bestcars/api/review"

        dealer = get_dealer_by_id(dealer_url, dealerId= dealer_id)
        dealer_reviews = get_dealer_reviews_from_cf(review_url, dealerId=dealer_id)

        context['dealer_reviews'] = dealer_reviews
        context['dealer'] = dealer[0]
        return render(request, 'djangoapp/dealer_details.html', context)

def add_review(request, dealer_id):
    context = {}

    user = request.user
    if(user.is_authenticated):


        if request.method == "GET" :
            dealer_url = "https://ba61a290.us-south.apigw.appdomain.cloud/bestcars/api/dealership"
            dealer = get_dealer_by_id(dealer_url, dealerId= dealer_id)
            context['dealership'] = dealer[0]
            cars = CarModel.objects.all()
            context['cars'] = cars

            return render(request, 'djangoapp/add_review.html', context)

        elif request.method == "POST":
            
            review_url = "https://ba61a290.us-south.apigw.appdomain.cloud/bestcars/api/review"

            review = {}
            review["time"] = datetime.utcnow().isoformat()
            review["dealership"] = dealer_id
            review["review"] = request.POST['review']

            review["name"] = request.POST['name']
            purchase = request.POST['purchase']
            if purchase:
                review["purchase"] = purchase
                review["purchase_date"] = request.POST['purchase_date']
                review["car_make"] = request.POST['car_make']
                review["car_model"] = request.POST['car_model']
                review["car_year"] = request.POST['car_year']

            else:
                review["purchase"] = purchase
            
            json_payload = {}
            json_payload["review"] = review

            result = post_request(review_url, json_payload, dealer_id=dealer_id)

            context['result'] = result
            context['message'] = "Success: Review added."
            return HttpResponseRedirect(reverse(viewname='djangoapp:dealer_details.html', args=(dealer_id, dealer.id)))
    else:
        context['message'] = "Error: User is unauthenticated."
        return redirect(request, 'djangoapp/dealer_details.html', context)
