import os
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from PIL import Image

from .models import Profile
from .forms import SignUpForm


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
            # welcome_post = '{0} has joined the network.'.format(user.username)
            # feed = Feed(user=user, post=welcome_post)
            #feed.save()
            return redirect('records:people_list')
        else:
            return render(request, 'authentication/signup.html', {'form': form })

    else:
        form = SignUpForm()
        return render(request, 'authentication/signup.html', {'form': form })


@login_required
def picture(request):
    uploaded_picture = False
    try:
        if request.GET.get('upload_picture') == 'uploaded':
            uploaded_picture = True
    except Exception:
        pass

    return render(request, 'authentication/picture.html',
                  {'uploaded_picture': uploaded_picture})


@login_required
def upload_picture(request):
    try:
        profile_pictures = settings.MEDIA_ROOT + '/user_profile/'
        if not os.path.exists(profile_pictures):
            os.makedirs(profile_pictures)
        f = request.FILES['picture']
        filename = profile_pictures + request.user.username + '_tmp.jpg'
        with open(filename, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        im = Image.open(filename)
        width, height = im.size
        if width > 350:
            new_width = 350
            new_height = (height * 350) / width
            new_size = new_width, new_height
            im.thumbnail(new_size, Image.ANTIALIAS)
            im.save(filename)

        return redirect('/authentication/picture/?upload_picture=uploaded')

    except Exception as e:
        print(e)
        return redirect('authentication:picture')


@login_required
def save_picture(request):
    try:
        x = int(request.POST.get('x'))
        y = int(request.POST.get('y'))
        # width = request.POST.get('width', 200)
        # height = request.POST.get('height', 200)
        tmp_filename = settings.MEDIA_ROOT + '/user_profile/' +\
            request.user.username + '_tmp.jpg'
        savefile = '/user_profile/' +\
            request.user.username + '.jpg'
        filename = settings.MEDIA_ROOT + savefile
            
        im = Image.open(tmp_filename)
        cropped_im = im.crop((x, y, x+200, y+200))
        cropped_im.thumbnail((200, 200), Image.ANTIALIAS)
        cropped_im.save(filename)
        os.remove(tmp_filename)
        profile, created = Profile.objects.update_or_create(
            user = request.user, image = savefile
        )

    except Exception:
        pass

    return redirect('authentication:picture')
