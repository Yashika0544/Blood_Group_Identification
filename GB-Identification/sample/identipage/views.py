from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import HttpResponseRedirect


# Create your views here.
def home(request):
    # request is use to navigate the command to our html page
    # use a render keywords function
    return render(request,'home.html')
def login_view(request):
    if(request.user.is_authenticated):
        return redirect('/')
    if(request.method=='POST'):
        un=request.POST['username']
        pw=request.POST['password']
        user = authenticate(request,username=un,password=pw)
        if(user is not None):
            # print('Login Successfull.')
            return redirect('/profile')
        else:
            # print('Error in login.')
            msg='error'
            form = AuthenticationForm()
            return render(request,'login.html',{'form': form,'msg': msg})
    else:
        form= AuthenticationForm()
        return render(request,'login.html',{'form': form})

def signup_view(request):
    if(request.user.is_authenticated):
        return redirect('/')
    if(request.method=='POST'):
        form = UserCreationForm(request.POST)
        if(form.is_valid()):
            form.save()
            un= form.cleaned_data.get('username')
            pw = form.cleaned_data.get('password1')
            authenticate(username=un, password=pw)
            return redirect('/login')
        else:
            return render(request, 'signup.html',{'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'signup.html',{'form': form})

def profile(request):
    return render(request,'profile.html')
