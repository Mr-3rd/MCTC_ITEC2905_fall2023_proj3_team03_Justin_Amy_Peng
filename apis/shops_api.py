"""
This API call will return the 5 highest rated autoshops that are near the users current location
The geocoder library gets the latitude and longitude of the current user.
The API takes in a car object then uses the API to search for auto repair shops. 
The response then extracts the name, URL, rating, street address, city, state and then will create a dictionary with these values.
If there are any errors, it catches and logs the error, then returns an error message.

geocoder reference: https://stackoverflow.com/questions/24906833/how-to-access-current-location-of-any-user-using-python

logging reference: https://docs.python.org/3/library/logging.html#levels

"""

import requests
import geocoder
import logging
import os

def get_location():
    g = geocoder.ip('me')
    return g.latlng

def get_shops(car):
    url = "https://api.yelp.com/v3/businesses/search?"
    API_key = os.environ.get('YELP_API_KEY')
    location = get_location()

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + API_key
    }

    payload = {
    'latitude': location[0],
    'longitude': location[1],
    'categories': 'autorepair',
    'sort_by': 'rating', 
    'limit':5,
    'term': car['make']
    }

    businesses = []
    

    try:
        response = requests.get(url, headers=headers, params=payload)
        response.raise_for_status()
        data = response.json()

        for business in data['businesses']:

            business = {
            'name': business['name'],
            'url': business['url'],
            'rating':  business['rating'],
            'street_address': business['location']['address1'],
            'city': business['location']['city'],
            'state': business['location']['state']

            }
            businesses.append(business)

        return businesses


    except requests.HTTPError as HTerror: 
        logging.exception(HTerror)
        error = 'Website error: ' + str(response.status_code)
        return error
    except requests.exceptions.Timeout: 
        error = 'The website has timed out' 
        logging.exception(error)
        return error
    except Exception:
        error = 'A catastrophic error has occurred: '
        logging.exception(error)
        return error