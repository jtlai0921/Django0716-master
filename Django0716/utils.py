from math import sin, cos, sqrt, atan2, radians
import requests
import json

from captcha.fields import CaptchaField
from django.forms import forms


def search(mylat, mylng, dist, sbi, bemp):
    url = 'https://data.tycg.gov.tw/api/v1/rest/datastore/a1b4714b-3b75-4ff8-a8f2-cc377e4eaa0f?format=json'
    r = requests.get(url)
    root_object = json.loads(r.text)
    result_object = root_object['result']
    records_array = result_object['records']
    dict = {}
    for record in records_array:
        lat = float(record['lat'])
        lng = float(record['lng'])
        m = distance(mylat, mylng, lat, lng)
        t = '%.1f' % (m / (3000/60))
        if int(record['sbi']) >= sbi and int(record['bemp']) >= bemp and m <= dist:
            record['m'] = m//1
            record['t'] = t
            # 格式化時間 ex:20190810100326 變成 2019/08/10 10:03:26
            mday = record['mday']
            record['mday'] = mday[0:4] + '/' + mday[4:6] + '/' + mday[6:8] + " " + \
                             mday[8:10] + ':' + mday[10:12] + ':' + mday[12:]
            dict.update({record['sna']: record})

    return dict


def distance(point_1_lat, point_1_lon, point_2_lat, point_2_lon):
    # approximate radius of earth in km
    R = 6373.0
    lat1 = radians(float(point_1_lat))
    lon1 = radians(float(point_1_lon))
    lat2 = radians(float(point_2_lat))
    lon2 = radians(float(point_2_lon))
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c * 1000  # m 公尺
    return distance


# 驗證碼類別
class CaptchaCheck(forms.Form):
    captcha = CaptchaField()
