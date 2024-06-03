import math
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.shortcuts import render
from .models import proerities
from .models import proeritie
# Create your views here.

def list(request):
    b=proeritie.objects.all()
    title=None
    mip=None
    map=None
    floor=None
    bd=None
    br=None
    countSearch=None
    if request.method == 'GET':
        if 'bd' in request.GET:
            bd=request.GET['bd']
            if bd:
                if bd.isdigit():   
                    b=b.filter(bedrooms=bd)
                    countSearch=b.filter(bedrooms=bd).count()
        if 'br' in request.GET:
            br=request.GET['br']
            if br:
                if br.isdigit():   
                    b=b.filter(bathrooms=br)
                    countSearch=b.filter(bathrooms=br).count()
        if 'title' in request.GET:
            title=request.GET['title']
            if title:
                b=b.filter(title__icontains=title)#للبحث في كل الاحرف
                countSearch=b.filter(title__icontains=title).count()
        if 'mip' in request.GET and 'map' in request.GET:
                mip=request.GET['mip']
                map=request.GET['map'] 
                if not mip :
                    mip=0
                if not map :
                    map=math.inf    
                b=b.filter(price__gte=mip,price__lte=map)
                countSearch=b.filter(price__gte=mip,price__lte=map).count()
        if 'floor' in request.GET:
            floor=request.GET['floor']
            if floor:
                if floor.isdigit():   
                    b=b.filter(floors=floor)
                    countSearch=b.filter(floors=floor).count()
        
    paginator=Paginator(b,9)
    page=request.GET.get('page')
    try:
        b=paginator.page(page)
    except PageNotAnInteger:
        b=paginator.page(1)
    except EmptyPage:
        b=paginator.page(paginator.num_page)
    c=proeritie.objects.all().count()
    return render(request,'list/list.html',{'countSearch':countSearch,'b':b,'c':c,'paginator':paginator})
