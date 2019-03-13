from __future__ import unicode_literals

from django.db import models

# Create your models here.



class Share(models.Model):
	"""
	Stores a share of a company, related to :model:`sellbuy.SharePrice` and :model:`portfolio.portfolio` and :
	"""
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=120,blank=True,null=True)
	company_name = models.CharField(max_length=120,blank=True,null=True)
	current_price = models.FloatField(default=1000.0000)

	def __str__(self):
		return str(self.name)

class SharePrice(models.Model):
	"""
	Stores a single price of a share in a time, related to :model:`sellbuy.Share` 
	"""
	share = models.ForeignKey('Share')
	price = models.FloatField(default=1000.00)
	time = 	models.TimeField(auto_now=True)

	


