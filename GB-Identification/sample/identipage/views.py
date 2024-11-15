from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import HttpResponseRedirect
# from django.core.files.storage import default_storage
# from django.core.files.base import ContentFile
import base64
from django.core.files.uploadedfile import InMemoryUploadedFile
import cv2
import numpy as np


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
    abd_image_url = None
    contour_count= 0
    if(request.method=='POST'):
        abd_image= request.FILES.get('abd_image')
        if abd_image:

            # media file storgage method --> it store the output each and every time which take a alloate of memory space.
            # abo_image_name = default_storage.save('blood_cell.jpg', ContentFile(abo_image.read()))
            # abo_image_url = default_storage.url(abo_image_name)
            # return render(request, "profile.html", {
            #     'abo_image_url': abo_image_url
            # })

        
            image_data = abd_image.read()
            #contour logic
            img_array = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contour_count = len(contours)
            # Base64 encoding for image
            _, buffer = cv2.imencode('.jpg', img)
            encoded_image = base64.b64encode(image_data).decode('utf-8')
            abd_image_url = f"data:image/jpg;base64,{encoded_image}"
        else:
            return render(request, "profile.html", {
                'error_message': "Please upload ABD blood cell images."
            })
    # return render(request,'profile.html',{'abd_image_url': abd_image_url})
    return render(request,'profile.html',{'abd_image_url': abd_image_url,'contour_count': contour_count})
