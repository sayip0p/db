from django.urls import path, include
from.import views

from django.conf.urls.static import static
from django.conf import settings





urlpatterns = [
    path("",views.index,name='index'),

    path("index/",views.index,name='index'),
    path("home/",views.home,name='home'),
    path("Register/",views.register,name='Register'),
    path("login/",views.login,name='login'),
    path("profile/",views.profile,name='profile'),
    path("restaurants/", views.restaurants, name="restaurants"),
    path("add_product/", views.add_product, name="add_product"),
    path("productlist/", views.productlist, name="productlist"),
    path("userproductlist/", views.userproductlist, name="userproductlist"),
    path("editproduct/<int:id>/", views.editproduct, name="editproduct"),
    path("deleteproduct/<int:id>/", views.deleteproduct, name="deleteproduct"),
    path("logout/", views.logout, name="logout"),
    path("adminlogin/", views.adminlogin, name="adminlogin"),
    path("admin_dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path('admin_users/', views.admin_users, name='admin_users'),
    path("delete_user/<int:user_id>/", views.delete_user, name='delete_user'),
    path('editprofile/', views.editprofile, name='editprofile'),
    path('feedback_view/', views.feedback_view, name='feedback_view'),
    path('delete_feedback/<int:feedback_id>/', views.delete_feedback, name='delete_feedback'),
    path('feedbackreview/', views.feedback_review, name='feedback_review'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart_view/', views.cart_view, name='cart_view'),
    path("removecart/<int:id>/", views.removecart, name="removecart"),
    path("update_cart/", views.update_cart, name="update_cart"),
    path('payment/', views.proceed_to_payment, name='proceed_to_payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('pizza_palace/', views.pizza_palace, name='pizza_palace'),
    path('noodle_nirvana/', views.noodle_nirvana, name='noodle_nirvana'),
    path('burger_king/', views.burger_king, name='burger_king'),
    path('stafflogin/', views.staff_login_view, name='staff_login'),
    path('staffdashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('api/menu/', views.menu_api, name='menu_api'),
    path('yemeni_mandhi/', views.yemeni_mandhi, name='yemeni_mandhi'),
    path('yemani/login/', views.yemani_staff_login_view, name='yemani_login'),
    path('yemani/dashboard/', views.yemani_dashboard, name='yemani_dashboard'),
    path('yemani/logout/', views.yemani_logout_view, name='yemani_logout'),
    path('yemani/menu-api/', views.yemani_menu_api, name='yemani_menu_api'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)