# Industry Oriented Project- EED IITR
### Group Participants:-
1. Ritesh Gupta
2. Siddhant Shekhar
3. Saurabh Mangla
4. Shivam Kr. Singhwal

# Cardiowatch - Live ECG Web Application
Cardiowatch is a web application designed for monitoring and analyzing live ECG (Electrocardiogram) data. It provides real-time visualization of a patient's heart activity and performs classification of ECG signals into different categories using a trained CNN model. The application utilizes sensor data from the patient to generate insights and provide a user-friendly interface for healthcare professionals.

![Screenshot (12)](https://github.com/Siddhant0507Shekhar/CardioWatch---Live-ECG-Web-App/assets/122518146/cbac12f2-a17b-4728-918e-488d2c10f2ca)

## Features
### Live ECG Monitoring:
The web application receives 20-second duration ECG data from the sensors and processes it in real-time.
### ECG Segmentation:
The backend segments the 20-second ECG data into individual heartbeats for further analysis.
### ECG Classification:
Each heartbeat is fed into a trained CNN model that classifies ECG signals into five classes, including one normal and four abnormal categories. The model has been trained using the MIT BIH database.
### Color Encoding:
The classification results are visually represented by embedding red and green colors of various intensities into the 20-second ECG data figure.
### Image Generation: 
The backend generates an image of the ECG data with embedded color coding, which can be accessed by the frontend API.
### User Authentication: 
The "authoriz" app handles user registration, login, and logout functionalities.
### Home Page: 
The "home" app renders the home page of the web application.
### LiveEcg Page:
The "LiveEcg" app renders the Live ECG web page, displaying real-time ECG data.
### Project APIs:
The "project" app includes several views functions such as "get_health_status," "get_ecg_image," and "get_live_data" to provide necessary data to the frontend API.
### User Report Page:
The "user-report" app renders the user report page, displaying the classification results and other relevant information.

![Screenshot (13)](https://github.com/Siddhant0507Shekhar/CardioWatch---Live-ECG-Web-App/assets/122518146/caefe952-6dca-4e44-b4f5-72e1a58b7422)

![Screenshot (15)](https://github.com/Siddhant0507Shekhar/CardioWatch---Live-ECG-Web-App/assets/122518146/190dc85a-829f-45ff-8368-953ba1eb5497)

## Setup Instructions
1. Clone the repository to your local machine.
2. Install the required dependencies using pip install -r requirements.txt.
3. Set up the necessary configurations in the Django settings file.
4. Migrate the database using python manage.py migrate.
5. Run the development server using python manage.py runserver.
6. 
## Usage
1. Access the web application through your preferred web browser.
2. Register as a user or log in if you already have an account.
3. Navigate to the Live ECG page to start monitoring the real-time ECG data.
4. View the classification results and the color-coded ECG image in the user report page.
5. Explore other features and functionalities provided by the application.


Note: This README file provides an overview of the Cardiowatch web application and its functionality. For more detailed documentation and instructions, please refer to the appropriate files and comments within the project codebase.