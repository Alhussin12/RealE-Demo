from . import views
from django.urls import URLPattern, path

urlpatterns=[
    path('profile',views.profile,name='profile'),
    path('profile/edit',views.edit,name='edit'),
    path('profile/proerities',views.proerities,name='proerities'),
    path('profile/proerities/<int:pro_id>',views.proeritiesPages,name='proeritiesPages'),
    path('profile/proerities/proeritiesMap',views.proeritiesMap,name='proeritiesMap'),
    path('profile/proerities/proeritiesReq',views.proeritiesReq,name='proeritiesReq'),
    path('profile/sell',views.sellProfile,name='sellProfile'),
    path('login',views.login_view,name='login'),
    path('logout',views.logout_view,name='logout'),
    path('register',views.register,name='register'),
    ]

