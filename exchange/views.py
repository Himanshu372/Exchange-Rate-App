from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from exchange.models import rateData
from exchange.serializers import rateDataSerializer
from rest_framework.response import Response
import requests
from datetime import datetime, timedelta
import json
from dateutil import relativedelta
from django.db import connection
from rest_framework.renderers import TemplateHTMLRenderer
from exchange.forms import ExchangeRateForm


def home(request):
    return render(request, 'exchange/index.html')

class ListRateDataView(viewsets.ModelViewSet):
    queryset = rateData.objects.all()
    serializer_class = rateDataSerializer
    template_name = 'exchange/exchange_data.html'

    def create(self, request, *args, **kwargs):
        '''

        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        form = ExchangeRateForm(request.GET)
        exchange_rate_base_api = 'https://api.exchangeratesapi.io/history'
        base_curr = request.POST.get('base_curr')
        target_curr = request.POST.get('target_curr')
        amount = request.POST.get('amount')
        max_waiting_time = request.POST.get('max_wait_time')
        start_date = request.POST.get('start_date')

        # if form.is_valid():
        #     data = form.cleaned_data
        #     base_curr = data.get('base_curr')
        #     target_curr = data.get('target_curr')
        #     amount = data.get('amount')
        #     max_waiting_time = data.get('max_wait_time')
        #     start_date = data.get('start_date')

        to_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        filtered_queryset = self.queryset.filter(base_currency__exact = base_curr, target_currency__exact = target_curr).order_by('-date')
        from_date = to_date - relativedelta.relativedelta(months = 2)

        #
        start_at = from_date
        end_at = to_date
        # end_at = datetime(end_at.year, end_at.month, end_at.day + 1).date()
        GET_API = exchange_rate_base_api + '?start_at={}&end_at={}&symbols={}&base={}'.format(start_at, end_at, target_curr, base_curr)
        rate_data = requests.get(GET_API).json()
        print(rate_data)
        for i in range(len(rate_data['rates'])):
            l = list(rate_data['rates'].keys())
            date = l[i]
            rate = rate_data['rates'][date][target_curr]
            print(date, rate)
            if len(filtered_queryset.filter(base_currency__exact = base_curr, target_currency__exact = target_curr, date__exact = date)) == 0:
                obj = rateData(base_currency = base_curr, target_currency = target_curr, date = date, rate = rate)
                obj.save()

        #
        result = {}
        result['type'] = 'line'
        result['data'] = {}
        result['data']['labels'] = []
        result['data']['datasets'] = []
        result['data']['datasets'].append({})
        result['data']['datasets'][0]['data'] = []
        result['data']['datasets'][0]['label'] = target_curr
        result['data']['datasets'][0]['borderColor'] = "#3e95cd"
        result['data']['datasets'][0]['fill'] = False
        result['options'] = {}
        result['options']['title'] = {}
        result['options']['title']['display'] = True
        result['options']['title']['text'] = 'Exchange Rate Forecasting'


        for i in range(int(max_waiting_time)):

            end_date = to_date
            start_date = to_date - relativedelta.relativedelta(days = 10)

            # while len(filtered_queryset.filter(date__exact = datetime.strftime(end_date, '%Y-%m-%d'))) == 0:
            #     end_date = end_date - relativedelta.relativedelta(days = 1)
            #     start_date = end_date - relativedelta.relativedelta(days = 3)

            end_date = datetime.strftime(end_date, '%Y-%m-%d')
            start_date = datetime.strftime(start_date, '%Y-%m-%d')

            avg_rate = "select avg(rate) as avg_rate from exchange_ratedata where date between '{}' and '{}'".format(start_date, end_date)
            cursor = connection.cursor()
            avg_rate = cursor.execute(avg_rate).fetchall()[0][0]
            # if len(avg_rate) == 0:
            #     avg_rate = list(result.keys())[i - 1]

            result['data']['labels'].append(end_date)
            result['data']['datasets'][0]['data'].append(avg_rate)

            # result[end_date] = avg_rate

            to_date = to_date + relativedelta.relativedelta(days = 1)
        return Response(result)



    def list(self, request, *args, **kwargs):
        '''

        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        form = ExchangeRateForm()
        args = {'form' : form}
        return render(request, self.template_name, args)