from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import exceptions

from .azienda_serializer import Aziendaserializer
from .cliente_seriallizer import Clienteserializer
#from .fornitori_serializer import Fornitoriserializer
from .ordine_serializer import Ordineserializer
#from .tipologialavori_serializer import TipologiaLavoriSerializer
from .personale_serializer import Personaleserializer
#from .responsabile_serializer import Responsabileserialize
from .cantiere_serializer import Cantiereserializer
from .magazzino_serializer import Magazzinoserializer
from .fornitori_serializer import Fornitoriserializer
from .fatture_serializer import Fattureserializer
#from .assegnato_cantiere_serializer import Assegnato_CantiereSerializer

#from .lavorieffettuatifornitori_serializer import LavoriEffettuatiFornitoriserializer
#from .lavorieffettuatipersonale_serializer import LavoriEffettuatiPersonaleserializer
#from .tipologiapersonale_serializer import TipologiaPersonaleserializer
#from moneyed import Money
# Create your views here.
from home.models import Azienda ,Personale,Assegnato_Cantiere,Cantiere #,Cliente,Fatture,Fornitori,Ordine,Personale,TipologiaLavori,Assegnato_Cantiere,Magazzino

import json
from django.conf import settings

class CurrentAzienda(APIView):
    serializer_class = Aziendaserializer

    def get(self,request):
        a = Azienda.objects.get(current=True)
        ret = self.serializer_class(a)
        return Response(ret.data)

class SetCurrentAzienda(APIView):
    serializer_class = Aziendaserializer

    def get(self,request,id_azienda):
        all = Azienda.objects.all()
        for one in all:
            one.current = False
            one.save()

        a = Azienda.objects.get(pk=id_azienda)
        a.current=True
        a.save()
        ret = self.serializer_class(a)
        return Response(ret.data)


class AziendaList(generics.ListCreateAPIView):
    queryset = Azienda.objects.all()
    serializer_class = Aziendaserializer


class AziendaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Azienda.objects.all()
    serializer_class = Aziendaserializer
    
    def destroy(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Azienda.objects.get(pk=pk).delete() #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response({'Msg':'OK '+str(pk) +' deleted'})

    def retrieve(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Azienda.objects.get(pk=pk) #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response(serializer.data)
    
class ClientiAzienda(APIView):
    serializer_class = Clienteserializer
    def get( self,request,azienda_id):
        object = Azienda.objects.get(pk=azienda_id)
        c = object.azienda_cliente.all()
        serializer = self.serializer_class(c,many=True)
        return Response(serializer.data)

class FornitoriAzienda(APIView):
    serializer_class = Fornitoriserializer
    def get( self,request,azienda_id):
        try:
            object = Azienda.objects.get(pk=azienda_id)
        except:
            msg = " Azienda non esiste " 
            return Response(msg)
        
        c = object.azienda_fornitore.all()
        serializer = self.serializer_class(c,many=True)
        return Response(serializer.data)
    
class CantieriAzienda(APIView):
    serializer_class = Clienteserializer
    def get(self,request,azienda_id):
        object = Azienda.objects.get(pk=azienda_id)
        clienti = object.azienda_cliente.all()
        serialzer = self.serializer_class(clienti,many=True)
        resp = []
        
        for one in clienti:
            cantieri = one.cliente_cantiere.all()
            serializer_cantieri = Cantiereserializer(cantieri,many=True)
            resp.append(serializer_cantieri.data)
        
        return Response(resp)



class PersonaleAzienda(APIView):
    serializer_class = Personaleserializer
    def get(self,request,azienda_id):
        object = Azienda.objects.get(pk=azienda_id)
        personale = object.azienda_personale.all()
        perscant = personale.filter(azienda=object)
        serializer = self.serializer_class(perscant,many=True)
        return Response(serializer.data)

class MagazzinoAzienda(APIView):
    serializer_class = Magazzinoserializer
    def get(self,request,azienda_id):
        object = Azienda.objects.get(pk=azienda_id)
        magazzino = object.azienda_magazzino.all()
        magaz = magazzino.filter(azienda=object)
        serializer = self.serializer_class(magaz,many=True)
        return Response(serializer.data)

class OrdiniAzienda(APIView):
    serializer_class = Ordineserializer
    def get(self,request,azienda_id):
        try:
            object = Azienda.objects.get(pk=azienda_id)
        except:
            msg=" Azienda non esiste "
            return Response(msg)
        clienti = object.azienda_cliente.all()
        resp = []
        for one in clienti:
            cantieri = one.cliente_cantiere.all()
            for cantiere in cantieri:
                ordini = cantiere.cantiere_ordine.all()
                serializer = self.serializer_class(ordini,many=True)
                for a in serializer.data:
                    a['azienda'] = object.id
                resp.append(serializer.data)
        return Response(resp)

class FattureAzienda(APIView):
    serializer_class = Fattureserializer
    def get(self,request,azienda_id):
        try:
            object = Azienda.objects.get(pk=azienda_id)
        except:
            msg=" Azienda non esiste "
            return Response(msg)
        clienti = object.azienda_cliente.all()
        resp = []
        for one in clienti:
            cantieri = one.cliente_cantiere.all()
            for cantiere in cantieri:
                ordini = cantiere.cantiere_ordine.all()
                for ordine in ordini:
                    fattura = ordine.ordine_fatture.all()
                    
                    if fattura:
                        serializer = self.serializer_class(fattura[0])
                    #for a in serializer.data:
                        serializer.data['azienda'] = object.id
                        resp.append(serializer.data)
        return Response(resp)
    
class PersonaleAziendaCantiere(APIView):
    serializer_class = Personaleserializer
    def get(self,request,azienda_id,cantiere_id):
        object = Personale.objects.filter(azienda_id=azienda_id)
        cas = Assegnato_Cantiere.objects.filter(cantiere_id=cantiere_id)
        ret=[]
        for one in cas:
            ret.append(one.personale)

        #personale = object.azienda_personale.all()
        #for one in object:
        #    pas =  Assegnato_Cantiere.objects.filter(personale=one,cantiere_id=cantiere_id)

        ##pas = Assegnato_Cantiere.objects.filter()
        #pc = object.cantiere_assegnato.filter(cantiere_id=cantiere_id)
        #perscant = personale.filter(azienda=object)
        serializer = self.serializer_class(ret,many=True)
        return Response(serializer.data)



