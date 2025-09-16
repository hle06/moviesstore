from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='cart.index'),
    path('<int:id>/add/', views.add, name='cart.add'),
    path('clear/', views.clear, name='cart.clear'),
    path('purchase/', views.purchase, name='cart.purchase'),
    path('orders/', views.orders, name='accounts.orders'),
    path('feedback/submit/', views.submit_feedback, name='cart.submit_feedback'),
    path('feedback/', views.view_feedback, name='cart.view_feedback'),
]