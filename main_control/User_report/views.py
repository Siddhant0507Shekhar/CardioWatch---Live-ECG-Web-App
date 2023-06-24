from django.shortcuts import render

# Create your views here.

def report_page(request):
    return render(request,"User_report/User_report.html", {})
