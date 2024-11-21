from django.db import models
#from djmoney.models.fields import MoneyField


class TipologiaLavori(models.Model):
    #codice = models.CharField(max_length=40, blank=True, null=True)
    descrizione = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tipologia_lavori'


#Responsabile: Id : Identificativo Nome : String Telefono : String Email : String

class Responsabile(models.Model):
    nome   = models.CharField(max_length=60, blank=True, null=True)
    telefono = models.CharField(max_length=40, blank=True, null=True)
    email = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'responsabile'






#Fornitore: ID: Identificativo Nome: String Indirizzo: String Email: String Numero di telefono: String IBAN: String Banca: String Descrizione: String Lavori: Lista di lavori forniti (es. Carpentiere, Manovale)

class Fornitori(models.Model):
    nome = models.CharField(max_length=60, blank=True, null=True)
    indirizzo = models.TextField(blank=True, null=True)
    descrizione = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=40, blank=True, null=True)
    p_iva_cf = models.CharField(max_length=40, blank=True, null=True)
    pec = models.CharField(max_length=40, blank=True, null=True)
    email = models.CharField(max_length=40, blank=True, null=True)
    banca = models.CharField(max_length=40,blank=True, null=True)
    iban = models.CharField(max_length=40,blank=True, null=True)
    responsabile = models.ForeignKey(Responsabile,null=True,on_delete=models.CASCADE,related_name='responsabile_fornitori')
    class Meta:
        managed = True
        db_table = 'fornitori'




#Cantiere: ID: Identificativo Nome: String Descrizione: String Responsabile : Chiave esterna del responsabile del cantiere
#Data Inizio: Date Data Fine: Date Status: Boolean Fatture: Array[Fattura] (array di chiavi esterne delle fatture che hanno articoli facente parte del cantiere) Ordini: Array[Ordine] (array di chiavi esterne delle fatture che hanno articoli facente parte del cantiere) Lavoratori: Lista di oggetti Lavoratore ID: String Nome: String Cognome: String Lavoro: String Wage Lordo: String Wage Netto: String

class Cantiere(models.Model):
    nome   = models.CharField(max_length=40, blank=True, null=True)
    descrizione = models.TextField(blank=True, null=True)
    responsabile = models.ForeignKey(Responsabile,null=True,on_delete=models.CASCADE,related_name='responsabile_cantiere')
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

    class Meta:
        managed = True
        db_table = 'cantiere'



class Personale(models.Model):
    
    nome = models.CharField(max_length=40, blank=True, null=True)
    cognome = models.CharField(max_length=40, blank=True, null=True)
    tipologia_lavoro = models.ForeignKey(TipologiaLavori,null=True,on_delete=models.CASCADE,related_name='tipolavoro_personale')
    cantiere = models.ForeignKey(Cantiere,null=True,on_delete=models.CASCADE,related_name='cantiere_personale')
    #assegnatocantiere = models.ForeignKey(Assegnato_Cantiere,null=True,on_delete=models.CASCADE,related_name='assegnato_personale')
    #lavoro  = models.CharField(max_length=40, blank=True, null=True)
    #wage_lordo = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR')
    #wage_netto = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR')
    wage_lordo = models.DecimalField(max_digits=19,blank=True,null=True,decimal_places=2) 
    wage_netto = models.DecimalField(max_digits=19,blank=True,null=True,decimal_places=2) 

    class Meta:
        managed = True
        db_table = 'personale'


class Assegnato_Cantiere(models.Model):
        personale = models.ForeignKey(Personale,null=True,on_delete=models.CASCADE,related_name='personale_assegnato')
        cantiere = models.ForeignKey(Cantiere,null=True,on_delete=models.CASCADE,related_name='cantiere_assegnato')
        class Meta:
            managed = True
            db_table = 'assegnato_cantiere'
#Ordine: ID: Identificativo Data Ordine: Date Fornitore: (Identificativo) Chiave esterna del fornitore da cui è stato effettuato ordine Articoli: Array[Articoli]

class Ordine(models.Model):
    data_ordine = models.DateField(blank=True, null=True)
    importo = models.DecimalField(max_digits=14,blank=True,null=True,decimal_places=2) #MoneyField(max_digits=14, decimal_places=2, default_currency='EUR',default=0.0)
    fornitore = models.ForeignKey(Fornitori,null=True,on_delete=models.CASCADE,related_name='fornitori_ordine')
    cantiere = models.ForeignKey(Cantiere,null=True,on_delete=models.CASCADE,related_name='cantiere_ordine')

    #articoli = models.ForeignKey(Articoli,null=True,on_delete=models.CASCADE,related_name='articoli_ordini')

    class Meta:
        managed = True
        db_table = 'ordine'



#Articolo ID : Identificativo Nome : String Descrizione : String Importo : Number

class Articoli(models.Model):
    nome = models.CharField(max_length=60, blank=True, null=True)
    descrizione = models.TextField(blank=True, null=True)
    quantita = models.IntegerField(blank=True, null=True)
    importo = models.DecimalField(max_digits=19,blank=True,null=True,decimal_places=2) #MoneyField(max_digits=14, decimal_places=2, default_currency='EUR')
    ordine = models.ForeignKey(Ordine,null=True,on_delete=models.CASCADE,related_name='ordine_articoli')


    class Meta:
        managed = True
        db_table = 'articoli'

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

class Cliente(models.Model):
    nome = models.CharField(max_length=60, blank=True, null=True)
    cognome = models.CharField(max_length=60, blank=True, null=True)
    indirizzo = models.TextField( blank=True, null=True)
    data_nascita = models.DateField(blank=True, null=True)
    numero_tel = models.CharField(max_length=40, blank=True, null=True)
    banca = models.CharField(max_length=60, blank=True, null=True)
    iban = models.CharField(max_length=60, blank=True, null=True)
    cantiere = models.ForeignKey(Cantiere,null=True,on_delete=models.CASCADE,related_name='cantiere_cliente')

    class Meta:
        managed = True
        db_table = 'cliente'



#Azienda ID: Identificativo (unico identificativo dell'azienda) Nome: String (nome dell'azienda) Descrizione: String (breve descrizione dell'azienda) Cantieri: Array[Cantieri] (lista di cantieri con chiave esterna di appartenenza all'azienda in questione) Lavoratori: Array[Lavoratori] (lista di lavoratori con chiave esterna di appartenenza all'azienda in questione) Fornitori: Array[Fornitori] (lista di fornitori con chiave esterna di appartenenza all'azienda in questione) Fatture: Array[Fatture] (lista di fatture con chiave esterna di appartenenza all'azienda in questione) Clienti: Array[Clienti] (lista di clienti con chiave esterna di appartenenza all'azienda in questione)

class Azienda(models.Model):
    nome = models.CharField(max_length=60, blank=True, null=True)
    descrizione = models.TextField(blank=True, null=True)
    cantiere = models.ForeignKey(Cantiere,null=True,on_delete=models.CASCADE,related_name='cantieri_azienda')
    personale = models.ForeignKey(Personale,null=True,on_delete=models.CASCADE,related_name='personale_azienda')
    #fornitore = models.ForeignKey(Fornitori,null=True,on_delete=models.CASCADE,related_name='fornitori_azienda')
    #fatture = models.ForeignKey(Fatture,null=True,on_delete=models.CASCADE,related_name='fatture_azienda')
    cliente = models.ForeignKey(Cliente,null=True,on_delete=models.CASCADE,related_name='cliente_azienda')

    class Meta:
        managed = True
        db_table = 'azienda'


"""

class AnagraficaFornitori(models.Model):
    codice = models.CharField(max_length=40, blank=True, null=True)
    descrizione = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=40, blank=True, null=True)
    pec = models.CharField(max_length=40, blank=True, null=True)
    email = models.CharField(max_length=40, blank=True, null=True)
    tipo_pagamento = models.CharField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'anagrafica_fornitori'


class AnagraficaPersonale(models.Model):
    
    codice = models.CharField(max_length=40, blank=True, null=True)
    nome = models.CharField(max_length=40, blank=True, null=True)
    cognome = models.CharField(max_length=40, blank=True, null=True)
    costo_orario_lordo = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR')
    costo_orario_netto = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR')

    class Meta:
        managed = True
        db_table = 'anagrafica_personale'




class TipologiaLavori(models.Model):
    codice = models.CharField(max_length=40, blank=True, null=True)
    descrizione = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tipologia_lavori'

class LavoriEffettuatiFornitori(models.Model):
    fornitore = models.ForeignKey(AnagraficaFornitori,null=True,on_delete=models.CASCADE,related_name='fornitore')
    n_fattura = models.CharField(db_column='n.fattura', max_length=40, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    data_fattura = models.DateField(blank=True, null=True)
    importo = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR')
    scadenza = models.DateField(blank=True, null=True)
    tipologia_lavori = models.ForeignKey(TipologiaLavori,null=True,on_delete=models.CASCADE,related_name='lavori_fornitore_tipologia')

    #cantiere = models.CharField(blank=True, null=True)
    cantiere = models.ForeignKey(Cantiere,null=True,on_delete=models.CASCADE,related_name='lavori_fornitore_cantiere')

    class Meta:
        managed = True
        db_table = 'lavori_effettuati_fornitori'


class LavoriEffettuatiPersonale(models.Model):
    #personale = models.CharField(blank=True, null=True)
    n_ore = models.FloatField(db_column='n.ore', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    tipologia_personale = models.CharField(blank=True, null=True)
    cantiere = models.ForeignKey(Cantiere,null=True,on_delete=models.CASCADE,related_name='lavori_personale_cantiere')
    personale = models.ForeignKey(AnagraficaPersonale,null=True,on_delete=models.CASCADE,related_name='lavori_personale_personale')

    class Meta:
        managed = True
        db_table = 'lavori_effettuati_personale'





class TipologiaPersonale(models.Model):
    codice = models.CharField(max_length=40, blank=True, null=True)
    descrizione = models.TextField(blank=True, null=True)
    personale = models.ForeignKey(AnagraficaPersonale,null=True,on_delete=models.CASCADE,related_name='tipologia_personale_personale')

    class Meta:
        managed = True
        db_table = 'tipologia_personale'
"""
"""
AAAAAAAAAAAA

from django.db import models
from djmoney.models.fields import MoneyField



#Responsabile: Id : Identificativo Nome : String Telefono : String Email : String

class Responsabile(models.Model):
    nome   = models.CharField(max_length=60, blank=True, null=True)
    telefono = models.CharField(max_length=40, blank=True, null=True)
    email = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'responsabile'


class Personale(models.Model):
    
    nome = models.CharField(max_length=40, blank=True, null=True)
    cognome = models.CharField(max_length=40, blank=True, null=True)
    lavoro  = models.CharField(max_length=40, blank=True, null=True)
    wage_lordo = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR')
    wage_netto = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR')

    class Meta:
        managed = True
        db_table = 'personale'
#Fornitore: ID: Identificativo Nome: String Indirizzo: String Email: String Numero di telefono: String IBAN: String Banca: String Descrizione: String Lavori: Lista di lavori forniti (es. Carpentiere, Manovale)

class Fornitori(models.Model):
    nome = models.CharField(max_length=60, blank=True, null=True)
    indirizzo = models.TextField(blank=True, null=True)
    descrizione = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=40, blank=True, null=True)
    p_iva_cf = models.CharField(max_length=40, blank=True, null=True)
    pec = models.CharField(max_length=40, blank=True, null=True)
    email = models.CharField(max_length=40, blank=True, null=True)
    banca = models.CharField(max_length=40,blank=True, null=True)
    iban = models.CharField(max_length=40,blank=True, null=True)
    responsabile = models.ForeignKey(Responsabile,null=True,on_delete=models.CASCADE,related_name='responsabile_fornitori')
    class Meta:
        managed = True
        db_table = 'fornitori'










#Cantiere: ID: Identificativo Nome: String Descrizione: String Responsabile : Chiave esterna del responsabile del cantiere
#Data Inizio: Date Data Fine: Date Status: Boolean Fatture: Array[Fattura] (array di chiavi esterne delle fatture che hanno articoli facente parte del cantiere) Ordini: Array[Ordine] (array di chiavi esterne delle fatture che hanno articoli facente parte del cantiere) Lavoratori: Lista di oggetti Lavoratore ID: String Nome: String Cognome: String Lavoro: String Wage Lordo: String Wage Netto: String

class Cantiere(models.Model):
    nome   = models.CharField(max_length=40, blank=True, null=True)
    descrizione = models.TextField(blank=True, null=True)
    responsabile = models.ForeignKey(Responsabile,null=True,on_delete=models.CASCADE,related_name='responsabile_cantiere')
    ubicazione = models.CharField(max_length=100, blank=True, null=True)
    #fatture = models.ForeignKey(Fatture,null=True,on_delete=models.CASCADE,related_name='fatture_cantiere')
    status = models.BooleanField(null=True)
    #ordine = models.ForeignKey(Ordine,null=True,on_delete=models.CASCADE,related_name='ordine_cantiere')
    personale = models.ForeignKey(Personale,null=True,on_delete=models.CASCADE,related_name='personale_cantiere')
    #p_iva_cf = models.CharField(db_column='P.IVA_CF', max_length=40, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    #valore_commessa = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR')
    #valore_commessa = models.FloatField(  blank=True, null=True)
    data_inizio_lavori = models.DateField(blank=True, null=True)
    data_fine_lavori = models.DateField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'cantiere'

#Ordine: ID: Identificativo Data Ordine: Date Fornitore: (Identificativo) Chiave esterna del fornitore da cui è stato effettuato ordine Articoli: Array[Articoli]

class Ordine(models.Model):
    data_ordine = models.DateField(blank=True, null=True)
    importo = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR',default=0.0)
    fornitore = models.ForeignKey(Fornitori,null=True,on_delete=models.CASCADE,related_name='fornitori_ordine')
    cantiere = models.ForeignKey(Cantiere,null=True,on_delete=models.CASCADE,related_name='cantiere_ordine')

    #articoli = models.ForeignKey(Articoli,null=True,on_delete=models.CASCADE,related_name='articoli_ordini')

    class Meta:
        managed = True
        db_table = 'ordine'



#Articolo ID : Identificativo Nome : String Descrizione : String Importo : Number

class Articoli(models.Model):
    nome = models.CharField(max_length=60, blank=True, null=True)
    descrizione = models.TextField(blank=True, null=True)
    importo = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR')
    ordine = models.ForeignKey(Ordine,null=True,on_delete=models.CASCADE,related_name='ordine_articoli')


    class Meta:
        managed = True
        db_table = 'articoli'

#Fattura: ID: Identificativo Numero Fattura Fornitore: Number Fornitore: chiave esterna fornitore Data Fattura: Date Data Scadenza: Date Importo: Number Pagato: Number Cantiere: Array[Cantiere] chiave esterna per tutti i cantieri a cui quella fattura fa riferimento ( molteplici perchè possibilità di scorporare ) Articoli: Array[Articoli] Ordine di rif.: Ordine

class Fatture(models.Model):
    ragione_sociale = models.CharField(max_length=100, blank=True, null=True)
    fornitore = models.ForeignKey(Fornitori,null=True,on_delete=models.CASCADE,related_name='fornitori_fatture')
    n_fattura = models.CharField(db_column='n.fattura', max_length=40, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    data_fattura = models.DateField(blank=True, null=True)
    importo = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR')
    pagato = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR')
    data_scadenza = models.DateField(blank=True, null=True)
    cantiere = models.ForeignKey(Cantiere,null=True,on_delete=models.CASCADE,related_name='cantiere_fatture')
    articoli = models.ForeignKey(Articoli,null=True,on_delete=models.CASCADE,related_name='articoli_fatture')
    ordine = models.ForeignKey(Ordine,null=True,on_delete=models.CASCADE,related_name='ordine_fatture')

    class Meta:
        managed = True
        db_table = 'fatture'

 #Cliente: Lista di oggetti Cliente ID: String Nome: String Cognome: String Indirizzo: String Data di nascita: Date Numero di telefono: String Banca: String IBAN: String

class Cliente(models.Model):
    nome = models.CharField(max_length=60, blank=True, null=True)
    cognome = models.CharField(max_length=60, blank=True, null=True)
    indirizzo = models.TextField( blank=True, null=True)
    data_nascita = models.DateField(blank=True, null=True)
    numero_tel = models.CharField(max_length=40, blank=True, null=True)
    banca = models.CharField(max_length=60, blank=True, null=True)
    iban = models.CharField(max_length=60, blank=True, null=True)
    cantiere = models.ForeignKey(Cantiere,null=True,on_delete=models.CASCADE,related_name='cantiere_cliente')

    class Meta:
        managed = True
        db_table = 'cliente'



#Azienda ID: Identificativo (unico identificativo dell'azienda) Nome: String (nome dell'azienda) Descrizione: String (breve descrizione dell'azienda) Cantieri: Array[Cantieri] (lista di cantieri con chiave esterna di appartenenza all'azienda in questione) Lavoratori: Array[Lavoratori] (lista di lavoratori con chiave esterna di appartenenza all'azienda in questione) Fornitori: Array[Fornitori] (lista di fornitori con chiave esterna di appartenenza all'azienda in questione) Fatture: Array[Fatture] (lista di fatture con chiave esterna di appartenenza all'azienda in questione) Clienti: Array[Clienti] (lista di clienti con chiave esterna di appartenenza all'azienda in questione)

class Azienda(models.Model):
    nome = models.CharField(max_length=60, blank=True, null=True)
    descrizione = models.TextField(blank=True, null=True)
    cantiere = models.ForeignKey(Cantiere,null=True,on_delete=models.CASCADE,related_name='cantieri_azienda')
    personale = models.ForeignKey(Personale,null=True,on_delete=models.CASCADE,related_name='personale_azienda')
    fornitore = models.ForeignKey(Fornitori,null=True,on_delete=models.CASCADE,related_name='fornitori_azienda')
    fatture = models.ForeignKey(Fatture,null=True,on_delete=models.CASCADE,related_name='fatture_azienda')
    cliente = models.ForeignKey(Cliente,null=True,on_delete=models.CASCADE,related_name='cliente_azienda')

    class Meta:
        managed = True
        db_table = 'azienda'


"""

