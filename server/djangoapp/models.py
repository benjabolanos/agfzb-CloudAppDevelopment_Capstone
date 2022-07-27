from django.db import models
from django.utils.timezone import now

class CarMake(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class CarModel(models.Model):
    CAR_TYPE_CHOICES = (
        ('micro','Micro'),
        ('sedan','Sedan'),
        ('cuv','CUV'),
        ('suv','SUV'),
        ('pickup','Pickup'),
        ('van','Van'),
        ('truck','Truck')
    )

    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    dealer_id = models.IntegerField()
    car_type = models.CharField(max_length=15, choices=CAR_TYPE_CHOICES)
    year = models.DateField(default=now)

    def __str__(self):
        return self.car_type + " "

class CarDealer:

    def __init__(self, address, city, full_name, dealer_id, lat, _long, st, state, zip_code):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.dealer_id = dealer_id
        self.lat = lat
        self._long = _long
        self.st = st
        self.state = state
        self.zip_code = zip_code

    def __str__(self):
        return "Dealer name: " + self.full_name


class DealerReview:

    def __init__(self, car_make, car_model, car_year, dealership, review_id, name, purchase, purchase_date, review, sentiment):
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.dealership = dealership
        self.review_id = review_id
        self.name = name
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.review = review
        self.sentiment = sentiment

    def __str__(self):
        return "Review ID: " + self.review_id

