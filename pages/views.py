import re
import time
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponse, reverse
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from accounts.models import StripeCustomer, CustomUser
from .forms import VideoLinkForm
from .video import check_video
from pprint import pprint
from pytube import YouTube
import stripe

# Stripe setup
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

def home(request):

    return render(request, 'pages/home.html')

@login_required
def start(request):
    
    form = VideoLinkForm()
    
    if request.method == 'POST':
        
        form = VideoLinkForm(request.POST)
        video_details = {}

        if form.is_valid():
            
            cd = form.cleaned_data
            
            #FIXME: AJAX zacne aj na empty keyUp - fix
            
            # Check if url is correct by searching for ID in the link
            try:
                match = re.search(r"/watch\?v=([^&]*)", cd['link'])
            except:
                return HttpResponse('<p>This doesn\'t look like correct youtube URL.</p>')

            # URL is okay, assign video ID
            id = match.group(1)
            
            try:
                # What if ID is wrong though?
                video = YouTube(cd['link'])
            except:
                return HttpResponse('<p>This doesn\'t look like correct youtube URL.</p>')
            
        
      
            #TODO: check for subtitles and tell them if video is okay and we can continue
            # Check video
            video_is_correct = check_video(cd['link'])
            
            if not video_is_correct:
                return HttpResponse('<p>Looks like this video is not supported :(</p>')
            
            # Load video and get info
            video_details = {
                'title': video.title,
                'thumbnail': video.thumbnail_url
            }
            
            return render(request, 'pages/partials/video.html', {'video_id': id, 'video': video_details, 'link': cd['link']})
        else:
            #FIXME: Bug, ak uz raz nastane tento response check_video() sa nespusta znova + text ostava na stranke a nerefreshuje sa
            return HttpResponse('<p>This doesn\'t look like a correct URL.</p>')

    return render(request, 'pages/start.html', {'form': form})

@login_required
def order_create(request):
    pass

def success(request):
    
    if request.method == 'GET' and 'session_id' in request.GET:
        session = stripe.checkout.Session.retrieve(request.GET['session_id'])
        print(session['metadata']['product_type'])
        customer = StripeCustomer()
        customer.user = request.user
        customer.stripe_id = session.customer
        customer.is_active = True
        customer.subscription_id = session.subscription
        # Update also User object
        current_user = CustomUser.objects.get(id=request.user.id)
        current_user.is_member = True
        if session['metadata']['product_type'] == '2':
            current_user.is_unlimited = True
        current_user.save()
        customer.save()
        
        return render(request, 'pages/success.html', {'session': session})

    

def cancel(request):
    return render(request, 'pages/cancel.html')

@login_required
def checkout(request, product_id):
    
    # success_url = request.build_absolute_uri(reverse('pages:success'))
    #TODO: Hardcoded URL
    success_url = 'http://127.0.0.1:8000/checkout/success?session_id={CHECKOUT_SESSION_ID}'
    cancel_url = request.build_absolute_uri(reverse('pages:cancel'))
    

    # redirect if user is already a member
    try:
        #TODO: AK je len member allow upgrade to unlimited
        current_user = StripeCustomer.objects.get(user=request.user)
        if current_user.is_active:
            return redirect('pages:start')
    except StripeCustomer.DoesNotExist:
        pass
    
    if request.method == 'POST':
        
        if product_id == 1:
            price_id = 'price_1MUTDRI7DEQKabRTAWZvrPKQ'
        elif product_id == 2:
            price_id = 'price_1MUTJWI7DEQKabRT6Ko81jS5'
            
        # Stripe checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_email = request.user.email,
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            metadata={
                'product_type': 1 if product_id == 1 else 2,
            },
            mode='subscription',
            success_url=success_url,
            cancel_url=cancel_url,
        )
        
        # redirect to Stripe payment form
        return redirect(session.url, code=303)


def about(request):
    return render(request, 'pages/about.html')

def pricing(request):
    return render(request, 'pages/pricing.html')