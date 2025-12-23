from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # Готовые views для входа/выхода

urlpatterns = [
    path('', views.home, name='home'),
    path('news/', views.news_list, name='news'),
    path('catalog/', views.catalog, name='catalog'),
    path('contacts/', views.contacts, name='contacts'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/order/', views.order_create, name='order_create'),
    path('orders/my/', views.my_orders, name='my_orders'),
    path('orders/manager/', views.manager_orders, name='manager_orders'),
    # Аутентификация
    path('register/', views.register, name='register'),      # Регистрация
      path('login/', auth_views.LoginView.as_view(
        template_name='login.html',
        redirect_authenticated_user=True  # Если уже вошёл — сразу на главную
    ), name='login'),
    
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/update/<int:product_id>/<int:quantity>/', views.cart_update, name='cart_update'),
    path('feedback/', views.feedback_view, name='feedback'),
]