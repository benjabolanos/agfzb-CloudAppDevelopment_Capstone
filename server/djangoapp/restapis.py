import requests
import json
from .models import CarModel, CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
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

    

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
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
                    review_id = entry['id'],
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
                    review_id = '',
                    name = entry['name'],
                    purchase = entry['purchase'],
                    purchase_date = '',
                    review = entry['review'],
                    sentiment = analyze_review_sentiments(entry['review'])
                )
            
            results.append(review_obj)
    return results



# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):

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
        features=Features(
        sentiment=SentimentOptions(),
        entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
        keywords=KeywordsOptions(emotion=True, sentiment=True, limit=2)))

    sentiment_result = response.result['sentiment']
    
    sentiment = sentiment_result['document']['label']

    return sentiment



