from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse , JsonResponse
from .models import * 
from django.contrib.auth.decorators import login_required
from portfolio.models import *
from plotly.offline import plot
from plotly.graph_objs import Bar , Scatter
from datetime import datetime
import time
from django.core import serializers
import random
import tushare as ts


@login_required
def share_price(request):
	user = request.user
	share_obj = Share.objects.order_by("name")
	
	

	return render(request,"sellbuy/transaction.html",{"share_obj" :share_obj })

@login_required
def current_price(request):
	share_obj = Share.objects.order_by("name")
	shares = Share.objects.all() 
	
	for share in shares:
			real_data = ts.get_realtime_quotes(share.name)
			share_price = float(real_data['price'][0])
			company_name_real = real_data['name'][0]

			new_share = SharePrice.objects.create(share=share, price=share_price)
			new_share.save()

			setattr(share, 'company_name', company_name_real)
			setattr(share, 'current_price', share_price)
			share.save()
	
	portfolio_obj = portfolio.objects.filter(user_id=request.user)
	

	total_share_value = float(0)
	total_quantity = float(0)

	for obj in portfolio_obj:
		temp_share = Share.objects.get(name=obj.share_id)
		total_share_value += temp_share.current_price
		total_quantity += obj.quantity

	holdings = float(total_share_value) * float(total_quantity)	

	holdings = round(holdings,2)

	user_holding_obj = UserHolding.objects.create(user_id=str(request.user),holdings=holdings)
	user_holding_obj.save()	


	data=""
	
	for obj in share_obj:
		data+="<tr><td class='center'>"+ str(obj.current_price) +"</td></tr>"

	return HttpResponse(data)




@login_required
def currentholding(request):
	user = request.user
	current_user_holding_obj = CurrentUserHolding.objects.get(user_id=user)
	current_holding = current_user_holding_obj.current_holdings

	return HttpResponse(current_holding)


@login_required
def current_quantity(request):
	user = request.user
	share_obj = Share.objects.order_by("name").distinct()


	data=""
	for obj in share_obj:
		try:
			portfolio_obj = portfolio.objects.get(user_id=user, share_id=obj.name)
			data+="<tr><td class='center'>"+str(portfolio_obj.quantity)+"</td></tr>"
		except portfolio.DoesNotExist:
			data+="<tr><td class='center'>"+str(0)+"</td></tr>"

	return HttpResponse(data)	



@login_required
def sharegraph(request,name):
	x=[]
	y=[]
	data_history = ts.get_hist_data(name, ktype='60')
	#data_history.reindex(index=data_history.index[::-1])
	for index, row in data_history.iterrows():
		x.append(datetime.strptime(index, '%Y-%m-%d %H:%M:%S'))
		print(x[-1])
		y.append(data_history.loc[index, 'ma5'])
	
	# today_history = ts.get_today_ticks(name)
	# today_str = datetime.now().strftime('%Y:%m:%d ')
	# for index, row in today_history.iterrows():
		# x.append(datetime.strptime(today_str + today_history.loc[index, 'time'], '%Y:%m:%d %H:%M:%S'))
		# y.append(today_history.loc[index, 'price'])
	
	share_obj = Share.objects.get(name=name)
	share_price_obj = SharePrice.objects.filter(share=share_obj)
	for obj in share_price_obj:
		x.append(obj.time)
		print(obj.time)
		y.append(obj.price)
	return HttpResponse(plot([Scatter(x=x, y=y)],auto_open=False,output_type='div'))	






	
	




