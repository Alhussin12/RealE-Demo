import imp
from django.shortcuts import render
from listpro.models import proeritie

def index(request):
    alls=proeritie.objects.all()
    return render(request ,'pages/index.html',{'alls':alls})
def about(request):
    return render(request ,'pages/about.html')
def sell(request):
    return render(request ,'pages/sell.html')
def terms(request):
    return render(request ,'pages/terms.html')
def search(request):
    return render(request ,'pages/search.html')
    
# def error_404(request,exception):
#     return render(request ,'pages/404.html')
