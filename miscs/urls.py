from django.urls import path
from .views import MiscDetailView, MiscListView, CommentListView

urlpatterns = [
    path('', MiscListView.as_view()),
    path('<int:pk>/', MiscDetailView.as_view()),
    path('<int:misc_pk>/comments/', CommentListView.as_view()),
]