from django.shortcuts import render
from sellbuy.models import *
from django.http import HttpResponse , HttpResponseRedirect
from .models import *
from django.contrib.auth.decorators import login_required
from plotly.offline import plot
from plotly.graph_objs import Bar , Scatter
import datetime
import tushare as ts


# Create your views here.
@login_required
def sellbuy(request):

	if request.method == "POST":
		# print(request.POST)
		share_choice = request.POST.get('shareid')
		# print(share_choice)
		quantity = int(request.POST.get('quantity'))
		# print(quantity)
		user = request.user.username


		user_holding_obj = CurrentUserHolding.objects.get(user_id=user)
		current_holding = user_holding_obj.current_holdings
		

		# if the share id you buy does not exist in the database, this will add a new share
		try:
			share_obj = Share.objects.get(name=share_choice)
			share_price = share_obj.current_price
		except Share.DoesNotExist:
			try:
				ts.get_realtime_quotes(share_choice)
				real_share_data = ts.get_realtime_quotes(share_choice)
				new_share = Share.objects.create(name=share_choice, company_name=real_share_data['name'][0],
													current_price= float(real_share_data['price'][0]))
				new_share.save()
				share_obj = Share.objects.get(name=share_choice)
				share_price = share_obj.current_price
			except Exception, e:
				return HttpResponse("Adding Stock ID Failed")	

		

		

		if quantity>int(0):

			if request.POST.get("button") == "BUY":
				
				if share_price*quantity <= current_holding:

					try:

						transaction_obj = Transaction.objects.create(share=share_choice,transaction='BY')
						transaction_obj.save()


						buy_obj = portfolio.objects.get(share_id=share_choice,user_id=user)
						buy_share_quantity = buy_obj.quantity

						setattr(buy_obj , 'quantity' , buy_share_quantity+quantity)
						buy_obj.save()

						cash_in_hand = current_holding-(share_price*quantity)

						setattr(user_holding_obj , 'current_holdings' , cash_in_hand)
						user_holding_obj.save()
						
						

					except portfolio.DoesNotExist:
				
						new_obj = portfolio.objects.create(share_id=share_choice,user_id=user,quantity=quantity)
						

						
					return HttpResponse("Share Bought")

				else:
					return HttpResponse("Current Holding is less only "+str(int(current_holding/share_price))+" share can be bought")


			if request.POST.get("button") == "SELL":
				try:
					sell_obj = portfolio.objects.get(share_id=share_choice,user_id=user)
					sell_share_quantity = sell_obj.quantity
			
					if sell_share_quantity>=quantity:

						transaction_obj = Transaction.objects.create(share=share_choice,transaction='SL')
						transaction_obj.save()
					
						setattr(sell_obj, 'quantity' , sell_share_quantity-quantity)
						sell_obj.save()

						cash_in_hand = current_holding+(share_price*quantity)

						setattr(user_holding_obj , 'current_holdings' , current_holding+share_price*quantity)
						user_holding_obj.save()

						




						return HttpResponse("Shares Sold")

					else:
						return HttpResponse("You don't have enough shares !")	
				
				except portfolio.DoesNotExist:
					return HttpResponse("You have not bought these shares !")		
		
		else:
			return	


@login_required
def profit_loss_graph(request,name):
	
	obj = UserHolding.objects.filter(user_id=name)

	x=[]
	y=[]

	for o in obj:
		x.append(o.time)
		# print(type(o.time))
		y.append(o.holdings)

	return HttpResponse(plot([Scatter(x=x, y=y)],auto_open=False,output_type='div'))	

			
				

		


	