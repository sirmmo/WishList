from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.db.models import Q

from core.models import *

import json

#APIS

def verbs(request):
	return HttpResponse(json.dumps({str(v.id):{"name":v.name} for v in Verb.objects.all()}))

def wishlisttypes(request):
	return HttpResponse(json.dumps({str(v.id):{"name":v.name, "icon":v.icon} for v in WishListType.objects.all()}))

def wishlistitemtypes(request):
	return HttpResponse(json.dumps({str(v.id):{"name":v.name, "icon":v.icon} for v in WishListItemType.objects.all()}))



def profile(request, user):
	u = User.objects.get(username = user)
	return HttpResponse(json.dumps({"username":u.username, "birthday":u.profile.all()[0].birthday}))

def wishlists(request, owner=None, wishlist=None):
	if owner is None:
		owner = request.user.username
	if request.REQUEST.get("add") is None:
		return HttpResponse(json.dumps({"wishlists":[{"name":wl.name, "id":wl.id, "type":wl.type, "public":wl.public} for wl in WishList.objects.filter(owner__username = owner, Q(owner=request.user.usernane)|Q(watchers__contains=requqest.user)|Q(public=True))]}))
	else:
		wl = WishList()
		wl.name = request.REQUEST.get("add")
		wl.owner = request.user
		wl.save()
		return HttpResponse({"result":"ok"})

def watchers(request, owner, wishlist):
	wl = WishList.objects.filter(id=wishlist, Q(owner=request.user.usernane)|Q(watchers__contains=requqest.user)|Q(public=True))
	wl.watchers.add(User.objects.get(username=request.REQUEST.get("username")))
	wl.save()
	return HttpResponse({"result":"ok"})

def items(request, owner, wishlist):
	wl = WishList.objects.filter(id=wishlist, Q(owner=request.user.usernane)|Q(watchers__contains=requqest.user)|Q(public=True))
	if wl.count() == 0:
		return HttpResponseForbidden()
	wl = wl[0]
	return HttpResponse(json.dumps({"wishlist":{"name":wl.name, "id":wl.id, "type":wl.type}, "items":[ {"id":i.id, "type":i.type, "description":i.description, "url":i.item.url, "picture":i.item.picture, "lon":i.item.lon, "lat":i.item.lat} for i in wl.wishlistitems.all()]}))

def map(request):
	return HttpResponse(json.dumps({"type":"FeatureCollection", "features":[{"type":"Feature", "geometry":{"type":"Point", "coordinates":[i.lon, i.lat]},  "properties":{"picture":i.picture, "url":i.url, "wishlists":i.wishlists.count()}} for i in Item.objects.exclude(lon__isnull=True, lat__isnull=True)]}))


def add_item(request):
	wl = WishList.objects.get(id=request.REQUEST.get("wl"))

	if request.REQUEST.get("url") is not None:
		i, c = Item.objects.get_or_create(url=request.REQUEST.get("url"))		
	else:
		i = Item()
		c = True

	if request.REQUEST.get("pic") is not None:
		i.picture = request.REQUEST.get("pic")	
	if request.REQUEST.get("lon") is not None:
		i.lon = float(request.REQUEST.get("lon"))
		i.lat = float(request.REQUEST.get("lat"))
	i.save()

	wli = WishListItem()
	wli.wishlist = wl
	wli.item = i
	if request.REQUEST.get("t") is not None:
		wli.type = WishListItemType.objects.get(id=request.REQUEST.get("t"))
	if request.REQUEST.get("description") is not None:
		wli.description = request.REQUEST.get("description")

	wli.save()

	return HttpResponse(json.dumps({"item":i.id, "wishlistitem":wli.id, "wishlist":wl.id, "result":"ok"}))

def add_comment(request, owner, wishlist, wishlistitem=None):
	pass

def activities(request):
	f = int(request.REQUEST.get("f", "0"))
	t = f+50
	return HttpResponse(json.dumps({"activities":[{"user":a.user.username, "verb":a.verb.name, "datetime":a.datetime, "obj_ct":a.content_type, "obj":a.content_object} for a in Activity.objects.all()[f:t]]}))



# VIEWS
def index(request):
	return render(request, "index.html")

