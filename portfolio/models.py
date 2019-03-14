from __future__ import unicode_literals

from django.db import models

# Create your models here.
class portfolio(models.Model):
	"""
	Stores a paricular amount of share of a company a user has bought, related to :model:`register.UserDetails` and :model:`sellbuy.Share` 
	"""
	share_id = models.CharField(max_length=120,blank=True,null=True)
	user_id = models.CharField(max_length=120,blank=True,null=True)
	quantity = models.IntegerField(default=0)
	

class UserHolding(models.Model):
	"""
	Stores the total stock value of a user, related to :model:`register.UserDetails`
	"""
	user_id = models.CharField(max_length=120,blank=True,null=True)
	time = models.DateTimeField(auto_now=True)
	holdings = models.FloatField(default=10000.00)

class CurrentUserHolding(models.Model):
	"""
	Stores the current holding money of a user, related to :model:`register.UserDetails`
	"""
	user_id = models.CharField(max_length=120,blank=True,null=True)
	current_holdings = models.FloatField(default=10000.00)

class Transaction(models.Model):
	"""
	Stores a transaction of a user, and the bought/sell share name, related to :model:`sellbuy.Share` 
	"""
	SELL = 'SL'
	BUY = 'BY'
	TRANSACTION_TYPE = (
		(SELL,'Sell'),
		(BUY,'Buy'),
		)
	share = models.CharField(max_length=120)
	transaction = models.CharField(max_length=20,choices=TRANSACTION_TYPE)