
import os
from django.conf import settings
from django.contrib import auth

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from PIL import Image

from .models import Profile
from .forms import SignUpForm, ProfileForm


def signup(request):
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, first_name=first_name, 
                            password=password, email=email)
            
            user = authenticate(username=username, password=password)
            login(request, user)
            
            Profile.objects.create(user=request.user)
            # welcome_post = '{0} has joined the network.'.format(user.username)
            # feed = Feed(user=user, post=welcome_post)
            #feed.save()
            return redirect('records:person_list')
        else:
            return render(request, 'authentication/signup.html', {'form': form })

    else:
        form = SignUpForm()
        return render(request, 'authentication/signup.html', {'form': form })


@login_required
def profile_detail(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
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
            return redirect('authentication:profile_detail')
    else:
        form = ProfileForm()
    return render(request, 'authentication/person_profile.html', {'form':form})


def logout(request):
    auth.logout(request)

    return redirect('login')

# @login_required
# def upload_picture(request):
#     try:
#         profile_pictures = settings.MEDIA_ROOT + '/user_profile/'
#         if not os.path.exists(profile_pictures):
#             os.makedirs(profile_pictures)
#         f = request.FILES['picture']
#         filename = profile_pictures + request.user.username + '_tmp.jpg'
#         with open(filename, 'wb+') as destination:
#             for chunk in f.chunks():
#                 destination.write(chunk)
#         im = Image.open(filename)
#         width, height = im.size
#         if width > 400:
#             new_width = 400
#             new_height = (height * 400) / width
#             new_size = new_width, new_height
#             im.thumbnail(new_size, Image.ANTIALIAS)
#             im.save(filename)

#         return redirect('/authentication/picture/?upload_picture=uploaded')

#     except Exception as e:
#         print(e)
#         return redirect('authentication:picture')


# @login_required
# def save_picture(request):
#     try:
#         x = int(request.POST.get('x'))
#         y = int(request.POST.get('y'))
#         width = int(request.POST.get('width', 200))
#         height = int(request.POST.get('height', 200))
#         tmp_filename = settings.MEDIA_ROOT + '/user_profile/' +\
#             request.user.username + '_tmp.jpg'
#         savefile = '/user_profile/' +\
#             request.user.username + '.jpg'
#         filename = settings.MEDIA_ROOT + savefile
            
#         im = Image.open(tmp_filename)
#         cropped_im = im.crop((x, y, x+width, y+height))
#         cropped_im.thumbnail((200, 200), Image.ANTIALIAS)
#         cropped_im.save(filename)
#         os.remove(tmp_filename)
#         profile, created = Profile.objects.update_or_create(
#             user = request.user, image = savefile
#         )

#     except Exception:
#         pass

#     return redirect('authentication:picture')
