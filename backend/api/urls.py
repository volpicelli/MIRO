
from django.urls import path
from api.views import ArticoliDetail,ArticoliList, AziendaDetail,AziendaList,CantiereDetail,CantiereList,\
                        ClienteDetail,ClienteList,FattureDetail,FattureList,FornitoriDetail,FornitoriList,\
                        OrdineDetail,OrdineList,PersonaleDetail,PersonaleList,ResponsabileDetail,ResponsabileList,ResponsabileCantiere,\
                        ArticoliOrdine,OrdiniCantiere,TipologiaLavoriList,TipologiaLavoriDetail,Assegnato_CantiereList,Assegnato_CantiereDetail,\
                        PersonaleSuCantiere,MagazzinoList,MagazzinoDetail,MagazzinoArticoli,CantieriPersonale
                

urlpatterns = [ 

        path('personale/cantiere/<int:id_cantiere>',PersonaleSuCantiere.as_view()),
        path('cantieri/personale/<int:id_personale>',CantieriPersonale.as_view()),
        path('assegnatocantiere/list', Assegnato_CantiereList.as_view()),
        path('assegnatocantiere/create', Assegnato_CantiereList.as_view()),
        path('assegnatocantiere/detail/<int:pk>', Assegnato_CantiereDetail.as_view()),
        path('assegnatocantiere/delete/<int:pk>', Assegnato_CantiereDetail.as_view()),
        path('assegnatocantiere/update/<int:pk>', Assegnato_CantiereDetail.as_view()),


        path('tipologialavori/list', TipologiaLavoriList.as_view()),
        path('tipologialavori/create', TipologiaLavoriList.as_view()),
        path('tipologialavori/detail/<int:pk>', TipologiaLavoriDetail.as_view()),
        path('tipologialavori/delete/<int:pk>', TipologiaLavoriDetail.as_view()),
        path('tipologialavori/update/<int:pk>', TipologiaLavoriDetail.as_view()),

        path('fornitori/list', FornitoriList.as_view()),
        path('fornitori/create', FornitoriList.as_view()),
        path('fornitori/detail/<int:pk>', FornitoriDetail.as_view()),
        path('fornitori/delete/<int:pk>', FornitoriDetail.as_view()),
        path('fornitori/update/<int:pk>', FornitoriDetail.as_view()),

        path('personale/list', PersonaleList.as_view()),
        path('personale/create', PersonaleList.as_view()),
        path('personale/detail/<int:pk>', PersonaleDetail.as_view()),
        path('personale/delete/<int:pk>', PersonaleDetail.as_view()),
        path('personale/update/<int:pk>', PersonaleDetail.as_view()),

        path('magazzino/list', MagazzinoList.as_view()),
        path('magazzino/create', MagazzinoList.as_view()),
        path('magazzino/detail/<int:pk>', MagazzinoDetail.as_view()),
        path('magazzino/delete/<int:pk>', MagazzinoDetail.as_view()),
        path('magazzino/update/<int:pk>', MagazzinoDetail.as_view()),
        path('magazzino/articoli', MagazzinoArticoli.as_view()),


        path('cantieri/list', CantiereList.as_view()),
        path('cantiere/create', CantiereList.as_view()),
        path('cantiere/detail/<int:pk>',CantiereDetail.as_view()),
        path('cantiere/delete/<int:pk>', CantiereDetail.as_view()),
        path('cantiere/update/<int:pk>',CantiereDetail.as_view()),
        path('cantiere/<int:cantiere_id>/ordini',OrdiniCantiere.as_view()),



        path('articoli/list', ArticoliList.as_view()),
        path('articoli/create',ArticoliList.as_view()),
        path('articoli/detail/<int:pk>',ArticoliDetail.as_view()),
        path('articoli/delete/<int:pk>', ArticoliDetail.as_view()),
        path('articoli/update/<int:pk>',ArticoliDetail.as_view()),

        path('articoli/ordine/<int:id_ordine>',ArticoliOrdine.as_view()),
        
        path('azienda/list', AziendaList.as_view()),
        path('azienda/create',AziendaList.as_view()),
        path('azienda/detail/<int:pk>',AziendaDetail.as_view()),
        path('azienda/delete/<int:pk>', AziendaDetail.as_view()),
        path('azienda/update/<int:pk>',AziendaDetail.as_view()),

        path('cliente/list', ClienteList.as_view()),
        path('cliente/create',ClienteList.as_view()),
        path('cliente/detail/<int:pk>',ClienteDetail.as_view()),
        path('cliente/delete/<int:pk>', ClienteDetail.as_view()),
        path('cliente/update/<int:pk>',ClienteDetail.as_view()),

        path('fatture/list', FattureList.as_view()),
        path('fatture/create',FattureList.as_view()),
        path('fatture/detail/<int:pk>',FattureDetail.as_view()),
        path('fatture/delete/<int:pk>', FattureDetail.as_view()),
        path('fatture/update/<int:pk>',FattureDetail.as_view()),

        path('ordine/list', OrdineList.as_view()),
        path('ordine/create',OrdineList.as_view()),
        path('ordine/detail/<int:pk>',OrdineDetail.as_view()),
        path('ordine/delete/<int:pk>', OrdineDetail.as_view()),
        path('ordine/update/<int:pk>',OrdineDetail.as_view()),
        #path('ordine/<int:ordine_id>/articoli',ArticoliOrdine.as_view()),
        
        path('ordini/cantiere/<int:id_cantiere>',OrdiniCantiere.as_view()),



        path('responsabile/list', ResponsabileList.as_view()),
        path('responsabile/create',ResponsabileList.as_view()),
        path('responsabile/detail/<int:pk>',ResponsabileDetail.as_view()),
        path('responsabile/delete/<int:pk>', ResponsabileDetail.as_view()),
        path('responsabile/update/<int:pk>',ResponsabileDetail.as_view()),

        path('responsabile/cantiere/<int:id_cantiere>',ResponsabileCantiere.as_view()),


]
    
