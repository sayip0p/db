from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from .models import Register,Product,Feedback,Cart,Payment,staff_login,FoodItem,yemani_login,YemaniFoodItem
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404 
from decimal import Decimal
from datetime import datetime
from django.contrib.auth import authenticate, login




def hello(request):
    return HttpResponse("Hello")


def index(request):
    return render(request,'index.html')

def home(request):
    return render(request,'home.html')
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = Register.objects.get(email=email, password=password)
            request.session['email'] = user.email
            return redirect('home')
        except Register.DoesNotExist:
            msg = "Invalid user name or password. Please Check Or try again."
            return render(request,'login.html' , {"msg" : msg})
    return render(request, 'login.html')


def profile(request):
    email = request.session.get('email')

    if email is not None:
        try:
            user = Register.objects.get(email=email)
            return render(request, 'profile.html', {'user': user})
        except Register.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('login')
    else:
        messages.warning(request, "You need to log in to access your profile.")
        return redirect('login')

def restaurants(request):
    return render(request, 'restaurants.html')

def add_product(request):
    if request.method == 'POST':
        name=request.POST.get("name")
        price=request.POST.get("price")
        brand=request.POST.get("brand")
        image=request.FILES.get("image")
        Product(name=name,price=price,brand=brand,image=image).save()
            
        return redirect('productlist')  
    return render(request, 'add_product.html')

def productlist(request):
    products=Product.objects.all()
    return render(request,'productlist.html',{'products':products})

def userproductlist(request):
    products=Product.objects.all()
    return render(request,'userproductlist.html',{'products':products})


def editproduct(request,id):
    pr=Product.objects.get(id=id)
    if request.method=='POST':
        name=request.POST.get("name")
        price=request.POST.get("price")
        brand=request.POST.get("brand")
        image=request.FILES.get("image")
        pr.name=name
        pr.price=price
        pr.brand=brand
        if image:
            pr.image=image
        pr.save()
        return redirect('productlist')
    return render(request,'editproduct.html',{'pr':pr})

from .models import Register
def register(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        phone=request.POST.get('phone')
        Register(name=name,email=email,password=password,phone=phone).save()
        return render(request,'index.html')
    return render(request,'register.html')

def deleteproduct(request,id):
    data=Product.objects.get(id=id)
    data.delete()
    return redirect('productlist')

def logout(request):
    request.session.flush()
    return redirect('index')

def adminlogin(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')
        if username == 'admin' and password == 'admin':
            return redirect('admin_dashboard')
    return render(request,'adminlogin.html')

def admin_dashboard(request):
    return render(request,'admin_dashboard.html')

def admin_users(request):
    users = Register.objects.all()
    return render(request, 'admin_users.html', {'users': users})

def delete_user(request, user_id):
    user = get_object_or_404(Register, id=user_id)
    user.delete()
    return redirect('admin_users')

def editprofile(request):
    email = request.session.get('email')
    user = Register.objects.get(email=email) 
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password=request.POST.get('password')


        user.name = name
        user.phone = phone
        user.email = email
        user.password = password

        user.save()

        messages.success(request, 'Profile updated successfully!')

        return redirect('profile')
    return render(request, 'editprofile.html',{'user':user})

def feedback_view(request):
    if request.method == 'POST':
        email = request.session.get('email')
        if email:
            Feedback.objects.create(
                feedback_text=request.POST['feedback_text'],
                rating=request.POST['rating'],
                email=email
            )
        else:
            return render(request, 'feedback.html', {'error': 'Email not found in session'})
    return render(request, 'feedback.html')

def admin_dashboard(request):
    feedbacks = Feedback.objects.all().order_by('-created_at')
    return render(request, 'admin_dashboard.html', {'feedbacks': feedbacks})

def delete_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    feedback.delete()
    return redirect('feedback_review')

def feedback_review(request):
    feedbacks = Feedback.objects.all().order_by('-created_at')
    return render(request, 'feedbackreview.html', {'feedbacks': feedbacks})


def add_to_cart(request, id):

    product = get_object_or_404(Product, id=id)

    email = request.session.get('email')
    if not email:
        messages.error(request, "Please log in to add products to your cart.")
        return redirect('login')
    try:
        user = Register.objects.get(email=email)
    except Register.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('login')
    
    cart_item, created = Cart.objects.get_or_create(
        user=user,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{product.name} added to cart!")
    return redirect('cart_view')

def cart_view(request): 
    email = request.session.get('email')
    if not email:
        return render(request, 'cart.html', {'cart_items': [], 'total': 0})
    user = get_object_or_404(Register, email=email)
    cart_items = Cart.objects.filter(user=user)
    for item in cart_items:
        item.subtotal = item.product.price * item.quantity
    total = sum(item.subtotal for item in cart_items)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })

def removecart(request,id):
    item = get_object_or_404(Cart, id=id)
    item.delete()
    return redirect('cart_view')

def update_cart(request):
    email = request.session.get('email')
    user = Register.objects.get(email=email)
    if request.method == 'POST':
        cart_items = Cart.objects.filter(user=user)

        for item in cart_items:
            new_quantity = request.POST.get(f'quantity_{item.id}')
            if new_quantity:
                item.quantity = int(new_quantity)
                item.save()

    return redirect('cart_view')

def proceed_to_payment(request):
    email = request.session.get('email')
    if not email:
        messages.error(request, "Please log in to proceed.")
        return redirect('login')
    
    user = get_object_or_404(Register, email=email)
    cart_items = Cart.objects.filter(user=user)

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('cart_view')

    total = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        method = request.POST.get('payment_method')
        transaction_id = f"TXN{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        for item in cart_items:
            Payment.objects.create(
                user=user,
                email=email,
                product=item.product,
                amount=item.product.price * item.quantity,
                payment_method=method,
                status='success',  
                transaction_id=transaction_id
            )
        
        cart_items.delete()  

        messages.success(request, "Payment successful!")
        return redirect('payment_success')

    return render(request, 'payment.html', {
        'total': total,
        'email': email
    })

def payment_success(request):
    return render(request, 'payment_success.html')

def pizza_palace(request):
    return render(request, 'pizza_palace.html')

def noodle_nirvana(request):
    return render(request, 'noodle_nirvana.html')

def burger_king(request):
    foods = FoodItem.objects.all()
    return render(request, 'burger_king.html', {'foods': foods})

def yemeni_mandhi(request):
    foods = FoodItem.objects.all()
    return render(request, 'yemenimandhi.html', {'foods' : foods})


def staff_login_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')

        try:
            staff = staff_login.objects.get(user_id=user_id, password=password)
            request.session['staff_id'] = staff.id
            return redirect('staff_dashboard')
        except staff_login.DoesNotExist:
            return render(request, 'staff_login.html', {'error': 'Invalid User ID or Password'})

    return render(request, 'staff_login.html')

def staff_dashboard(request):
    if 'staff_id' not in request.session:
        return redirect('staff_login')

    menu_items = FoodItem.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            name = request.POST.get('name')
            price = request.POST.get('price')
            description = request.POST.get('description')
            image = request.FILES.get('image')
            stock_status = request.POST.get('stock_status')

            if name and price and image and stock_status:
                try:
                    FoodItem.objects.create(
                        name=name,
                        price=float(price),
                        description=description or '',
                        image=image,
                        stock_status=stock_status
                    )
                    return render(request, 'staff_dashboard.html', {
                        'menu_items': FoodItem.objects.all(),
                        'success': 'Menu item added successfully!'
                    })
                except ValueError:
                    return render(request, 'staff_dashboard.html', {
                        'menu_items': menu_items,
                        'error': 'Invalid price format.'
                    })
            else:
                return render(request, 'staff_dashboard.html', {
                    'menu_items': menu_items,
                    'error': 'All required fields must be filled.'
                })

        elif action == 'update':
            try:
                for item in menu_items:
                    item_id = str(item.id)
                    name = request.POST.get(f'item_{item_id}_name')
                    price = request.POST.get(f'item_{item_id}_price')
                    description = request.POST.get(f'item_{item_id}_desc')
                    stock_status = request.POST.get(f'item_{item_id}_stock_status')
                    image = request.FILES.get(f'item_{item_id}_image')

                    if name and price and stock_status:
                        item.name = name
                        item.price = float(price)
                        item.description = description or ''
                        item.stock_status = stock_status
                        if image:
                            item.image = image
                        item.save()
                    else:
                        return render(request, 'staff_dashboard.html', {
                            'menu_items': menu_items,
                            'error': f'Missing fields for item {item.name}.'
                        })
                return render(request, 'staff_dashboard.html', {
                    'menu_items': menu_items,
                    'success': 'Menu items updated successfully!'
                })
            except ValueError:
                return render(request, 'staff_dashboard.html', {
                    'menu_items': menu_items,
                    'error': 'Invalid price format. Please enter valid numbers.'
                })

        elif action == 'delete':
            item_id = request.POST.get('item_id')
            try:
                item = FoodItem.objects.get(id=item_id)
                item.delete()
                return render(request, 'staff_dashboard.html', {
                    'menu_items': FoodItem.objects.all(),
                    'success': 'Menu item deleted successfully!'
                })
            except FoodItem.DoesNotExist:
                return render(request, 'staff_dashboard.html', {
                    'menu_items': menu_items,
                    'error': 'Menu item not found.'
                })

    return render(request, 'staff_dashboard.html', {'menu_items': menu_items})

def logout_view(request):
    if request.method == 'POST':
        request.session.flush()
        return redirect('staff_login')
    return redirect('staff_dashboard')

def menu_api(request):
    menu_items = FoodItem.objects.filter(stock_status='In Stock').values('name', 'price', 'description', 'image')
    for item in menu_items:
        item['image_url'] = f"{settings.MEDIA_URL}{item['image']}"
        del item['image']
    return JsonResponse(list(menu_items), safe=False)

def yemani_staff_login_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')

        try:
            staff = yemani_login.objects.get(user_id=user_id, password=password)
            request.session['staff_id'] = staff.id
            return redirect('yemani_dashboard')
        except yemani_login.DoesNotExist:
            return render(request, 'yemani_login.html', {'error': 'Invalid User ID or Password'})

    return render(request, 'yemani_login.html')

def yemani_dashboard(request):
    if 'staff_id' not in request.session:
        return redirect('yemani_login')

    menu_items = YemaniFoodItem.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            name = request.POST.get('name')
            price = request.POST.get('price')
            description = request.POST.get('description')
            image = request.FILES.get('image')
            stock_status = request.POST.get('stock_status')

            if name and price and image and stock_status:
                try:
                    YemaniFoodItem.objects.create(
                        name=name,
                        price=float(price),
                        description=description or '',
                        image=image,
                        stock_status=stock_status
                    )
                    return render(request, 'yemani_dashboard.html', {
                        'menu_items': YemaniFoodItem.objects.all(),
                        'success': 'Menu item added successfully!'
                    })
                except ValueError:
                    return render(request, 'yemani_dashboard.html', {
                        'menu_items': menu_items,
                        'error': 'Invalid price format.'
                    })
            else:
                return render(request, 'yemani_dashboard.html', {
                    'menu_items': menu_items,
                    'error': 'All required fields must be filled.'
                })

        elif action == 'update':
            try:
                for item in menu_items:
                    item_id = str(item.id)
                    name = request.POST.get(f'item_{item_id}_name')
                    price = request.POST.get(f'item_{item_id}_price')
                    description = request.POST.get(f'item_{item_id}_desc')
                    stock_status = request.POST.get(f'item_{item_id}_stock_status')
                    image = request.FILES.get(f'item_{item_id}_image')

                    if name and price and stock_status:
                        item.name = name
                        item.price = float(price)
                        item.description = description or ''
                        item.stock_status = stock_status
                        if image:
                            item.image = image
                        item.save()
                    else:
                        return render(request, 'yemani_dashboard.html', {
                            'menu_items': menu_items,
                            'error': f'Missing fields for item {item.name}.'
                        })
                return render(request, 'yemani_dashboard.html', {
                    'menu_items': menu_items,
                    'success': 'Menu items updated successfully!'
                })
            except ValueError:
                return render(request, 'yemani_dashboard.html', {
                    'menu_items': menu_items,
                    'error': 'Invalid price format. Please enter valid numbers.'
                })

        elif action == 'delete':
            item_id = request.POST.get('item_id')
            try:
                item = YemaniFoodItem.objects.get(id=item_id)
                item.delete()
                return render(request, 'yemani_dashboard.html', {
                    'menu_items': YemaniFoodItem.objects.all(),
                    'success': 'Menu item deleted successfully!'
                })
            except YemaniFoodItem.DoesNotExist:
                return render(request, 'yemani_dashboard.html', {
                    'menu_items': menu_items,
                    'error': 'Menu item not found.'
                })

    return render(request, 'yemani_dashboard.html', {'menu_items': menu_items})

def yemani_logout_view(request):
    if request.method == 'POST':
        request.session.flush()
        return redirect('yemani_login')
    return redirect('yemani_dashboard')

def yemani_menu_api(request):
    menu_items = YemaniFoodItem.objects.filter(stock_status='In Stock').values('name', 'price', 'description', 'image')
    for item in menu_items:
        item['image_url'] = f"{settings.MEDIA_URL}{item['image']}"
        del item['image']
    return JsonResponse(list(menu_items), safe=False)