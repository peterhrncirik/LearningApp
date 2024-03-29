import re
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponse, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from accounts.models import StripeCustomer, CustomUser
from .forms import VideoLinkForm, ContactUsForm
from accounts.forms import LanguagesForm
from .video import check_video
from pprint import pprint
from pytube import YouTube
import stripe

# Stripe setup
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

LANGUAGES = (
    ('de', 'German'),
    ('en', 'English'),
    ('zh-HK', 'Chinese'),
    ('pt-PT', 'Portuguese'),
    #TODO: Add spanish
    # ('zh-HK', 'Chinese (Hong Kong)'),
    # ('zh-TW', 'Chinese (Taiwan)'),
    # ('en-GB', 'English (United Kingdom)'),
    ('fr-FR', 'French'),
    # ('fr-FR', 'French (France)'),
    # ('fr-CA', 'French (Canada)'),
    ('ja', 'Japanese'),
    # ('pt-BR', 'Portuguese (Brazil)'),
    # ('pt-PT', 'Portuguese (Portugal)'),
    ('ru', 'Russian'),
    ('it', 'Italian'),
)

def home(request):

    return render(request, 'pages/home.html')

def about(request):
    return render(request, 'pages/about.html')

def pricing(request):
    return render(request, 'pages/pricing.html')

def how(request):
    return render(request, 'pages/how.html')

def contact(request):
    
    form = ContactUsForm()
    
    if request.method == 'POST':
        
        form = ContactUsForm(request.POST)

        if form.is_valid():
            sender = form.cleaned_data['sender']
            msg = form.cleaned_data['message']
            
            send_mail('AnkifyVideo - Message From Contact Form', msg, sender, ['peto.hrncirik@gmail.com'])
            messages.success(request, 'Thanks for the message, we will get back to you :)')
        else:
            messages.warning(request, 'Please give us your E-Mail as well as message :)')
            return render(request, 'pages/contact.html', {'form': form})
            
    return render(request, 'pages/contact.html', {'form': form})

# Start Learning Page
@login_required
def start(request):
    
    # user_languages = [(short, long) for short, long in LANGUAGES if short in request.user.language]
    
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
                return HttpResponse('<p class="fw-bold text-white">This doesn\'t look like correct youtube URL.</p>')
            
        
      
            #TODO: check for subtitles and tell them if video is okay and we can continue
            # Check video
            video_is_correct = check_video(cd['link'], language=request.user.language)
            
            if not video_is_correct:
                return HttpResponse('<p class="fw-bold text-white">Looks like this video is not supported for this language :(</p>')
            
            # Load video and get info
            video_details = {
                'title': video.title,
                'thumbnail': video.thumbnail_url
            }
            
            return render(request, 'pages/partials/video.html', {'video_id': id, 'video': video_details, 'link': cd['link']})
        else:
            #FIXME: Bug, ak uz raz nastane tento response check_video() sa nespusta znova + text ostava na stranke a nerefreshuje sa
            return HttpResponse('<p class="fw-bold text-white">This doesn\'t look like a correct URL.</p>')

    return render(request, 'pages/start.html', {'form': form})

# User Account Details
@login_required
def user_detail(request, user_id):
    
    #TODO: Messages showing stacked up - update to show only the one that actually matter
    
    if request.method == 'POST':
        form = LanguagesForm(request.POST)
        user = CustomUser.objects.get(id=request.user.id)

        if form.is_valid():
            cd = form.cleaned_data['languages']
            user.language = cd
            user.save()
            messages.success(request, 'Language updated :)')
            return redirect(reverse('pages:user_detail', kwargs={ 'user_id': request.user.id }))
        else:
            messages.warning(request, 'Something went wrong.')
            return redirect(reverse('pages:user_detail', kwargs={ 'user_id': request.user.id }))
    
    subscription = None
    # Retrieve Stripe Customer Data
    try:
        stripe_customer = StripeCustomer.objects.get(user=request.user)
        subscription = stripe.Subscription.retrieve(stripe_customer.subscription_id)
    except:
        pass
    
    # Send to template
    context = {
        'subscription': subscription,
        'form': LanguagesForm(),
    }
    
    return render(request, 'account/details.html', context)

# User Files
@login_required
def user_files(request, user_id):
    
    return render(request, 'account/files.html',)

# Stripe Views
@login_required
def success(request):
     
    return render(request, 'pages/success.html')

@login_required
def cancel(request):
           
    return render(request, 'pages/cancel.html')

@login_required
def checkout(request, product_id):
    
    #FIXME: Bug when redirecting after login
    
    success_url = request.build_absolute_uri(reverse('pages:success'))
    #TODO: Hardcoded URL
    # success_url = 'http://127.0.0.1:8000/checkout/success?session_id={CHECKOUT_SESSION_ID}'
    cancel_url = request.build_absolute_uri(reverse('pages:cancel'))
    

    # redirect if user is already a member
    try:
        #TODO: AK je len member allow upgrade to unlimited
        if request.user.is_member:
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
            client_reference_id = request.user.id,
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


            