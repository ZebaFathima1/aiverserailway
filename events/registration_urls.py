from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventRegistrationViewSet

router = DefaultRouter()
router.register(r'', EventRegistrationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
