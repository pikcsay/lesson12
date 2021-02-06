import requests


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
