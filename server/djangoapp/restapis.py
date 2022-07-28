import requests
import json
from .models import CarModel, CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from django.conf import settings
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions, EntitiesOptions, KeywordsOptions, ClassificationsOptions

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    
    try:
        api_key = kwargs.get("api_key")
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            
            response = requests.get(url, 
                    params=params, 
                    headers= {
                        'Content-Type': 'application/json'
                    }, 
                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)

        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data

    except:
        print("Network exception occurred")

def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url)

    if json_result:
        entries = json_result['entries']
        for entry in entries:
            dealer_obj = CarDealer(
                address = entry['address'],
                city = entry['city'],
                full_name = entry['full_name'],
                dealer_id = entry['id'],
                lat = entry['lat'],
                _long = entry['long'],
                st = entry['st'],
                state = entry['state'],
                zip_code = entry['zip']
            )
            results.append(dealer_obj)
    return results

def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    json_result = get_request(url, dealerId = dealerId)

    if json_result:
        entries = json_result['entries']
        for entry in entries:

            if entry['purchase'] == True:
                review_obj = DealerReview(
                    car_make = entry['car_make'],
                    car_model = entry['car_model'],
                    car_year = entry['car_year'],
                    dealership = entry['dealership'],
                    review_id = 0,
                    name = entry['name'],
                    purchase = entry['purchase'],
                    purchase_date = entry['purchase_date'],
                    review = entry['review'],
                    sentiment = analyze_review_sentiments(entry['review'])
                )
            else:
                review_obj = DealerReview(
                    car_make = '',
                    car_model = '',
                    car_year = '',
                    dealership = entry['dealership'],
                    review_id = 0,
                    name = entry['name'],
                    purchase = entry['purchase'],
                    purchase_date = '',
                    review = entry['review'],
                    sentiment = analyze_review_sentiments(entry['review'])
                )
            
            results.append(review_obj)
    return results

def analyze_review_sentiments(dealer_review):

    sentiment_result = []

    api_key = settings.SENTIMENT_API_KEY
    api_url = settings.SENTIMENT_API_URL

    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2021-08-01',
        authenticator=authenticator)

    natural_language_understanding.set_service_url(api_url)

    response = natural_language_understanding.analyze(
        text=dealer_review,
        language = 'en',
        features=Features(
        sentiment=SentimentOptions()
        )).get_result()

    sentiment_result = response['sentiment']
    
    sentiment = sentiment_result['document']['label']

    return sentiment

def post_request(url, json_payload, **kwargs):
    
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data

    except:
        print("Network exception occurred")
    
    
def get_dealer_by_id(url, dealerId):
    result = []
    json_result = get_request(url, dealerId=dealerId)
    
    if json_result:
        entry = json_result['entries'][0]
        dealer_obj = CarDealer(
                address = entry['address'],
                city = entry['city'],
                full_name = entry['full_name'],
                dealer_id = entry['id'],
                lat = entry['lat'],
                _long = entry['long'],
                st = entry['st'],
                state = entry['state'],
                zip_code = entry['zip']
            )
        result.append(dealer_obj)
    return result