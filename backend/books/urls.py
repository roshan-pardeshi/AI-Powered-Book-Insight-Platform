from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'books', views.BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('upload/', views.upload_books, name='upload_books'),
    path('recommend/', views.recommend_books, name='recommend_books'),
    path('ask/', views.ask_question, name='ask_question'),
]