from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^kvp/verbs$', "core.views.verbs"),
    url(r'^kvp/wishlisttypes$', "core.views.wishlisttypes"),
    url(r'^kvp/wishlistitemtypes$', "core.views.wishlistitemtypes"),


    url(r'^lists$', "core.views.wishlists"),
    url(r'^lists/owner$', "core.views.wishlists"),
    url(r'^lists/owner/wishlist$', "core.views.wishlists"),
    url(r'^lists/owner/wishlist/watchers$', "core.views.watchers"),

    url(r'^map.geojson$', "core.views.map"),

    url(r'^items/add$', "core.views.add_item"),

    url(r'^activities$', "core.views.activities"),
)
