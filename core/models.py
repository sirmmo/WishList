from django.db import models

from django.contrib.auth.models import * 
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType



class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True, related_name="profile")
	birthday = models.DateField()



class Item(models.Model):
	url = models.UrlField(blank = True, null=True)
	picture = models.UrlField(blank = True, null=True)
	lon = models.FloatField(blank = True, null=True)
	lat = models.FloatField(blank = True, null=True)

	class Meta:
		unique_together=["url", "picture"]



class WishListType(models.Model):
	name = models.CharField(max_length=1000)
	icon = models.UrlField()

class WishListItemType(models.Model):
	name = models.CharField(max_length=1000)
	icon = models.UrlField()



class Verb(models.Model):
	name = models.TextField()

class Activity(models.Model):
	user = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    verb = models.ForeignKey(Verb)
    datetime = models.DateTimeField(auto_now=True)
    


class WishList(models.Model):
	owner = models.ForeignKey(User)
	type = models.ForeignKey(WishListType, blank = True, null=True)
	watchers = models.ManyToManyField(User, blank=True, null=True)
	public = models.BooleanField(default=False)
	name = models.CharField(max_length=1000)
	created = models.DateTimeField(auto_now=True)

class WishListItem(models.Model):
	wishlist = models.ForeignKey(WishList, related_name = "wishlistitems")
	type = models.ForeignKey(WishListItemType, blank = True, null=True)
	item = models.ForeignKey(Item, related_name="wishlists")
	description = models.TextField()
	created = models.DateTimeField(auto_now=True)

class WishListItemClosure(models.Model):
	wishlistitem = models.ForeignKey(WishListItem)
	date = models.DateField()

class WishListComment(models.Model):
	wishlist = models.ForeignKey(WishList)
	created = models.DateTimeField(auto_now=True)
	user = models.ForeignKey(User)
	comment = models.TextField()

class WishListItemComment(models.Model):
	wishlistitem = models.ForeignKey(WishListItem)
	created = models.DateTimeField(auto_now=True)
	user = models.ForeignKey(User)
	comment = modles.TextField()

class WishListRating(models.Model):
	wishlist = models.ForeignKey(WishList)
	created = models.DateTimeField(auto_now=True)
	user = models.ForeignKey(User)
	rating = models.IntegerField()

class WishListItemRating(models.Model):
	wishlistitem = models.ForeignKey(WishListItem)
	created = models.DateTimeField(auto_now=True)
	user = models.ForeignKey(User)
	rating = models.IntegerField()
