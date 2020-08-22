import math
import urllib
from urllib.parse import urlencode
import csv
from django.core import paginator
from django.core.paginator import Paginator
from django.shortcuts import render_to_response, redirect, render
from django.urls import reverse
from django.http import HttpResponse

from app.settings import BUS_STATION_CSV


def index(request):
    return redirect(reverse('bus_stations'))


def read_csv():
    with open(BUS_STATION_CSV, encoding='cp1251') as csvfile:
        reader = csv.DictReader(csvfile)
        reader_sorted = []
        for row in reader:
            temp = {'Name': row.get('Name'), 'Street': row.get('Street'), 'District': row.get('District')}
            reader_sorted.append(temp)
    return reader_sorted


def bus_stations(request):

    data = read_csv()

    paginator_obj = Paginator(data, 10)

    current_page = int(request.GET.get('page', 1))

    page_obj = paginator_obj.get_page(current_page)

    if page_obj.has_next():
        next_page_url = reverse('bus_stations') + '?' + urllib.parse.urlencode({'page':
                                                                                    page_obj.next_page_number()})
    else:
        next_page_url = None

    if page_obj.has_previous():
        prev_page_url = reverse('bus_stations') + '?' + urllib.parse.urlencode({'page':
                                                                                    page_obj.previous_page_number()})
    else:
        prev_page_url = None

    return render_to_response('index.html', context={
        'bus_stations': page_obj,
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url
    })

"""
Для формирования url'а с get параметром помимо reverse используйте 

"""