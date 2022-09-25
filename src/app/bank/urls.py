from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views


router = DefaultRouter()

router.register('account', views.AccountView)
router.register('replenishment', views.ReplenishmentView)


urlpatterns = [
    path('', include(router.urls)),
    path('customer/', views.CustomerDetail.as_view(), name='customer'),
]
