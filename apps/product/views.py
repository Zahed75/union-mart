import math
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.db import transaction
from django.core.mail import EmailMessage

from apps.users.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Product, UpdateNews, Slider, Trend, ProductPhoto, Cart, Review, PaymentPhoneNumber, OrderPayment
from .send_data_to_spread_sheet import send_to_spreadsheet


def home(request):
    slider_ins = Slider.objects.all().order_by('-id')
    product_ins = Product.objects.all().order_by('-upload_date')
    updated_news_ins = UpdateNews.objects.all().order_by('-id')
    trend_ins = Trend.objects.all().order_by('-id')
    women_ins = product_ins.filter(category='Women')[:3]
    men_ins = product_ins.filter(category='Men')[:3]
    bag_ins = product_ins.filter(sub_category='Bag')[:3]
    shoe_ins = product_ins.filter(sub_category='Shoe')[:3]
    watch_ins = product_ins.filter(sub_category='Watch')[:3]
    cart_count = Cart.objects.filter(user_id=request.user.id).count()

    context = {
        'products': product_ins,
        'sliders': slider_ins,
        'updated_news': updated_news_ins,
        'trends': trend_ins,
        'womens': women_ins,
        'mens': men_ins,
        'bags': bag_ins,
        'shoes': shoe_ins,
        'watches': watch_ins,
        'cart_count': cart_count if cart_count else 0,
    }
    return render(request, 'index.html', context)


def product(request):
    category = request.GET.get('category', None)
    sub_category = request.GET.get('sub_category', None)
    trend = request.GET.get('trend', None)
    search_product = request.POST.get('search_product', None)
    price_filter_first = request.GET.get('price', None)

    product_ins = Product.objects.all().order_by('-upload_date')

    if price_filter_first:
        price_filter = price_filter_first.split('-')
        if category and sub_category:
            product_ins = product_ins.filter(Q(category=category) & Q(sub_category=sub_category) & Q(price__gte=price_filter[0]) & Q(price__lte=price_filter[1]))
            context = {
                'products': product_ins,
                'category': category,
                'sub_category': sub_category,
                # 'price': price_filter_first,
            }
            return render(request, 'product.html', context)
        elif category:
            product_ins = product_ins.filter(Q(category=category) & Q(price__gte=price_filter[0]) & Q(price__lte=price_filter[1]))
            context = {
                'products': product_ins,
                'category': category,
                'sub_category': sub_category,
                # 'price': price_filter_first,

            }
            return render(request, 'product.html', context)

        elif trend:
            product_ins = product_ins.filter(Q(category=category) & Q(trend=trend))
            context = {
                'products': product_ins,
                'category': category,
                'sub_category': sub_category,
                # 'price': price_filter_first,

            }
            return render(request, 'product.html', context)

        else:
            product_ins = product_ins.filter(Q(sub_category=sub_category) & Q(price__gte=price_filter[0]) & Q(price__lte=price_filter[1]))
            context = {
                'products': product_ins,
                'category': category,
                'sub_category': sub_category,
                # 'price': price_filter_first,

            }
            return render(request, 'product.html', context)

    if search_product:
        strip_regex = search_product.strip()
        arr_regex = strip_regex.split(' ')
        str_regex = ''
        for element in arr_regex:
            str_regex += r'\b' + str(element) + r'\b|'
        str_regex = str_regex[:-1]
        if category and sub_category:
            product_ins = product_ins.filter(Q(category=category) & Q(sub_category=sub_category) & Q(description__iregex=r"" + str_regex + ""))
            context = {
                'products': product_ins,
                'category': category,
                'sub_category': sub_category,
                # 'price': price_filter_first,
            }
            return render(request, 'product.html', context)
        elif category:
            product_ins = product_ins.filter(Q(category=category) & Q(description__iregex=r"" + str_regex + ""))
            context = {
                'products': product_ins,
                'category': category,
                'sub_category': sub_category,
                # 'price': price_filter_first,

            }
            return render(request, 'product.html', context)
        else:
            product_ins = product_ins.filter(Q(sub_category=sub_category) & Q(description__iregex=r"" + str_regex + ""))
            context = {
                'products': product_ins,
                'category': category,
                'sub_category': sub_category,
                # 'price': price_filter_first,

            }
            return render(request, 'product.html', context)

    if category and sub_category:
        product_ins = product_ins.filter(Q(category=category) & Q(sub_category=sub_category))
    elif category:
        product_ins = product_ins.filter(category=category)
    elif sub_category:
        product_ins = product_ins.filter(sub_category=sub_category)

    else:
        product_ins = product_ins

    context = {
        'products': product_ins,
        'category': category,
        'sub_category': sub_category,
        # 'price': price_filter_first,

    }
    return render(request, 'product.html', context)


def product_details(request, product_id):
    product_ins = Product.objects.filter(id=product_id).first()
    reviews = Review.objects.filter(product_id=product_id).order_by('-id')
    product_photo_ins = ProductPhoto.objects.filter(product_id=product_id).order_by('-id')
    related_products = Product.objects.filter(category=product_ins.category, sub_category=product_ins.sub_category).exclude(id=product_ins.id).order_by('-upload_date')[:20]

    user_review = reviews.filter(user_id=request.user.id).first()
    # import pdb;
    # pdb.set_trace()
    quantity = request.GET.get('quantity_id')
    review = request.POST.get('review')
    if review:
        review_ins = Review(user_id=request.user.id, product_id=product_id, description=review.strip())
        review_ins.save()
        context = {
            'product_details': product_ins,
            'product_images': product_photo_ins,
            'related_products': related_products,
            'reviews': reviews,
            'user_review': user_review,
        }
        return render(request, 'product-detail.html', context)

    if quantity:
        check_card_ins = Cart.objects.filter(user_id=request.user.id, product_id=product_ins.id).exists()
        if not check_card_ins:
            card = Cart(user_id=request.user.id, product_id=product_ins.id, quantity=quantity)
            card.save()
            return JsonResponse({'valid': True, 'message': 'success.'})
        else:
            return JsonResponse({'valid': False, 'message': 'This product is already added.'})

    if product_ins:
        context = {
            'product_details': product_ins,
            'product_images': product_photo_ins,
            'related_products': related_products,
            'reviews': reviews,
            'user_review': user_review,
        }
        return render(request, 'product-detail.html', context)


@login_required
@transaction.atomic
def cart_list(request):
    user = User.objects.filter(id=request.user.id).first()
    delete_cart_id = request.GET.get('delete_cart_id')
    num_product1 = request.GET.get('num-product1')

    cart_ins = Cart.objects.filter(user_id=request.user.id).order_by('-quantity')
    product_arr = []
    total_price = 0
    if user.has_discount:
        for cart in cart_ins:
            temp = {}
            temp['product_id'] = cart.product.id
            temp['name'] = cart.product.name
            temp['price'] = cart.product.price
            temp['default_photo_url'] = cart.product.default_photo.url
            temp['quantity'] = cart.quantity
            temp['discount'] = user.discount
            if user.discount:
                per_discount_tk = cart.product.price * user.discount / 100
                # print('per_discount_tk ', per_discount_tk)
                total_discount = cart.quantity * per_discount_tk
                # print('total_discount ', total_discount)

                temp['per_total'] = (cart.product.price * cart.quantity) - math.floor(total_discount)
                # print(' total ', (cart.product.price * cart.quantity) - total_discount)

                total_price += (cart.product.price * cart.quantity) - math.floor(total_discount)
                # print('total_price 1111 ', total_price)

            else:
                temp['per_total'] = cart.product.price * cart.quantity
                total_price += cart.product.price * cart.quantity
                # print('total_price ', total_price)
            product_arr.append(temp)

        context = {
            'carts': product_arr,
            'total_price': total_price,
        }
        return render(request, 'shoping-cart.html', context)

    for cart in cart_ins:
        temp = {}
        temp['product_id'] = cart.product.id
        temp['name'] = cart.product.name
        temp['price'] = cart.product.price
        temp['default_photo_url'] = cart.product.default_photo.url
        temp['quantity'] = cart.quantity
        temp['discount'] = cart.product.discount
        if cart.product.discount:
            per_discount_tk = cart.product.price * cart.product.discount / 100
            # print('per_discount_tk ', per_discount_tk)
            total_discount = cart.quantity * per_discount_tk
            # print('total_discount ', total_discount)

            temp['per_total'] = (cart.product.price * cart.quantity) - math.floor(total_discount)
            # print(' total ', (cart.product.price * cart.quantity) - total_discount)

            total_price += (cart.product.price * cart.quantity) - math.floor(total_discount)
            # print('total_price 1111 ', total_price)

        else:
            temp['per_total'] = cart.product.price * cart.quantity
            total_price += cart.product.price * cart.quantity
            # print('total_price ', total_price)
        product_arr.append(temp)

    context = {
        'carts': product_arr,
        'total_price': total_price,
    }

    if delete_cart_id:
        cart_ins = cart_ins.filter(id=delete_cart_id).first()
        cart_ins.delete()

    if num_product1:
        product_ins = Product.objects.all().first()
        # send to spread sheet
        send_to_spreadsheet(product_ins)
    return render(request, 'shoping-cart.html', context)


@login_required
@transaction.atomic
def order_payment(request):
    payment_gateway = request.GET.get('payment_gateway')
    payment_number = request.POST.get('payment_number')
    contact_number = request.POST.get('contact_number')
    delivery_location = request.POST.get('delivery_location')
    city = request.POST.get('city')

    payment_pnumber_ins = PaymentPhoneNumber.objects.filter(payment_gateway=payment_gateway).first()
    if payment_pnumber_ins:
        context = {
            'payment_pnumber': payment_pnumber_ins
        }
        return render(request, 'payment.html', context)
    elif request.POST:
        order_payment = OrderPayment(payment_gateway=payment_gateway, payment_number=payment_number,
                                     delivery_location=delivery_location, contact_number=contact_number, city=city)
        order_payment.product_list = 'json product_list'
        order_payment.delivery_charge = 60 if city == 'Dhaka' else 'Depends on courier.'
        order_payment.total = request.user.id
        order_payment.save()
        messages.INFO(request, _('Successfully order done!'))

        # email = EmailMessage(mail_subject, message, to=[request.user.email])
        # email.send()
        return reverse('product:payment', kwargs={'payment_gateway': payment_gateway})
    else:
        return redirect('product:carts')
    
'''
    def send_confirmation_link(self, user):
        current_site = get_current_site(self.request)
        mail_subject = "Activate your codefolio account."
        message = render_to_string(
            self.activation_email_template,
            {
                "protocol": "https" if self.request.is_secure() else "http",
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.id)),
                "token": account_activation_token.make_token(user),
            },
        )
        to_email = user.email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()'''

@login_required
def invoice(request, id):
    return render(request, 'invoice.html', {})


def about(request, ):
    return render(request, 'about.html', {})


def contact(request):
    return render(request, 'contact.html', {})


def reward(request):
    return render(request, 'reward.html')


def privacy(request):
    return render(request, 'privacy.html', {})
