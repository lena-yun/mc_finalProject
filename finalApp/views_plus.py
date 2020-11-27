from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect ,  get_object_or_404
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.clickjacking import xframe_options_deny
from djangofinal.settings import BASE_DIR
import json
import csv
import pandas as pd

# Create your views here.

def index(request):
    return render(request, 'finalApp/index_2.html')

def about(request):
    return render(request, 'finalApp/about.html')

def shop(request):
    return render(request, 'finalApp/shop.html')

def selectshop(request):
    return render(request, 'finalApp/selectshop.html')

def noonegu(request,id):
    list_num = []
    cabbage_price_mart = []
    cabbage_price_si = []
    # print("param >>>>>>>>>>>>>>>>>>>>>>>>> " , id)
    with open('C:/mc_final_data/seoul_4years_avg.csv',
              mode='r') as seoul_lists:
        reader = csv.reader(seoul_lists)

        for list_num in reader:
            if list_num[5] == str(id) and list_num[1] =='배추' and list_num[7] =='시장':
                cabbage_price_si.append(int(list_num[3]))
            elif list_num[5] == str(id) and list_num[1] =='배추' and list_num[7] =='마트':
                cabbage_price_mart.append(int(list_num[3]))

#########
    list_num02 = []
    cheaper_price_si = []
    cheaper_price_mart = []

    c_m_image_src_li = []
    c_s_image_src_li = []

    label_mart = []
    label_si = []

    expensive_li = []
    cheap_li = []

    # price_vs_lists = pd.read_excel('C:/mc_final_data/jang_mart_price_vs.xlsx')

# 시장과 대형마트 가격비교 - 해당 농산물 이미지 넣기
    with open('C:/mc_final_data/jang_mart_price_vs.csv',
              mode='r') as seoul_lists02:
        reader = csv.reader(seoul_lists02)

        for list_num02 in reader:
            if list_num02[0] == str(id) and list_num02[3] == '시장':
                cheaper_price_mart.append(str(list_num02[4]))
            elif list_num02[0] == str(id) and list_num02[3] == '마트':
                cheaper_price_si.append(str(list_num02[4]))

        for i in cheaper_price_mart:
            if i == '무' :
                # c_m_image_src_li.append("Radish.jpg")
                label_mart.append(1)
            elif i == '배추' :
                label_mart.append(2)
            elif i == '상추' :
                label_mart.append(3)
            elif i == '양파' :
                label_mart.append(4)
            elif i == '오이' :
                label_mart.append(5)

        for i in cheaper_price_si:
            if i == '무' :
                label_si.append(1)
            elif i == '배추' :
                label_si.append(2)
            elif i == '상추' :
                label_si.append(3)
            elif i == '양파' :
                label_si.append(4)
            elif i == '오이' :
                label_si.append(5)


# 서울에 비해 00구의 가격 수준은?
# 지역별 농산물 싼곳, 비싼곳
    with open('C:/mc_final_data/dict_expensive_cheap.csv',
              mode='r') as dict_expensive_cheap:
        reader = csv.reader(dict_expensive_cheap)

        for ex_li in reader:
            if ex_li[0] == str(id) :
                expensive_li.append(str(ex_li[1]))
                cheap_li.append(str(ex_li[2]))

        expensive_li = ','.join(expensive_li)
        cheap_li = ','.join(cheap_li)



    context = {
        'cheaper_price_si': cheaper_price_si,
        'cheaper_price_mart': cheaper_price_mart,

        'cabbage_price_si': cabbage_price_si,
        'cabbage_price_mart': cabbage_price_mart,
        'name': id,
        'c_m_image_src_li' : c_m_image_src_li,
        'c_s_image_src_li': c_s_image_src_li,

        'expensive_li' : expensive_li,
        'cheap_li' : cheap_li,

        'label_mart' : label_mart,
        'label_si' : label_si,
    }

    return render(request, 'finalApp/noonegu.html', context)




def noonegucabbage(request):
    return render(request, 'finalApp/noonegu_cabbage.html')

def noonegucabbageajax(request):
    exmaple = 'noonegu_cabbage'
    data = {'noonegucabbage' : exmaple}
    return JsonResponse(data, safe=False)
@csrf_exempt
def ajax_test(request):
    if 'number' in request.POST:
        num = request.POST['number']

    if num=='1':
      answer = {str(num):"1입니다."}                # json형식으로 넘겨줄 데이터를 만들어준다.
    else:
        answer = {str(num):"1이 아닙니다."}

    return JsonResponse(answer)

@xframe_options_exempt
def ok_to_load_in_a_frame(request):
    return HttpResponse("This page is safe to load in a frame on any site.")

@xframe_options_deny
def view_one(request):
    return HttpResponse("I won't display in any frame!")



def noonegucabbageajaxgraph(self, request):
    day = []
    category = []
    price = []
    region = []
    location = []
    division = []

    # list_num = []

    with open('C:/mc_final_data/seoul_mart_jang_graph.csv', mode='r') as seoul_lists:
        reader = csv.reader(seoul_lists)

        for list in reader:
            day.append(list[0])
            category.append(list[1])
            price.append([3])
            region.append([5])
            location.append([6])
            division.append([7])
        data = {
            'day' : day,
            'category' : category,
            'price' : price,
            'region' : region,
            'location' : location,
            'division' : division,
        }
    return render(request, 'finalApp/noonegu.html', data)

# def get(self, request, *args, **kwargs):
#         return render(request, 'finalApp/noonegu.html', )


def auctionPriceGraph(self, request):

    day = []
    price = []

    with open('C:/mc_final_data/weather_test.csv', mode='r') as seoul_lists:
        reader = csv.reader(seoul_lists)

        for list in reader:
            day.append(list[0])
            price.append(list[1])

        context = {
            'day': day,
            'price': price,
        }

    return render(request, 'finalApp/shop.html', context)

