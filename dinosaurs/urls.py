from django.urls import path
from .views import DinosaurDetailView, DinosaurListView, CommentListView, CommentDetailView

urlpatterns = [
    path('', DinosaurListView.as_view()),
    path('<int:pk>/', DinosaurDetailView.as_view()),
    path('<int:dino_pk>/comments/', CommentListView.as_view()),
    path('<int:_dino_pk>/comments/<int:comment_pk/', CommentDetailView.as_view())
]