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
from home.models import Cantiere,Articoli,Fatture,Fornitori,Ordine,Personale,TipologiaLavori,Assegnato_Cantiere,Magazzino,\
                        Documenti

import json
from django.db.models import Sum
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                       context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        all = user.userazienda.all()
        azn= []
        azid = []
        for one in all:
            azn.append( one.azienda.nome )
            azid.append( one.azienda.id)
            request.session['azienda']=one.azienda.id
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'azienda_name': azn,
            'azienda_id' : azid,
            'email': user.email
        })

class LoginView(APIView):
    #authentication_classes = [TokenAuthentication]

    def post(self, request):
        # Your authentication logic here
        return Response({'user': request.POST.get('username'),'pasword': request.POST.get('password')})

        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=401)

class AddOreLavoro(APIView):
    serializer_class = Assegnato_CantiereSerializer

    def get(self,request,cantiere_id,personale_id,ore):

        #return Response(ore)
    
        try:
            ac = Assegnato_Cantiere.objects.get(cantiere=cantiere_id,personale=personale_id)
            ac.ore_lavorate = ac.ore_lavorate + ore
            ac.save()

        except ObjectDoesNotExist:
            c = Cantiere.objects.get(pk=cantiere_id)
            p = Personale.objects.get(pk=personale_id)

            ac=Assegnato_Cantiere(cantiere=c,personale=p,ore_lavorate=ore)
            ac.save()
        serialzer = self.serializer_class(ac)

        return Response(serialzer.data)



class ResponsabileCantiere(APIView):
    serializer_class = Personaleserializer
    #permission_classes = [IsAuthenticated]


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


class CantieriPersonale(APIView):
    serializer_class = Cantiereserializer

    def get(self,request,id_personale):
        ret=[]
        try:
            p = Personale.objects.get(pk=id_personale)
            
        except ObjectDoesNotExist:
            ret.append({'Error': "Personale {} non esiste".format(id_personale)})
            return Response(ret)
        
        pac = p.personale_assegnato.all()
        
        for one in pac:
            c = one.cantiere
            s = self.serializer_class(c)
            ret.append(s.data)

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
                "ore_lavorate": one.ore_lavorate,
                "responsabile" : one.responsabile,
                "cantiere": one.cantiere_id
                }
            ret.append(o)

        return Response(ret)
        
        
        #serializer = self.serializer_class(pers,many=True)

        #return Response(serializer.data)







class FattureOrdine(APIView):
    serializer_class = Fattureserializer
    def get(self,request,ordine_id):
        fatture = Fatture.objects.filter(ordine_id=ordine_id)
        serializer = self.serializer_class(fatture,many=True)
        return Response(serializer.data)
 
class FattureList(generics.ListCreateAPIView):
    queryset = Fatture.objects.all()
    serializer_class = Fattureserializer
    #permission_classes = [IsAuthenticated]

    

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
    #permission_classes = [IsAuthenticated]


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
        #user = request.user.last_name
        ##ss={}
        #ss['q']=serializer.data
        #ss['user']=user
        return Response(serializer.data)


class OrdineGetTipologia(APIView):
    def get(self,request):
        o = Ordine.tipologia.field.choices
        return Response(o)


class OrdineCreate(APIView):
    """
    json={'fornitore':2,
        'cantiere':16,
        'tipologia':'NO',
        'data_ordine':'2026-5-23',
        'damagazzino': false,
        'permagazzino': false,
        'articoli':[{'id':1,'descrizione': 'mattoni 40x40','quantita': 230,'prezzo_unitario':0.34,'preleva':12},
                    {'id': 2,'descrizione': ' seconda ','quantita': 12,'prezzo_unitario': 12.4,'preleva':4}
                    ]}

    """
    def post(self,request):
        data = json.loads(request.body)
        #return Response(data)
        # If data['permagazzino'] == True
        # Ordine da fornitore esterno per riempire il magazzino

        # if data['damagazzino'] == True
        # ordine per un cantiere con materiale preso dal Magazzino

        # data['permagazzino'] == False e data['damagazzino'] == False
        # Ordine normale da fornitore per un cantiere

        # Tipologia qualsiasi
        #if data['magazzino'] is not True and data['mestesso'] is not True:
        damagazzino = False
        if 'damagazzino' not in data or data['damagazzino'] == False:
        
            try:
                f = Fornitori.objects.get(pk=data['fornitore'])
            except ObjectDoesNotExist:
                error_msg=" Fornitore non esiste"
                return Response(error_msg)#,safe=False)
        else:
            damagazzino = True
            try:
                f = Fornitori.objects.get(pk=data['fornitore'])
            except ObjectDoesNotExist:
                error_msg=" Fornitore non esiste"
                return Response(error_msg)

        permagazzino = False
        if 'permagazzino' not in data or data['permagazzino']== False:

            try:
                c  = Cantiere.objects.get(pk=data['cantiere'])
            except ObjectDoesNotExist:
                error_msg=" Cantiere non esiste"
                return Response(error_msg)#,safe=False)
        else:
            c=None
            permagazzino=True
        #if 'damagazzino' in data or data['damagazzino']== True:

# Ordine.TipologiaFornitore.choices
# [('SE', 'Servizio'), ('MA', 'Materiale'), ('NO', 'Noleggio')]
        #try:
        #    t  = TipologiaLavori.objects.get(pk=data['tipologia'])
        #except ObjectDoesNotExist:
        #    error_msg=" Tipologia non esiste"
        #    return Response(error_msg)#,safe=False)
        o = Ordine( cantiere=c,
                    fornitore=f,
                    data_ordine=data['data_ordine'],
                    data_consegna = data['data_consegna'],
                    #importo=data['importo'],
                    permagazzino=permagazzino,
                    damagazzino= damagazzino, #data['mestesso'],
                    tipologia= data['tipologia'], #t.id #data['tipologia']
                    azienda=f.azienda
                    )
        o.save()
        importo = 0.0
        # Preleva materiale dal Magazzino
        if damagazzino: # not in data or data['damagazzino'] == False:
            for one in data['articoli']:
                a = Articoli()
                a.ordine=o
                a.descrizione=one['descrizione']
                a.quantita = one['preleva']
                a.prezzo_unitario = one['prezzo_unitario']
                a.importo_totale = int(one['preleva']) * float(one['prezzo_unitario'])
                importo += a.importo_totale
                a.save()
                m = Magazzino.objects.get(pk=one['id'])
                m.quantita = m.quantita - a.quantita
                m.save()
            o.importo = importo
            o.save()
            """
            else: 
                for one in data['articoli']:
                    a = Articoli()
                    a.ordine=o
                    a.descrizione=one['descrizione']
                    a.quantita = one['quantita']
                    a.prezzo_unitario = one['prezzo_unitario']
                    a.importo_totale = int(one['quantita']) * float(one['prezzo_unitario'])
                    importo += a.importo_totale
                    a.save()
                o.importo = importo
                o.save()
                """
            # Ordina  materiale per il  Magazzino
        elif permagazzino: 
            for one in data['articoli']:
                a = Articoli()
                a.ordine=o
                a.descrizione=one['descrizione']
                a.quantita = one['quantita']
                a.prezzo_unitario = one['prezzo_unitario']
                a.importo_totale = int(one['quantita']) * float(one['prezzo_unitario'])
                importo += a.importo_totale
                a.save()
                try:
                    m = Magazzino.objects.get(descrizione=one['descrizione'])
                    #if m.exists():
                    m.quantita = m.quantita+a.quantita
                    m.prezzo_unitario = (m.prezzo_unitario + a.prezzo_unitario)/2
                    m.save()
                except:
                    m = Magazzino()
                    m.descrizione = a.descrizione
                    m.quantita = a.quantita
                    m.prezzo_unitario = a.prezzo_unitario
                    m.importo_totale = a.importo_totale
                    m.ordine=o
                    m.azienda=f.azienda
                    m.save()
            o.importo = importo
            o.save()
        
        else: 
            for one in data['articoli']:
                a = Articoli()
                a.ordine=o
                a.descrizione=one['descrizione']
                a.quantita = one['quantita']
                a.prezzo_unitario = one['prezzo_unitario']
                a.importo_totale = int(one['quantita']) * float(one['prezzo_unitario'])
                importo += a.importo_totale
                a.save()
            o.importo = importo
            o.save()
        
        
        os = Ordineserializer(o)
        return Response(os.data)#,safe=False)

        #    os = Ordineserializer(o)



class OrdineDaMagazzino(APIView):
    #permission_classes = [IsAuthenticated]

    def get(sef,request):
        m = Magazzino.objects.all()
            #data['articoli']=[]
        tmp = []
        ret={}
        for one in m:
            tmp.append(one)
        
        ms = Magazzinoserializer(tmp,many=True)
        ret['articoli']= ms.data
        #os.data['articoli']=ms
            
        return Response(ret)

    def post(self,request):
        data = json.loads(request.body)
        

        if data['mestesso']:
            try:
                f = Fornitori.objects.get(pk=data['fornitore']) # Fornitore questa azienda
            except ObjectDoesNotExist:
                error_msg=" Fornitore non esiste"

            o = Ordine( #cantiere=c,
                        fornitore=f,
                        data_ordine=data['data_ordine'],
                        importo=data['importo'],
                        #magazzino=False,
                        mestesso=True, #data['mestesso'],
                        tipologia='MA'
                        )
            o.save()
            os = Ordineserializer(o)
            os.data['POLLO'] = "POLLO"
            ret={}
            ret = os.data
            m = Magazzino.objects.all()
            #data['articoli']=[]
            tmp = []
            for one in m:
                tmp.append(one)
            
            ms = Magazzinoserializer(tmp,many=True)
            ret['articoli']= ms.data
            #os.data['articoli']=ms
                
        return Response(ret)

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


class GroupMagazzino(APIView):
    def get(self,request):
        articolimag = Magazzino.objects.values('descrizione').annotate(totale=Sum('importo_totale'),quantita=Sum('quantita'))
        res=[]
        for one in articolimag:
            a={}
            a['descrizione']=one['descrizione']
            a['importo_totale'] = one['totale']
            a['quantita'] = one['quantita']
            res.append(a)

        return Response(res  )

class MagazzinoList(generics.ListCreateAPIView):
    queryset = Magazzino.objects.all()
    serializer_class = Magazzinoserializer

class MagazzinoDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Magazzino.objects.all()
    serializer_class = Magazzinoserializer
     
    def destroy(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Magazzino.objects.get(pk=pk).delete() #kwargs['pk'])
        #object.magazzino = False
        #serializer = self.serializer_class(object)
        return Response({'Msg':'OK '+str(pk) +' Non piu in magazzino'})

    
class MagazzinoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Magazzino.objects.all()
    serializer_class = Magazzinoserializer
     
    def destroy(self, request, pk,*args, **kwargs):
        #pk = self.kwargs.get('pk')
        object = Magazzino.objects.get(pk=pk).delete() #kwargs['pk'])
        #object.magazzino = False
        #serializer = self.serializer_class(object)
        return Response({'Msg':'OK '+str(pk) +' Non piu in magazzino'})

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
            ret = self.serializer_class(a)
            
            o = a.ordine
            os = Ordineserializer(o)
            ret.data['ordine']= os.data

            tret.append(ret)


        
        #ret = self.serializer_class(tret,many=True)
        #ret.data[0]['ordine']= os.data
        return Response(tret)


    
