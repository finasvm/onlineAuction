from django.db.models.fields import DecimalField
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User,auth    
from .models import *
from django.contrib import messages
from django.core.files import File
import base64
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.contrib.auth.hashers import check_password
from datetime import date
from datetime import datetime
import time


# Create your views here.
def Index1(request):
    today = date.today()
    if request.user.is_authenticated:
        BidProducts=addProduct.objects.filter(Status='Confirm',bid_ends__gte = today,payment='not paid')
        context = {'Bidproducts':BidProducts}
        return render(request,'user/Bidded_Products.html',context)
    else:
        BidProducts=addProduct.objects.filter(Status='Confirm',bid_ends__gte = today,payment='not paid')
        return render(request,'user/Bidded_Products.html',{'Bidproducts':BidProducts})

def Sign_in(request):
    if request.user.is_authenticated:
        return redirect(Index1)
    else:
        if request.method =='POST':
            username=request.POST['username']
            password=request.POST['password']
            # user = auth.authenticate(username=username,password=password)
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                if user.is_active==True:
                    user = auth.authenticate(username=username,password=password)
                    if user is not None:
                        auth.login(request,user)
                        return JsonResponse('true', safe=False)
                        #return redirect('welcome')
                    else:
                        return JsonResponse('false', safe=False)
                        #messages.info(request,'USERNAME AND PASSWORD IS WRONG')
                else:
                    return JsonResponse('block',safe=False)
            else:
                return JsonResponse('false',safe=False)
        else:
            return render(request,'user/sign-in.html')

def Signup(request):
    if request.user.is_authenticated:
        return redirect(Index1)
    else:  
        if request.method =='POST' :
            username=request.POST['username']
            email=request.POST['email']
            number=request.POST['number']
            password=request.POST['password']   
            password_confirm=request.POST['password_confirm'] 
            if password == password_confirm:
                if User.objects.filter(username=username).exists():
                    return JsonResponse('false3', safe=False) 
                elif User.objects.filter(email=email).exists():
                    return JsonResponse('false4', safe=False)
                elif Person.objects.filter(number=number).exists():
                    return JsonResponse('false5', safe=False)
                else:
                    u = User.objects.create_user(username=username,email=email,password=password)
                    Person.objects.create(user=u,number=number)
                    return JsonResponse('true', safe=False) 
                
            else:
                return JsonResponse('false', safe=False)
        else:
            return render(request,'user/sign-up.html')

def Profile(request):
    if request.user.is_authenticated:
        User_Details = Person.objects.get(user=request.user)
        return render(request,'user/profile.html',{'User_Details':User_Details})
    else:   
        return redirect(Index1)

def Edit_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            username1 = request.POST['username']
            number1 = request.POST['number']
            email1= request.POST['email']
            u = User.objects.filter(id=request.user.id).update(username=username1,email=email1)
            Person.objects.filter(user=request.user).update(user=u,number=number1)
            return redirect(Profile)
        else:
            return redirect(Profile)
    else:
        return redirect(Index1)

def changepassword(request):
    if request.user.is_authenticated:
        if request.method =='POST':
            oldpass = request.POST['oldpass']
            newpass1 = request.POST['newpass']
            conpass = request.POST['conpass']
            current_password = request.user.password
            matchcheck = check_password(oldpass,current_password)
            if matchcheck == True:
                if newpass1 == conpass:
                    u = User.objects.get(id=request.user.id)
                    u.set_password(newpass1)
                    u.save()
                    return JsonResponse('true',safe=False)
                else:
                    return JsonResponse('false',safe=False)
            else:
                return JsonResponse('false1',safe=False)
    else:
        return redirect(Index1)

def SellProduct(request):
    if request.user.is_authenticated:
        categ=Add_Category.objects.all()
        return render(request,'user/sellproduct.html',{'categ': categ})
    else:
        return redirect(Index1)

def SendingProducts(request):
    if request.user.is_authenticated:
        if request.method =='POST' :
            p_name=request.POST['pro_name']
            p_desc=request.POST['pro_desc']
            p_cate=request.POST['p_cate']
            p_price=request.POST['p_price']
            timefrom=request.POST['timefrom']
            image1=request.POST['imageurl1']
            image2=request.POST['imageurl2']
            image3=request.POST['imageurl3']
            persuser = Person.objects.get(user=request.user)  
            today =  datetime.today().strftime('%Y-%m-%d')
            one = timefrom
            print(today)
            print(one)     
            if image1 == '' or image2 == '' or image3 == '': 
                messages.info(request,'you should crop the images')
                return redirect(SellProduct)
            elif(one == today):
                messages.info(request,'you cannot take today as deadline ')
                return redirect(SellProduct)
            else:
                format, imgstr1 = image1.split(';base64,')
                ext = format.split('/')[-1]
                img1 = ContentFile(base64.b64decode(imgstr1),name=p_name+ '.' + ext)
                
                format, imgstr2 = image2.split(';base64,')
                ext1 = format.split('/')[-1]
                img2 = ContentFile(base64.b64decode(imgstr2),name=p_name+ '.' + ext1)
                
                format, imgstr3 = image3.split(';base64,')
                ext2 = format.split('/')[-1]
                img3 = ContentFile(base64.b64decode(imgstr3),name=p_name+ '.' + ext2)

                category = Add_Category.objects.get(category=p_cate)
                addproduct = addProduct.objects.create(p_name=p_name,p_desc=p_desc,p_cate=category,p_price=p_price,bid_ends=timefrom,Main_image=img1,secondary_image=img2,ter_image=img3,Status='pending',Seller=persuser)

                addproduct.save()
                return redirect(Index1)
    else:
        return redirect(Index1)

def bid_details(request):
    if request.user.is_authenticated:
        products = addProduct.objects.all()
        return render(request,'user/bid_Details.html',{'bidproduct':products})
    else:
        return redirect(Index1)

def auction_details(request,pk):
    if request.user.is_authenticated:
        request.session['bid']=pk
        products = addProduct.objects.get(id=pk)
        try:
            Bid = Bidding.objects.filter(Products=pk).order_by('-Bid_Price')
            winner = Bid[0]
            today = date.today()
            Buyer = Person.objects.get(user=request.user)
            print(today)
            print(products.bid_ends)
            print(winner.buyer)
            print(Buyer)
            print(winner)
            if products.bid_ends == today:
                context = {'bidproduct':products,'bid':Bid,'winner':winner}
                return render(request,'user/bid_winner.html',context)
            else:
                print('////////')
                context = {'bidproduct':products,'bid':Bid,'winner':winner}
                print('//////////')
                return render(request,'user/auction_details.html',context)
        except:
            context = {'bidproduct':products}
            return render(request,'user/no_bid.html',context)
    else:
        return redirect(Index1)
 



def submit_bid(request,pk):      
    if request.user.is_authenticated:
        request.session['bid']=pk
        products = addProduct.objects.get(id=pk)
        try:
            Bid = Bidding.objects.filter(Products=pk).order_by('-Bid_Price')
            winner = Bid[0]
            today = date.today()
            Buyer = Person.objects.get(user=request.user)
            print(today)
            print(products.bid_ends)
            print(winner.buyer)
            print(Buyer)
            print(winner)
            if winner.buyer == Buyer and  products.bid_ends == today:         
                context = {'bidproduct':products,'bid':Bid,'winner':winner}
                return render(request,'user/winner_user.html',context)
            elif products.bid_ends == today:
                context = {'bidproduct':products,'bid':Bid,'winner':winner}
                return render(request,'user/bid_winner.html',context)
            else:
                print('////////')
                context = {'bidproduct':products,'bid':Bid,'winner':winner}
                print('//////////')
                return render(request,'user/submit_bid.html',context)
        except:
            context = {'bidproduct':products}
            return render(request,'user/no_bid.html',context)
    else:
        return redirect(Index1)

def Bid_price(request):
    print('hbfjek')
    print('////////')
    if request.user.is_authenticated:
        if request.method =='POST':
            print('////////')
            id1=request.POST['id2']
            price1=request.POST['price']
            Product_Details = addProduct.objects.get(id=id1)
            User_Details = Person.objects.get(user=request.user)
            pro = (float(Product_Details.p_price))
            pri = (float(price1))
            if pro == pri: 
                return JsonResponse('false1', safe=False)
            elif (pri < pro):
                return JsonResponse('false1', safe=False)
            elif Bidding.objects.filter(Products=Product_Details,buyer=User_Details).exists():
                u = Bidding.objects.filter(Products=Product_Details,buyer=User_Details).update(Bid_Price=price1)
            else:
                Bidding_price = Bidding.objects.create(Products=Product_Details,Bid_Price=price1,buyer=User_Details)
                Bidding_price.save()
                Product_Details.p_price = price1
                Product_Details.save()
                print(Product_Details.p_price)
                Product_Details.save()
                try:
                    Bid = Bidding.objects.filter(Products=id1).order_by('-Bid_Price')
                    winner = Bid[0]
                    today = date.today()
                    Buyer = Person.objects.get(user=request.user)
                    if winner.buyer == Buyer and  Product_Details.bid_ends == today:         
                        context = {'bidproduct':Product_Details,'bid':Bid,'winner':winner}
                        return render(request,'user/winner_user.html',context)
                    elif products.bid_ends == today:
                        context = {'bidproduct':products,'bid':Bid,'winner':winner}
                        return render(request,'user/bid_winner.html',context)
                    else:
                        context = {'bidproduct':Product_Details,'bid':Bid,'winner':winner}
                        return render(request,'user/submit_user.html',context)
                except:
                    context = {'bidproduct':Product_Details,'bid':Bid,'winner':winner}
                    return render(request,'user/submit_user.html',context)
        else:
            pk = request.session['bid']
            products = addProduct.objects.get(id=pk)
            try:
                Bid = Bidding.objects.filter(Products=pk).order_by('-Bid_Price')
                winner = Bid[0]
                today = date.today()
                Buyer = Person.objects.get(user=request.user)
                print(products.bid_ends)
                print(winner.buyer)
                print(Buyer)
                print(winner)
                if winner.buyer == Buyer and  products.bid_ends == today:         
                    context = {'bidproduct':products,'bid':Bid,'winner':winner}
                    return render(request,'user/winner_user.html',context)
                elif products.bid_ends == today:
                    context = {'bidproduct':products,'bid':Bid,'winner':winner}
                    driver.navigate.refresh
                    return render(request,'user/bid_winner.html',context)
                else:
                    print('////////')
                    context = {'bidproduct':products,'bid':Bid,'winner':winner}
                    print('//////////')
                    return render(request,'user/submit_user.html',context)
            except:
                print('////////')
                context = {'bidproduct':products,'bid':Bid,'winner':winner}
                print('//////////')
                return render(request,'user/submit_user.html',context)
    else:
        return redirect(Index1)
    
def checkout(request,pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            Fullname = request.POST['fullname']
            pincode = request.POST['pincode']
            city = request.POST['city']
            state = request.POST['state']
            housename = request.POST['housename']   
            landmark = request.POST['landmark']
            user = Person.objects.get(user=request.user)
            address = User_Address.objects.create(Full_name=Fullname,pinCode=pincode,city=city,state=state,HouseName=housename,landMark=landmark,
            user_address=user)
            address_user = User_Address.objects.filter(user_address=user)
            winner_checkout = Bidding.objects.get(id=pk)
            request.session['winnerid'] = pk
            context = {'winner':winner_checkout,'address':address_user}
            return render(request,'user/checkout.html',context)
        else:
            add = Person.objects.get(user=request.user)
            address_user = User_Address.objects.filter(user_address=add)
            winner_checkout = Bidding.objects.get(id=pk)
            request.session['winnerid'] = pk
            context = {'winner':winner_checkout,'address':address_user}
            return render(request,'user/checkout.html',context)
    else:
        return redirect(Index1)

@csrf_exempt
def chooseaddress(request,id):
    request.session['addressid']=id
    return JsonResponse('true',safe=False)

@csrf_exempt
def payment(request):
    if request.method == 'POST':
        value = request.POST['value']
        if value == 'razarpay':
            return JsonResponse('true',safe=False)
        elif value == 'paypal':
            return JsonResponse('true1',safe=False)
        elif value == 'cod':
            return JsonResponse('true2',safe=False)
    else:
        add = Person.objects.get(user=request.user)
        address_user = User_Address.objects.filter(user_address=add)
        pk = request.session['winnerid'] 
        winner_checkout = Bidding.objects.get(id=pk)
        context = {'winner':winner_checkout,'address':address_user}
        return render(request,'user/checkout.html',context)

def cod(request):
    if request.user.is_authenticated:
        user = Person.objects.get(user=request.user)
        address = request.session['addressid']
        address1 = User_Address.objects.get(id=address)
        winner = request.session['winnerid']
        winners = Bidding.objects.get(id=winner)
        winner_price = winners.Bid_Price
        product_id = winners.Products
        prod = winners.Products.id
        product = addProduct.objects.get(id=prod)
        product.payment = 'PAID'
        product.save()
        Order.objects.create(user_order=user,Product=product_id,address=address1,Price=winner_price,Status="ordered",PaymentMethod="COD")
        return redirect(ordersuccess)
    else:
        return redirect(Index1)



def beforepaypal(request):
    id1 = request.session['winnerid'] 
    winner_cash = Bidding.objects.get(id=id1)
    price = winner_cash.Bid_Price
    grand_total = int(price)
    context = {'grand_total':grand_total}
    return render(request,'user/paypal.html',context)


def paypal(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            return JsonResponse('true',safe=False)
    else:
        return redirect(login)

def paypal_confirm(request):
    if request.user.is_authenticated:
        user = Person.objects.get(user=request.user)
        address = request.session['addressid']
        address1 = User_Address.objects.get(id=address)
        winner = request.session['winnerid']
        winners = Bidding.objects.get(id=winner)
        winner_price = winners.Bid_Price
        product_id = winners.Products
        prod = winners.Products.id
        product = addProduct.objects.get(id=prod)
        product.payment = 'PAID'
        product.save()
        Order.objects.create(user_order=user,Product=product_id,address=address1,Price=winner_price,Status="ordered",PaymentMethod="PAYPAL")
        return redirect(ordersuccess)
    else:
        return redirect(Index1)

def razarpay(request):
    id1 = request.session['winnerid'] 
    winner_cash = Bidding.objects.get(id=id1)
    price = winner_cash.Bid_Price
    grand_total = int(price)
    context = {'grand_total':grand_total}
    return render(request,'user/razarpay.html',context)

def razar_success(request):
    if request.user.is_authenticated:
        user = Person.objects.get(user=request.user)
        address = request.session['addressid']
        address1 = User_Address.objects.get(id=address)
        winner = request.session['winnerid']
        winners = Bidding.objects.get(id=winner)
        winner_price = winners.Bid_Price
        product_id = winners.Products
        prod = winners.Products.id
        product = addProduct.objects.get(id=prod)
        product.payment = 'PAID'
        product.save()
        Order.objects.create(user_order=user,Product=product_id,address=address1,Price=winner_price,Status="ordered",PaymentMethod="RAZARPAY")
        return redirect(ordersuccess)
    else:
        return redirect(Index1)




def ordersuccess(request):
    if request.user.is_authenticated:
        if request.session.has_key('winnerid'):
            del request.session['winnerid']
            return render(request,'user/ordersuccess.html')
    else:
        return redirect(Index1)
def Logout(request):
    auth.logout(request)
    return redirect(Index1)
