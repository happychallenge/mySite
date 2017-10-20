import os
from django.conf import settings
from django.contrib import auth

from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.core.checks import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.db.models import Count
from PIL import Image

from mySite.records.models import Person, Tag
from .models import Profile
from .forms import SignUpForm, ProfileForm, ChangePasswordForm
from .tokens import account_activation_token

def signup(request):
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            # email = form.cleaned_data.get('email')
            # username = form.cleaned_data.get('username')
            # first_name = form.cleaned_data.get('first_name')
            # password = form.cleaned_data.get('password')
            # User.objects.create_user(username=username, first_name=first_name, 
            #                 password=password, email=email)

            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            message = render_to_string('authentication/active_email.html', {
                    'user':user, 'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })

            mail_subject = 'Activate your account of "IRememberYourPast.com".'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(request, 'authentication/send_email_for_confirmation.html', {'email': to_email })

        else:
            return render(request, 'authentication/signup.html', {'form': form })

    else:
        form = SignUpForm()
        return render(request, 'authentication/signup.html', {'form': form })

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # Profile.objects.create(user=request.user)

        return redirect('authentication:profile_edit')
    else:
        return 

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # profile = form.save(commit=False)
            # profile.user = request.user
            x = form.cleaned_data.get('x')
            y = form.cleaned_data.get('y')
            width = form.cleaned_data.get('width')
            height = form.cleaned_data.get('height')
            picture = form.cleaned_data.get('picture')

            image = Image.open(picture)
            cropped_image = image.crop((x, y, width+x, height+y))
            resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
            savefile = '/user_profile/' + request.user.username + '-' + picture.name
            filename = settings.MEDIA_ROOT + savefile
            resized_image.save( filename )

            if Profile.objects.filter(user=request.user).count():
                Profile.objects.filter(user=request.user).update(picture=savefile)
            else:
                Profile.objects.create(user=request.user, picture=savefile)
            return redirect('authentication:profile_edit')
    else:
        user = request.user
        form = ProfileForm()

        person_list = Person.objects.annotate(
            num_following=Count('following')).filter(status='P', 
            created_user=user).order_by('-num_following')

        popular_tags = Tag.get_person_popular_tags()
        following = Person.get_persons_following()[:10]
        context = {'person_list': person_list, 'popular_tags': popular_tags, 
                    'following': following, 'form':form}
    return render(request, 'authentication/person_profile.html', context)


def logout(request):
    auth.logout(request)

    return redirect('login')


############################
# Email Check
############################
def checkemail(request):
    data = {}
    email = request.GET.get('email')
    if email:
        email = User.objects.filter(email = email).exists()
        if email:
            data["exists"] = True
        
    return JsonResponse(data, safe=False)

############################
# Change Password
############################
@login_required
def password(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            messages.add_message(request, messages.SUCCESS,
                                 'Your password was successfully changed.')
            return redirect('authentication:profile_edit')

    else:
        form = ChangePasswordForm(instance=user)

    return render(request, 'authentication/password.html', {'form': form})
