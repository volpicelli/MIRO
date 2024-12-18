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
#from .responsabile_serializer import Responsabileserializer
from .tipologialavori_serializer import TipologiaLavoriSerializer
from .assegnato_cantiere_serializer import Assegnato_CantiereSerializer

#from .lavorieffettuatifornitori_serializer import LavoriEffettuatiFornitoriserializer
#from .lavorieffettuatipersonale_serializer import LavoriEffettuatiPersonaleserializer
#from .tipologiapersonale_serializer import TipologiaPersonaleserializer
#from moneyed import Money
# Create your views here.
from home.models import Cantiere,Articoli,Azienda,Cliente,Fatture,Fornitori,Ordine,Personale,TipologiaLavori,Assegnato_Cantiere,Magazzino


class ResponsabileCantiere(APIView):
    serializer_class = Personaleserializer

    def get(self,request,id_cantiere):
        ret=[]
        try:
            ac = Assegnato_Cantiere.objects.get(cantiere=id_cantiere,responsabile=True)
            
        except ObjectDoesNotExist:
            ret.append({'Warning': "Sul Cantiere {}  Responsabile non assegnato".format(id_cantiere)})
            return Response(ret)
        
        c = ac.personale  #_assegnato.all()

        #for one in c:
        #p={}
        p ={ "id": c.id,
                "nome": c.nome,
                "cognome": c.cognome,
                "wage_lordo" : c.wage_lordo,
                "wage_netto" : c.wage_netto
        }
            #ret.append(p)
        return Response(p)
"""
    def get(self,request,id_cantiere):
        a = Assegnato_Cantiere.objects.get(cantiere=id_cantiere,responsabile=True)
        #a = o.ordine_articoli.all()
        serializer = self.serializer_class(a.personale,many=True)
        return Response(serializer.data)
"""


class Assegnato_CantiereList(generics.ListCreateAPIView):
    queryset = Assegnato_Cantiere.objects.all()
    serializer_class = Assegnato_CantiereSerializer
    cognome = ""
    cantiere = ""

    def post(self, request, *args, **kwargs):
        personale = request.POST['personale']
        cantiere = request.POST['cantiere']
        p = Personale.objects.get(pk=personale)
        #c = Cantiere.objects.get(pk=cantiere)
        self.cognome  = p.cognome
        self.cantiere = cantiere
        return self.create(request, *args, **kwargs)

    def handle_exception(self, exc):
        """
        Handle any exception that occurs, by returning an appropriate response,
        or re-raising the error.
        """
        if isinstance(exc, (exceptions.NotAuthenticated,
                            exceptions.AuthenticationFailed)):
            # WWW-Authenticate header for 401 responses, else coerce to 403
            auth_header = self.get_authenticate_header(self.request)

            if auth_header:
                exc.auth_header = auth_header
            else:
                exc.status_code = status.HTTP_403_FORBIDDEN

        exception_handler = self.get_exception_handler()

        context = self.get_exception_handler_context()
        #context="POLLO"
        response = exception_handler(exc, context)

        if response is None:
            self.raise_uncaught_exception(exc)

        response.exception = True
        response.data.pop('non_field_errors')
        response.data["warning"]="Personale {} gia assegnato al cantiere {}".format(self.cognome.upper(),self.cantiere)
        return response


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
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

class ClientePersoc(APIView):
    def get(self,request):
        c = Cliente.persoc.field.choices
    
        return Response(c)
 
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


class OrdineGetTipologia(APIView):
    def get(self,request):
        o = Ordine.tipologia.field.choices
        return Response(o)

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

"""
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

"""
class MagazzinoList(generics.ListCreateAPIView):
    queryset = Ordine.objects.filter(magazzino=True)
    serializer_class = Ordineserializer

class MagazzinoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ordine.objects.filter(magazzino=True)
    serializer_class = Ordineserializer
    
    def destroy(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Ordine.objects.get(pk=pk) #.delete() #kwargs['pk'])
        object.magazzino = False
        serializer = self.serializer_class(object)
        return Response({'Msg':'OK '+str(pk) +' Non piu in magazzino'})

    def retrieve(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Ordine.objects.get(pk=pk) #kwargs['pk'])
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


    
