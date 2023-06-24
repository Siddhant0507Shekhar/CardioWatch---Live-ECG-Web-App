from django.shortcuts import render

# Create your views here.

def home_view(request):
    messag = "Home aa gya"
    context = {"message":messag}
    return render(request,"home/home.html",context=context)