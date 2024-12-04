# Blood_Group_Identification


# Overview
The Blood Group Identification System is a Django-based web application that uses OpenCV for detecting blood groups through advanced image processing techniques. It streamlines blood group identification during emergencies and routine checkups, providing healthcare practitioners and patients with quick and informed decisions without long laboratory tests.


# Features
- User Management:
Secure sign-up and login functionalities with password protection.
User authentication ensures data security.

- Image Upload:
Users can upload images of ABD blood cells for analysis.

- Blood Group Detection:
Utilizes OpenCV for image preprocessing and contour analysis to identify the blood type.

- Output Display:
Displays the original uploaded image, processed image, and the predicted blood type.


# Technology Stack
# Frontend
- HTML/CSS: To create a responsive and user-friendly interface.
- Django Templates: For rendering dynamic content such as images and blood group results.
# Backend
- Django Framework: Handles user authentication, image uploads, and result generation.
- Python Libraries:
   - OpenCV: Image processing (grayscale conversion, thresholding, morphological operations).
   - NumPy: For numerical operations.
   - Base64: Encodes images for seamless display on web pages.


# Workflow
- Frontend Workflow:
User uploads an ABD blood cell image.
Image is sent to the Django backend via a POST request.
The system shows results, including the original and processed image, and the predicted blood type.

- Backend Workflow:
Accepts image via a POST request and preprocesses it using OpenCV.
Divides the image into regions (A, B, D) for analysis.
Detects agglutination patterns and classifies the blood type.
Sends results (images and blood type) back to the frontend.

- Output
Original Image: The uploaded ABD blood cell image.
Processed Image: Morphologically enhanced image with key features.
Predicted Blood Type: Final result based on the image analysis.


# Site Overview
-Home Page
![Screenshot 2024-11-08 151220](https://github.com/user-attachments/assets/e92b934b-fb06-4f59-a0c3-d6b96fb9f9fa)

-SignUp Page
![Screenshot 2024-11-08 144146](https://github.com/user-attachments/assets/36df3928-47f1-4e9a-ab40-4cccbc5e9ee4)

-LogIn Page
![Screenshot 2024-11-08 144219](https://github.com/user-attachments/assets/401b334e-2f38-4b8a-8190-f8d5015f3bd8)

-Profile Page
![Screenshot 2024-11-08 144247](https://github.com/user-attachments/assets/fe83aab4-56fd-4404-b749-9c6f8d8e1749)

-Final Output
![Screenshot 2024-11-25 134840](https://github.com/user-attachments/assets/310d4890-e524-4783-b6f0-cdf17f9742cf)


# PPT (For Referance)
[BlooD group identification.pdf](https://github.com/user-attachments/files/18005618/BlooD.group.identification.pdf)


# How to Run the Project
-Clone the repository:
 git clone <repository-url>

-Install dependencies:
 pip install -r requirements.txt

-Run the server:
 python manage.py runserver
 Access the application at http://127.0.0.1:8000.

# Conclusion
The system combines Django's secure backend with OpenCV's advanced image processing to provide accurate blood type predictions.
It offers a user-friendly experience for both personal and medical use.
Ensures data security and enhances accessibility to blood typing information.

# Acknowledgments
Special thanks to the team and mentors for their guidance and support throughout the project.
