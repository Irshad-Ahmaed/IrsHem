import datetime
import time
from email import message
import os
from django.shortcuts import render,redirect
import stripe
from store_app.models import Product,Categories,Filter_Price,Color,Brand,Contact_us,Order,OrderItem,Product_review, ORDERSTATUS
from django.conf import settings

from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from email.mime.image import MIMEImage
from django.template.loader import render_to_string

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.contrib import messages

from django.utils.html import strip_tags
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_KEY


def BASE(request):
    return render(request,'Main/base.html')

def HOME(request):
    #  Main start here
    product = Product.objects.filter(status = 'Publish')
    context = {
        'product':product,
    }
    
    return render(request, 'Main/index.html',context)

def PRODUCT(request):
    product = Product.objects.filter(status = 'Publish')
    categories = Categories.objects.all()
    filter_price = Filter_Price.objects.all()
    color = Color.objects.all()
    brand = Brand.objects.all()

    CAT_ID = request.GET.get('categories')
    # SIZE_ID = request.GET.get('size')
    PRICE_FILTER_ID = request.GET.get('filter_price')
    COLOR_ID = request.GET.get('color')
    BRAND_ID = request.GET.get('brand')
    ATOZ_ID = request.GET.get('AtoZ')
    ZTOA_ID = request.GET.get('ZtoA')

    PRICE_LOWTOHIGH_ID = request.GET.get('PRICE_LOWTOHIGH')
    PRICE_HIGHTOLOW_ID = request.GET.get('PRICE_HIGHTOLOW')

    SORT_BYNEW_ID = request.GET.get('SORT_BYNEW')
    SORT_BYOLD_ID = request.GET.get('SORT_BYOLD')

    if CAT_ID:
        product = Product.objects.filter(categories = CAT_ID,status = 'Publish' )
    # elif SIZE_ID:
    #     product = size.objects.filter(size = SIZE_ID,status = 'Publish' )
    elif PRICE_FILTER_ID:
        product = Product.objects.filter(filter_price = PRICE_FILTER_ID,status = 'Publish' )
    elif COLOR_ID:
        product = Product.objects.filter(color = COLOR_ID,status = 'Publish' )
    elif BRAND_ID:
        product = Product.objects.filter(brand = BRAND_ID,status = 'Publish' )
    elif ATOZ_ID:
        product = Product.objects.filter(status = 'Publish' ).order_by('name')
    elif ZTOA_ID:
        product = Product.objects.filter(status = 'Publish' ).order_by('-name')
    elif PRICE_LOWTOHIGH_ID:
        product = Product.objects.filter(status = 'Publish' ).order_by('price')
    elif PRICE_HIGHTOLOW_ID:
        product = Product.objects.filter(status = 'Publish' ).order_by('-price')
    elif SORT_BYNEW_ID:
        product = Product.objects.filter(status = 'Publish',condition='New' ).order_by('-id')
    elif SORT_BYOLD_ID:
        product = Product.objects.filter(status = 'Publish',condition='Old' ).order_by('-id')
    else:
        product = Product.objects.filter(status = 'Publish').order_by('-id')

    context = {
        'product':product,
        'categories':categories,
        'filter_price':filter_price,
        'color':color,
        'brand':brand,
    }
    
    return render(request,'Main/product.html',context)

def SEARCH(request):
    query = request.GET.get('query')
    product = Product.objects.filter(name__icontains=query)

    context = {'product':product}
    return render(request,'Main/search.html',context)

def PRODUCT_DETAIL_PAGE(request,id):
   # Main code:
    if request.method == 'POST':
        star = request.POST.get('star')
        message = request.POST.get('message')

        productt = Product.objects.filter(id = id).first()
        print(productt.name)

        xy = OrderItem.objects.filter(userDetail = request.user.email)
        # print(xy[1])
        OrderData = Order.objects.filter(email = request.user.email)

        for i in OrderData:
            print(i.firstname)

        print("xy initialized")
        count = 0;

        for i in xy:
            count = count + len([i])

        print("xy in for loop")

        if count >= 1 :
            print("if count >= 1")
            for x in range(count):
                print("check if the product is present")
                prod_review = Product_review.objects.filter(prod_id = id)
                reviewCount = 0
                for z in prod_review:
                    reviewCount = reviewCount + len([z])

                    if reviewCount > 0:
                        for y in prod_review:
                            if productt.unique_id[-1] == y.prod_id:
                                for OrDa in OrderData:
                                    if OrDa.firstname == y.name:
                                        reviewId = Product_review.objects.all()
                                        productt = Product.objects.filter(id = id).first()
                                        context = {
                                            'reviewId': reviewId,
                                            'productt':productt,
                                            'id': id,
                                        }
                                        print("1st if statement")
                                        messages.success(request, "please delete previous review to continue")
                                        return render(request,'Main/singleProduct.html', context)
                    else:
                        break
              
                if productt.name == xy[x].product:
                    review = Product_review(
                        prod_id = id,
                        name = request.user.username,
                        email = request.user.email,
                        rating = star,
                        reviewMessage = message,
                    )
                    print("save initiate")
                    review.save()
                    print("save completed")
                    reviewId = Product_review.objects.filter(prod_id = id)
                    print("reviewId")

                    context = {
                        'reviewId': reviewId,
                        'id': id,
                        'productt': productt,
                        'review': review,
                    }
                
                    print("1st if statement")
                    return render(request,'Main/singleProduct.html',context)
                
            print("product in not present ")
            if productt.name != xy[0].product:
                print("inside else")
                reviewId = Product_review.objects.all()
                productt = Product.objects.filter(id = id).first()
                context = {
                    'reviewId': reviewId,
                    'productt':productt,
                    'id': id,
                }
                messages.success(request, "#2 By the product first, for writing the review!")
                return render(request,'Main/singleProduct.html', context)

        if xy == []:
            review = Product_review(
                prod_id = id,
                name = request.user.username,
                email = request.user.email,
                rating = star,
                reviewMessage = message,
            )
            print("save initiate")
            review.save()
            print("save completed")
            reviewId = Product_review.objects.filter(prod_id = id)
            print("reviewId")

            context = {
                'reviewId': reviewId,
                'id': id,
                'productt': productt,
                'review': review,
            }
        
            print("2nd if statement")
            return render(request,'Main/singleProduct.html',context)  
        else:
            print("inside else")
            reviewId = Product_review.objects.all()
            productt = Product.objects.filter(id = id).first()
            context = {
                'reviewId': reviewId,
                'productt':productt,
                'id': id,
            }
            messages.success(request, "#1 By the product first, for writing the review!")
            return render(request,'Main/singleProduct.html', context)
        
    else:
        print("outside else")
        productt = Product.objects.filter(id = id).first()
        reviewId = Product_review.objects.all()

        context = {
            'reviewId': reviewId,
            'productt':productt,
            'id': id,
        }
        return render(request,'Main/singleProduct.html',context)

def Review_delete(request, id):
    print(request.user.email)
    productt = Product.objects.filter(id = id).first()
    reviewId = Product_review.objects.filter(email = request.user.email)
    print(reviewId)
    reviewId.delete()
    context = {
        'reviewId': reviewId,
        'productt':productt,
        'id': id,
    }
    return render(request,'Main/singleProduct.html',context)

def CONTACT(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        html_message = render_to_string("Main/contact_email.html", {'name': name, 'subject': message})
        plan_message = strip_tags(html_message)

        msg = EmailMultiAlternatives(
            subject + "query",
            plan_message,
            settings.EMAIL_HOST_USER,
            [email],
        )

        msg.attach_alternative(html_message, "text/html")

        try:
            msg.send() 
            messages.success(request, 'mail is sent successfully')
            return redirect('home')
        except:
            messages.success(request, " Something wrong! Please try again")
            return redirect('contact')

    return render(request,'Main/contact.html')

def ABOUT(request):
    # Main 
    return render(request,'Main/about.html')

def HandleRegister(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user_email = request.POST.get('user_email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        customer = User.objects.create_user(username, user_email, pass1)
        customer.first_name = first_name
        customer.last_name = last_name
        customer.save()
        return redirect('register')
    return render(request,'Registration/auth.html')

def HandleLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username= username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have login successfully")
            return redirect('home')
        else:
            return redirect('login')
        
    return render(request, 'Registration/auth.html')

def HandleLogout(request):
    logout(request)
    messages.success(request, "You have logout successfully")
    return redirect('home')

# Cart start 

@login_required(login_url="/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    messages.success(request, " Add to cart successfully")
    return redirect("home")


@login_required(login_url="/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    messages.success(request, "Item is deleted successfully")
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    messages.success(request, "All Item is deleted successfully")
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_detail(request):
    cart = request.session.get('cart')
    count = 0
    for i in cart:
        count = count + 1

    if count > 0 :
        for i in cart:
            Order.objects.filter(amount = cart[i]['price']).delete()
    
    # Main
    return render(request, 'Cart/cart_details.html')

@login_required(login_url="/login/")
def cart_detail_coupon(request):
    messages.success(request, "Coupon applied successfully")
    return render(request, 'Cart/cart_coupon.html')

@login_required(login_url="/login/")
def Check_out(request):
    cart = request.session.get('cart')
    count = 0
    for i in cart:
        count = count + 1

    if count > 0 :
        for i in cart:
            Order.objects.filter(amount = cart[i]['price']).delete()
    return render(request, 'Cart/checkout.html')

@login_required(login_url="/login/")
def checkout_coupon(request):
    cart = request.session.get('cart')
    count = 0
    for i in cart:
        count = count + 1

    if count > 0 :
        for i in cart:
            Order.objects.filter(amount = cart[i]['price']).delete()
    return render(request, 'Cart/checkout_coupon.html')


def checkout_session(request, id):
    if request.method == "POST":
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(id = uid)
        cart = request.session.get('cart')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        country = request.POST.get('country')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        if request.POST.get('amountWithTax'):
            amount = request.POST.get('amountWithTax') 
            # Tax = str(149)
        else:
            # Tax = str(0)
            amount = request.POST.get('amount')

        print(amount)
        for i in cart:
            print(i)
            order = Order(
                user = user,
                firstname = firstname,
                lastname = lastname,
                country = country,
                city = city,
                address = address,
                state = state,
                postcode = postcode,
                phone = phone,
                email = email,
                amount = cart[i]['price'],
            )

            item = OrderItem(
                order = order,
                userDetail = email,
                product = cart[i]['name'],
                image = cart[i]['image'],
                quantity = cart[i]['quantity'],
                price = cart[i]['price'],
                total = amount,
            )
            order.save()
            item.save()
    
            # plan = Product.objects.get(price=id)
        line_item = []
        TPrice = 0
        for y in cart:
            print(cart[y]['name'])
            line_item = line_item + [{
                'price_data': {
                    'currency': 'inr',
                    'unit_amount': int(cart[y]['price'])*100,
                    'product_data': {
                        'name': cart[y]['name'],
                    },
                },
                'quantity': cart[y]['quantity'],
            },
            ]
            TPrice = TPrice + int(cart[y]['price'])
        print(TPrice)

        session = stripe.checkout.Session.create(
            customer_email = email,
            payment_method_types=['card'],
            line_items=line_item,
            mode='payment',
            success_url='http://127.0.0.1:8000/cart/order-placed/' + amount,
            cancel_url='http://127.0.0.1:8000/cart/pay_cancel/',
        )

        try:
            print(amount)
        except:
            for y in cart:
                Order.objects.filter(amount=cart[y]['price']).delete()
            messages.success(request, " Something wrong! Please try again")
            return redirect('checkout')
        
        return redirect(session.url, code=303)

def pay_cancel(request):
    cart = request.session.get('cart')
    
    for y in cart:
        print("deleting")
        Order.objects.filter(amount=cart[y]['price']).delete()

    return render(request, 'cart/cancel.html')

def OrderPlaced(request, amount):
    cart = request.session.get('cart')

    First_name = request.user.username
    UserMail = request.user.email
    PName = ''
    quantity = 0
    count = 0

    for i in cart:
        count = count + 1
        if count > 1:
            PName = PName + ', ' + cart[i]['name']
            quantity = str(quantity) + ', ' + str(cart[i]['quantity'])
        else:
            PName = PName + cart[i]['name']
            quantity = quantity + cart[i]['quantity']
        

    html_message = render_to_string("Cart/email_template.html", {'name': First_name,
                                "ProductName": PName, "Quantity": quantity , "TotalPrice": amount})
    plan_message = strip_tags(html_message)

    msg = EmailMultiAlternatives(
        "Order Confirmed",
        plan_message,
        settings.EMAIL_HOST_USER,
        [UserMail],
    )

    msg.attach_alternative(html_message, "text/html")

    try:
        msg.send()
    except:
        for y in cart:
            print("Message deleting")
            Order.objects.filter(amount = cart[y]['price']).delete()
        messages.success(request, " Something wrong! Please try again")
        return redirect('checkout')
    
    cart_clear(request)
    return render(request, 'Cart/order_placed.html')

@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    
    if event['type'] == 'checkout.session.completed':
    # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
        session = stripe.checkout.Session.retrieve(
        event['data']['object']['id'],
        expand=['line_items'],
        )

        fulfill_order()
    else:
        cart = request.session.get('cart')
        count = 0
        for i in cart:
            count = count + 1

        if count > 0 :
            for i in cart:
                Order.objects.filter(amount = cart[i]['price']).delete()
    # Passed signature verification
    return HttpResponse(status=200)

def fulfill_order():
    print("Fulfilled order")

@login_required(login_url="/login/")
def MyOrders(request):
    cart = request.session.get('cart')
    count = 0
    for i in cart:
        count = count + 1

    if count > 0 :
        for i in cart:
            Order.objects.filter(amount = cart[i]['price']).delete()
    
    #  Main Code
    order = OrderItem.objects.filter(userDetail = request.user.email)
    return render(request, 'Cart/myOrders.html', locals())


def TrackOrder(request, pid):
    order = OrderItem.objects.filter(status = pid)
    orderCorr = OrderItem.objects.filter(userDetail = request.user.email)

    for i in orderCorr:
        if i.userDetail == request.user.email:
            print(i)
        strDate = i.created

    orderstatus = ORDERSTATUS
    expectedDelivery = strDate + datetime.timedelta(days=3)

    for y in order:
        if y.status == 5:
            print("reach it")
            y.created = datetime.datetime.today
            
    return render(request, 'Cart/order_tracking.html', locals())
