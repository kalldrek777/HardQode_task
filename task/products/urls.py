from django.urls import path
from .views import ProductView, ProductDetailView, user_in_group

app_name = 'products'

urlpatterns = [
    path('', ProductView.as_view(), name='index_page'),
    path('<int:pk>/detail/', ProductDetailView.as_view(), name='detail_page'),
    path('<int:pk>/buy/', user_in_group, name='buy_page')
]
