from django.urls import path
from . import views

urlpatterns = [

    path('', views.sklep, name="sklep"),
    path('koszyk/', views.koszyk, name="koszyk"),
    path('checkout/', views.checkout, name="checkout"),
    path('kontakt/', views.kontakt, name="kontakt"),
    path('blog/', views.blog, name="blog"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order")

]
