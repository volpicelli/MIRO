from django.db import models
from django.utils.translation import gettext_lazy as _
#from djmoney.models.fields import MoneyField


#Azienda ID: Identificativo (unico identificativo dell'azienda) Nome: String (nome dell'azienda) Descrizione: String (breve descrizione dell'azienda) Cantieri: Array[Cantieri] (lista di cantieri con chiave esterna di appartenenza all'azienda in questione) Lavoratori: Array[Lavoratori] (lista di lavoratori con chiave esterna di appartenenza all'azienda in questione) Fornitori: Array[Fornitori] (lista di fornitori con chiave esterna di appartenenza all'azienda in questione) Fatture: Array[Fatture] (lista di fatture con chiave esterna di appartenenza all'azienda in questione) Clienti: Array[Clienti] (lista di clienti con chiave esterna di appartenenza all'azienda in questione)

class Azienda(models.Model):
    nome = models.CharField(max_length=60, blank=True, null=True)
    descrizione = models.TextField(blank=True, null=True)
    #cantiere = models.ForeignKey(Cantiere,null=True,on_delete=models.CASCADE,related_name='cantieri_azienda')
    #personale = models.ForeignKey(Personale,null=True,on_delete=models.CASCADE,related_name='personale_azienda')
    #fornitore = models.ForeignKey(Fornitori,null=True,on_delete=models.CASCADE,related_name='fornitori_azienda')
    #fatture = models.ForeignKey(Fatture,null=True,on_delete=models.CASCADE,related_name='fatture_azienda')
    #cliente = models.ForeignKey(Cliente,null=True,on_delete=models.CASCADE,related_name='cliente_azienda')

    class Meta:
        managed = True
        db_table = 'azienda'


class TipologiaLavori(models.Model):
    #codice = models.CharField(max_length=40, blank=True, null=True)
    descrizione = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tipologia_lavori'


#Responsabile: Id : Identificativo Nome : String Telefono : String Email : String
"""
class Responsabile(models.Model):
    nome   = models.CharField(max_length=60, blank=True, null=True)
    telefono = models.CharField(max_length=40, blank=True, null=True)
    email = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'responsabile'

"""


#CODPAG;DESC;RATAIVA;TIPORATE;GGSCDFIX;TIPOPAG;NUMRATE;GG1RATA;GGRATE;TIPOSCAD;GGFIXANT;GGDOPOFM
class CondizioniPagamento(models.Model):
   # prova = models.ForeignKey(Fornitori,null=True,on_delete=models.CASCADE,to_field='codpag', related_name='prova',unique=True)
    #codpag = models.ForeignKey(Fornitori, on_delete=models.CASCADE)

    codpag = models.CharField(max_length=10,unique=True)
    desc = models.CharField(max_length=70, blank=True, null=True)
    rataiva = models.IntegerField(blank=True, null=True)
    tiporate = models.CharField(max_length=2,blank=True, null=True)
    ggscdfix = models.IntegerField(blank=True, null=True)
    tipopag = models.IntegerField(blank=True, null=True)
    numrate = models.IntegerField(blank=True, null=True)
    gg1rata = models.IntegerField(blank=True, null=True)
    ggrate = models.IntegerField(blank=True, null=True)
    tiposcad = models.CharField(max_length=3, blank=True, null=True)
    ggfixant = models.CharField(max_length=3, blank=True, null=True)
    ggdopofm = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'condizionipagamento'
    
#CLFR;CODCF;RAGSOC;RAGSOC1;INDIR;CAP;LOCAL;PROV;CODFISC;PARTIVA;CODPAG;PERSOC;TEL;TEL2;FAX;EMAIL;RESPRAP;FMEMO;NOME_PF;COGN_PF;SESSO;PEC_FE;BANCA

#Fornitore: ID: Identificativo Nome: String Indirizzo: String Email: String Numero di telefono: String IBAN: String Banca: String Descrizione: String Lavori: Lista di lavori forniti (es. Carpentiere, Manovale)

class Fornitori(models.Model):
    
    class ClienteFornitore(models.TextChoices):
        CLIENTE = "C"
        FORNITORE = "F"
    class Sesso(models.TextChoices):
        MASCHIO='M'
        FEMMINA='F'
    class PersonaSocieta(models.TextChoices):
        Persona='P'
        Societa='S'

#    clfr = models.CharField(max_length=2, choices=ClienteFornitore.choices,
#        default=ClienteFornitore.CLIENTE, blank=True, null=True)
    codcf = models.CharField(max_length=60, blank=True, null=True)
    ragione_sociale = models.CharField(max_length=100, blank=True, null=True)
    indirizzo = models.CharField(max_length=100,blank=True, null=True)
    cap = models.CharField(max_length=20,blank=True, null=True)
    local = models.CharField(max_length=40,blank=True, null=True)
    prov = models.CharField(max_length=40,blank=True, null=True)
    codfisc = models.CharField(max_length=40,blank=True, null=True)
    partiva = models.CharField(max_length=40,blank=True, null=True)
    descrizione = models.TextField(blank=True, null=True)
    #codpag = models.CharField(max_length=10, blank=True, default="", unique=True)
    codpag = models.ForeignKey(CondizioniPagamento,null=True,on_delete=models.CASCADE,related_name='pppp',to_field='codpag')
    persoc = models.CharField(max_length=2,blank=True, null=True,choices=PersonaSocieta.choices)

    telefono = models.CharField(max_length=40, blank=True, null=True)
    cellulare = models.CharField(max_length=40, blank=True, null=True)
    pec_fe = models.CharField(max_length=40, blank=True, null=True)
    fax = models.CharField(max_length=40, blank=True, null=True)
    email = models.CharField(max_length=40, blank=True, null=True)
    resprap = models.CharField(max_length=40, blank=True, null=True)
    fmemo = models.TextField( blank=True, null=True)
    nome_pf = models.CharField(max_length=40, blank=True, null=True)
    cogn_pf = models.CharField(max_length=40, blank=True, null=True)
    sesso = models.CharField(max_length=2, blank=True, null=True,choices=Sesso.choices)

    banca = models.CharField(max_length=40,blank=True, null=True)
    iban = models.CharField(max_length=40,blank=True, null=True)

   
    #responsabile = models.ForeignKey(Responsabile,null=True,on_delete=models.CASCADE,related_name='responsabile_fornitori')
    class Meta:
        managed = True
        db_table = 'fornitori'

class Sesso(models.TextChoices):
        MASCHIO='M'
        FEMMINA='F'

class Cliente(models.Model):
    class ClienteFornitore(models.TextChoices):
        CLIENTE = "C"
        FORNITORE = "F"
    
    class PersonaSocieta(models.TextChoices):
        Persona='P'
        Societa='S'

#    clfr = models.CharField(max_length=2, choices=ClienteFornitore.choices,
#        default=ClienteFornitore.CLIENTE, blank=True, null=True)
    codcf = models.CharField(max_length=60, blank=True, null=True)
    ragione_sociale = models.CharField(max_length=100, blank=True, null=True)
    indirizzo = models.CharField(max_length=100,blank=True, null=True)
    cap = models.CharField(max_length=20,blank=True, null=True)
    local = models.CharField(max_length=40,blank=True, null=True)
    prov = models.CharField(max_length=40,blank=True, null=True)
    codfisc = models.CharField(max_length=40,blank=True, null=True)
    partiva = models.CharField(max_length=40,blank=True, null=True)
    #descrizione = models.TextField(blank=True, null=True)
    #codpag = models.ForeignKey(CondizioniPagamento,null=True,on_delete=models.CASCADE,related_name='pppp',to_field='codpag')
    persoc = models.CharField(max_length=2,blank=True, null=True,choices=PersonaSocieta.choices)

    telefono = models.CharField(max_length=40, blank=True, null=True)
    cellulare = models.CharField(max_length=40, blank=True, null=True)
    pec_fe = models.CharField(max_length=40, blank=True, null=True)
    fax = models.CharField(max_length=40, blank=True, null=True)
    email = models.CharField(max_length=40, blank=True, null=True)
    #resprap = models.CharField(max_length=40, blank=True, null=True)
    fmemo = models.TextField( blank=True, null=True)
    nome_pf = models.CharField(max_length=40, blank=True, null=True)
    cogn_pf = models.CharField(max_length=40, blank=True, null=True)
    sesso = models.CharField(max_length=2, blank=True, null=True,choices=Sesso.choices)

    banca = models.CharField(max_length=40,blank=True, null=True)
    iban = models.CharField(max_length=40,blank=True, null=True)

    azienda = models.ForeignKey(Azienda,null=True,on_delete=models.CASCADE,related_name='azienda_cliente')

    class Meta:
        managed = True
        db_table = 'cliente'

    def getSesso(self):
        
        return getattr(self.Countries, self.name)

#Cantiere: ID: Identificativo Nome: String Descrizione: String Responsabile : Chiave esterna del responsabile del cantiere
#Data Inizio: Date Data Fine: Date Status: Boolean Fatture: Array[Fattura] (array di chiavi esterne delle fatture che hanno articoli facente parte del cantiere) Ordini: Array[Ordine] (array di chiavi esterne delle fatture che hanno articoli facente parte del cantiere) Lavoratori: Lista di oggetti Lavoratore ID: String Nome: String Cognome: String Lavoro: String Wage Lordo: String Wage Netto: String

class Cantiere(models.Model):
    nome   = models.CharField(max_length=40, blank=True, null=True)
    descrizione = models.TextField(blank=True, null=True)
    #responsabile = models.ForeignKey(Responsabile,null=True,on_delete=models.CASCADE,related_name='responsabile_cantiere')
    ubicazione = models.CharField(max_length=100, blank=True, null=True)
    #fatture = models.ForeignKey(Fatture,null=True,on_delete=models.CASCADE,related_name='fatture_cantiere')
    status = models.BooleanField(null=True)
    #ordine = models.ForeignKey(Ordine,null=True,on_delete=models.CASCADE,related_name='ordine_cantiere')
    #personale = models.ForeignKey(Personale,null=True,on_delete=models.CASCADE,related_name='personale_cantiere')
    #p_iva_cf = models.CharField(db_column='P.IVA_CF', max_length=40, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    valore_commessa =  models.DecimalField(max_digits=14,blank=True,null=True,decimal_places=2) #MoneyField(max_digits=14, decimal_places=2, default_currency='EUR')
    #valore_commessa = models.FloatField(  blank=True, null=True)
    data_inizio_lavori = models.DateField(blank=True, null=True)
    data_fine_lavori = models.DateField(blank=True, null=True)
    cliente = models.ForeignKey(Cliente,null=True,on_delete=models.CASCADE,related_name='cliente_cantiere')

    class Meta:
        managed = True
        db_table = 'cantiere'



class Personale(models.Model):
    
    nome = models.CharField(max_length=40, blank=True, null=True)
    cognome = models.CharField(max_length=40, blank=True, null=True)
    tipologia_lavoro = models.ForeignKey(TipologiaLavori,null=True,on_delete=models.CASCADE,related_name='tipolavoro_personale')
    responsabile = models.BooleanField(null=False,default=False)

    #cantiere = models.ForeignKey(Cantiere,null=True,on_delete=models.CASCADE,related_name='cantiere_personale')
    #assegnatocantiere = models.ForeignKey(Assegnato_Cantiere,null=True,on_delete=models.CASCADE,related_name='assegnato_personale')
    #lavoro  = models.CharField(max_length=40, blank=True, null=True)
    #wage_lordo = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR')
    #wage_netto = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR')
    wage_lordo = models.DecimalField(max_digits=19,blank=True,null=True,decimal_places=2) 
    wage_netto = models.DecimalField(max_digits=19,blank=True,null=True,decimal_places=2) 
    azienda = models.ForeignKey(Azienda,null=True,on_delete=models.CASCADE,related_name='azienda_personale')


    class Meta:
        managed = True
        db_table = 'personale'


class Assegnato_Cantiere(models.Model):
        personale = models.ForeignKey(Personale,null=True,on_delete=models.CASCADE,related_name='personale_assegnato')
        cantiere = models.ForeignKey(Cantiere,null=True,on_delete=models.CASCADE,related_name='cantiere_assegnato')
        responsabile = models.BooleanField(null=False,default=False)

        class Meta:
            unique_together = ('personale', 'cantiere')
            managed = True
            db_table = 'assegnato_cantiere'

#Ordine: ID: Identificativo Data Ordine: Date Fornitore: (Identificativo) Chiave esterna del fornitore da cui è stato effettuato ordine Articoli: Array[Articoli]

class Ordine(models.Model):
    class TipologiaFornitore(models.TextChoices):
        SERVIZIO = "SE",_("Servizio")
        MATERIALE = "MA",_("Materiale")
        MACCHINARI = "NO",_("Noleggio")


    data_ordine = models.DateField(blank=True, null=True)
    importo = models.DecimalField(max_digits=14,blank=True,null=True,decimal_places=2) #MoneyField(max_digits=14, decimal_places=2, default_currency='EUR',default=0.0)
    fornitore = models.ForeignKey(Fornitori,null=True,on_delete=models.CASCADE,related_name='fornitori_ordine')
    cantiere = models.ForeignKey(Cantiere,null=True,on_delete=models.CASCADE,related_name='cantiere_ordine')
    magazzino = models.BooleanField(null=False,default=False)
    tipologia = models.CharField(max_length=2, choices=TipologiaFornitore.choices,
        default=TipologiaFornitore.MATERIALE, blank=True, null=True)

    #articoli = models.ForeignKey(Articoli,null=True,on_delete=models.CASCADE,related_name='articoli_ordini')

    class Meta:
        managed = True
        db_table = 'ordine'



#Articolo ID : Identificativo Nome : String Descrizione : String Importo : Number

class Articoli(models.Model):
    #nome = models.CharField(max_length=60, blank=True, null=True)
    descrizione = models.TextField(blank=True, null=True)
    quantita = models.IntegerField(blank=True, null=True)
    importo = models.DecimalField(max_digits=19,blank=True,null=True,decimal_places=2) #MoneyField(max_digits=14, decimal_places=2, default_currency='EUR')
    ordine = models.ForeignKey(Ordine,null=True,on_delete=models.CASCADE,related_name='ordine_articoli')


    class Meta:
        managed = True
        db_table = 'articoli'

class Magazzino(models.Model):
    articolo = models.ForeignKey(Articoli,null=True,on_delete=models.CASCADE,related_name='magazzino_articoli')
    #ordine = models.ForeignKey(Ordine,null=True,on_delete=models.CASCADE,related_name='ordine_magazzino')
    quantita = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'magazzino'




#Fattura: ID: Identificativo Numero Fattura Fornitore: Number Fornitore: chiave esterna fornitore Data Fattura: Date Data Scadenza: Date Importo: Number Pagato: Number Cantiere: Array[Cantiere] chiave esterna per tutti i cantieri a cui quella fattura fa riferimento ( molteplici perchè possibilità di scorporare ) Articoli: Array[Articoli] Ordine di rif.: Ordine

class Fatture(models.Model):
    ragione_sociale = models.CharField(max_length=100, blank=True, null=True)
    #fornitore = models.ForeignKey(Fornitori,null=True,on_delete=models.CASCADE,related_name='fornitori_fatture')
    n_fattura = models.CharField(db_column='n.fattura', max_length=40, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    data_fattura = models.DateField(blank=True, null=True)
    importo =  models.DecimalField(max_digits=14,blank=True,null=True,decimal_places=2)#MoneyField(max_digits=14, decimal_places=2, default_currency='EUR')
    pagato =  models.DecimalField(max_digits=14,blank=True,null=True,decimal_places=2)#MoneyField(max_digits=14, decimal_places=2, default_currency='EUR')
    data_scadenza = models.DateField(blank=True, null=True)
    ##cantiere = models.ForeignKey(Cantiere,null=True,on_delete=models.CASCADE,related_name='cantiere_fatture')
    #articoli = models.ForeignKey(Articoli,null=True,on_delete=models.CASCADE,related_name='articoli_fatture')
    ordine = models.ForeignKey(Ordine,null=True,on_delete=models.CASCADE,related_name='ordine_fatture')

    class Meta:
        managed = True
        db_table = 'fatture'

 #Cliente: Lista di oggetti Cliente ID: String Nome: String Cognome: String Indirizzo: String Data di nascita: Date Numero di telefono: String Banca: String IBAN: String







