from re import S
import rest_framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

from .models import Dinosaur
from .serializers import DinosaurSerializer

# Create your views here.
class DinosaurListView(APIView):

  def get(self, _request):

    dinosaurs = Dinosaur.objects.all()
    serialized_dinosaurs = DinosaurSerializer(dinosaurs, many=True)
    return Response(serialized_dinosaurs.data, status=status.HTTP_200_OK)

  def post(self, request):
    new_dinosaur = DinosaurSerializer(data=request.data)
    if new_dinosaur.is_valid():
      new_dinosaur.save()
      return Response(new_dinosaur.data, status=status.HTTP_201_CREATED)
    return Response(new_dinosaur.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)  

class DinosaurDetailView(APIView):

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

  

    

