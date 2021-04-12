
from django.urls import path
from . import views

from .views import PaymentView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('product_search', views.product_search, name='product_search'),
    path('blog', views.blog, name='blog'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('profile', views.profile, name='profile'),
    path('my_orders', views.my_orders, name='my_orders'),
    path('login-signup', views.signup_login, name='signup_login'),
    path('login', views.login_func, name='login_func'),
    path('logout_func', views.logout_func, name='logout_func'),
    path('product_detail/<int:pk>', views.product_detail, name='product_detail'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),

    # activation email
    path('email/confirmation/<str:activation_key>/', views.email_confirm, name='email_activation'  ),


    path('payment', PaymentView.as_view(), name='payment'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
