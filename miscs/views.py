
from re import S
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import Misc, Comment
from .serializers import MiscSerializer, PopulatedMiscSerializer, CommentSerializer
# Create your views here.

# MISC

class MiscListView(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, _request):

        miscs = Misc.objects.all()
        serialized_miscs = PopulatedMiscSerializer(miscs, many=True)
        return Response(serialized_miscs.data, status=status.HTTP_200_OK)

### VIEW SINGLE MISCS

class MiscDetailView(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_misc(self, pk):
        try:
            return Misc.objects.get(pk=pk)
        except Misc.DoesNotExist:
            raise NotFound()

    def get(self, _request, pk):
        misc = self.get_misc(pk=pk)
        serialized_misc = MiscSerializer(misc)
        return Response(serialized_misc.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        misc_to_update = self.get_misc(pk=pk)
        updated_misc = MiscSerializer(misc_to_update, data=request.data)
        if updated_misc.is_valid():
            updated_misc.save()
            return Response(updated_misc.data, status=status.HTTP_202_ACCEPTED)
        return Response(updated_misc.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, _request, pk):
        misc_to_delete = self.get_misc(pk=pk)
        misc_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)       

# COMMENTS

class CommentListView(APIView):

    permission_classes = (IsAuthenticated, )

    def post(self, request, misc_pk):
        request.data['misc'] = misc_pk
        request.data['owner'] = request.user.id
        serialized_comment = CommentSerializer(data=request.data)
        if serialized_comment.is_valid():
            serialized_comment.save()
            return Response(serialized_comment.data, status=status.HTTP_201_CREATED)
        return Response(serialized_comment.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class CommentDetailView(APIView):

    def delete(self, request, _misc_pk, comment_pk):
        try:
            comment_to_delete = Comment.objects.get(pk=comment_pk)
            if comment_to_delete.owner != request.user:
                raise PermissionDenied()
            comment_to_delete.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            raise NotFound()