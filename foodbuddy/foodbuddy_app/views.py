import datetime

from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
import sqlite3
from .models import *
from .forms import ModifyForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
# Create your views here.
# https://www.geeksforgeeks.org/handling-ajax-request-in-django/
from django.template.defaultfilters import register
from django.contrib import messages
from django.core.mail import send_mail

from django.conf import settings

@register.filter(name='get_UID')
def get_UID(id):
    '''
    Function to return the UID value corresponding to id
    Parameters:
    id (str): the user id

    Returns:
    str: the output
    '''
    temp=User.objects.get(id=id)
    temp2=UserDetail.objects.get(user=temp)
    return temp2.UID

@register.filter(name='dict_key')
def dict_key(d, k):
    '''
    Function to return the value corresponding to the key k in the dictionary d
    Parameters:
    d (dict): a dictionary object
    k (str): the key

    Returns:
    str: the output
    '''
    #https://stackoverflow.com/questions/19745091/accessing-dictionary-by-key-in-django-template
    print(k)
    print(d)
    return d[k]

@register.filter(name='cust_name')
def cust_name(d, k):
    '''
    Function to return the customer name corresponding to the key k in the dictionary d
    Parameters:
    d (dict): a dictionary object
    k (str): the key

    Returns:
    str: the output
    '''
    #https://stackoverflow.com/questions/19745091/accessing-dictionary-by-key-in-django-template
    return d[k]['name']

@register.filter(name='cust_email')
def cust_email(d, k):
    '''
    Function to return the customer email corresponding to the key k in the dictionary d
    Parameters:
    d (dict): a dictionary object
    k (str): the key

    Returns:
    str: the output
    '''
    #https://stackoverflow.com/questions/19745091/accessing-dictionary-by-key-in-django-template
    return d[k]['email']

@register.filter(name='cust_phone')
def cust_phone(d, k):
    '''
    Function to return the customer phone number corresponding to the key k in the dictionary d
    Parameters:
    d (dict): a dictionary object
    k (str): the key

    Returns:
    str: the output
    '''
    #https://stackoverflow.com/questions/19745091/accessing-dictionary-by-key-in-django-template
    return d[k]['phone']

# @login_required(login_url="/m")
def index(request):
    '''
    Function to render and return the main webpage
    Parameters:
    request (HttpRequest): a HttpRequest object

    Returns:
    an HttpResponse object
    '''
    
    if (request.user.is_authenticated and request.user.has_perm('foodbuddy_app.isRestaurant')):
        res = Restaurant.objects.get(user=request.user)
        return redirect("/restadmin?id="+str(res.RID))
    rest=Restaurant.objects.all().order_by('-Rating')[0:12]
    rest1=Restaurant.objects.all()
    # print("\n\n\n\n\n",rest1[0].Name,rest1[0].RID,rest1[0].Email,"\n\n\n\n\n")
    # fitems=pd.read_csv("foodbuddy_app/indian_food.csv")['name']
    # fitems=['food','idli','dosa','panner','pizza','colddrink','meal','rice','pavbhaji','snaks','chicken','french fries','burger','egg','soup','paratha','dal makhni','chole','bhature','maggie','noodles','manchurian','tandori','roti']
    fitems=[]
    # print(fitems)
    # fitems=['burger.png','pizza.png']

    
  
    return render(request,'foodbuddy_html/index.html',{"rest":rest,"lst":fitems})
# def home_view(request):

@login_required(login_url="/")
def restHome(request):
    '''
    Function to render and return the homepage for a restaurant
    Parameters:
    request (HttpRequest): a HttpRequest object

    Returns:
    an HttpResponse object
    '''
    r=Restaurant.objects.get(RID=request.GET.get("id"))
    userdet=User
    date=datetime.datetime.now().date()
    booking=Bookings.objects.filter(RID=request.GET.get("id"),Status="A",Start_Date__lte=date,End_Date__gte=date)
    
    
    SigDish,names=[],[]
    for i in range(len(booking)):
        SigDish.append(booking[i])
        obj=UserDetail.objects.get(UID=booking[i].UID.UID)
        unamee=User.objects.get(username=obj.user)
        #print(SigDish)
        #print(i)
        SigDish[i].Address=unamee.first_name+" "+unamee.last_name

    # print("\n"*5,len(SigDish),"\n"*5)
    return render(request,'foodbuddy_html/RestHome.html',{"rest":r,"SigDish":SigDish})


@login_required(login_url="/")
def restAdmin(request):
    '''
    Function to render and return the homepage for a restaurant admin
    Parameters:
    request (HttpRequest): a HttpRequest object

    Returns:
    an HttpResponse object
    '''
    if request.user.has_perm("isRestaurant"):
        logout(request)
        return redirect("/")

    r=Restaurant.objects.get(RID=request.GET.get("id"))
    bk=Bookings.objects.filter(RID=request.GET.get("id"))
    uname={}
    for i in bk:
        obj=UserDetail.objects.get(UID=i.UID.UID)
        unamee=User.objects.get(username=obj.user)
        uname[i.UID.UID]={"name":unamee.first_name+" "+unamee.last_name,"email":unamee.email,"phone":obj.Phone_No}
    form=ModifyForm()
    # print("test: "+str(uname))
    return render(request,'foodbuddy_html/restAdmin.html',{"user_details":r,"book":bk,"rest":uname,"form":form})


@login_required(login_url="/")
def acceptofferR(request):
    '''
    Function to render and return the restaurant admin page after accepting ac offer from the restaurant side.
    Parameters:
    request (HttpRequest): a HttpRequest object

    Returns:
    an HttpResponse object
    '''
    if request.user.has_perm("isRestaurant"):
        logout(request)
        return redirect("/")


    temp=Bookings.objects.get(BID=request.GET.get("bid"))
    rr=Restaurant.objects.get(RID=temp.RID.RID)
    bk=Bookings.objects.filter(RID=temp.RID.RID)
    t=Bookings.objects.get(BID=request.GET.get("bid"))
    t.Status="A"
    t.save()
    uname={}
    for i in bk:
        obj=UserDetail.objects.get(UID=i.UID.UID)
        unamee=User.objects.get(username=obj.user)
        uname[i.UID.UID]={"name":unamee.first_name+" "+unamee.last_name,"email":unamee.email,"phone":obj.Phone_No}
    
    tt=UserDetail.objects.get(UID=temp.UID.UID)
    email_id=tt.user.email
    # print(rr.Name)
    # print(email_id)
    # print(t.Start_Date)
    send_mail(

    'Reservation ACCEPTED Successfully!',

    'Dear '+tt.user.first_name+' '+tt.user.last_name+'\nYour Reservation Request has been ACCEPTED by the Restaurant '+rr.Name+'\nStart Date :'+str(t.Start_Date)+'\nStart Time :'+str(t.Start_Time)+'\nEnd Date: '+str(t.End_Date)+'\nEnd Time: '+str(t.End_Time)+'\n\n\nThanks and Regards,\n  FoodBuddy Team',

    'Your_Business_Email',

    [tt.user.email],

    fail_silently=False,

    )
    return render(request,'foodbuddy_html/restAdmin.html',{"user":rr,"book":bk,"rest":uname})
    
@login_required(login_url="/")
def rejectofferR(request):
    '''
    Function to render and return the restaurant admin page after rejecting ac offer from the restaurant side.
    Parameters:
    request (HttpRequest): a HttpRequest object

    Returns:
    an HttpResponse object
    '''
    if request.user.has_perm("isRestaurant"):
        logout(request)
        return redirect("/")
    
    temp=Bookings.objects.get(BID=request.GET.get("bid"))
    rr=Restaurant.objects.get(RID=temp.RID.RID)
    bk=Bookings.objects.filter(RID=temp.RID.RID)
    t=Bookings.objects.get(BID=request.GET.get("bid"))
    t.Status="R"
    t.save()
    uname={}
    for i in bk:
        obj=UserDetail.objects.get(UID=i.UID.UID)
        unamee=User.objects.get(username=obj.user)
        uname[i.UID.UID]={"name":unamee.first_name+" "+unamee.last_name,"email":unamee.email,"phone":obj.Phone_No}
    

    tt=UserDetail.objects.get(UID=temp.UID.UID)
    email_id=tt.user.email
    # print(rr.Name)
    # print(email_id)
    # print(t.Start_Date)
    send_mail(

    'Reservation Request REJECTED!',

    'Dear '+tt.user.first_name+' '+tt.user.last_name+'\nYour Reservation Request has been REJECTED by the Restaurant '+rr.Name+'\n\n\nThanks and Regards,\n FoodBuddy Team',

    'Your_Business_Email',

    [tt.user.email],

    fail_silently=False,

    )

    return render(request,'foodbuddy_html/restAdmin.html',{"user":rr,"book":bk,"rest":uname})

@login_required(login_url="/")
def modifyofferR(request):
    '''
    Function to render and return the restaurant admin page after modifying ac offer from the restaurant side.
    Parameters:
    request (HttpRequest): a HttpRequest object

    Returns:
    an HttpResponse object
    '''
    if request.user.has_perm("isRestaurant"):
        logout(request)
        return redirect("/")

    bking=Bookings.objects.get(BID=request.GET.get("bid"))
    # print(type(bking.RID.RID))
    rr=Restaurant.objects.get(RID=bking.RID.RID)
    bk=Bookings.objects.filter(RID=bking.RID.RID)
    t=Bookings.objects.get(BID=request.GET.get("bid"),RID=bking.RID.RID,UID=bking.UID.UID)
    t.Status="M"
    t.Start_Date=request.GET.get("SDate")
    t.End_Date=request.GET.get("EDate")
    t.Start_Time=request.GET.get("STime")
    t.End_Time=request.GET.get("ETime")
    t.Party=request.GET.get("party")
    t.save()
    uname={}
    for i in bk:
        obj=UserDetail.objects.get(UID=i.UID.UID)
        unamee=User.objects.get(username=obj.user)
        uname[i.UID.UID]={"name":unamee.first_name+" "+unamee.last_name,"email":unamee.email,"phone":obj.Phone_No}
    
    temp=Bookings.objects.get(BID=request.GET.get("bid"))
    tt=UserDetail.objects.get(UID=temp.UID.UID)
    email_id=tt.user.email
    # print(rr.Name)
    # print(email_id)
    # print(t.Start_Date)
    send_mail(

    'Reservation Request Modified!',

    'Dear '+tt.user.first_name+' '+tt.user.last_name+',\nYour Reservation Request has been MODIFIED by the Restaurant '+rr.Name+'\nStart Date :'+str(t.Start_Date)+'\nStart Time :'+str(t.Start_Time)+'\nEnd Date: '+str(t.End_Date)+'\nEnd Time: '+str(t.End_Time)+'To Accept the Modified offer, kindly visit the FoodBuddy Portal.\n\n\nThanks and Regards,\n  FoodBuddy Team',

    'Your_Business_Email',

    [tt.user.email],

    fail_silently=False,

    )
    return render(request,'foodbuddy_html/restAdmin.html',{"user":rr,"book":bk,"rest":uname})


@login_required(login_url="/")
def userHome(request):
    '''
    Function to render and return the homepage of a user
    Parameters:
    request (HttpRequest): a HttpRequest object

    Returns:
    an HttpResponse object
    '''
    rr=UserDetail.objects.get(UID=request.GET.get("id"))
    bk=Bookings.objects.filter(UID=request.GET.get("id"))
    uname=User.objects.get(username=rr.user)
    rname={}
    for i in bk:
        rname[i.RID.RID]=Restaurant.objects.get(RID=i.RID.RID).Name
    # print(rname)
    return render(request,'foodbuddy_html/UserHome.html',{"user_details":rr,"book":bk,"rest":rname,"uname":uname})

@login_required(login_url="/")
def acceptoffer(request):
    '''
    Function to render and return the user home page after accepting an offer from the user side.
    Parameters:
    request (HttpRequest): a HttpRequest object

    Returns:
    an HttpResponse object
    '''
    t=Bookings.objects.get(BID=request.GET.get("bid"))
    t.Status="A"
    t.save()   
    bk=Bookings.objects.filter(UID=t.UID.UID)
    rr=UserDetail.objects.get(UID=t.UID.UID)
    print(bk)
    print(rr)
    rname={}
    for i in bk:
        rname[i.RID.RID]=Restaurant.objects.get(RID=i.RID.RID).Name
    return render(request,'foodbuddy_html/UserHome.html',{"user":rr,"book":bk,"rest":rname})

@login_required(login_url="/")
def rejectoffer(request):
    '''
    Function to render and return the user home page after rejecting an offer from the user side.
    Parameters:
    request (HttpRequest): a HttpRequest object

    Returns:
    an HttpResponse object
    '''
    t=Bookings.objects.get(BID=request.GET.get("bid"))
    t.Status="R"
    t.save()   
    bk=Bookings.objects.filter(UID=t.UID.UID)
    rr=UserDetail.objects.get(UID=t.UID.UID)
    print(bk)
    print(rr)
    rname={}
    for i in bk:
        rname[i.RID.RID]=Restaurant.objects.get(RID=i.RID.RID).Name
    return render(request,'foodbuddy_html/UserHome.html',{"user":rr,"book":bk,"rest":rname})


# def testReg(request):
#     if request.method == "GET":
#         return render(request,"foodbuddy_html/regTest.html",{})
#     elif request.method == "POST":
#         u=User.objects.create_user(request.POST['unm'], request.POST['eml'], request.POST['pas'])
        
#         permission = Permission.objects.get(name='Regular System User')
#         u.user_permissions.add(permission)

#         user = UserDetail(user=u,Address=request.POST['add'],Type='U' )
#         user.save()
#         print(request.POST)
#         return HttpResponse("Reg Success")

# def testLogin(request):
#     if request.method == "GET":
#         return render(request,"foodbuddy_html/login.html")
#     elif request.method == "POST":
#         user = authenticate(username=request.POST['unm'], password=request.POST['pas'])
#         if user is not None:
#             login(request, user)
#             return HttpResponse("Login Success")
#         else:
#             return HttpResponse("Login Fail")

def usr_logout(request):
    '''
    Function to logout a user
    Parameters:
    request (HttpRequest): a HttpRequest object

    Returns:
    an HttpResponse object
    '''
    logout(request)
    # return HttpResponse("Log Out")
    return redirect(reverse("index"))

@login_required(login_url="/")
def adddescrip(request):
    '''
    Function to render and return the user home page after adding the signature dish details from the user side.
    Parameters:
    request (HttpRequest): a HttpRequest object

    Returns:
    an HttpResponse object
    '''
    
    bking=Bookings.objects.get(BID=request.GET.get("bid"))
    # print(type(bking.RID.RID))
    rr=UserDetail.objects.get(UID=bking.UID.UID)
    bk=Bookings.objects.filter(UID=bking.UID.UID)
    t=Bookings.objects.get(BID=request.GET.get("bid"),RID=bking.RID.RID,UID=bking.UID.UID)
    t.Name=request.GET.get("name")
    t.Descrip=request.GET.get("desc")
    t.save()  
    rname={}
    for i in bk:
        rname[i.RID.RID]=Restaurant.objects.get(RID=i.RID.RID).Name
    return render(request,'foodbuddy_html/UserHome.html',{"user":rr,"book":bk,"rest":rname})

@login_required(login_url="/")
def addrating(request):
    '''
    Function to render and return the user home page after adding the rating for a restaurant from the user side.
    Parameters:
    request (HttpRequest): a HttpRequest object

    Returns:
    an HttpResponse object
    '''
    bking=Bookings.objects.get(BID=request.GET.get("bid"))
    # print(type(bking.RID.RID))
    rr=UserDetail.objects.get(UID=bking.UID.UID)
    bk=Bookings.objects.filter(UID=bking.UID.UID)
    t=Bookings.objects.get(BID=request.GET.get("bid"),RID=bking.RID.RID,UID=bking.UID.UID)
    t.Rating=request.GET.get("rate")
    t.save()
    
    rest=Restaurant.objects.get(RID=bking.RID.RID)
    # print(type(rest.Rating))
    rest.Rating=(rest.Rating_Cnt*rest.Rating+int(t.Rating))/(rest.Rating_Cnt+1)
    rest.Rating_Cnt=rest.Rating_Cnt+1
    rest.save()
    rname={}
    for i in bk:
        rname[i.RID.RID]=Restaurant.objects.get(RID=i.RID.RID).Name
    return render(request,'foodbuddy_html/UserHome.html',{"user":rr,"book":bk,"rest":rname})

def usignup(request):
    '''
    Function to render and return the index page after successfully adding a user
    Parameters:
    request (HttpRequest): a HttpRequest object

    Returns:
    an HttpResponse object
    '''
    if(request.method=="POST"):
        usname=request.POST['usname']
        usemail=request.POST['usemail']
        usphone=request.POST['usphone']
        usadd=request.POST['usaddr']
        uspass=request.POST['uspass']
        try:
            # user=User(Name=usname,Password=uspass,Email=usemail,Phone_No =usphone,Address=usadd)
            
            u=User.objects.create_user(username=usemail,email=usemail, first_name=usname, password=uspass)
        
            permission = Permission.objects.get(name='Regular System User')
            u.user_permissions.add(permission)

            user = UserDetail(user=u,Address=usadd,Phone_No=usphone,Type='U' )
            user.save()
            
        except Exception as e:
            print("OK Not success Error -> ",e)

    rest = Restaurant.objects.all().order_by('-Rating')[0:12]
    rest1 = Restaurant.objects.all()
    # print("\n\n\n\n\n",rest1[0].Name,rest1[0].RID,rest1[0].Email,"\n\n\n\n\n")
    # fitems = pd.read_csv("foodbuddy_app/indian_food.csv")['name']
    # fitems = ['food', 'idli', 'dosa', 'panner', 'pizza', 'colddrink', 'meal', 'rice', 'pavbhaji', 'snaks', 'chicken',
    #           'french fries', 'burger', 'egg', 'soup', 'paratha', 'dal makhni', 'chole', 'bhature', 'maggie', 'noodles',
    #           'manchurian', 'tandori', 'roti']
    fitems=[]
    # print(fitems)
    # fitems=['burger.png','pizza.png']

    return render(request, 'foodbuddy_html/index.html', {"rest": rest, "lst": fitems})

def ulogin(request):
    '''
    Function to render and return the index page after successfully logging in a user
    Parameters:
    request (HttpRequest): a HttpRequest object

    Returns:
    an HttpResponse object
    '''
    if (request.method == "POST"):
        # usemail = request.POST['usemail']
        # uspass = request.POST['uspass']
        # try:
        #     t=User.objects.get(Email=usemail,Password=uspass)
        # except:
        #     print("User email or password error ")
        user = authenticate(username=request.POST['usemail'], password=request.POST['uspass'])
        if user is not None:
            login(request, user)
            if(user.has_perm("foodbuddy_app.isUser")):
                return redirect(reverse("index"))
            elif(user.has_perm("foodbuddy_app.isRestaurant")):
                res = Restaurant.objects.get(user=user)
                return redirect("/restadmin?id="+str(res.RID))
                # return redirect(reverse("restadmin"))
        else:
            # print('login fail')
            messages.error(request, 'Please enter valid credentials!')

    rest = Restaurant.objects.all().order_by('-Rating')[0:12]
    rest1 = Restaurant.objects.all()
    # print("\n\n\n\n\n",rest1[0].Name,rest1[0].RID,rest1[0].Email,"\n\n\n\n\n")
    # fitems = pd.read_csv("foodbuddy_app/indian_food.csv")['name']
    # fitems = ['food', 'idli', 'dosa', 'panner', 'pizza', 'colddrink', 'meal', 'rice', 'pavbhaji', 'snaks', 'chicken',
    #           'french fries', 'burger', 'egg', 'soup', 'paratha', 'dal makhni', 'chole', 'bhature', 'maggie', 'noodles',
    #           'manchurian', 'tandori', 'roti']
    fitems=[]
    # print(fitems)
    # fitems=['burger.png','pizza.png']

    return render(request, 'foodbuddy_html/index.html', {"rest": rest, "lst": fitems})




def rsignup(request):
    '''
    Function to render and return the index page after successfully adding a restaurant
    Parameters:
    request (HttpRequest): a HttpRequest object

    Returns:
    an HttpResponse object
    '''
    if(request.method=="POST"):
        rsname=request.POST['rsname']
        rsemail=request.POST['rsemail']
        rsphone=request.POST['rsphone']
        rsadd=request.POST['rsaddr']
        rspass=request.POST['rspass']
        # rslat=request.POST['rslat']
        # rslog=request.POST['rslog']
        #fetch image from user

        try:
            # res=Restaurant(Name=rsname,Email=rsemail,Phone_No =rsphone,Address=rsadd,
            #                Rating_Cnt=0,Rating=9,Lat=rslat,Long=rslog)
            # res.save()
            u=User.objects.create_user(rsemail,rsemail, rspass)
        
            permission = Permission.objects.get(name='Restaurant Admin')
            u.user_permissions.add(permission)

            user = Restaurant(user=u,Name=rsname,Address=rsadd,Type='R',Phone_No=rsphone, Rating_Cnt=1,Rating=1 )
            user.save()
        except Exception as e:
            print("OK Not success", e)

    rest = Restaurant.objects.all().order_by('-Rating')[0:12]
    # print("\n\n\n\n\n",rest1[0].Name,rest1[0].RID,rest1[0].Email,"\n\n\n\n\n")
    # fitems = pd.read_csv("foodbuddy_app/indian_food.csv")['name']
    # fitems = ['food', 'idli', 'dosa', 'panner', 'pizza', 'colddrink', 'meal', 'rice', 'pavbhaji', 'snaks', 'chicken',
    #           'french fries', 'burger', 'egg', 'soup', 'paratha', 'dal makhni', 'chole', 'bhature', 'maggie', 'noodles',
    #           'manchurian', 'tandori', 'roti']
    # print(fitems)
    # fitems=['burger.png','pizza.png']
    fitems=[]
    return render(request, 'foodbuddy_html/index.html', {"rest": rest, "lst": fitems})

@login_required(login_url="/")
def reserved_table(request):
    try:
        # print(type(request.user.id))
        temp=User.objects.get(id=request.user.id)
        bk = Bookings(
            RID=Restaurant.objects.get(RID=request.GET.get("rid")),
            UID=UserDetail.objects.get(user=temp),
            Start_Date=request.GET.get("SDate"),
            End_Date=request.GET.get("EDate"),
            Start_Time=request.GET.get("STime"),
            End_Time=request.GET.get("ETime"),
            Party=request.GET.get("party"),
            Status="S" ,
        )
        bk.save()
    except Exception as e:
        print(e)
    return HttpResponse("Booked")

    # uname={}
    # for i in bk:
    #     obj=UserDetail.objects.get(UID=i.UID.UID)
    #     unamee=User.objects.get(username=obj.user)
    #     uname[i.UID.UID]={"name":unamee.first_name+" "+unamee.last_name,"email":unamee.email,"phone":obj.Phone_No}
    # return render(request,'foodbuddy_html/restAdmin.html',{"user":rr,"book":bk,"rest":uname})
