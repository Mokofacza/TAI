from django.urls import path
from . import views
from .views import register,random_meal,usun_komentarz
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('api/sklep/', views.sklep_api, name="sklep_api"),
    path('', views.sklep, name="sklep"),
    path('sklep_testowy/', views.sklep_test, name="sklep_testowy"),
    path('koszyk/', views.koszyk, name="koszyk"),
    path('checkout/', views.checkout, name="checkout"),
    path('kontakt/', views.kontakt, name="kontakt"),
    path('blog/', views.blog, name="blog"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='sklep'), name='logout'),
    path("register/", register, name="register"),
    path('random-meal/', random_meal, name='random-meal'),
    path('usun_komentarz/<int:komentarz_id>/', usun_komentarz, name='usun_komentarz'),
    path('api/', views.getData),
    path('panel_admina/', views.panel_admina, name='panel_admina'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),

]


