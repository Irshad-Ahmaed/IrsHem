from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HOME,name='home'),
    path('base/', views.BASE,name ='base'),
    path('products/', views.PRODUCT,name ='products'),
    path('products/<str:id>', views.PRODUCT_DETAIL_PAGE,name ='product_detail'),
    path('products/message_delete/<str:id>', views.Review_delete,name ='Review_delete'),

    path('search/', views.SEARCH,name ='search'),
    path('contact/', views.CONTACT,name ='contact'),
    path('about/', views.ABOUT,name ='about'),


    path('register/', views.HandleRegister,name ='register'),
    path('login/', views.HandleLogin,name ='login'),
    path('logout/', views.HandleLogout,name ='logout'),

    # Cart paths
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
    path('cart/cart-detail-coupon/',views.cart_detail_coupon,name='cart_coupon'),

    path('cart/checkout/',views.Check_out,name='checkout'),
    path('cart/checkout-coupon/',views.checkout_coupon,name='checkout_coupon'),


     #     Stripe URL:
     path('checkout_session/<int:id>', views.checkout_session, name='checkout_session'),
     path('cart/order-placed/<int:amount>',views.OrderPlaced,name='order_placed'),
     path('cart/pay_cancel/',views.pay_cancel,name='pay_cancel'),
     path('webhook/stripe',views.my_webhook_view,name='webhook-stripe'),

     #    Order Page:
     path('cart/my_orders/',views.MyOrders,name='my_orders'),
     path('cart/track-order/<int:pid>',views.TrackOrder,name='track_order'),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
