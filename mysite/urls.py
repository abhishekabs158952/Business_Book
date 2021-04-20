from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path("@@",views.homeSeller,name="home1"),
    path('seller_signup',views.seller_signup, name='seller_signup'),
    path('customer_signup',views.customer_signup, name='customer_signup'),
    path('login',views.login1, name='login1'),
    path('addStock',views.add_Stock, name='addStock'),
    path('logout', views.logoutFBT, name='logout'),
    path('billBook', views.billBook, name='billBook'),
    path('QandA', views.QandA, name='QandA'),
    path('search', views.search, name='search'),
    path('myStock', views.myStock, name='myStock'),
    path('bill', views.bill, name='bill'),
    path('updateStock', views.updateStock, name='updateStock'),
    path('updateStockSubmit', views.updateStock, name='updateStock'),
    path('shopDetails', views.shopDetails, name='shopDetails'),
    path('itemDetails', views.itemDetails, name='itemDetails'),
    path('showDetails', views.showDetails, name='showDetails'),
    path('transectionValidity', views.transectionValidity, name='transectionValidity'),
    path('allTransection', views.allTransection, name='allTransection'),
    path('myOrder', views.myOrder, name='myOrder'),
    path('cart', views.cart, name='cart'),
    path('resetPassword', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('resetPasswordSent', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('resetPasswordComplete', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('chat', views.chat, name='chat'),
    path('myAccount', views.myAccount, name='myAccount'),
       
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)