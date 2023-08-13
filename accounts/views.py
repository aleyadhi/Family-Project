from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Create your views here.

def login_view(request):
    next_url = request.GET.get('next')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            context = {
                'error': 'Invalid username or password.',
                'auth_screen': True,
                'kind' : 'L'
            }
            return render(request, 'accounts/login.html', context)
        login(request, user)
        if not next_url == None:
            if not next_url.startswith('/'):
                next_url = '/' + next_url
            return redirect(next_url)
        return redirect('/')
    context = {
        'auth_screen': True,
        'kind' : 'L'
    }
    return render(request, 'accounts/login.html', context)

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/')
    return render(request, 'accounts/logout.html', {})

    
def register_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user_obj = form.save()
        return redirect('/accounts/login')
    context = {
        'form': form,
        'auth_screen': True,
        'kind' : 'R'
    }
    return render(request, 'accounts/register.html', context)