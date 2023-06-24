import matplotlib
import time
from dateutil.parser import parse
from django.shortcuts import render
from django.utils.dateparse import parse_date,parse_datetime
from django.core.files import File
from keras.models import load_model
# Create your views here.
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse
from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.decorators import login_required
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import biosppy
import matplotlib
from django.utils.timezone import make_aware
import json
import os
import matplotlib.patches as patches
import threading
from datetime import time
from .models import Health_Status
import random
from .models import Ecg_data
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings


def window_average(arr):
    arr = list(arr)
    brr = arr[:4]
    for i in range(4,len(arr)-4):
        window = np.array(arr[i-1:i+2])
        brr.append(int(window.mean()))
    brr+=arr[len(arr)-4:]
    return np.array(brr)

def segmentation(arr,r_peaks):
    diff = [r_peaks[0]]+ [r_peaks[i]-r_peaks[i-1] for i in range(1,len(r_peaks))]
    diff.sort()
    median = diff[len(diff)//2]//2
    output_arr = []
    for i in range(1,len(r_peaks)-1):
        output_arr.append(arr[r_peaks[i]-median:r_peaks[i]+median+1])
    return output_arr


class My_ML_model:
    def __init__(self):
        self.my_model = load_model("D:/model_0.h5")

    def predict_test(self,test_data):# test_data will be in input format of trained data just like [ (150X224) 2-D array]
        result = self.my_model.predict(test_data)
        result = list(result[0])
        ans = [result[0],max(result[1:])]
        return ans

model_class = My_ML_model()
matplotlib.use('agg')

def model_predict(ecg_seg):
    fig = plt.figure(figsize=(3,5), dpi=170)
    plt.plot(ecg_seg)
    plt.axis('off')
    image_seg_name = f"./ecg_image{ecg_seg[0]}.png"
    # folder = "/content/drive/My Drive/Colab Notebooks/cnn_ecg_image/"
    plt.savefig(image_seg_name)
    plt.clf()
    plt.close(fig)
    img = Image.open(image_seg_name).convert('L')
    img = img.resize((224,150))
    img_arr = np.asarray(img) / 255.0
    img_arr = img_arr.reshape(1,150, 224, 1)
    ans = model_class.predict_test(img_arr)
    os.remove(image_seg_name)
    return ans


def saving_data(np_arr,r_peaks,user_name,location):
    ecg_segments = segmentation(np_arr, r_peaks)
    print('ecg_seg_len',len(ecg_segments))
    healthy = []  # 1 as healthy and 0 as unhealthy
    color = []

    for i in range(len(ecg_segments)):
        res = model_predict(ecg_segments[i])
        if res[0] >= res[1]:
            healthy.append(1)
        else:
            healthy.append(0)
        res[0] = round(res[0], 2)
        res[1] = round(res[1], 2)
        color.append(res)
        # print(res)

    print(color)
    # Number of desired data points after downsampling
    desired_num_points = 600
    original_time = np.arange(len(np_arr))
    desired_time = np.linspace(original_time[0], original_time[-1], desired_num_points)
    downsampled_data = np.interp(desired_time, original_time, np_arr)
    fig, ax = plt.subplots(figsize=(20, 6))
    l = len(np_arr)
    hgt = max(np_arr) - min(np_arr) + 50
    x1 = (r_peaks[0]+r_peaks[1])//2
    ax.add_patch(patches.Rectangle((0, min(np_arr)-20), width=desired_num_points * (x1/l), height=hgt,
                                   color=(abs(1-min(healthy)),max(healthy), 0), alpha=0.3))
    for i in range(1, len(r_peaks) - 1):
        x1 = (r_peaks[i-1]+r_peaks[i])//2
        x2 = (r_peaks[i]+r_peaks[i+1])//2
        ax.add_patch(patches.Rectangle(  ((x1/l)*desired_num_points, min(np_arr)-20),
                                       width=((x2-x1) / l)*desired_num_points, height=hgt,
                                       color=(color[i - 1][1], color[i - 1][0], 0), alpha=0.3+((i%2)/20)))
    ax.add_patch(
        patches.Rectangle(  (desired_num_points*(((r_peaks[-2] + r_peaks[-1])/ 2)/l) , min(np_arr)-20)  ,
                          width=desired_num_points*((l-((r_peaks[-1] + r_peaks[-2]) / 2))/ l),  height=hgt,
                          color=(abs(1-min(healthy)), max(healthy), 0), alpha=0.3))
    plt.plot(downsampled_data)
    image_name = f"./Img_db/ecg_image{np_arr[0]}.png"
    plt.savefig(image_name)
    plt.clf()
    plt.close(fig)
    specific_user = User.objects.get(username=user_name)
    if specific_user:
        ecg_data_instance = Ecg_data()
        ecg_data_instance.user_name = specific_user
        ecg_data_instance.date_time = timezone.now()
        ecg_data_instance.ecg_image.save(((image_name)),File(open((image_name),'rb')))
        ecg_data_instance.latitude = location[0]
        ecg_data_instance.longitude = location[1]
        ecg_data_instance.altitude = location[2]
        ecg_data_instance.ecg_arr = str(downsampled_data)
        ecg_data_instance.heart_beat = len(r_peaks)*3
        ecg_data_instance.save()
        health_status_instance = Health_Status()
        health_status_instance.health = min(healthy)
        health_status_instance.user_name = specific_user
        health_status_instance.date = timezone.now().date()
        health_status_instance.timer = timezone.now().time()
        health_status_instance.save()

def asynchronous_fun(np_arr,user_name,location):
    r_peaks = biosppy.signals.ecg.christov_segmenter(signal=np_arr, sampling_rate=200.0)[0]
    saving_data(np_arr, r_peaks, user_name,location)



@csrf_exempt
def receive_array(request):
    if request.method == 'POST':
        # Receive the array from the request
        data = json.loads(request.body)
        user_name = data.get('username')
        location = data.get('location')
        print('location',location)
        print(type(location))
        location = location.split(",")
        print(location)
        if len(location)!=3:
            location = ["29.86","77.90","264.20"]
        # user_name = "shekh"
        received_array = data.get('ecg_array')
        p = received_array.split(",")
        # print(p)
        for i in range(len(p)):
            p[i] = int(p[i])
        received_array = p[:]
        print(len(received_array),"length of received array")
        for i in range(len(received_array)):
            received_array[i] = int(received_array[i])
        np_arr = np.array(received_array)
        np_arr = window_average(np_arr)
        result = threading.Thread(target=asynchronous_fun,args=[np_arr,user_name,location])
        result.start()
        # Change sampling rate according to the sampling rate of physical device(arduino)
        # task = asyncio.create_task(aynchronous_fun(np_arr,user_name))
        # Return a JSON response indicating successful receipt of the array
        response_data = {'message': "OK"}

        return JsonResponse(response_data,status=200)
    else:
        # Return an error response for other HTTP methods
        response_data = {'status': 'error', 'message': '''Invalid request'''}
        return JsonResponse(response_data, status=400)




def del_img_name(img_name):
    time.sleep(4)
    os.remove(img_name)

def get_health_status(request,date):
    if request.method == 'GET':
        # date = "17/04/2023"
        print(date)
        # Check if user is authenticated
        # if request.user.is_authenticated and (date is not None):
        if request.user.is_authenticated and (date is not None):
            username = request.user.username
            # date_string = parse_date(date)
            # username = "shekh"
            # date_string = "17/04/2023"
            date_object = parse_date(date)
            health_status_list = Health_Status.objects.filter(user_name__username=username, date=date_object)
            arr = [2 for i in range(1440)]
            for obj in health_status_list:
                hlt = obj.health
                my_time = str(obj.timer)
                # formatted_time = time.strftime(my_time)
                formatted_time = my_time
                hr = int(formatted_time[:2])
                mn = int(formatted_time[3:5])
                total = (60*hr)+mn
                arr[total] = min(arr[total],hlt)
            brr = []
            for i in range(0,len(arr),5):
                brr.append(min(arr[i:i+5]))
            colors = {0: 'red', 1: 'green', 2: 'white'}
            length_to_breadth_ratio = 5 / 15
            width = 10
            height = width * length_to_breadth_ratio
            fig, ax = plt.subplots(figsize=(width, height))
            img_name = f"./media/health/health_status_img{random.randint(1,100)}.png"
            for i, val in enumerate(brr):
                ax.bar(i, 1, color=colors[val], width=1)
            ax.set_yticks([])
            ax.set_yticklabels([])
            ax.set_xlabel('Time from 0 to 288 (5 X 12 X 24) 5-min segment in a day')
            plt.savefig(img_name)
            plt.clf()
            plt.close(fig)
                       # Uncomment this later
            # result = threading.Thread(target=del_img_name, args=[img_name])
            # result.start()
            return JsonResponse({'new_url': img_name},status=200)
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)



def is_valid_date(date_str):
    try:
        parse(date_str)
        return True
    except ValueError:
        return False

def is_valid_time(time_str):
    try:
        parse(time_str)
        return True
    except ValueError:
        return False




def get_ecg_image(request,date,time=''):
    if request.method=="GET":
        if request.user.is_authenticated and is_valid_date(date) and is_valid_time(time):
            username = request.user.username
            datetime_obj1 = parse_datetime(date+" "+time)
            datetime_obj1 = make_aware(datetime_obj1)
            ecg_image_recent = Ecg_data.objects.filter(user_name__username=username, date_time__lte=datetime_obj1).order_by('-date_time').first()
            response = {}
            response["ecg_image"] ="/media/"+ecg_image_recent.ecg_image.name
            response["datetime"] = ecg_image_recent.date_time
            response["heart_beat"] = ecg_image_recent.heart_beat
            return JsonResponse(response,status=200)
        else:
            return JsonResponse({"error":"Invalid User/date/time"},status=401)
    else:
        return JsonResponse({"error":"Wrong http method"},status=405)


def get_live_data(request):
    if request.method=="GET":
        if request.user.is_authenticated:
            username = request.user.username
            # username = "shekh"
            date_now = timezone.now()
            ecg_image_now = Ecg_data.objects.filter(user_name__username=username,date_time__lte=date_now).order_by('-date_time').first()
            response = {}
            response["live_arr"] = ecg_image_now.ecg_arr
            return JsonResponse(response,status=200)
        else:
            return JsonResponse({'error':"Not Authenticated"},status=401)
    else:
        return JsonResponse({"error":"Invalid method"},status=405)



