from django.urls import path
from .views import DinosaurDetailView, DinosaurListView

urlpatterns = [
  path('', DinosaurListView.as_view()),
  path('<int:pk>/', DinosaurDetailView.as_view())
]