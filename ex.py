import sys
from io import BytesIO

from second import get_ll_spn, geocode
import requests
from PIL import Image


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
