from django.urls import include, path, re_path
from rest_framework import routers
from rest_api import views
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register(r'products', views.ProductApiViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('categories/', views.CategoryListOnlyAPIView.as_view()),
    re_path(r'vendas/(?P<pk>\d+)?', views.OrderAPIView.as_view()),
    
    #  username  e um password
    path('get_token', obtain_auth_token),
]