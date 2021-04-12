from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .models import EmailConfirmed, products, Order, Categories, contact_us
from django.shortcuts import get_object_or_404
import random
from django.db.models import Q
import stripe
from django.conf import settings
from django.urls import reverse
from django.views.generic import ListView, DetailView, View
# Create your views here.


import stripe
stripe.api_key = "sk_test_51IWuSRFzvY3Oon8KHXlURApAt4rjhN1qKfh37Xvcwam0uzfvzZt8o3TJCirb5uFParGlho3a15S6V2s0mZLXsaOg00woMU6Fen"



def index(request):
    all_products = products.objects.all()
    all_Categories = Categories.objects.all()
    context1 = {'all_products':all_products, 'all_Categories':all_Categories}
    return render(request, 'index.html', context1)


def product_search(request):
    search_product  = request.GET.get('search')
    print(search_product)

    if search_product:
        search_result = products.objects.filter(Q(product_name__icontains = search_product) | Q(description__icontains = search_product)).order_by('-id')

        search_result_count = products.objects.filter(Q(product_name__icontains = search_product) | Q(description__icontains = search_product)).count()


        context5 = {'search_product':search_product, 'search_result' :search_result, 'search_result_count':search_result_count}
        return render(request, 'product.html', context5)



def blog(request):
    return render(request, 'blog.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method=="POST":
        email=request.POST.get('email')
        msg=request.POST.get('msg')
        print(email, msg)

        contactus = contact_us(email=email, message=msg)
        contactus.save()
        messages.success(request, 'Message Has been sent to admin !!')
        return redirect('index')


    return render(request, 'contact.html')

def profile(request):
    return render(request, 'profile.html')

def my_orders(request):
    user = request.user
    get_all_order = Order.objects.filter(user=user)
    context = {'get_all_order':get_all_order}
    return render(request, 'my_order.html', context)

def signup_login(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email_sign = request.POST.get('email_sign')
        password_sign = request.POST.get('password_sign')
        password_sign_re = request.POST.get('password_sign_re')


        # chech the error inputs
        user_email_info = User.objects.filter(email=email_sign)

        erorr_message = ""

        if user_email_info:
            # messages.error(request, "Email Already Exist")
            erorr_message = "Email Already Exist"

        elif password_sign != password_sign_re:
            # messages.error(request, "Passwords are not match")
            erorr_message = "Passwords are not match !!"

        elif len(password_sign) < 7:
            # messages.error(request, "Passwords Must be Al least 7 Digits")
            erorr_message = "Passwords Must be Al least 7 Digits !!"

        if not erorr_message:

            # create user
            myuser = User.objects.create_user(email_sign, email_sign, password_sign)
            myuser.first_name = first_name
            myuser.last_name = last_name
            myuser.is_active = False
            myuser.save()

            # send mail
            user = EmailConfirmed.objects.get(user=myuser)
            site = get_current_site(request)
            email = myuser.email
            first_name = myuser.first_name
            last_name = myuser.last_name

            sub_of_email = "Activation Email From Medicify."
            email_body = render_to_string(
                'verify_email.html',
                {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'domain': site.domain,
                    'activation_key': user.activation_key
                }
            )

            send_mail(
                sub_of_email,  # Subject of message
                email_body,  # Message
                '',  # From Email
                [email],  # To Email

                fail_silently=True
            )

            messages.success(request, 'Check Your Email for Activate Your Account !!!')

            return redirect('/')

        else:

            value_dic = {'first_name': first_name, 'last_name': last_name, 'email_sign': email_sign,
                         'erorr_message': erorr_message}
            return render(request, 'signup_func.html', value_dic)
    return render(request, 'signup_func.html')



def email_confirm(request, activation_key):
    user= get_object_or_404(EmailConfirmed, activation_key=activation_key)
    if user is not None:
        user.email_confirmed=True
        user.save()

        myuser=User.objects.get(email=user)
        myuser.is_active=True
        myuser.save()
        first_name=myuser.first_name
        last_name=myuser.last_name

        condict = {'first_name': first_name, 'last_name':last_name}
        return render(request, 'registration_complete.html', condict)


def login_func(request):
    if request.method == 'POST':
        log_username = request.POST['log_username']
        log_password = request.POST['log_password']
        # this is for authenticate username and password for login
        user = authenticate(username=log_username, password=log_password)

        erorr_message_2 = ""

        if user is not None:
            login(request, user)
            # messages.success(request, "Successfully Logged In !!")
            return redirect('index')
        else:
            erorr_message_2 ="Invalid Credentials, Please Try Again !!"

            value_func2 = {'erorr_message_2':erorr_message_2, 'log_username':log_username}
            # messages.error(request, "Invalid Credentials, Please Try Again !!")
            return render(request, 'signup_func.html', value_func2)


def logout_func(request):
    # this is for logout from user id
    logout(request)
    return redirect('index')

def product_detail(request, pk):
    get_product = products.objects.get(id=pk)
    # products category
    cat_pro = get_product.category
    # get all product by category
    all_pro_cat = products.objects.filter(category=cat_pro)

    context2 = {'get_product':get_product, 'all_pro_cat':all_pro_cat}
    return render(request, 'product-detail.html', context2)

def cart(request):
    # stripe.api_key = settings.STRIPE_PRIVET_KEY
    #
    # session = stripe.checkout.Session.create(
    #     payment_method_types=['card'],
    #     line_items=[{
    #         'price': 'price_1IWudUFzvY3Oon8K1C66bAva',
    #         'quantity': 1,
    #     }],
    #     mode='payment',
    #     success_url=request.build_absolute_uri(reverse('checkout')) + '?session_id={CHECKOUT_SESSION_ID}',
    #     cancel_url=request.build_absolute_uri(reverse('cart')),
    # )
    return render(request, 'shoping-cart.html')#, {'session_id':session.id, 'stripe_public_key':settings.STRIPE_PUBLIC_KEY})


def checkout(request):
    if request.method =="POST":
        prod_details = request.POST.get('prod_details')
        checkout_money = request.POST.get('checkout_money')
        print('total')
        print(checkout_money, prod_details)

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        country = request.POST.get('country')
        street = request.POST.get('street')
        city = request.POST.get('city')
        zip = request.POST.get('zip')
        # print(full_address, city, postal_code, country, phone)

        # make random order ID
        random_num = random.randint(2345678909800, 9923456789000)

        uniqe_confirm = Order.objects.filter(order_id=random_num)
        # print(random_num)

        while uniqe_confirm:
            random_num = random.randint(234567890980000, 992345678900000)
            if not Order.objects.filter(order_id=random_num):
                break
        # print(random_num)

        user = request.user

        post_order = Order(user=user, order_id=random_num, product_details=prod_details, total_bill=checkout_money,
                           first_name=first_name, last_name=last_name, email=email, phone=phone,
                           country=country, street=street, city=city, zip=zip)
        post_order.save()
        order_id = post_order.order_id
        # print(order_id)

        Thank = True

        return render(request, 'checkout.html', {'Thank': Thank, 'order_id': order_id})

    else:
        user=request.user
        order = Order.objects.filter(user=user, ordered=False)
        if order:
            messages.info(request, 'You Have a Order Remain to Payment !! To Order New, You Have to Pay The first One.')
            return redirect('payment')
        else:
            return render(request, 'checkout.html')
        # return render(request, 'checkout.html')

class PaymentView(View):
    def get(self, *args, **kwargs):
        user = self.request.user
        order = Order.objects.get(user=user, ordered=False)

        context = {
            'order': order,
            "DISPLAY_COUPON_FORM": False

        }
        return render(self.request, 'payment.html', context)

    def post(self, *args, **kwargs):
        print(self.request.user)

        user=self.request.user
        order = Order.objects.get(user=user, ordered=False)

        try:
            customer = stripe.Customer.create(
                email=self.request.user.email,
                description=self.request.user.username,
                source=self.request.POST['stripeToken']
            )
            amount = int(order.total_bill)
            charge = stripe.Charge.create(
                amount=(amount * 100),
                currency="usd",
                customer=customer,
                description="Payment for Fabmom online",
            )

            order.ordered = True

            order.save()

            order_id=order.order_id

            email_for_buy = render_to_string(
                'email_for_buy.html',
                {
                    'order_id': order_id,
                    'first_name': self.request.user.first_name,
                    'last_name': self.request.user.last_name,
                    'prod_details': order.product_details,
                    'total_bill': order.total_bill,
                    'street': order.street,
                    'city': order.city,
                    'postal_code': order.zip,
                    'country': order.country,
                    'phone': order.phone,
                    'email': order.email,
                }
            )
            email=order.email
            send_mail(
                'Purchase Order',  # subject
                email_for_buy,  # massage
                '',  # from email
                [email],  # to email

                fail_silently=True,
            )



            print('okkk')
            messages.success(self.request, 'Payment was Successfull !!')

        except stripe.error.CardError as e:
            messages.info(self.request, f"{e.error.message}")
            return redirect('index')

        except stripe.error.RateLimitError as e:
            messages.info(self.request, f"{e.error.message}")
            return redirect('index')
        except stripe.error.InvalidRequestError as e:
            messages.info(self.request, "Invalid Request !")
            return redirect('index')
        except stripe.error.AuthenticationError as e:
            messages.info(self.request, "Authentication Error !!")
            return redirect('index')
        except stripe.error.APIConnectionError as e:
            messages.info(self.request, "Check Your Connection !")
            return redirect('index')
        except stripe.error.StripeError as e:
            messages.info(self.request, "There was an error please try again !")
            return redirect('index')
        except Exception as e:
            messages.info(self.request, "A serious error occured we were notified !")
            return redirect('index')

        return redirect('index')
