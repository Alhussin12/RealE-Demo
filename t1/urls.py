from . import views
from django.urls import path


urlpatterns = [
    path('',views.index,name='index'),
    path('about',views.about,name='about'),
    path('terms',views.terms,name='terms'),
    path('sell',views.sell,name='sell'),
    path('search',views.search,name='search')
]