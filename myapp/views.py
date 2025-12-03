from datetime import date, datetime
import re
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate,login,logout
from django.core.files.storage import FileSystemStorage
import razorpay



# Create your views here.
def shp_rgstr(request):
    return render(request,"shop/shop_register.html")

def shp_rgstr_post(request):
    shop_name=request.POST['shp_name']
    password=request.POST['password']
    username=request.POST['username']
    owner=request.POST['owner']
    email=request.POST['email']
    phone=request.POST['phone']
    place=request.POST['place']
    post=request.POST['post']
    pin=request.POST['pin']
    district=request.POST['district']
    photo=request.FILES['image']
    fs=FileSystemStorage()
    img=fs.save(photo.name,photo)

    proof=request.FILES['proof']
    fs=FileSystemStorage()
    prf=fs.save(proof.name,proof)

    if User.objects.filter(username=username).exists():
        return HttpResponse("<script>alert('User already registered!');window.location='/myapp/login/'</script>")

    log=User.objects.create(username=username,password=make_password(password))
    log.save()
    log.groups.add(Group.objects.get(name="shoper"))


    ob=shop_table()
    ob.name=shop_name
    ob.owner_name=owner
    ob.email=email
    ob.phone_no=phone
    ob.place=place
    ob.post=post
    ob.pincode=pin
    ob.district=district
    ob.photo=img
    ob.proof=prf
    ob.LOGIN=log
    ob.status="pending"
    ob.save()
    return HttpResponse("<script>alert('Register successfully');window.location='/myapp/login/'</script>")



def cntrctr_rgstr(request):
    return render(request,"contractor/contractor_register.html")

def cntrctr_rgstr_post(request):
    username=request.POST['username']
    contractor_name=request.POST['cntrctr_name']
    password=request.POST['password']
    email=request.POST['email']
    dob=request.POST['dob']
    gender=request.POST['gender']
    phone=request.POST['phone']
    address=request.POST['address']
    photo=request.FILES['image']
    fs=FileSystemStorage()
    img=fs.save(photo.name,photo)

    proof=request.FILES['proof']
    fs=FileSystemStorage()
    prf=fs.save(proof.name,proof)

    if User.objects.filter(username=username).exists():
        return HttpResponse("<script>alert('User already registered!');window.location='/myapp/login/'</script>")

    log=User.objects.create(username=username,password=make_password(password))
    log.save()
    log.groups.add(Group.objects.get(name="contractor"))


    ob=contractor_table()
    ob.name=contractor_name
    ob.email=email
    ob.dob=dob
    ob.gender=gender
    ob.phone_no=phone
    ob.address=address
    ob.photo=img
    ob.proof=prf
    ob.LOGIN=log
    ob.status="pending"
    ob.save()
    return HttpResponse("<script>alert('Register successfully');window.location='/myapp/login/'</script>")



def username_validation(request):
    uname=request.GET['name']
    kk=User.objects.filter(username=uname)
    ischeck=""
    if kk.exists():
        ischeck=False
    else:
        ischeck=True

    return JsonResponse({"check":ischeck})
   

def login_get(request):
    return render(request,"login.html")

def login_post(request):
    username=request.POST['username']
    password=request.POST['password']

    ob=authenticate(request,username=username,password=password)
    if ob is not None:
        if ob.groups.filter(name="shoper").exists():
            if shop_table.objects.filter(LOGIN_id=ob.id,status="approved").exists():
                k=shop_table.objects.get(LOGIN_id=ob.id)
                login(request,ob)
                request.session['shop_id']=k.id
                return redirect("/myapp/shop_home/")
            
            else:
                return HttpResponse("<script>alert('Not approved');window.location='/myapp/shp_rgstr/'</script>")    
            
        elif ob.groups.filter(name="contractor").exists():
            if contractor_table.objects.filter(LOGIN_id=ob.id,status="approved").exists():
                k=contractor_table.objects.get(LOGIN_id=ob.id)
                login(request,ob)
                request.session['contractor_id']=k.id
                return redirect("/myapp/contractor_home/") 
            
            else:
                return HttpResponse("<script>alert('Not approved');window.location='/myapp/cntrctr_rgstr/'</script>")  
            
         
        elif ob.groups.filter(name="admin").exists():
            login(request,ob)
            return redirect("/myapp/admin_home/") 
        
        elif ob.groups.filter(name="user").exists():
            
            login(request,ob)
            return redirect("/myapp/user_home/") 
        
    else:
        return HttpResponse("<script>alert('Not Registered');window.location='/myapp/login/'</script>")

def all_logout(request):
    logout(request)
    return HttpResponse("<script> alert('Logout successfully');window.location='/myapp/home/';</script>")


# def admin_home(request):
#     return render(request,"admin/admin_home.html")

def admin_home(request):
    shop_count = shop_table.objects.filter(status="pending").count()
    complaint_count = complaint_table.objects.filter(status="pending").count()
    contractor_count = contractor_table.objects.filter(status="pending").count()

    return render(request, "admin/admin_home.html", {
        "shop_count": shop_count,
        "contractor_count": contractor_count,
        "complaint_count":complaint_count
    })


def contractor_home(request):
    return render(request,"contractor/contractor_home.html")

# def shop_home(request):
#     order_count = order_main_table.objects.filter(status="paid",
#     order_sub_table__PRODUCT_SHOP_id=request.session['shop_id'] 
#     ).distinct().count()
#     return render(request,"shop/shop_home.html",{
#         "order_count":order_count
#     })



def shop_home(request):
    sub_orders = order_sub_table.objects.filter(
        PRODUCT__SHOP_id=request.session['shop_id'],  
        ORDER_MAIN__status="paid"
    ).values_list('ORDER_MAIN_id', flat=True).distinct()

    order_count = sub_orders.count()  

    return render(request, "shop/shop_home.html", {
        "order_count": order_count
    })


def user_home(request):
    return render(request,"user/user_home.html")

def verify_shop(request):
    ob=shop_table.objects.all()
    return render(request,"admin/verify_shop.html",{"data":ob})

def shop_accept(request,id):
    ob = shop_table.objects.filter(id=id).update(status="approved") 
    return HttpResponse("<script>alert('Approved');window.location='/myapp/admin_home/'</script>")

def shop_reject(request,id):
    ob = shop_table.objects.filter(id=id).update(status="rejected") 
    return HttpResponse("<script>alert('rejected');window.location='/myapp/shp_rgstr/'</script>")


def verify_contractor(request):
    ob=contractor_table.objects.all()
    for i in ob:
        today = datetime.today()
        i.age = today.year - i.dob.year - ((today.month, today.day) < (i.dob.month, i.dob.day))
    return render(request,"admin/verify_contractor.html",{"data":ob})

def contractor_accept(request,id):
    ob = contractor_table.objects.filter(id=id).update(status="approved") 
    return HttpResponse("<script>alert('Approved');window.location='/myapp/admin_home/'</script>")

def contractor_reject(request,id):
    ob = contractor_table.objects.filter(id=id).update(status="rejected") 
    return HttpResponse("<script>alert('rejected');window.location='/myapp/admin_home/'</script>")

def add_category(request):
    return render(request,"admin/add_category.html")

def add_category_post(request):
    category_name=request.POST['category_name']

    ob=category_table()
    ob.category_name=category_name
    ob.save()
    return HttpResponse("<script>alert('Added Successfully');window.location='/myapp/view_category/'</script>")

def view_category(request):
    ob=category_table.objects.all()
    return render(request,"admin/view_category.html",{"data":ob})

def delete_category(request,id):
    ob=category_table.objects.get(id=id)
    ob.delete()
    return HttpResponse("<script>alert('deleted Successfully');window.location='/myapp/view_category/'</script>")



def add_shop_product(request):
    return render(request,"shop/add_shop_product.html")

def add_shop_product_post(request):
    item=request.POST['item_name']
    price=request.POST['price']
    photo=request.FILES['image']
    fs=FileSystemStorage()
    img=fs.save(photo.name,photo)
    details=request.POST['details']
   

    ob=product_table()
    ob.item_name=item
    ob.price=price
    ob.photo=img
    ob.details=details
    ob.SHOP = shop_table.objects.get(id=request.session['shop_id']) 
    ob.save()
    return HttpResponse("<script>alert('Added Successfully');window.location='/myapp/view_shop_product/'</script>")


def edit_shop_product(request,id):
    request.session['pid']=id
    ob=product_table.objects.get(id=id)
    return render(request,"shop/edit_shop_product.html",{"data":ob})

def edit_shop_product_post(request):
    item=request.POST['item_name']
    price=request.POST['price']
    photo=request.FILES['image']
    fs=FileSystemStorage()
    img=fs.save(photo.name,photo)
    details=request.POST['details']
   

    ob=product_table.objects.get(id=request.session['pid'])
    ob.item_name=item
    ob.price=price
    ob.photo=img
    ob.details=details
    ob.save()
    return HttpResponse("<script>alert('Edit Successfully');window.location='/myapp/view_shop_product/'</script>")

def delete_shop_product(request,id):
    ob=product_table.objects.get(id=id)
    ob.delete()
    return HttpResponse("<script>alert('delete Successfully');window.location='/myapp/view_shop_product/'</script>")

def view_shop_product(request):
    ob=product_table.objects.filter(SHOP__id=request.session['shop_id'])
    return render(request,"shop/view_shop_product.html",{"data":ob})


def add_offer_product(request,id):
    ob=product_table.objects.get(id=id)
    request.session['pid']=id
    return render(request,"shop/add_offer_product.html",{"data":ob})


def add_offer_product_post(request):
    price=request.POST['offer_price']
    start_date=request.POST['start_date']
    end_date=request.POST['end_date']
    details=request.POST['details']
    offer_name=request.POST['offer_name']
    

    ob=offer_table()
    ob.date_entry=date.today()
    ob.start_date=start_date
    ob.end_date=end_date
    ob.offer_name=offer_name
    ob.offer_price=price
    ob.details=details
    ob.PRODUCT =product_table.objects.get(id=request.session['pid'])

    ob.save()
    return HttpResponse("<script>alert('Added Successfully');window.location='/myapp/view_offer_product/'</script>")

def view_offer_product(request):
    ob=offer_table.objects.all()
    return render(request,"shop/view_offer_product.html",{"data":ob})


def edit_offer_product(request,id):
    ob=offer_table.objects.get(id=id)
    request.session['oid']=id
    return render(request,"shop/edit_offer_product.html",{"data":ob})


def edit_offer_product_post(request):
    price=request.POST['offer_price']
    start_date=request.POST['start_date']
    end_date=request.POST['end_date']
    details=request.POST['details']
    offer_name=request.POST['offer_name']
    

    ob=offer_table.objects.get(id=request.session['oid'])
    ob.start_date=start_date
    ob.end_date=end_date
    ob.offer_name=offer_name
    ob.offer_price=price
    ob.details=details
    # ob.PRODUCT =product_table.objects.get(id=request.session['pid'])
    ob.save()
    return HttpResponse("<script>alert('Edit Successfully');window.location='/myapp/view_offer_product/'</script>")

def delete_offer_product(request,id):
    ob=offer_table.objects.get(id=id)
    ob.delete()
    return HttpResponse("<script>alert('delete Successfully');window.location='/myapp/view_offer_product/'</script>")

def view_product(request):
    ob=product_table.objects.all()
    return render(request,"user/view_product.html",{"data":ob})

def view_offer(request,id):
    ob=offer_table.objects.filter(PRODUCT__id=id)
    if ob.exists():
        return render(request,"view_offer.html",{"i":ob})

    else:
           
       k=request.user.id
       print(k)
       if k.groups.filter(name="user").exists():
                return HttpResponse("<script>alert('it has no offer');window.location='/myapp/view_product/'</script>")

       else:
                return HttpResponse("<script>alert('it has no offer');window.location='/myapp/contractor_view_product/'</script>")

               



def add_contractor_work(request):
    return render(request,"contractor/add_contractor_work.html")

def add_contractor_work_post(request):
    work=request.POST['work_name']
    photo=request.FILES['image']
    fs=FileSystemStorage()
    img=fs.save(photo.name,photo)
    description=request.POST['description']
    rate=request.POST['rate']
   

    ob=work_table()
    ob.work_name=work
    ob.photo=img
    ob.description=description
    ob.rate=rate
    ob.CONTRACTOR = contractor_table.objects.get(id=request.session['contractor_id']) 
    ob.save()
    return HttpResponse("<script>alert('Added Successfully');window.location='/myapp/view_contractor_work/'</script>")

def view_contractor_work(request):
    ob=work_table.objects.filter(CONTRACTOR__id=request.session['contractor_id'])
    return render(request,"contractor/view_contractor_work.html",{"data":ob})


def delete_contractor_work(request,id):
    ob=work_table.objects.get(id=id)
    ob.delete()
    return HttpResponse("<script>alert('delete Successfully');window.location='/myapp/view_contractor_work/'</script>")

def edit_contractor_work(request,id):
      ob=work_table.objects.get(id=id)
      request.session['cid']=id
      return render(request,"contractor/edit_contractor_work.html",{"data":ob})

def edit_contractor_work_post(request):
    work=request.POST['work_name']
    description=request.POST['description']
    rate=request.POST['rate']
    ob=work_table.objects.get(id=request.session['cid'])
    if 'image' in request.FILES:
        photo=request.FILES['image']
        fs=FileSystemStorage()
        img=fs.save(photo.name,photo)
        ob.photo=img

    ob.work_name=work
    ob.description=description
    ob.rate=rate
    ob.save()
    return HttpResponse("<script>alert('Edit Successfully');window.location='/myapp/view_contractor_work/'</script>")


def user_register(request):
    return render (request,"user/user_register.html")

# def user_register_post(request):
#     username=request.POST['username']
#     password=request.POST['password']
#     email=request.POST['email']
#     phone=request.POST['phone_no']
#     place=request.POST['place']
#     post=request.POST['post']
#     pin=request.POST['pin']
#     district=request.POST['district']
    

#     if User.objects.filter(email=email).exists():
#         return HttpResponse("<script>alert('Email aaaaa already registered!');window.location='/myapp/login/'</script>") 
    
#     log=User.objects.create(username=email,email=email,password=make_password(password))
#     log.save()
#     log.groups.add(Group.objects.get(name="user"))

#     ob=user_table()
#     ob.name=username
#     ob.email=email
#     ob.phone_no=phone
#     ob.place=place
#     ob.post=post
#     ob.pincode=pin
#     ob.district=district
#     ob.LOGIN=log
#     ob.save()
#     return HttpResponse("<script>alert('Register Successfully');window.location='/myapp/user_login/'</script>") 


def user_register_post(request):
    # Get POST data
    username = request.POST.get('username', '').strip()
    password = request.POST.get('password', '').strip()
    email = request.POST.get('email', '').strip()
    phone = request.POST.get('phone_no', '').strip()
    place = request.POST.get('place', '').strip()
    post = request.POST.get('post', '').strip()
    pin = request.POST.get('pin', '').strip()
    district = request.POST.get('district', '').strip()

    # -----------------------
    # SERVER-SIDE VALIDATION
    # -----------------------

    # Check required fields
    if not all([username, password, email, phone, place, post, pin, district]):
        return HttpResponse("<script>alert('All fields are required!');window.history.back();</script>")

    # Email validation
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_regex, email):
        return HttpResponse("<script>alert('Invalid email format!');window.history.back();</script>")

    # Check if email already exists
    if User.objects.filter(email=email).exists():
        return HttpResponse("<script>alert('Email already registered!');window.location='/myapp/login/'</script>") 

    # Password validation: at least 6 characters, one number
    if len(password) < 3 or not any(c.isdigit() for c in password):
        return HttpResponse("<script>alert('Password must be at least 6 characters and include a number!');window.history.back();</script>")

    # Phone validation: must be digits and 10 characters
    if not phone.isdigit() or len(phone) != 10:
        return HttpResponse("<script>alert('Phone number must be 10 digits!');window.history.back();</script>")

    # PIN code validation: must be digits and 6 characters
    if not pin.isdigit() or len(pin) != 6:
        return HttpResponse("<script>alert('Pincode must be 6 digits!');window.history.back();</script>")

    # -----------------------
    # SAVE USER
    # -----------------------
    log = User.objects.create(
        username=email,
        email=email,
        password=make_password(password)
    )
    log.save()
    log.groups.add(Group.objects.get(name="user"))

    # Save additional user info
    ob = user_table(
        name=username,
        email=email,
        phone_no=phone,
        place=place,
        post=post,
        pincode=pin,
        district=district,
        LOGIN=log
    )
    ob.save()

    return HttpResponse("<script>alert('Registered Successfully!');window.location='/myapp/user_login/'</script>")



def user_login(request):
    return render(request,"user/user_login.html")

def user_login_post(request):
    email=request.POST['email']
    password=request.POST['password']

    ob=authenticate(request,username=email,password=password)
    if ob is not None:
       if ob.groups.filter(name="user").exists():
        login(request,ob)
        return redirect("/myapp/user_home/")

    else:
        return HttpResponse("<script>alert('Not Registered');window.location='/myapp/user_login/'</script>")

def home(request):
    return render(request,"home.html")


def cart(request,id):
    request.session['pid']=id
    return render(request,"user/cart.html")

def cart_post(request):
    quantity=request.POST['quantity']
    

    ob=cart_table()
    ob.date=date.today()
    ob.quantity=quantity
    ob.PRODUCT=product_table.objects.get(id= request.session['pid'])
    ob.lOGIN_id=request.user.id
    ob.save()


   

    return redirect("/myapp/view_product/")

# def contractor_cart_post(request):
#     quantity=request.POST['quantity']

#     ob=cart_table()
#     ob.date=date.today()
#     ob.quantity=quantity
#     ob.PRODUCT=product_table.objects.get(id= request.session['pid'])
#     ob.USER=contractor_table.objects.get(LOGIN_id=request.user.id)
#     ob.save()
#     return redirect("/myapp/view_product/")


def view_cart(request):
    # try:
    #     # If the logged-in account is a user
    #     user = user_table.objects.get(LOGIN_id=request.user.id)
    #     ob = cart_table.objects.filter(USER=user)
    # except user_table.DoesNotExist:
    #     # Otherwise it must be a contractor
    #     contractor = contractor_table.objects.get(LOGIN_id=request.user.id)
    #     ob = cart_table.objects.filter(CONTRACTOR=contractor)

    ob = cart_table.objects.filter(lOGIN=request.user)

    return render(request, "user/view_cart.html", {"data": ob})


def remove_cart(request,id):
    ob=cart_table.objects.get(id=id)
    ob.delete()
    return redirect("/myapp/view_cart/")





def raz_pay(request):
    # import razorpay
    razorpay_api_key = "rzp_test_MJOAVy77oMVaYv"
    razorpay_secret_key = "MvUZ03MPzLq3lkvMneYECQsk"

    razorpay_client = razorpay.Client(auth=(razorpay_api_key, razorpay_secret_key))

   # ✅ Get cart items for logged-in user
    cart_items = cart_table.objects.filter(lOGIN=request.user.id)

# ✅ Calculate total amount
    total_amount = 0
    for item in cart_items:
      try:
        total_amount += item.PRODUCT.price * item.quantity
      except AttributeError:
        raise Exception("Your product_table must have a 'price' field")

# ✅ Define amount properly
      amount = int(total_amount)


    # Create a Razorpay order (you need to implement this based on your logic)
    order_data = {
        'amount': amount,
        'currency': 'INR',
        'receipt': 'order_rcptid_11',
        'payment_capture': '1',  # Auto-capture payment
    }

    # Create an order
    order = razorpay_client.order.create(data=order_data)

    context = {
        'razorpay_api_key': razorpay_api_key,
        'amount': order_data['amount'],
        'currency': order_data['currency'],
        'order_id': order['id'],
    }


    ob=order_main_table()
    ob.date=datetime.now().today()
    ob.total_amount=total_amount
    ob.status="pending"
    ob.USER=user_table.objects.get(LOGIN_id=request.user.id)
    ob.save()


    for i in cart_items:

        obs=order_sub_table()
        obs.ORDER_MAIN=ob
        obs.quantity=i.quantity
        obs.price=i.PRODUCT.price*i.quantity
        # obs.ORDER_MAIN.
        obs.PRODUCT=i.PRODUCT
        obs.save()




    obj = payment_table()
    obj.ORDER_MAIN= ob
    obj.date = datetime.now().strftime('%Y%m%d')
    obj.total_amount = float(amount)
    obj.status = 'paid'
    obj.save()

    ob.status="paid"
    ob.save()

    cart_items.delete()

    return render(request, 'pay.html',{ 'razorpay_api_key': razorpay_api_key,
        'amount': order_data['amount'],
        'currency': order_data['currency'],
        'order_id': order['id'],"id":id})

 


# def send_rating(request):
#     return render(request,"user/send_rating.html")
    
# def send_rating_post(request):
#     rating=request.POST['rating']


def view_contractors(request):
    ob=contractor_table.objects.all()
    return render(request,"user/view_contractor.html",{"data":ob})

def view_work(request,id):
    # ob=work_table.objects.all()
    ob=work_table.objects.filter(CONTRACTOR_id=id)
    return render(request,"user/view_work.html",{"data":ob})

def send_feedback(request):
    return render(request,"user/send_feedback.html")

def send_feedback_post(request):
    feedback=request.POST['feedback']
    rating=request.POST['star']


    ob=feedback_table()
    ob.date=datetime.now().today()
    ob.feedback=feedback
    ob.USER=user_table.objects.get(LOGIN_id=request.user.id)
    ob.rating=rating
    ob.save()
    return HttpResponse("<script>alert('Sent your feedback');window.location='/myapp/user_home/'</script>")

def view_feedback_review(request):
    ob=feedback_table.objects.all()
    return render(request,"user/view_feedback_review.html",{"data":ob})


def send_complaint(request):
    return render(request,"user/send_complaint.html")

def send_complaint_post(request):
    complaint=request.POST['complaint']

    ob=complaint_table()
    ob.date=datetime.now().today()
    ob.complaint=complaint
    ob.status="pending"
    ob.USER=user_table.objects.get(LOGIN_id=request.user.id)
    ob.save()
    return HttpResponse("<script>alert('Sent your complaint');window.location='/myapp/user_home/'</script>")


def view_order_main(request):
    ob=order_main_table.objects.filter(USER__LOGIN_id=request.user.id)
    return render(request,"user/view_orders.html",{"data":ob})

def view_order_sub(request,id):
    ob=order_sub_table.objects.filter(ORDER_MAIN_id=id)
    return render(request,"user/view_order_sub.html",{"data":ob})


def view_shop_orders(request):
     k=order_sub_table.objects.filter(PRODUCT__SHOP_id=request.session['shop_id'])
     r= set(i.ORDER_MAIN_id for i in k)
     ob=order_main_table.objects.filter(id__in=r)
     return render(request,"shop/view_shop_order.html",{"data":ob})

def view_shop_order_sub(request,id):
     ob=order_sub_table.objects.filter(ORDER_MAIN_id=id)
     return render(request,"shop/view_shop_order_sub.html",{"data":ob})


def order_confirm(request,id):
    ob = order_main_table.objects.filter(id=id).update(status="Delivered") 
    return HttpResponse("<script>alert('Approved');window.location='/myapp/view_shop_order/'</script>")


def order_reject(request,id):
    ob = order_main_table.objects.filter(id=id).update(status="cancelled") 
    return HttpResponse("<script>alert('rejected');window.location='/myapp/view_shop_order/'</script>")


def view_feedback(request):
    ob=feedback_table.objects.all()
    for i in ob:
        i.rating=i.rating/5*100
    return render(request,"admin/view_feedback.html",{"data":ob})


def view_complaints(request):
    ob=complaint_table.objects.all()
    return render(request,"admin/view_complaint.html",{"data":ob})

def send_reply(request,id):
    request.session['cid']=id
    return render(request,"admin/send_reply.html")


def send_reply_post(request):
    reply=request.POST['reply']

    ob=complaint_table.objects.get(id=request.session['cid'])
    ob.reply=reply
    ob.status="replied"
    ob.save()
    return HttpResponse("<script>alert('Sent your reply');window.location='/myapp/admin_home/'</script>")

def view_reply(request):
    ob=complaint_table.objects.filter(USER_id__LOGIN=request.user.id)
    return render(request,"user/view_reply.html",{"data":ob})

def contractor_view_product(request):
    ob=product_table.objects.all()
    return render(request,"contractor/contractor_view_product.html",{"data":ob})


def send_work_request(request,id):
    work = work_table.objects.get(id=id)  


    ob=request_table()
    ob.WORK=work
    ob.USER=user_table.objects.get(LOGIN_id=request.user.id)
    ob.date = datetime.now().date() 
    ob.status="pending"
    ob.save()
    return HttpResponse(f"<script>alert('Request for  \"{work.work_name}\" successfully sent');window.location='/myapp/user_home/'</script>")

def view_work_request(request):
    ob=request_table.objects.filter(WORK__CONTRACTOR__LOGIN__id=request.user.id)
    return render(request,"contractor/view_work_request.html",{"data":ob})



def work_request_accept(request,id):
    ob = request_table.objects.filter(id=id).update(status="approved") 
    return HttpResponse("<script>alert('Approved');window.location='/myapp/view_work_request/'</script>")

def work_request_reject(request,id):
    ob = request_table.objects.filter(id=id).update(status="rejected") 
    return HttpResponse("<script>alert('rejected');window.location='/myapp/view_work_request/'</script>")

def user_view_request_status(request,id):
    ob=request_table.objects.filter(WORK__id=id,USER__LOGIN__id=request.user.id)
    return render(request,"user/view_request_status.html",{"data":ob})