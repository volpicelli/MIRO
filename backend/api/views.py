from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework import generics
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist

from .articoli_serializer import Articoliserializer
from .azienda_serializer import Aziendaserializer
from .cantiere_serializer import Cantiereserializer
from .cliente_seriallizer import Clienteserializer
from .fatture_serializer  import Fattureserializer
from .fornitori_serializer import Fornitoriserializer
from .ordine_serializer import Ordineserializer
from .magazzino_serializer import Magazzinoserializer
#from .tipologialavori_serializer import TipologiaLavoriSerializer
from .personale_serializer import Personaleserializer
from .responsabile_serializer import Responsabileserializer
from .tipologialavori_serializer import TipologiaLavoriSerializer
from .assegnato_cantiere_serializer import Assegnato_CantiereSerializer

#from .lavorieffettuatifornitori_serializer import LavoriEffettuatiFornitoriserializer
#from .lavorieffettuatipersonale_serializer import LavoriEffettuatiPersonaleserializer
#from .tipologiapersonale_serializer import TipologiaPersonaleserializer
#from moneyed import Money
# Create your views here.
from home.models import Cantiere,Articoli,Azienda,Cliente,Fatture,Fornitori,Ordine,Personale,Responsabile,TipologiaLavori,\
                        Assegnato_Cantiere,Magazzino


class Assegnato_CantiereList(generics.ListCreateAPIView):
    queryset = Assegnato_Cantiere.objects.all()
    serializer_class = Assegnato_CantiereSerializer


class Assegnato_CantiereDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assegnato_Cantiere.objects.all()
    serializer_class = Assegnato_CantiereSerializer
    
    def destroy(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Assegnato_Cantiere.objects.get(pk=pk).delete() #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response({'Msg':'OK '+str(pk) +' deleted'})

    def retrieve(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Assegnato_Cantiere.objects.get(pk=pk) #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response(serializer.data)
class CantieriPersonale(APIView):
    serializer_class = Cantiereserializer

    def get(self,request,id_personale):
        ret=[]
        try:
            p = Personale.objects.get(id=id_personale)
            
        except ObjectDoesNotExist:
            ret.append({'Error': "Personale {} non esiste".format(id_personale)})
            return Response(ret)
        
        c = p.personale_assegnato.all()

        for one in c:
            p={}
            p ={ "id": one.cantiere.id,
                 "nome": one.cantiere.nome,
                 "descrizione": one.cantiere.descrizione
            }
            ret.append(p)
        return Response(ret)

class PersonaleSuCantiere(APIView):
    serializer_class = Personaleserializer

    def get(self,request,id_cantiere):
        ret=[]
        try:
            c = Cantiere.objects.get(id=id_cantiere)
            
        except ObjectDoesNotExist:
            ret.append({'Error': "Cantiere {} non esiste".format(id_cantiere)})
            return Response(ret)
        
        pers = c.cantiere_assegnato.all()

        
        
        for one in pers:
            o = {}
            o = {"id": one.personale.id,
                "nome": one.personale.nome,
                "cognome": one.personale.cognome,
                "wage_lordo": one.personale.wage_lordo,
                "wage_netto": one.personale.wage_netto,
                "tipologia_lavoro_id" : one.personale.tipologia_lavoro_id,
                "tipologia_lavoro": TipologiaLavori.objects.values('descrizione').get(pk=one.personale.tipologia_lavoro_id)['descrizione'],
                "cantiere": one.cantiere_id
                }
            ret.append(o)

        return Response(ret)
        
        
        #serializer = self.serializer_class(pers,many=True)

        #return Response(serializer.data)
"""
        ret = {}
        for key,value in pers:
            ret['key'] = value
        return Response(ret)
"""

class TipologiaLavoriList(generics.ListCreateAPIView):
    queryset = TipologiaLavori.objects.all()
    serializer_class = TipologiaLavoriSerializer


class TipologiaLavoriDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TipologiaLavori.objects.all()
    serializer_class = TipologiaLavoriSerializer
    
    def destroy(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = TipologiaLavori.objects.get(pk=pk).delete() #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response({'Msg':'OK '+str(pk) +' deleted'})

    def retrieve(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = TipologiaLavori.objects.get(pk=pk) #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response(serializer.data)

class ArticoliList(generics.ListCreateAPIView):
    queryset = Articoli.objects.all()
    serializer_class = Articoliserializer


class ArticoliDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Articoli.objects.all()
    serializer_class = Articoliserializer
    
    def destroy(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Articoli.objects.get(pk=pk).delete() #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response({'Msg':'OK '+str(pk) +' deleted'})

    def retrieve(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Articoli.objects.get(pk=pk) #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response(serializer.data)
    
class ArticoliOrdine(APIView):
    serializer_class = Articoliserializer

    def get(self,request,id_ordine):
        o = Ordine.objects.get(pk=id_ordine)
        a = o.ordine_articoli.all()
        serializer = self.serializer_class(a,many=True)
        return Response(serializer.data)




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
    
class CantiereList(generics.ListCreateAPIView):
    queryset = Cantiere.objects.all()
    serializer_class = Cantiereserializer

    

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

 
class ClienteList(generics.ListCreateAPIView):
    queryset = Cliente.objects.all()
    serializer_class = Clienteserializer

    

class ClienteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cliente.objects.all()
    serializer_class = Clienteserializer
    
    def destroy(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Cliente.objects.get(pk=pk).delete() #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response({'Msg':'OK '+str(pk) +' deleted'})

    def retrieve(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Cliente.objects.get(pk=pk) #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response(serializer.data)
 
class FattureList(generics.ListCreateAPIView):
    queryset = Fatture.objects.all()
    serializer_class = Fattureserializer

    

class FattureDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Fatture.objects.all()
    serializer_class = Fattureserializer
    
    def destroy(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Fatture.objects.get(pk=pk).delete() #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response({'Msg':'OK '+str(pk) +' deleted'})

    def retrieve(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Fatture.objects.get(pk=pk) #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response(serializer.data)
 
class FornitoriList(generics.ListCreateAPIView):
    queryset = Fornitori.objects.all()
    serializer_class = Fornitoriserializer


class FornitoriDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Fornitori.objects.all()
    serializer_class = Fornitoriserializer
    
    def destroy(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Fornitori.objects.get(pk=pk).delete() #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response({'Msg':'OK '+str(pk) +' deleted'})

    def retrieve(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Fornitori.objects.get(pk=pk) #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response(serializer.data)


class OrdineList(generics.ListCreateAPIView):
    queryset = Ordine.objects.all()
    serializer_class = Ordineserializer

    

class OrdineDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ordine.objects.all()
    serializer_class = Ordineserializer
    
    def destroy(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Ordine.objects.get(pk=pk).delete() #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response({'Msg':'OK '+str(pk) +' deleted'})

    def retrieve(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Ordine.objects.get(pk=pk) #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response(serializer.data)




class PersonaleList(generics.ListCreateAPIView):
    queryset = Personale.objects.all()
    serializer_class = Personaleserializer


class PersonaleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Personale.objects.all()
    serializer_class = Personaleserializer
    
    def destroy(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Personale.objects.get(pk=pk).delete() #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response({'Msg':'OK '+str(pk) +' deleted'})

    def retrieve(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Personale.objects.get(pk=pk) #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response(serializer.data)


class ResponsabileList(generics.ListCreateAPIView):
    queryset = Responsabile.objects.all()
    serializer_class = Responsabileserializer


class ResponsabileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Responsabile.objects.all()
    serializer_class = Responsabileserializer
    
    def destroy(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Responsabile.objects.get(pk=pk).delete() #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response({'Msg':'OK '+str(pk) +' deleted'})

    def retrieve(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Responsabile.objects.get(pk=pk) #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response(serializer.data)

class ResponsabileCantiere(APIView):
    serializer_class = Responsabileserializer

    def get(self,request,id_cantiere):
        c = Cantiere.objects.get(pk=id_cantiere)
        r = c.responsabile
        serializer = self.serializer_class(r)
        return Response(serializer.data)   


class MagazzinoList(generics.ListCreateAPIView):
    queryset = Magazzino.objects.all()
    serializer_class = Magazzinoserializer

class MagazzinoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Magazzino.objects.all()
    serializer_class = Magazzinoserializer
    
    def destroy(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Magazzino.objects.get(pk=pk).delete() #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response({'Msg':'OK '+str(pk) +' deleted'})

    def retrieve(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Magazzino.objects.get(pk=pk) #kwargs['pk'])
        serializer = self.serializer_class(object)
        return Response(serializer.data)
    

class MagazzinoArticoli(APIView):
    """
    Lista tutti gli articoli presenti in Magazzino

    """
    #queryset = Magazzino.objects.all()
    serializer_class = Articoliserializer
    #model = Magazzino
    
    def get(self,request):
        queryset = Magazzino.objects.all()
        tret=[]
        for one in queryset:
            a = one.articolo
            tret.append(a)
        
        ret = self.serializer_class(tret,many=True)
        return Response(ret.data)


    
