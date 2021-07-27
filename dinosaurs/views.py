from django.core.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import Dinosaur, Comment
from .serializers import DinosaurSerializer, PopulatedDinosaurSerializer, CommentSerializer

# Create your views here.
class DinosaurListView(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, _request):

        dinosaurs = Dinosaur.objects.all()
        serialized_dinosaurs = PopulatedDinosaurSerializer(dinosaurs, many=True)
        return Response(serialized_dinosaurs.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data['owner'] = request.user.id
        new_dinosaur = DinosaurSerializer(data=request.data)
        if new_dinosaur.is_valid():
            new_dinosaur.save()
            return Response(new_dinosaur.data, status=status.HTTP_201_CREATED)
        return Response(new_dinosaur.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)  

class DinosaurDetailView(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_dinosaur(self, pk):
        try:
            return Dinosaur.objects.get(pk=pk)
        except Dinosaur.DoesNotExist:
            raise NotFound()
  
    def get(self, _request, pk):   
            dinosaur = self.get_dinosaur(pk=pk)
            serialized_dinosaur = DinosaurSerializer(dinosaur)
            return Response(serialized_dinosaur.data, status=status.HTTP_200_OK)
  
    def put(self, request, pk):
        dinosaur_to_update = self.get_dinosaur(pk=pk)
        updated_dinosaur = DinosaurSerializer(dinosaur_to_update, data=request.data)
        if updated_dinosaur.is_valid():
            updated_dinosaur.save()
            return Response(updated_dinosaur.data, status=status.HTTP_202_ACCEPTED)
        return Response(updated_dinosaur.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)  

    def delete(self, _request, pk):    
        dinosaur_to_delete = self.get_dinosaur(pk=pk)
        dinosaur_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentListView(APIView):

    permission_classes = (IsAuthenticated, )

    def post(self, request, dino_pk):
        request.data['dinosaur'] = dino_pk
        request.data['owner'] = request.user.id
        serialized_comment = CommentSerializer(data=request.data)
        if serialized_comment.is_valid():
            serialized_comment.save()
            return Response(serialized_comment.data, status=status.HTTP_201_CREATED)
        return Response(serialized_comment.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class CommentDetailView(APIView):

   def delete(self, request, _dino_pk, comment_pk):
        try:
            comment_to_delete = Comment.objects.get(pk=comment_pk)
            if comment_to_delete.owner != request.user:
                raise PermissionDenied()
            comment_to_delete.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            raise NotFound()

  

    

