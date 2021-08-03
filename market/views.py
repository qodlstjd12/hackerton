from django.shortcuts import render

# Create your views here.

def market_view(request):
    return render(request, 'market.html')

def market_Detail(request):
    return render(request, 'marketDetail.html')

def market_Write(request):
    return render(request, 'marketWrite.html') 