import sys
from io import BytesIO

import requests
from PIL import Image


def geocode(address):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": address,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        print('BAD REQUEST')
        sys.exit(1)
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    return toponym


def get_coordinates(address):
    toponym = geocode(address)
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = map(float,
                                               toponym_coodrinates.split(" "))
    return toponym_longitude, toponym_lattitude


def show_map(ll, spn, l='map', add_params=None):
    map_params = {
        "ll": ll,
        "spn": spn,
        "l": l
    }
    if add_params:
        map_params['pt'] = ll
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    if not response:
        print('BAD REQUEST')
        sys.exit(1)
    Image.open(BytesIO(
        response.content)).show()


def get_ll_spn(address):
    toponym = geocode(address)
    toponym_coordinate = toponym["Point"]["pos"]

    lower_corner = toponym['boundedBy']['Envelope']['lowerCorner']
    upper_corner = toponym['boundedBy']['Envelope']['upperCorner']
    left, bottom = map(float, lower_corner.split())
    right, up = map(float, upper_corner.split())
    delta_x = abs(left - right) / 2
    delta_y = abs(bottom - up) / 2
    ll = toponym_coordinate.replace(' ', ',')
    spn = ','.join([str(delta_x), str(delta_y)])
    return ll, spn


toponym_to_find = " ".join(sys.argv[1:])
if not toponym_to_find:
    print('No params')
    sys.exit(1)

toponym_longitude, toponym_lattitude = get_coordinates(toponym_to_find)

delta_x = delta_y = "0.005"
spn = ",".join([delta_x, delta_y])
ll = ",".join([str(toponym_longitude), str(toponym_lattitude)])
show_map(ll, spn)

ll, spn = get_ll_spn(toponym_to_find)
show_map(ll, spn)

show_map(ll, spn, add_params=True)