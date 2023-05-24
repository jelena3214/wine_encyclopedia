from django.contrib.auth.models import AbstractUser
from django.db import models
from userApp.manager import KorisnikManager

class Korisnik(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    javnoime = models.CharField(db_column='javnoIme', max_length=20, blank=True, null=True)
    adresa = models.CharField(max_length=50, blank=True, null=True)
    brtelefona = models.CharField(db_column='brTelefona', max_length=50, blank=True, null=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = KorisnikManager()
    class Meta:
        db_table = 'korisnik'


class Kupac(Korisnik):
    datumrodjenja = models.DateTimeField(db_column='datumRodjenja', blank=True, null=True)

    class Meta:
        db_table = 'kupac'


class Proizvodjac(Korisnik):
    imefirme = models.CharField(db_column='imeFirme', max_length=50, blank=True, null=True)
    registarskibroj = models.IntegerField(db_column='registarskiBroj', blank=True, null=True)
    opis = models.TextField(blank=True, null=True)
    #logo = models.ImageField(upload_to='images', null=True)

    class Meta:
        db_table = 'proizvodjac'


class Obilazak(models.Model):
    idponuda = models.OneToOneField('Ponudaprostor', models.CASCADE, db_column='idPonuda',
                                    primary_key=True)
    cenasomelijera = models.IntegerField(db_column='cenaSomelijera', blank=True,
                                         null=True)

    class Meta:
        db_table = 'obilazak'


class Ponuda(models.Model):
    idponuda = models.IntegerField(db_column='idPonuda', primary_key=True)
    idkorisnik = models.ForeignKey(Korisnik, models.CASCADE, db_column='idKorisnik')

    class Meta:
        db_table = 'ponuda'


class Ponudaprostor(models.Model):
    idponuda = models.OneToOneField(Ponuda, models.CASCADE, db_column='idPonuda', primary_key=True)

    class Meta:
        db_table = 'ponudaprostor'


class Pretplata(models.Model):
    idpretplata = models.IntegerField(db_column='idPretplata', primary_key=True)
    naslov = models.CharField(max_length=20, blank=True, null=True)
    cena = models.IntegerField(blank=True, null=True)
    opis = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'pretplata'


class Pretplacen(models.Model):
    idkorisnik = models.OneToOneField(Korisnik, models.CASCADE, db_column='idKorisnik', null=False)
    idpretplata = models.ForeignKey(Pretplata, models.CASCADE, db_column='idPretplata', null=False)
    datumpocetak = models.DateTimeField(db_column='datumPocetak', blank=True, null=True)
    datumkraj = models.DateTimeField(db_column='datumKraj', blank=True, null=True)
    trenutnistatus = models.CharField(db_column='trenutniStatus', max_length=20, blank=True,
                                      null=True)

    class Meta:
        db_table = 'pretplacen'
        unique_together = (('idkorisnik', 'idpretplata'),)


class Proslava(models.Model):
    idponuda = models.OneToOneField(Ponudaprostor, models.CASCADE, db_column='idPonuda',
                                    primary_key=True)
    opisproslave = models.TextField(db_column='opisProslave', blank=True, null=True)
    cenapoosobi = models.IntegerField(db_column='cenaPoOsobi', blank=True, null=True)
    kapacitet = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'proslava'


class Recenzija(models.Model):
    idrecenzija = models.IntegerField(db_column='idRecenzija', primary_key=True)
    opisrec = models.CharField(db_column='opisRec', max_length=20, blank=True, null=True)
    idponuda = models.ForeignKey(Ponuda, models.CASCADE, db_column='idPonuda')
    ocena = models.IntegerField(blank=True, null=True)
    idkorisnik = models.ForeignKey(Korisnik, models.CASCADE)

    class Meta:
        db_table = 'recenzija'


class Termin(models.Model):
    idtermin = models.IntegerField(db_column='idTermin', primary_key=True)
    vreme = models.DateTimeField(blank=True, null=True)
    idponuda = models.ForeignKey(Ponudaprostor, models.CASCADE, db_column='idPonuda')

    class Meta:
        db_table = 'termin'


class Rezervacija(models.Model):
    idtermin = models.OneToOneField(Termin, models.CASCADE, db_column='idTermin',
                                    primary_key=True)
    idkorisnik = models.ForeignKey(Korisnik, models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'rezervacija'


class Tag(models.Model):
    idtag = models.IntegerField(db_column='idTag', primary_key=True)
    tag = models.CharField(max_length=20, blank=True, null=True)
    idponuda = models.ForeignKey('Vino', models.CASCADE, db_column='idPonuda')

    class Meta:
        db_table = 'tag'


class Rezultatupitnika(models.Model):
    idkorisnik = models.OneToOneField(Korisnik, models.CASCADE, db_column='idKorisnik', null=False)
    idtag = models.ForeignKey(Tag, models.CASCADE, db_column='idTag', null=False)

    class Meta:
        db_table = 'rezultatupitnika'
        unique_together = (('idkorisnik', 'idtag'),)


class Slika(models.Model):
    idponuda = models.ForeignKey(Ponuda, models.CASCADE, db_column='idPonuda')
    idslika = models.IntegerField(db_column='idSlika', primary_key=True)
    slika = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'slika'


class Somelijer(models.Model):
    idsomelijer = models.IntegerField(db_column='idSomelijer', primary_key=True)
    idponuda = models.ForeignKey(Obilazak, models.CASCADE, db_column='idPonuda')
    ime = models.CharField(max_length=20, blank=True, null=True)
    biografija = models.TextField(blank=True, null=True)
    slika = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'somelijer'


class Ukorpi(models.Model):
    idkorisnik = models.ForeignKey(Korisnik, models.CASCADE, db_column='idKorisnik', blank=True,
                                   null=True)
    idponuda = models.ForeignKey('Vino', models.CASCADE, db_column='idPonuda', blank=True,
                                 null=True)
    idkorpa = models.IntegerField(db_column='idKorpa', primary_key=True)

    class Meta:
        db_table = 'ukorpi'


class Upitnikpitanje(models.Model):
    idpitanje = models.IntegerField(db_column='idPitanje', primary_key=True)
    tekst = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'upitnikpitanje'


class Upitnikodgovor(models.Model):
    idpitanje = models.ForeignKey(Upitnikpitanje, models.CASCADE, db_column='idPitanje', blank=True,
                                  null=True)
    idodgovor = models.IntegerField(db_column='idOdgovor', primary_key=True)
    odgovor = models.CharField(max_length=20, blank=True, null=True)
    idtag = models.ForeignKey(Tag, models.CASCADE, db_column='idTag')

    class Meta:
        db_table = 'upitnikodgovor'


class Vino(models.Model):
    idponuda = models.OneToOneField(Ponuda, models.CASCADE, db_column='idPonuda',
                                    primary_key=True)
    naziv = models.CharField(max_length=20, blank=True, null=True)
    cena = models.IntegerField(blank=True, null=True)
    opisvina = models.CharField(db_column='opisVina', max_length=200, blank=True,
                                null=True)
    brojprodatih = models.IntegerField(db_column='brojProdatih', blank=True, null=True)

    class Meta:
        db_table = 'vino'


class Vrstaobilaska(models.Model):
    idobilazak = models.IntegerField(db_column='idObilazak', primary_key=True)
    idponuda = models.ForeignKey(Obilazak, models.CASCADE, db_column='idPonuda')
    naziv = models.CharField(max_length=20, blank=True, null=True)
    cena = models.IntegerField(blank=True, null=True)
    opis = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'vrstaobilaska'
