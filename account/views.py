from lzma import is_check_supported
from math import ceil
from django.core.files.storage import FileSystemStorage
from django.contrib import auth
from listpro.models import proeritie as pro
from .models import UserProfile as up
from django.contrib.auth.models import User
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages as mess
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
import re
from django.contrib.auth.hashers import check_password,make_password
from django.core.mail import send_mail
from django.conf import settings
# generate random integer values
from random import randint


def register(request):
    isadded=False
    if request.method == 'POST' and 'messok' in request.POST :
        if not request.POST['mess'].isdigit():
            mess.error(request,'must br a number')
        else:
            if len(request.POST['mess']) != 4:
                mess.error(request,'must be 4 number')
            else:          
                if up.objects.filter(code=int(request.POST['mess'])).exists():
                    up.objects.filter(code=int(request.POST['mess'])).update(isvarifaied=True)
                    up.objects.filter(code=int(request.POST['mess'])).update(code=0000)
                    mess.info(request,'varifaed sucsses login')
                    return redirect('login')
                else:
                    mess.error(request,'the code is wrong')
        isadded=True
        return render(request,'accounts/register.html',{'isadded':isadded})
    elif request.method == 'POST' and 'messsend' in request.POST:
        value =randint(1000,9999)

        
        subject = 'Thank you for registering to our site'
        message = f'''     <div>
                    <div style="background-color: #212529; color: green; text-align: center; font-size: xx-large;" >
                        <a style="color: green;" href="http://127.0.0.1:8000/">AQAR</a>
                    </div>
                        <div style="display: flex;
                            justify-items: center; justify-content: center;
                            align-items: center;  background-color: #76b852;
                            height: 400px; margin-left: 10px; margin-right: 10px;
                            border-radius: 10px;">
                            Thanke You for Trusting Us Your Code is :: {value}
                        </div>
                    <div style="background-color: #212529;">.</div>
                </div>'''
        email_from =  settings.EMAIL_HOST_USER
        recipient_list = ['hosenrast@gmail.com']
        send_mail( subject, message, email_from, recipient_list ,html_message=message,fail_silently=False)
        isadded=True
        return render(request,'accounts/register.html',{'isadded':isadded})    

    
    if request.method == 'POST':
        # variables for fileds
        
        fname=None
        lname=None
        address1=None
        address2=None
        city=None
        state=None
        zip_number=None
        email=None
        username=None
        password1=None
        password2=None
        terms=None
        stateoferror=[]
        isadded=False

        if 'fname' in request.POST:
            fname=request.POST['fname']
        else:
            mess.error(request,'error in first name')


        if 'lname' in request.POST:
            lname=request.POST['lname']
        else:
            mess.error(request,'error in last name')    

        if 'address1' in request.POST:
            address1=request.POST['address1']
        else:
            mess.error(request,'error in address1')

        if 'address2' in request.POST:
            address2=request.POST['address2']
        else:
            mess.error(request,'error in address2')

        if 'city' in request.POST:
            city=request.POST['city']
        else:
            mess.error(request,'error in city')                     
        if 'state' in request.POST:
            state=request.POST['state']
        else:
            mess.error(request,'error in state')

        if 'zip' in request.POST:
            zip_number=request.POST['zip']
        else:
            mess.error(request,'error in zip')  

        if 'email' in request.POST:
            email=request.POST['email']
        else:
            mess.error(request,'error in email') 
        if 'username' in request.POST:
            username=request.POST['username']
        else:
            mess.error(request,'error in username')        

        if 'password1' in request.POST:
            password1=request.POST['password1']
        else:
            mess.error(request,'error in passowrd')

        if 'password2' in request.POST:
            password2=request.POST['password2']   
        else:
            mess.error(request,'error in password') 

        if 'term' in request.POST:
            terms=request.POST['term']   

        #check the values
        if fname and lname and address1 and address2 and city and state and zip_number and email and username and password1 and password2:
            if ' ' in fname or ' ' in lname or ' ' in address1 or ' ' in address2 or ' ' in city or ' ' in state or ' ' in zip_number or ' ' in email or ' ' in username or ' ' in password1 or ' ' in password2:
                mess.error(request,'you have a space in your fileds')
            else:
                if terms == 'on':
                    #chick if username taken
                    if User.objects.filter(username=username).exists():
                        stateoferror.append('1')
                        mess.error(request,'this name are taken')
                    else:
                        #chick if email taken
                        if User.objects.filter(email=email).exists():
                            stateoferror.append('2')
                            mess.error(request,'this email are taken')
                        else:
                            #chick frrom of email 
                            pattrens="^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"  
                            if re.match(pattrens,email):
                                #passord check
                                special_characters = '"!@#$%^&*()-+?_=,<>/"'

                                if str(password1) != str(password2):
                                    mess.error(request,'password dosent match')
                                    stateoferror.append('3')    
                                elif len(password1)<=7 or len(password2)<=7:
                                    mess.error(request,'password less than 8 letter')
                                    stateoferror.append('3')    
                                elif  not any(c in special_characters for c in password1):
                                    mess.error(request,'password dosent have a special characters')
                                    stateoferror.append('3')    
                                else: 
                                    #add user
                                    user=User.objects.create_user(
                                        first_name=fname,
                                        last_name=lname,
                                        email=email,
                                        username=username
                                        ,password=password1
                                        )
                                    user.save()
                                    #add user profile
                                    userprofile=up(
                                        user=user,
                                        address=address1,
                                        address2=address2,
                                        city=city,
                                        state=state,
                                        zip_number=zip_number
                                        )
                                    userprofile.save()
                                    value =randint(1000,9999)
                                    up.objects.filter(user__username=username).update(code=value)
                                    subject = 'Thank you for registering to our site'
                                    message = f'''     <div>
                                                <div style="background-color: #212529; color: green; text-align: center; font-size: xx-large;" >
                                                    <a style="color: green;" href="http://127.0.0.1:8000/">AQAR</a>
                                                </div>
                                                    <div style="display: flex;
                                                        justify-items: center; justify-content: center;
                                                        align-items: center;  background-color: #76b852;
                                                        height: 400px; margin-left: 10px; margin-right: 10px;
                                                        border-radius: 10px;">
                                                        Thanke You for Trusting Us Your Code is :: {value}
                                                    </div>
                                                <div style="background-color: #212529;">.</div>
                                            </div>'''
                                    email_from =  settings.EMAIL_HOST_USER
                                    recipient_list = ['hosenrast@gmail.com']
                                    send_mail( subject, message, email_from, recipient_list ,html_message=message,fail_silently=False)
                                                            #empty filed
                                    fname=''
                                    lname=''
                                    address1=''
                                    address2=''
                                    city=''
                                    state=''
                                    zip_number=''
                                    email=''
                                    username=''
                                    password1=''
                                    password2=''
                                    terms='off'
                                    #succsec
                                    #mess.success(request,'account created you will redirict after 5s')
                                    mess.info(request,'we send a code to your mail Plz enter it her')
                                    isadded=True   
                            else:
                                mess.error(request,'error in email')

                else:      
                    mess.error(request,'you most ageir the terms')
        else:       
            mess.error(request,'there is null value')
        return render(request,'accounts/register.html',{
            'fname':fname,
            'lname':lname,
            'email':email,
            'username':username,
            'password1':password1,
            'password2':password2,
            'address1':address1,
            'address2':address2,
            'city':city,
            'state':state,
            'zip':zip_number,
            'stateoferror':stateoferror,
            'isadded':isadded,
        })

   
        # if not str(request.POST['email']).endswith('@gmail.com') :
        #      mess.error(request,'error in email')     
 
    else:        
        return render(request,'accounts/register.html')


def login_view(request):

    username=None
    password=None
    if request.method == 'POST':
    
        username=request.POST['useenames']
        password=request.POST['passwords']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            #for one login
            if 'rememberme' not in request.POST:
                request.session.set_expiry(0)
            auth.login(request,user)
            # mess.success(request,'you are logged in')
            return redirect('index')
        else:
            mess.error(request,'username or passowrd invalid')
            return redirect('login')
                
    else:
        return render(request,'accounts/login.html')
        

def logout_view(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('index')

#profile
def profile(request):
    isvarifaied=False    
    if request.method == 'POST' and 'messok' in request.POST :
        if up.objects.filter(user__username=request.user.username).exists():
            if not request.POST['mess'].isdigit():
                mess.error(request,'must br a number')
            else:
                if len(request.POST['mess']) != 4:
                    mess.error(request,'must be 4 number')
                else:
                    isvarifaied=True
                    up.objects.filter(user__username=request.user.username).update(isvarifaied=True)
                    up.objects.filter(code=int(request.POST['mess'])).update(code=0000)
                    return render(request,'accounts/profile.html',{'isvarifaied':isvarifaied})
        else:
            mess.error(request,'you dident send a code')
    elif request.method == 'POST' and 'messsend' in request.POST :
        test =up.objects.get(user=request.user)
        test.code=0
        if test.code == 0:        
            value =randint(1000,9999)
            up.objects.filter(user__username=request.user.username).update(code=value)
            subject = 'Thank you for registering to our site'
            message = f'''     <div>
                        <div style="background-color: #212529; color: green; text-align: center; font-size: xx-large;" >
                            <a style="color: green;" href="http://127.0.0.1:8000/">AQAR</a>
                        </div>
                            <div style="display: flex;
                                justify-items: center; justify-content: center;
                                align-items: center;  background-color: #76b852;
                                height: 400px; margin-left: 10px; margin-right: 10px;
                                border-radius: 10px;">
                                Thanke You for Trusting Us Your Code is :: {value}
                            </div>
                        <div style="background-color: #212529;">.</div>
                    </div>'''
            email_from =  settings.EMAIL_HOST_USER
            recipient_list = ['hosenrast@gmail.com']
            send_mail( subject, message, email_from, recipient_list ,html_message=message,fail_silently=False)
            mess.info(request,f'the code send to {test.user.email} ')
        else:
            mess.error(request,'you alreay sent an code')    




    dif = up.objects.filter(user__username=request.user.username)[0]
    if dif.isvarifaied:
        isvarifaied=True
        return render(request,'accounts/profile.html',{'isvarifaied':isvarifaied})
    else:       
        return render(request,'accounts/profile.html')    

def proerities(request):

        #for Delete
        if request.method =='POST' and 'deletePro' in request.POST:
            pro.objects.filter(id=int(request.POST['deletePro'])).delete()

        #FOR PROIORTY COUNT 
        all=pro.objects.all()
        users=request.user.username
        countP=int(pro.objects.filter(rel__username=users).count())
        #FOR PAGINATION 
        alls=pro.objects.filter(rel__username=users)
        if request.method =='POST':
            alls=pro.objects.filter(rel__username=users)
            if  'se' in request.POST:
                    alls=pro.objects.filter(type='Sell',rel__username=users)    
            if 're' in request.POST:
                    alls=pro.objects.filter(type='Rent',rel__username=users)
        paginator=Paginator(alls,8)
        page=request.GET.get('page')
        try:
            alls=paginator.page(page)
        except PageNotAnInteger:
            alls=paginator.page(1)
        except EmptyPage:
            alls=paginator.page(paginator.num_page)

        isvarifaied=False    
        dif = up.objects.get(user=request.user)
        if dif.isvarifaied:
            isvarifaied=True
        return render(request,'accounts/profilePart/proerities.html',
        {'all':all,
        'countP':countP,
        'paginator':paginator,
        'alls':alls,
        'page':page,
        'isvarifaied':isvarifaied,
        })

def edit(request):
    fname=None
    lname=None
    address1=None
    address2=None
    city=None
    state=None
    zip_number=None
    email=None
    username=None
    passw=None
    fileurl=None
    if request.user and not request.user.is_superuser :
            #if not authecnated
            if request.user.is_anonymous: return  render(request,'accounts/profilePart/edit.html')
            #if authecnated
            #does click on change photo button
            if request.method=='POST' and 'uploadbtn' in request.POST:
                #is there file in request
                request_file = request.FILES['document'] if 'document' in request.FILES else None
                if request_file:
                    fs = FileSystemStorage()
                    file = fs.save(request_file.name, request_file)
                    fileurl = fs.url(file) 
                    if str(fileurl).endswith(('jpg', 'jpeg', 'png')):
                        up.objects.filter(user=request.user).update(userphoto=request_file)
                        mess.info(request,'you update the photo')
                    else:
                        mess.error(request,'that file is not photo use(jpg,jpeg,png)')
                else:
                    mess.error(request,'you dosent enter an image')
            #Delete Account
            elif request.method=='POST' and 'deleteAccount' in request.POST:
                if request.user.is_authenticated:
                    User.objects.filter(username=request.user).delete()
                    up.objects.filter(user=request.user).delete()
                    auth.logout(request)
                    return redirect('index')
            elif request.method=='POST' and 'SaveProfile' in request.POST:
                fname=None
                lname=None
                address1=None
                address2=None
                city=None
                state=None
                zip_number=None
                if 'fname' in request.POST:fname=request.POST['fname']
                else:mess.error(request,'error in first name')
                if 'lname' in request.POST:lname=request.POST['lname']
                else:mess.error(request,'error in last name')    
                if 'address1' in request.POST:address1=request.POST['address1']
                else:mess.error(request,'error in address1')
                if 'address2' in request.POST:address2=request.POST['address2']
                else:mess.error(request,'error in address2')
                if 'city' in request.POST:city=request.POST['city']
                else:mess.error(request,'error in city')                     
                if 'state' in request.POST:state=request.POST['state']
                else:mess.error(request,'error in state')
                if 'zip' in request.POST:zip_number=request.POST['zip']
                else:mess.error(request,'error in zip')
                # check all request is OK
                if  fname and lname and address1  and city and zip_number and state:
                    if ' ' in fname or ' ' in lname or ' ' in address1  or ' ' in city or ' ' in state or ' ' in zip_number  :
                        mess.error(request,'you have a space in your fileds')
                    else:
                         User.objects.filter(username=request.user).update(
                         first_name=fname,
                         last_name=lname)
                         up.objects.filter(user=request.user).update(
                            address=address1,
                            address2=address2,
                            city=city,
                            state=state,
                            zip_number=zip_number
                         )
                         mess.info(request,'your update your profile')
                else:
                    mess.error(request,'you have an empty filed or you play with elements')
                    return redirect('edit')
            elif request.method=='POST' and 'change' in request.POST:
                if 'pass1' in request.POST and 'pass2' in request.POST and 'oldpass' in request.POST:
                    if ' ' in  request.POST['pass2'] or ' ' in  request.POST['pass1'] or ' ' in  request.POST['oldpass']:
                        mess.error(request,'there is a space or empty value')
                    else:    
                        thisUser=up.objects.get(user=request.user)
                        if check_password(request.POST['oldpass'],thisUser.user.password):
                            if request.POST['pass1'] == request.POST['pass1']:
                                if len(request.POST['pass1'])<=7 or len(request.POST['pass2'])<=7:
                                    mess.error(request,'the miniume is 8 letters')
                                else:
                                    special_characters = '"!@#$%^&*()-+?_=,<>/"'
                                    if not any(c in special_characters for c in request.POST['pass1']):
                                        mess.error(request,'password dosent have a special characters')
                                    else:
                                        if request.POST['pass1'] == request.POST['oldpass']:
                                            mess.error(request,'you cant enter the same password')
                                        else:   
                                            User.objects.filter(username=request.user).update(password=make_password(request.POST['pass1']))
                                            mess.info(request,'password changed')
                                            return redirect('login')

                            else:
                                mess.error(request,'password dosent match')    
                        else:
                            mess.error(request,'invalied password')
                else:
                    mess.error(request,'you play with elements')           
                 #pbkdf2_sha256$
            isvarifaied=False    
            dif = up.objects.get(user__username=request.user.username)
            if dif.isvarifaied:
                isvarifaied=True
            thisUser=up.objects.get(user=request.user)
            fname=thisUser.user.first_name
            lname=thisUser.user.last_name
            email=thisUser.user.email
            username=thisUser.user.username
            address1=thisUser.address
            address2=thisUser.address2
            userphoto=thisUser.userphoto
            city=thisUser.city
            state=thisUser.state
            zip_number=thisUser.zip_number
            context={
                'fname':fname,
                'lname':lname,
                'email':email,
                'username':username,
                'address1':address1,
                'address2':address2,
                'userphoto':userphoto,
                'city':city,
                'state':state,
                'zip':zip_number,
                'fileurl':fileurl,
                'isvarifaied':isvarifaied
                            }
            return render(request,'accounts/profilePart/edit.html',context)
#if there an admin            
    else:
        isvarifaied=False    
        dif = up.objects.get(user__username=request.user.username)
        if dif.isvarifaied:
            isvarifaied=True
        return render(request,'accounts/profilePart/edit.html',{'isvarifaied':isvarifaied})
        
   
def sellProfile(request):
            type=None
            title=None
            floor=None
            date=None
            bed=None
            bath=None
            price=None
            lat=None
            lng=None
            if 'type' in request.POST:type=request.POST['type']
            else:mess.error(request,'Error in Type')
            if 'title' in request.POST:title=request.POST['title']
            else:mess.error(request,'error in title')    
            if 'floor' in request.POST:floor=request.POST['floor']
            else:mess.error(request,'error in floor')
            if 'date' in request.POST:date=request.POST['date']
            else:mess.error(request,'error in date')
            if 'bed' in request.POST:bed=request.POST['bed']
            else:mess.error(request,'error in bed')                     
            if 'bath' in request.POST:bath=request.POST['bath']
            else:mess.error(request,'error in bath')
            if 'price' in request.POST:price=request.POST['price']
            else:mess.error(request,'error in price')
            # if 'photo' in request.POST:photo=request.POST['photo']
            # else:mess.error(request,'error in photo')
            if 'lat' in request.POST:lat=request.POST['lat']
            else:mess.error(request,'error in lat')
            if 'lng' in request.POST:lng=request.POST['lng']
            else:mess.error(request,'error in lng')
            isvarifaied=False    
            dif = up.objects.get(user=request.user)
            if dif.isvarifaied:
                isvarifaied=True
            return render(request,'accounts/profilePart/sell.html',{'isvarifaied':isvarifaied})
def proeritiesPages(request,pro_id):
        hi=pro.objects.filter(id=pro_id)
        for i in hi:
         his=i.rel.id
        ho=up.objects.get(user=his)
        if request.method =='POST':
            subject = 'Thank you for registering to our site'
            for i in hi:
                title=i.title
                id=i.id
            name=request.POST['name']
            mail=request.POST['email']
            messs= request.POST['mess']   
            message = f'''     <div>
                        <div style="background-color: #212529; color: green; text-align: center; font-size: xx-large;" >
                            <a style="color: green;" href="http://127.0.0.1:8000/">AQAR</a>
                        </div>
                            <div style="display: flex;
                                justify-items: center; justify-content: center;
                                align-items: center;  background-color: #76b852;
                                height: 400px; margin-left: 10px; margin-right: 10px;
                                border-radius: 10px;">
                                <p>
                                 houseTitle :: {title}
                                <br>
                                houseId :: {id}
                                <br>
                                from :: {name}
                                <br>
                                email :: {mail}
                                <br>
                                mess::{messs}
                                </p>
                            </div>
                        <div style="background-color: #212529;">.</div>
                    </div>'''
            email_from =  settings.EMAIL_HOST_USER
            recipient_list = ['hosenrast@gmail.com']
            send_mail( subject, message, email_from, recipient_list ,html_message=message,fail_silently=False)
            mess.info(request,'the meesage send to Sucssec')
        isvarifaied=False    
        dif = up.objects.get(user=request.user)
        if dif.isvarifaied:
            isvarifaied=True
        return render(request,'accounts/profilePart/proPag.html',{
            'isvarifaied':isvarifaied,
            'pro':get_object_or_404(pro,pk=pro_id),
            'ho':ho
            })
def proeritiesMap(request):
        proUser=pro.objects.filter(rel=request.user)
        proUserCount=pro.objects.filter(rel=request.user).count()
        isvarifaied=False    
        dif = up.objects.get(user=request.user)
        if dif.isvarifaied:
            isvarifaied=True
        return render(request,'accounts/profilePart/proMap.html',{
            'isvarifaied':isvarifaied,'proUser':proUser,'proUserCount':proUserCount})
       
def  proeritiesReq(request):
        if request.method == 'POST':
            if 'add' in request.POST:
                pro.objects.filter(id=request.POST['add']).update(is_check=True)
            if 'del' in request.POST:
                pro.objects.filter(id=request.POST['del']).delete()
        check=pro.objects.filter(is_check=False)
        isvarifaied=False    
        dif = up.objects.get(user=request.user)
        if dif.isvarifaied:
            isvarifaied=True
        return render(request,'accounts/profilePart/proeritiesReq.html',{'isvarifaied':isvarifaied,'check':check})  
