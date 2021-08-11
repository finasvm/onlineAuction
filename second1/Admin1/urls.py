from django.urls import path

from . import views

urlpatterns = [

     path('',views.Index,name="Index"),
     path('AdminDash/',views.AdminDash,name="AdminDash"),
     path('UserTable/',views.UserTable,name="UserTable"),
     path('Block/<int:pk>/',views.Block,name="Block"),
     path('Block/<int:pk>/',views.Block,name="Block"),
     path('AddCategory/',views.AddCategory,name="AddCategory"),
     path('AddedCategory/',views.AddedCategory,name="AddedCategory"),
     path('DeleteCategory/<int:pk>/',views.DeleteCategory,name="DeleteCategory"),
     path('Product_Sanction/',views.Product_Sanction,name="Product_Sanction"),
     path('Product_Status_change/',views.Product_Status_change,name="Product_Status_change"),
     


]