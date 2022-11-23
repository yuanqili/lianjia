# Baidu Map Console: https://lbsyun.baidu.com/apiconsole/center#/home
# Baidu Map Web API: https://lbsyun.baidu.com/index.php?title=webapi

import shutil

import requests
from pprint import pprint
from configparser import ConfigParser


class BaiduMap:

    def __init__(self, ak=None):
        if ak is None:
            config = ConfigParser()
            config.read('config.ini')
            ak = config['Settings']['BaiduMapAk']
        self.ak = ak

    def location_query(self, query, region):
        url = f'https://api.map.baidu.com/place/v2/search'
        params = {
            'query': query,
            'region': region,
            'output': 'json',
            'ak': self.ak,
        }
        response = requests.get(url, params=params)
        response = response.json()
        return response

    def static_image(self, outpath, lng, lat, width=512, height=512, zoom=11):
        url = 'https://api.map.baidu.com/staticimage/v2'
        params = {
            'center': f'{lng},{lat}',
            'width': width,
            'height': height,
            'zoom': zoom,
            'dpiType': 'ph',
            'copyright': 1,
            'ak': self.ak,
        }
        response = requests.get(url, params=params, stream=True)
        with open(outpath, 'wb') as outfile:
            shutil.copyfileobj(response.raw, outfile)

    def route_matrix(self, origins, destinations):
        url = 'https://api.map.baidu.com/routematrix/v2/driving'
        params = {
            'origins': '|'.join([f'{origin["lat"]},{origin["lng"]}' for origin in origins]),
            'destinations': '|'.join([f'{dest["lat"]},{dest["lng"]}' for dest in destinations]),
            'tactics': 12,
            'ak': self.ak,
        }
        response = requests.get(url, params=params)
        response = response.json()
        return response


if __name__ == '__main__':
    baidu_map = BaiduMap()

    result = baidu_map.location_query('御景华府', '南京')
    pprint(result)

    origins = [
        {'lng': 118.877639, 'lat': 32.088052, 'name': '钟山高尔夫'},
        {'lng': 118.789745, 'lat': 32.079796, 'name': '御景华府'},
    ]
    destinations = [
        {'lng': 118.791895, 'lat': 32.047041, 'name': '南京中心'},
        {'lng': 118.76378, 'lat': 32.083167, 'name': '南师附中'},
        {'lng': 118.807781, 'lat': 32.062704, 'name': '南京外国语学校'},
    ]
    result = baidu_map.route_matrix(origins=origins, destinations=destinations)
    pprint(result)
