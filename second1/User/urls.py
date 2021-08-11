from django.urls import path

from . import views

urlpatterns = [

    path('',views.Index1,name="Index1"),
    path('Sign_in/',views.Sign_in,name="Sign_in"),
    path('Signup/',views.Signup,name="Signup"),
    path('Profile/',views.Profile,name="Profile"),
    path('Edit_profile/',views.Edit_profile,name="Edit_profile"),
    path('changepassword/',views.changepassword,name="changepassword"),
    path('SellProduct/',views.SellProduct,name="SellProduct"),
    path('SendingProducts/',views.SendingProducts,name="SendingProducts"),
    path('bid_details/',views.bid_details,name="bid_details"),
    path('auction_details/<int:pk>/',views.auction_details,name="auction_details"),
    path('submit_bid/<int:pk>/',views.submit_bid,name="submit_bid"),
    path('Bid_price/',views.Bid_price,name="Bid_price"),
    path('checkout/<int:pk>',views.checkout,name="checkout"),
    path('chooseaddress/<int:id>',views.chooseaddress,name='chooseaddress'),
    path('payment/',views.payment,name='payment'),
    path('cod/',views.cod,name='cod'),
    path('beforepaypal/',views.beforepaypal,name='beforepaypal'),
    path('paypal/',views.paypal,name='paypal'),
    path('paypal_confirm/',views.paypal_confirm,name='paypal_confirm'),
    path('razarpay/',views.razarpay,name='razarpay'),
    path('razar_success/',views.razar_success,name='razar_success'),
    path('ordersuccess/',views.ordersuccess,name='ordersuccess'),
    path('Logout/',views.Logout,name="Logout"),




]