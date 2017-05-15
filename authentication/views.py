from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms import SignUpForm


def signup(request):
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = email
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, password=password,
                                     email=email)
            user = authenticate(username=username, password=password)
            login(request, user)
            # welcome_post = '{0} has joined the network.'.format(user.username)
            # feed = Feed(user=user, post=welcome_post)
            #feed.save()
            return redirect('records:people_list')

    else:
        form = SignUpForm()
        return render(request, 'authentication/signup.html', {'form': form })
