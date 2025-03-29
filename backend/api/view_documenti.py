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

from .documenti_serializer import Documentiserializer
from home.models import Documenti,Cantiere,Azienda
import json
from django.db.models import Sum
from django.conf import settings

class DocumentiList(generics.ListCreateAPIView):
    queryset = Documenti.objects.all()
    serializer_class = Documentiserializer
    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        for one in serializer.data:
            c=Cantiere.objects.get(pk=one['cantiere'])
            a=c.cliente.azienda
            one['azienda']=a.id
        return Response(serializer.data)

class DocumentiDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Documenti.objects.all()
    serializer_class = Documentiserializer
    
    def destroy(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Documenti.objects.get(pk=pk).delete() #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response({'Msg':'OK '+str(pk) +' deleted'})

    def retrieve(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Documenti.objects.get(pk=pk) #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response(serializer.data)
    
class DocumentiCantiere(APIView):
    serializer_class = Documentiserializer

    def get(self,request,cantiere_id):
        c = Cantiere.objects.get(pk=cantiere_id)
        d=c.cantiere_documenti.all()
        
        serializer = self.serializer_class(d,many=True)
        return Response(serializer.data)


class DocumentiAzienda(APIView):
    serializer_class = Documentiserializer

    def get(self,request,azienda_id):
        a = Azienda.objects.get(pk=azienda_id)
        clienti = a.azienda_cliente.all()
        #serialzer = self.serializer_class(clienti,many=True)
        resp = []
        
        for one in clienti:
            cantieri = one.cliente_cantiere.all()
            for c in cantieri:
                d=c.cantiere_documenti.all()
                serializer = self.serializer_class(d,many=True)
                resp.append(serializer.data)

            #serializer_cantieri = Cantiereserializer(cantieri,many=True)
            #resp.append(serializer_cantieri.data)
        
        return Response(resp)
        a = o.ordine_articoli.all()
        serializer = self.serializer_class(a,many=True)
        #return Response(serializer.data)


