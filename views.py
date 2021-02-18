from django.shortcuts import render
from rest_framework import generics
from app.serializers import BookSerializer
from app.models import Book
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# Create your views here.
class BookList(generics.ListCreateAPIView):
    queryset=Book.objects.all()
    serializer_class=BookSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Book
    serializer_class=BookSerializer
    #def delete(self,request,pk,format=None):
      #  Book=self.get_object()
      #  Book.delete() 
       # return Response({'response:':"Book deleted susccessfully"})
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]



