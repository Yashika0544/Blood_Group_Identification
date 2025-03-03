from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import HttpResponseRedirect
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
    # contour_count= 0
    morphologic_image_url = None
    blood_type = None
    if(request.method=='POST'):
        abd_image= request.FILES.get('abd_image')
        if abd_image:

            image_data = abd_image.read()
            img_array = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            #contour logic
            # img_array = np.frombuffer(image_data, np.uint8)
            # img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            # contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # contour_count = len(contours)
            
            # Step 1: Convert to grayscale
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Step 2: Apply Gaussian blur to reduce noise
            blur_img = cv2.GaussianBlur(gray_img, (5, 5), 0)

            # Step 3: Enhance the contrast of the image
            enhance_img = cv2.equalizeHist(blur_img)

            # Step 4: Apply Otsu's thresholding
            _, bin_img = cv2.threshold(enhance_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # Step 5: Perform morphological operations
            kernel_imp = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            bin_img = cv2.morphologyEx(bin_img, cv2.MORPH_OPEN, kernel_imp)  # Remove small noise
            bin_img = cv2.morphologyEx(bin_img, cv2.MORPH_CLOSE, kernel_imp)  # Fill small holes

             # Encode the morphologically processed image to base64
            _, morphologic_buffer = cv2.imencode('.jpg', bin_img)
            morphologic_encoded = base64.b64encode(morphologic_buffer).decode('utf-8')
            morphologic_image_url = f"data:image/jpg;base64,{morphologic_encoded}"

            # Base64 encoding for image
            _, buffer = cv2.imencode('.jpg', img)
            encoded_image = base64.b64encode(image_data).decode('utf-8')
            abd_image_url = f"data:image/jpg;base64,{encoded_image}"

            # Calculate blood type
            hei, wid = bin_img.shape
            mid_wid = wid // 3

            region_A = bin_img[:, 0:mid_wid]
            region_B = bin_img[:, mid_wid:2 * mid_wid]
            region_D = bin_img[:, 2 * mid_wid:]

            # Define agglutination calculation
            def cal_agg(region):
                num_labels, labels, stats, var = cv2.connectedComponentsWithStats(region, connectivity=8)
                return num_labels - 1

            # Calculate connected components in each region
            num_region_A = cal_agg(region_A)
            num_region_B = cal_agg(region_B)
            num_region_D = cal_agg(region_D)
            
            agglutination_threshold = 3
        
            # Determine positive reactions
            a_positive = num_region_A >= agglutination_threshold 
            b_positive = num_region_B >= agglutination_threshold 
            rh_positive = num_region_D >= agglutination_threshold 

            # Determine the blood type based on agglutination
            if a_positive and b_positive:
                blood_type = "AB+"
            elif a_positive:
                blood_type = "A+"
            elif b_positive:
                blood_type = "B+"
            elif not a_positive and not b_positive and rh_positive:
                blood_type = "O+"
            elif a_positive and not b_positive and not rh_positive:
                blood_type = "A-"
            elif not a_positive and b_positive and not rh_positive:
                blood_type = "B-"
            elif a_positive and b_positive and not rh_positive:
                blood_type = "AB-"
            elif not a_positive and not b_positive and not rh_positive:
                blood_type = "O-"
            else:
                blood_type = "Unknown"
        else:
            return render(request, "profile.html", {
                'error_message': "Please upload ABD blood cell images."
            })
    return render(request,'profile.html',{'abd_image_url': abd_image_url, 'morphologic_image_url': morphologic_image_url, 'blood_type': blood_type})
