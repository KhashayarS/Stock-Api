from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about.html', views.about, name='about'),
    path('add_stock', views.add_stock, name='add_stock'),
    path('delete/<stock_id>', views.delete, name='delete'),
    path('ticker_view/<symbol>', views.ticker_view, name='ticker_view'),
    path('delete_stock', views.delete_stock, name='delete_stock'),
]
