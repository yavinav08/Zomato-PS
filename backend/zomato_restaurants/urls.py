from django.urls import path
from .views import RestaurantList, RestaurantDetail, RestaurantSearch, classify_image

urlpatterns = [
    path('', RestaurantList.as_view(), name='restaurant-list'),
    path('<int:pk>/', RestaurantDetail.as_view(), name='restaurant-detail'),
    path('search/', RestaurantSearch.as_view(), name='restaurant-search'),
    path('classify-image/', classify_image, name='classify-image'),
]
