from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:item_id>", views.item_view, name="item"),
    path("accounts/login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:item_id>/watchlist", views.watchlist_view, name="watchlist"),
    path("watchlist", views.watchlist_view, name="watchlist_listing"),
    path("<int:item_id>/bid", views.bid_view, name="bid"),
    path("listing", views.create_listing_view, name="listing"),
    path("<int:item_id>/comments", views.comments_view, name="comments"),
]
