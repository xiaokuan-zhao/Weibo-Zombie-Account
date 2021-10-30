from django.shortcuts import render
from django.http import JsonResponse
import codecs
import copy
import csv
import json
import math
import os
import random
import sys
import traceback
from collections import OrderedDict
from datetime import date, datetime, timedelta
from time import sleep

import requests
from lxml import etree
from requests.adapters import HTTPAdapter

from backend.myspyder import Myspyder
import numpy as np

# Create your views here.


def getUserById(request):
    response = {}
    try:
        ms = Myspyder(request.GET.get('id'))
        ms.start()
        response["userInfo"] = ms.userinfo
        print(response)
        beta = np.array([[0.121707753444338, -4.1358307801440995e-06, -3.527123578084805e-08,
                          -0.0007500391966586345, 3.294255952390543, 0.06183729675139181,
                          0.5816625232025247, 2.015305703694417, 0.011993442356175974,
                          0.0009872074670918191, 0.0003517953080281057, 0.0006158663242654701,
                          8.5096926677883e-05, -0.0007104432102140811, -7.694630079720831e-06,
                          -6.66246428948503]])
        datax = []
        if ms.userinfo['gender'] == 'm':
            datax.append(1)
        else:
            datax.append(0)
        datax.append(ms.userinfo['statuses_count'])
        datax.append(ms.userinfo['followers_count'])
        datax.append(ms.userinfo['follow_count'])
        if ms.userinfo['avatar_hd']:
            datax.append(1)
        else:
            datax.append(0)
        datax.append(ms.userinfo['urank'])
        datax.append(ms.userinfo['mbrank'])
        if ms.userinfo['verified']:
            datax.append(1)
        else:
            datax.append(0)
        datax.append(ms.userinfo['verified_type'])
        datax.append(ms.userinfo['retweets'])
        datax.append(ms.userinfo['original'])
        print('predicting')
        if ms.userinfo['retweets'] == 0:
            datax.append(100)
        else:
            datax.append(ms.userinfo['original']/ms.userinfo['retweets'])
        datax.append(ms.userinfo['dalllike'])
        datax.append(ms.userinfo['dallcomm'])
        datax.append(ms.userinfo['dallrepo'])

        print(datax)

        result = 0

        for i in range(len(datax)):
            result += beta[0, i]*datax[i]
        result += beta[0, -1]
        result = 1/(1+np.exp(-result))
        print('result:')
        print(result)
        if result > 0.5:
            result = 1
        else:
            result = 0
        response['isreal'] = result
        print(response)
        return JsonResponse(response)
    except Exception:
        print(Exception)
        return JsonResponse(None)
