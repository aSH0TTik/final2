from django.shortcuts import render, redirect, get_object_or_404
from .models import News, Category, Product
from django.contrib.auth import login
from .forms import RegisterForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .cart import Cart
from .models import Order, OrderItem
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.conf import settings
from .forms import FeedbackForm
from .models import Feedback

def home(request):
    latest_news = News.objects.order_by('-date')[:3]
    popular_products = Product.objects.all()[:6]  
    context = {
        'news_list': latest_news,
        'popular_products': popular_products, 
    }
    return render(request, 'home.html', context)
def news_list(request):
    all_news = News.objects.order_by('-date')
    return render(request, 'news.html', {'news_list': all_news})

def catalog(request):
    categories = Category.objects.all()
    return render(request, 'catalog.html', {'categories': categories})

def contacts(request):
    return render(request, 'contacts.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Создаём группу Client, если её нет
            client_group, created = Group.objects.get_or_create(name='Client')
            user.groups.add(client_group)  # Добавляем пользователя в группу Client
            
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})



def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'Товар "{product.name}" добавлен в корзину!'
        })
    
    return redirect('cart_detail')  # Только если не AJAX (на всякий случай)

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart.html', {'cart': cart})

@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        order = Order.objects.create(user=request.user, total_price=cart.get_total_price())
        for item in cart:
            OrderItem.objects.create(order=order,
                                     product=item['product'],
                                     price=item['price'],
                                     quantity=item['quantity'])
        cart.clear()  # очищаем корзину
        return redirect('my_orders')
    return render(request, 'order_create.html', {'cart': cart})

@login_required
def my_orders(request):
    # Заказы только текущего пользователя
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_orders.html', {'orders': orders})

def is_manager(user):
    return user.groups.filter(name='Manager').exists()

@user_passes_test(is_manager)
def manager_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')
        order = get_object_or_404(Order, id=order_id)
        order.status = new_status
        order.save()
    
    return render(request, 'manager_orders.html', {'orders': orders})

def product_detail(request, product_id):
    """
    Страница детального просмотра товара
    """
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

def cart_update(request, product_id, quantity):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    if quantity > 0:
        cart.add(product=product, quantity=quantity, override_quantity=True)
    else:
        cart.remove(product)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        item_price = product.price  # цена за штуку
    return JsonResponse({
        'success': True,
        'item_quantity': cart.cart.get(str(product_id), {}).get('quantity', 0),
        'item_price': float(item_price),
        'total_price': float(cart.get_total_price()),
    })
    
    return redirect('cart_detail')

def feedback_view(request):
    if request.method == 'POST':
        # Используем Django форму для валидации
        form = FeedbackForm(request.POST)
        
        if form.is_valid():
            # Получаем очищенные данные
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data.get('phone', '')  # phone может быть пустым
            subject = form.cleaned_data['subject']
            message_text = form.cleaned_data['message']
            
            try:
                # Формируем сообщение для администратора
                admin_message = f"""
                Новое сообщение с сайта PCShop:
                
                От: {name}
                Email: {email}
                Телефон: {phone if phone else 'не указан'}
                
                Тема: {subject}
                
                Сообщение:
                {message_text}
                
                ---
                Это письмо отправлено автоматически с сайта PCShop.
                """
                
                # Отправляем email администратору
                send_mail(
                    subject=f'Обратная связь: {subject}',
                    message=admin_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                    fail_silently=False,
                )
                
                # Отправляем копию пользователю (опционально)
                user_message = f"""
                Уважаемый(ая) {name},
                
                Благодарим вас за обращение в PCShop!
                
                Мы получили ваше сообщение на тему "{subject}".
                Наши специалисты рассмотрят его в ближайшее время и свяжутся с вами.
                
                Текст вашего сообщения:
                {message_text}
                
                ---
                С уважением,
                Команда PCShop
                """
                
                send_mail(
                    subject=f'Копия вашего сообщения: {subject}',
                    message=user_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=True,  # Не показывать ошибки пользователю
                )
                
                messages.success(request, 'Спасибо! Ваше сообщение отправлено. Мы ответим вам в ближайшее время.')
                
                # Очищаем форму после успешной отправки
                form = FeedbackForm()
                
            except BadHeaderError:
                messages.error(request, 'Обнаружен неверный заголовок.')
            except Exception as e:
                messages.error(request, 'Ошибка при отправке сообщения. Пожалуйста, попробуйте позже.')
                print(f"Ошибка отправки email: {e}")
        else:
            # Форма не валидна, покажем ошибки
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        # GET запрос - создаем пустую форму
        form = FeedbackForm()
    
    # ВСЕГДА передаем форму в шаблон!
    return render(request, 'feedback.html', {'form': form})
