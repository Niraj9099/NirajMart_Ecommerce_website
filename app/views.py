from django.shortcuts import render, redirect
from .models import User, Customer, Product, Cart, OrderPlace
from .form import UserragistrationForm, CustomerForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import F, Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def home(request): 
    topware = Product.objects.filter(category='TW')
    bottomware = Product.objects.filter(category='BW')
    mobile = Product.objects.filter(category='M')
    cart_lenth = 0
    if request.user.is_authenticated:
       cart_lenth = Cart.objects.filter(user=request.user).count()
    return render(request, 'app/home.html', {'topware':topware, 'bottomware':bottomware, 'mobile':mobile, 'cart_lenth':cart_lenth})


def search(request):
   name = request.GET.get('search')
   print('name' , name)
   data = Product.objects.filter(title__icontains=name)
   return render(request, 'app/search.html', {'data':data})



def product_detail(request, id):
    cart_lenth = 0
    exis = 0
    if request.user.is_authenticated:
      cart_lenth = Cart.objects.filter(user=request.user).count()
      exis = Cart.objects.filter(Q(product = id) & Q(user=request.user))
    product_item = Product.objects.get(pk=id)
    # print(exis)
    return render(request, 'app/productdetail.html', {'item':product_item, 'exis':exis, 'cart_lenth':cart_lenth})

@login_required
def add_to_cart(request):
    if request.user.is_authenticated:
      user = request.user
      product_id = request.GET.get('prod_id')
      product_data = Product.objects.get(id=product_id)
      Cart(user=user, product=product_data).save()
      return redirect('/cart')
    else:
       return redirect('/accounts/login/')

@login_required
def add_to_checkout(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product_data = Product.objects.get(id=product_id)
    check = Cart.objects.filter(Q(user=user) & Q(product=product_data))
    if (check):
      pass
    else:
      Cart(user=user, product=product_data).save()
    # return redirect('/checkout')
    customer = Customer.objects.filter(user=user)
    cart = Cart.objects.filter(Q(user=user) & Q(product=product_data))
    amount = 0.0
    delivery_charge = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user==user and p.product==product_data]
    if cart_product:
        for p in cart_product:
          temp_amount = (p.quantity * p.product.discount_price)
          amount += temp_amount
          totalamount = amount + delivery_charge  
    return render(request, 'app/checkout.html',{'add':customer, 'cart':cart,'totamount':totalamount})


@login_required
def show_cart(request):
   if request.user.is_authenticated:
      cart_lenth = Cart.objects.filter(user=request.user).count()
      user = request.user
      cart_data = Cart.objects.filter(user=user)
      amount = 0.0
      delivery_charge = 70.0
      totamount = 0.0
      cart_product = [p for p in Cart.objects.all() if p.user==user]
      if cart_product:
         for p in cart_product:
            temp_amount = (p.quantity * p.product.discount_price)
            amount += temp_amount
            totamount = amount + delivery_charge
      return render(request, 'app/addtocart.html', {'cart':cart_data, 'amount':amount, 'totamount':totamount, 'cart_lenth':cart_lenth})

def plus_cart(request):
   if request.method == 'GET':
      prod_id = request.GET['prod_id']
      print('ids = ' ,prod_id)
      c = Cart.objects.get(Q(product=prod_id) & Q(user = request.user))
      c.quantity += 1
      c.save()
      amount = 0.0
      delivery_charge = 70.0
      totamount = 0.0
      cart_product = [p for p in Cart.objects.all() if p.user==request.user]
      for p in cart_product:
            temp_amount = (p.quantity * p.product.discount_price)
            amount += temp_amount
            totamount = amount + delivery_charge
      data = {
         'quantity' : c.quantity,
         'amount' : amount,
         'totalamount' : totamount
      }
      return JsonResponse(data)

def minus_cart(request):
   if request.method == 'GET':
      prod_id = request.GET['prod_id']
      print('ids = ' ,prod_id)
      c = Cart.objects.get(Q(product=prod_id) & Q(user = request.user))
      if c.quantity == 1:
        c.quantity = 1
      else:
        c.quantity -= 1
      c.save()
      amount = 0.0
      delivery_charge = 70.0
      totamount = 0.0
      cart_product = [p for p in Cart.objects.all() if p.user==request.user]
      for p in cart_product:
            temp_amount = (p.quantity * p.product.discount_price)
            amount += temp_amount
            totamount = amount + delivery_charge
      data = {
         'quantity' : c.quantity,
         'amount' : amount,
         'totalamount' : totamount
      }
      return JsonResponse(data)

# logic to add and remove quntity:

# def Add_Quntity(request, id):
#     user = request.user
#     product = id
#     cart_item, created = Cart.objects.update_or_create(
#         user=user,
#         product=product,
#         defaults={
#             'quantity': F('quantity') + 1  # Use F() expression to increment the existing value
#         }
#     )
#     print('hii', cart_item.quantity)
#     return redirect('/cart')

# def Mines_Quntity(request, id):
#     user = request.user
#     product = id
#     qty = Cart.objects.filter(Q(user=user) & Q(product=product)).first().quantity
#     if qty == 1:
#        pass
#     else:
#       cart_item, created = Cart.objects.update_or_create(
#           user=user,
#           product=product,
          
            
#           defaults={
#               'quantity': F('quantity') - 1  # Use F() expression to increment the existing value
#           }
#       )
#       print('hii', cart_item.quantity)
#     return redirect('/cart')



def remove_cart(request, id):
   pi = Cart.objects.get(pk=id)
   pi.delete()
   return redirect('/cart')



@login_required
def buy_now(request):
    return render(request, 'app/buynow.html')

@login_required
def profile(request):
    if request.method == 'POST':
       cp = CustomerForm(request.POST)
       if cp.is_valid():
          usr = request.user
          nm = cp.cleaned_data['name']
          vl = cp.cleaned_data['village']
          ct = cp.cleaned_data['city']
          pc = cp.cleaned_data['pincode']
          st = cp.cleaned_data['state']
          ck = Customer(user=usr, name=nm, village=vl,city=ct,pincode=pc,state=st)
          ck.save()
          messages.success(request, 'Profile Update Successfully !!!')
          cp = CustomerForm()
    else:
      cp = CustomerForm()
    return render(request, 'app/profile.html', {'form':cp})

@login_required
def address(request):
    data = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'data':data})


@login_required
def change_password(request):
    return render(request, 'app/changepassword.html')


def mobile(request, data=None):
    
    if data == None :
      context = {
        'mobile' : Product.objects.filter(category="M"),
        'blue0' : 'active'
      }
    elif data == 'redmi':
      context = {
        'mobile' : Product.objects.filter(category="M").filter(brand=data),
        'blue1' : 'active'
      }
    elif data == 'samsung':
      context = {
        'mobile' : Product.objects.filter(category="M").filter(brand=data),
        'blue2' : 'active'
      }
    elif data == 'upto':
      context = {
        'mobile' :  Product.objects.filter(category="M").filter(discount_price__lte=10000),
        'blue3' : 'active'
      }
    elif data == 'above':
        context = {
        'mobile' :   Product.objects.filter(category="M").filter(discount_price__gte=10000),
        'blue4' : 'active'
      }
    return render(request, 'app/mobile.html', context)


def customerregistration(request):
    if request.method == 'POST':
      fm = UserragistrationForm(request.POST)
      if fm.is_valid():
        name = fm.cleaned_data['username']
        email = fm.cleaned_data['email']
        print("email" , email)
        fm.save()
        messages.success(request, 'Ragistration Successfully !!!')
        # try:   
        subject = 'Welcome To NirajMart'
        message = f'Hi {name}, thank you for registering in NirajMart.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail( subject, message, email_from, recipient_list )
        # except:
        #   pass
        fm = UserragistrationForm()
    else:
      fm = UserragistrationForm()
    return render(request, 'app/customerregistration.html', {'form':fm})


@login_required
def checkout(request):
    cart_lenth = Cart.objects.filter(user=request.user).count()
    user = request.user
    customer = Customer.objects.filter(user=user)
    cart = Cart.objects.filter(user=user)
    amount = 0.0
    delivery_charge = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user==user]
    if cart_product:
        for p in cart_product:
          temp_amount = (p.quantity * p.product.discount_price)
          amount += temp_amount
          totalamount = amount + delivery_charge  
    return render(request, 'app/checkout.html',{'add':customer, 'cart':cart,'totamount':totalamount, 'cart_lenth':cart_lenth})

@login_required
def payment_done(request):
   user = request.user
   custid = request.GET.get('custid')
   customer = Customer.objects.get(id=custid)
   cart = Cart.objects.filter(user=user)
   for c in cart:
      OrderPlace(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
      c.delete()
   return redirect("orders")

@login_required
def orders(request):
    op = OrderPlace.objects.filter(user = request.user)
    return render(request, 'app/orders.html', {'op':op})
