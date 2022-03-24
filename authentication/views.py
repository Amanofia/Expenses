from django.shortcuts import redirect, render
from django.views.generic import View
from expenses.models import User
from django.contrib import auth, messages
from .utils import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls.base import reverse


def signup(request):
    if request.method == 'POST':

        email = request.POST['email']
        password = request.POST['password']
        username = request.POST['username']
        context = {
            "fieldvalue": request.POST
        }
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(username=username, email=email, password=password)
                user.is_active = False
                user.save()

                current_site = get_current_site(request)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = account_activation_token.make_token(user)
                link = reverse('auth:activate', kwargs={'uid': uid, 'token': token})
                acti_url = "http://" + current_site.domain + link

                user.save()
                messages.success(request, "Account Created Successfully")
                return redirect(acti_url)
            messages.error(request, "User Account Already exists!")
            return render(request, 'auth/signup.html', context)
        messages.error(request, "Username Already Exists!")
        return render(request, 'auth/signup.html', context)
    return render(request, 'auth/signup.html')


class activate(View):
    def get(self, request, uid, token):
        try:
            id = force_text(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=id)
            if not account_activation_token.check_token(user, token):
                return redirect('auth:login')
            if user.is_active:
                return redirect('auth:login')
            user.is_active = True
            user.save()
            messages.success(request, "Account Activated")
            return redirect('auth:login')
        except Exception as e:
            return redirect('auth:login')


class Login(View):
    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username != None and password != None:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, "Welcome " + username + ", You have been Authenticated successfully!")
                    return redirect('expenses:expenses')
                else:
                    messages.error(request, "Account is not active!")
                    return render(request, 'auth/login.html')
            messages.error(request, "Invalid credentials!")
            return redirect('auth:login')
        messages.error(request, "Invalid Fields!")
        return redirect('auth:login')


class Logout(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, "You have been logged out")
        return redirect('auth:login')


