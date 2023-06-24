from django.shortcuts import render

# Create your views here.
def LiveEcg_page(request):
    return render(request,"LiveEcg/LiveEcg.html",{})