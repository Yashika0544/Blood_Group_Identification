from django.shortcuts import render

# Create your views here.
def home(request):
    # request is use to navigate the command to our html page
    # use a render keywords function
    return render(request,'home.html')
def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')
