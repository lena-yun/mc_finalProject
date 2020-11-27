from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.clickjacking import xframe_options_deny
from djangofinal.settings import BASE_DIR
import json
import csv
import ast
import folium
import pandas as pd
from datetime import datetime
from time import mktime, strptime
from django.utils.dateformat import DateFormat


# Create your views here.

def index(request):
    return render(request, 'finalApp/index_2.html')

def about(request):
    return render(request, 'finalApp/about.html')


def shop(request):
    return render(request, 'finalApp/shop.html')


def selectshop(request):
    return render(request, 'finalApp/selectshop.html')

def news(request):
    return render(request, 'finalApp/news.html')


def mapseoulprice(request):
    return render(request, 'finalApp/seoul_map_price.html')

def seoulprice(request):
    return render(request, 'finalApp/seoul_lettuce_map.html')

def cu(request):
    return render(request, 'finalApp/seoul_cabbage_map.html')

def distribution(request):
    return render(request, 'finalApp/distribution.html')

def cart(request):
    return render(request, 'finalApp/cart.html')

def news(request):
    return render(request, 'finalApp/news.html')

def singlenews(request):
    return render(request, 'finalApp/single-news.html')

def page404(request):
    return render(request, 'finalApp/404.html')
def checkout(request):
    return render(request, 'finalApp/checkout.html')

def noonegu(request, id):
    price_mart = []
    price_si = []
    price_seoul = []
    category = []
    name = id
    dada = []
    with open('./static/seoul_mart_jang_graph.csv', mode='r', encoding='utf-8') as seoul_lists:
        reader = csv.reader(seoul_lists)

        for list_num in reader:
            if list_num[4] == str(id):
                if list_num[1] == '':
                    price_si.append(0)
                    price_mart.append(int(round(float(list_num[2]), 0)))
                    price_seoul.append(int(round(float(list_num[3]), 0)))
                    category.append(list_num[5])
                    dada.append(list_num[0])


                elif list_num[2] == '':
                    price_si.append(int(round(float(list_num[1]),0)))
                    price_mart.append(0)
                    price_seoul.append(int(round(float(list_num[3]),0)))
                    category.append(list_num[5])
                    dada.append(list_num[0])

                elif list_num[3] == '':
                    price_si.append(int(round(float(list_num[1]),0)))
                    price_mart.append(int(round(float(list_num[2]),0)))
                    price_seoul.append(0)
                    category.append(list_num[5])
                    dada.append(list_num[0])

                elif list_num[3] != '' and list_num[2] != '' and list_num[1] != '':
                    price_si.append(int(round(float(list_num[1]),0)))
                    price_mart.append(int(round(float(list_num[2]),0)))
                    price_seoul.append(int(round(float(list_num[3]),0)))
                    category.append(list_num[5])
                    dada.append(list_num[0])

    name_list = [name for _ in range(len(category))]
    csvData = [[price_si[i], price_mart[i], price_seoul[i], dada[i], category[i], name_list[i]] for i in
               range(len(category))]

    with open('./static/seoul_mart_jang_graph_select.csv',  mode='w', encoding='utf-8-sig', newline='') as csvfile:
        wr = csv.writer(csvfile, delimiter=',')
        for i in csvData:
            wr.writerow(i)

    cheaper_price_si = []
    cheaper_price_mart = []

    label_mart = []
    label_si = []

    expensive_li = []
    cheap_li = []

    with open('./static/jang_mart_price_vs.csv', mode='r') as seoul_lists02:
        reader = csv.reader(seoul_lists02)

        for list_num02 in reader:
            if list_num02[0] == str(id) and list_num02[3] == '시장':
                cheaper_price_mart.append(str(list_num02[4]))
            elif list_num02[0] == str(id) and list_num02[3] == '마트':
                cheaper_price_si.append(str(list_num02[4]))

        for i in cheaper_price_mart:
            if i == '무':
                # c_m_image_src_li.append("Radish.jpg")
                label_mart.append(1)
            elif i == '배추':
                label_mart.append(2)
            elif i == '상추':
                label_mart.append(3)
            elif i == '양파':
                label_mart.append(4)
            elif i == '오이':
                label_mart.append(5)

        for i in cheaper_price_si:
            if i == '무':
                label_si.append(1)
            elif i == '배추':
                label_si.append(2)
            elif i == '상추':
                label_si.append(3)
            elif i == '양파':
                label_si.append(4)
            elif i == '오이':
                label_si.append(5)

    with open('./static/dict_expensive_cheap.csv', mode='r') as dict_expensive_cheap:
        reader = csv.reader(dict_expensive_cheap)

        for ex_li in reader:
            if ex_li[0] == str(id):
                expensive_li.append(str(ex_li[1]))
                cheap_li.append(str(ex_li[2]))

        expensive_li = ','.join(expensive_li)
        cheap_li = ','.join(cheap_li)

    local = []
    category_local = []
    ratio = []
    expen_cheap = []

    with open('./static/gu_expen_cheaper.csv', mode='r', encoding='utf-8') as seoul_lists:
        reader = csv.reader(seoul_lists)

        for list_num in reader:
            if list_num[0] == str(id):
                local.append(list_num[0])
                category_local.append(list_num[1])
                ratio.append(list_num[2])
                expen_cheap.append(list_num[3])

    csvData4 = [[local[i], category_local[i], ratio[i], expen_cheap[i]] for i in
               range(len(local))]

    with open('./static/gu_expen_cheaper_select.csv', mode='w', encoding='utf-8-sig', newline='') as csvfile:
        wr = csv.writer(csvfile, delimiter=',')
        for i in csvData4:
            wr.writerow(i)

    local_next = []
    cheaper_next = []
    expen_next = []
    category_next = []



    with open('./static/local_expen_cheaper.csv', mode='r', encoding='utf-8') as seoul_lists:
        reader = csv.reader(seoul_lists)

        for list_num in reader:
            if list_num[0] == str(id):
                if list_num[1] == 'nothing':
                    local_next.append(list_num[0])
                    cheaper_next.append('無')
                    expen_next.append(list_num[2])
                    category_next.append(list_num[3])
                elif list_num[2] == 'nothing':
                    local_next.append(list_num[0])
                    cheaper_next.append(list_num[1])
                    expen_next.append('無')
                    category_next.append(list_num[3])
                elif list_num[1] != 'nothing' and list_num[2] != 'nothing':
                    local_next.append(list_num[0])
                    cheaper_next.append(list_num[1])
                    expen_next.append(list_num[2])
                    category_next.append(list_num[3])

    csvData5 = [[local_next[i], cheaper_next[i], expen_next[i], category_next[i]] for i in
                range(len(category_next))]

    with open('./static/local_expen_cheaper_select.csv', mode='w', encoding='utf-8-sig', newline='') as csvfile:
        wr = csv.writer(csvfile, delimiter=',')
        for i in csvData5:
            wr.writerow(i)

    year2020_mean = []
    year2020_local = []
    year2020_place = []
    year2020_category = []

    with open('./static/seoul_1year_mean.csv', mode='r', encoding='utf-8') as seoul_lists:
        reader = csv.reader(seoul_lists)

        for list_num in reader:
            if list_num[1] == str(id):
                year2020_mean.append(int(round(float(list_num[0]),0)))
                year2020_local.append(list_num[1])
                year2020_place.append(list_num[2])
                year2020_category.append(list_num[3])

    csvData6 = [[year2020_mean[i], year2020_local[i], year2020_place[i], year2020_category[i]] for i in
                range(len(year2020_category))]

    with open('./static/seoul_1year_mean_select.csv', mode='w', encoding='utf-8-sig', newline='') as csvfile:
        wr = csv.writer(csvfile, delimiter=',')
        for i in csvData6:
            wr.writerow(i)



    context = {
        'price_si': price_si,
        'price_mart': price_mart,
        'price_seoul': price_seoul,
        'name': name,
        'dada': dada,
        'category': category[0],

        'expensive_li' : expensive_li,
        'cheap_li' : cheap_li,

        'label_mart' : label_mart,
        'label_si' : label_si,

        'cheaper_price_si': cheaper_price_si,
        'cheaper_price_mart': cheaper_price_mart,
    }
    return render(request, 'finalApp/noonegu.html', context)

@csrf_exempt
def vegetableSelect(request, id):
    print(id)
    print('----------- ajax json vegetableSelect')
    price_si = []
    price_mart = []
    price_seoul = []
    category = []
    name = []
    dada = []
    with open('./static/seoul_mart_jang_graph_select.csv', mode='r', encoding='utf-8-sig') as vegetable_lists:
        reader = csv.reader(vegetable_lists)

        for list_num in reader:
            if list_num[4] == str(id):
                if list_num[0] == '':
                    price_si.append(0)
                    price_mart.append(int(list_num[1]))
                    price_seoul.append(int(list_num[2]))
                    dada.append(list_num[3])
                    category.append(list_num[4])
                    name.append(list_num[5])


                elif list_num[1] == '':
                    price_si.append(int(list_num[0]))
                    price_mart.append(0)
                    price_seoul.append(int(list_num[2]))
                    dada.append(list_num[3])
                    category.append(list_num[4])
                    name.append(list_num[5])

                elif list_num[2] == '':
                    price_si.append(int(list_num[0]))
                    price_mart.append(int(list_num[1]))
                    price_seoul.append(0)
                    dada.append(list_num[3])
                    category.append(list_num[4])
                    name.append(list_num[5])

                elif list_num[2] != '' and list_num[1] != '' and list_num[0] != '':
                    price_si.append(int(list_num[0]))
                    price_mart.append(int(list_num[1]))
                    price_seoul.append(int(list_num[2]))
                    dada.append(list_num[3])
                    category.append(list_num[4])
                    name.append(list_num[5])

    local = []
    category_local = []
    ratio = []
    ExpCheap = []


    with open('./static/gu_expen_cheaper_select.csv', mode='r', encoding='utf-8-sig') as vegetable_lists:
        reader = csv.reader(vegetable_lists)

        for list_num in reader:
            if list_num[1] == str(id):
                local.append(list_num[0])
                category_local.append(list_num[1])
                ratio.append(list_num[2])
                if str(list_num[3]) == '비싸다':
                    ExpCheap.append(str('비싸게'))
                else:
                    ExpCheap.append(str('싸게'))

    local_next = []
    cheaper_next = []
    expen_next = []
    category_next = []

    with open('./static/local_expen_cheaper_select.csv', mode='r', encoding='utf-8-sig') as vegetable_lists:
        reader = csv.reader(vegetable_lists)

        for list_num in reader:
            if list_num[3] == str(id):
                local_next.append(list_num[0])
                cheaper_next.append(list_num[1])
                expen_next.append(list_num[2])
                category_next.append(list_num[3])

    year2020_mean = []
    year2020_place = []

    with open('./static/seoul_1year_mean_select.csv', mode='r', encoding='utf-8-sig') as vegetable_lists:
        reader = csv.reader(vegetable_lists)

        for list_num in reader:
            if list_num[3] == str(id):
                year2020_mean.append(int(list_num[0]))
                year2020_place.append(list_num[2])

    context = {
        'price_si': price_si,
        'price_mart': price_mart,
        'price_seoul': price_seoul,
        'name': name[0],
        'category': category[0],
        "dada":dada,

        'ratio': ratio,
        'ExpCheap': ExpCheap,

        'expen_next': expen_next,
        'cheaper_next': cheaper_next,

        'year2020_mean': year2020_mean,
        'year2020_place': year2020_place,
        'length': len(year2020_place)
    }

    print(context.get('dada'))
    if price_si[0] == 0:
        context['sizero'] = 'False'

    if price_mart[0] == 0:
        context['martzero'] = 'False'
    if price_seoul[0] == 0:
        context['seoulzero'] = 'False'

    if price_si[0] == 0 and price_mart[0] == 0 and price_seoul[0] == 0:
        context['priceZero'] = 'False'

    data = [context]

    return JsonResponse(data, safe=False)


def mapseoulpriceajax(request, id):
    print(id)
    print('<----------------------Ajax 통신')
    category = []
    location = []
    place = []
    year4mean = []
    martsi = []

    with open('./static/map_seoul_mean_price.csv', mode='r', encoding='utf-8') as seoul_lists:
        reader = csv.reader(seoul_lists)

        for list_num in reader:
            if list_num[0] == str(id):
                category.append(list_num[0])
                location.append(list_num[1])
                place.append(list_num[2])
                year4mean.append(int(round(float(list_num[3]),0)))
                martsi.append(list_num[4])

    pricelist = [[location[i], place[i], year4mean[i], martsi[i]] for i in range(len(martsi))]

    pricelistdesc = sorted(pricelist, key=lambda x:-x[2])

    pricelistasc = sorted(pricelist, key=lambda x:x[2])

    price_ex_location = [pricelistdesc[i][0] for i in range(3)]
    price_ex_place = [pricelistdesc[i][1] for i in range(3)]
    price_ex_price = [pricelistdesc[i][2] for i in range(3)]
    price_ex_martsi = [pricelistdesc[i][3] for i in range(3)]

    price_ch_location = [pricelistasc[i][0] for i in range(3)]
    price_ch_place = [pricelistasc[i][1] for i in range(3)]
    price_ch_price = [pricelistasc[i][2] for i in range(3)]
    price_ch_martsi = [pricelistasc[i][3] for i in range(3)]
    rank_num = [i for i in range(1,4)]

    print(rank_num, price_ex_location, price_ex_place, price_ex_price, price_ex_martsi)
    print('*'*100)
    print(rank_num, price_ch_location,price_ch_place, price_ch_price,  price_ch_martsi)

    context = {
        'priceExLocation':price_ex_location,
        'priceExPlace': price_ex_place,
        'priceExPrice': price_ex_price,
        'priceExMartsi': price_ex_martsi,

        'priceChLocation': price_ch_location,
        'priceChPlace': price_ch_place,
        'priceChPrice': price_ch_price,
        'priceChMartsi': price_ch_martsi,

        'length': len(price_ch_martsi),

        'rankNum': rank_num,

        'name': category[0]
    }
    data = [context]

    return JsonResponse(data, safe=False)

def vegetableSelectProducer(request, id):
    print(id)
    print('----------- ajax json vegetableSelectProducer')
    price_total = []
    category = []
    days = []
    with open('./static/seoul_mart_jang_graph_select_test_producer02.csv', mode='r', encoding='utf-8-sig') as vegetable_lists_p:
        reader = csv.reader(vegetable_lists_p)

        for list_num in reader:
            if list_num[2] == str(id):
                price_total.append(int(list_num[0]))
                category.append(list_num[2])
                days.append(list_num[1])


    context = {

        'price_total': price_total,
        'days': days,
        'category': category[0]
    }
    data = [context]
    return JsonResponse(data, safe=False)



def chartInModal(request, id):
    print(id)
    print('----------- ajax json vegetableSelectProducer')

    category = []
    days = []
    modal_si_price = []
    modal_mart_price = []

    with open('./static/modal_test_noonegu.csv', mode='r',
              encoding='utf-8-sig') as vegetable_lists_p:
        reader = csv.reader(vegetable_lists_p)

        for list_num in reader:
            if list_num[4] == str(id):
                modal_si_price.append(int(list_num[1]))
                modal_mart_price.append(int(list_num[1]))
                category.append(list_num[4])
                days.append(list_num[0])

    context = {

        'modal_si_price': modal_si_price,
        'modal_mart_price': modal_mart_price,
        'days': days,
        'category': category[0]
    }
    data = [context]
    return JsonResponse(data, safe=False)