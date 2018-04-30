from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
import requests
import urllib.request
import csv

from rest_framework.views import APIView
from rest_framework.response import Response



class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'charts.html', {})

def get_data(request,*args,**kwargs):
    data={
        "China":3,
        "Japan":2,
    }
    return JsonResponse(data) #http response


class ChartData(APIView):

    authentication_classes = []
    permission_classes = []
    
        














    def get(self, request, format=None):
        labels2=[]
        default_items2=[]
        labels=[]
        default_items=[] 
        url = 'https://my.api.mockaroo.com/interview-api-1.json?key=e6ac1da0'
        response = requests.get(url)
        if response.status_code != 200:
            print('Failed to get data:', response.status_code)
        else:
            c=dict() #hashmaps are an effective data structure here, c is for county, m is for make
            m=dict()
            wrapper = csv.reader(response.text.strip().split('\n'))
            for record in wrapper:
                if record[0] != 'id': #checks after first line of mockaroo
                    id=int(record[0]) # holds values
                    country=str(record[1])
                    model=str(record[2])
                    make=str(record[3])
                    sold_by=str(record[4])
                    price=int(record[5])
                    if country in c: #if country inside of dictionary, then increase its count by 1
                        c[country]+=1
                    else: #if country is not inside of dictionary, then set its count to 1
                        c[country]=1
                    if make in m:
                        m[make]+=1
                    else:
                        m[make]=1       
            for k,v in c.items():
                labels.append(k)
                default_items.append(v)
            
            for k,v in m.items():
                labels2.append(k)
                default_items2.append(v)
        
        # labels=["Russia","Brazil", "Nigeria", "Mexico", "Indonesia", "Serbia"]
        # default_items=[9,5,3,2,2,1]
        data={
                "labels":labels,
                "default":default_items,
                "labels2":labels2,
                "default2":default_items2,
        
        }
        return Response(data)