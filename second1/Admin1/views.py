
from django.shortcuts import render,redirect
from django.http import JsonResponse
from User.models import *
from Admin1.models import *


# Create your views here.
def Index(request):
    if request.session.has_key('key'):
        return redirect(AdminDash)
    else:
        if request.method =='POST':
            username=request.POST["username"]
            password=request.POST["password"]
            if (username =="finasvm" and password =="1234"):
                request.session['key'] = 'sir'
                return JsonResponse('true', safe=False)
            else:
                return JsonResponse('false', safe=False)

        else:
            return render(request,'admin/adminlogin.html')

def AdminDash(request):
    return render(request,'admin/base.html')

def UserTable(request):
    if request.session.has_key('key'):
        users= Person.objects.all()
        return render(request,'admin/User view.html',{'users' : users})
    else:
        return redirect(Index)

def Block(request,pk):
    if request.session.has_key('key'):
        current_user = Person.objects.get(id=pk)
        user=User.objects.get(id=current_user.user_id)
        if user.is_active == True:
            user.is_active = False
            user.save()
            return redirect(UserTable)
        else:
            user.is_active = True
            user.save()
            return redirect(UserTable)
    else:
        return redirect(Index)

def AddCategory(request):
    if request.session.has_key('key'):
        if request.method == 'POST':
            category=request.POST['category']
            Add_Category.objects.create(category=category)
            return redirect(AddedCategory)
        else:
            return render(request,'admin/AddCategory.html')
    else:
        return redirect(Index)

def AddedCategory(request):
    if request.session.has_key('key'):
        cat=Add_Category.objects.all()
        return render(request,'admin/addedcategory.html',{'cat': cat})
    else:
        return redirect(Index)

def DeleteCategory(request,pk):
    if request.session.has_key('key'):
        categ = Add_Category.objects.get(id=pk)
        categ.delete()
        return redirect(AddedCategory) 
    else:
        return redirect(Index)
    

def Product_Sanction(request):
    if request.session.has_key('key'):
        products = addProduct.objects.all()
        return render(request,'admin/Product_confirmation.html',{'bidproduct':products})
    else:
        return redirect(Index)

def Product_Status_change(request):
    if request.session.has_key('key'):
        if request.method == 'POST':
            values =request.POST['Value']
            id1 = request.POST['id1']
            orders = addProduct.objects.get(id=id1)
            orders.Status = values
            orders.save()
            return JsonResponse('true',safe=False)
        else:
            return redirect(Product_Sanction)
    else:
        return redirect(Index1)






