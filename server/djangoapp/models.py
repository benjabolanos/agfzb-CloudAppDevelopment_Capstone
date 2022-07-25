from django.db import models
from django.utils.timezone import now

class CarMake(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=50)
    
    def __str__(self):
        return "Name: " + self.name + "," + \
            "Description: " + self.description

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

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
