from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework import generics
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import exceptions
from .cantiere_serializer import Cantiereserializer
from .ordine_serializer import Ordineserializer

from home.models import Cantiere
import json
from django.conf import settings


class CantiereList(APIView):
    serializer_class = Cantiereserializer

    def get(self,request,id_cliente,id_azienda):
        c = Cantiere.objects.filter(cliente=id_cliente)
        serializer = self.serializer_class(c,many=True)
        return Response(serializer.data)
"""
class CantiereList(generics.ListCreateAPIView):
    azienda=Azienda.objects.get(current=True)
    queryset = Cantiere.objects.all()
    serializer_class = Cantiereserializer
"""
    

class CantiereDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cantiere.objects.all()
    serializer_class = Cantiereserializer
    
    def destroy(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Cantiere.objects.get(pk=pk).delete() #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response({'Msg':'OK '+str(pk) +' deleted'})

    def retrieve(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Cantiere.objects.get(pk=pk) #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response(serializer.data)
    
class OrdiniCantiere(APIView):
    serializer_class = Ordineserializer

    def get(self,request,id_cantiere):
        c = Cantiere.objects.get(pk=id_cantiere)
        o = c.cantiere_ordine.all()
        serializer = self.serializer_class(o,many=True)

        return Response(serializer.data)
