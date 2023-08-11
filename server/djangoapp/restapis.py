import requests
import json
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview

api_key = ''
cloud_function_url = ''

def get_request(url, params=None, headers=None, auth=None):
    response = requests.get(url, params=params, headers=headers, auth=auth)
    return response

def post_request(url, params=None, json_data=None):
    response = requests.post(url, params=params, json=json_data)
    return response

def get_dealers_from_cf(url, **kwargs):
    response = get_request(url, params=kwargs, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('apikey', api_key))
    dealers_data = response.json()

    dealers = []
    for dealer_data in dealers_data:
        dealer = CarDealer(
            dealer_id=dealer_data.get('dealerId'),
            name=dealer_data.get('name'),
            address=dealer_data.get('address'),
        )
        dealers.append(dealer)
    return dealers

def get_dealer_reviews_from_cf(url, dealerId):
    response = get_request(url, params={'dealerId': dealerId}, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('apikey', api_key))
    reviews_data = response.json()

    reviews = []
    for review_data in reviews_data:
        review = DealerReview(
            review_id=review_data.get('reviewId'),
            dealer_id=review_data.get('dealerId'),
            sentiment=review_data.get('sentiment'),
            text=review_data.get('reviewText'),
        )
        reviews.append(review)
    return reviews

def analyze_review_sentiments(text):
    nlu_url = ""
    nlu_api_key = ""
    payload = {
        "text": text,
        "features": {
            "sentiment": {}
        }
    }
    response = post_request(nlu_url, json_data=payload, headers={'Content-Type': 'application/json', 'apikey': nlu_api_key})
    sentiment_data = response.json()

    return sentiment_data.get('sentiment', {}).get('document', {}).get('label', 'Unknown')
