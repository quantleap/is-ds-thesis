# Entities
## Curatoren
De curatoren kunnen in kaart worden gebracht door meerdere informatiebronnen te koppelen:

- cir register
- insolad website <http://www.insolad.nl>
- nederlandse orde van advocaten <https://www.advocatenorde.nl/vind-een-advocaat>

Insolad scrape: 639 leden

CIR:  distinct 3168 curatoren (C) / bewindvoerders (B) 
      distinct 2565 curatoren
      dit moet nog ontdubbeld worden
      

'In Nederland zijn momenteel zo’n 1.800 professionele curatoren, beschermingsbewindvoerders en mentoren actief in 200.000 zaken.'

branchevereniging
<https://www.veweve.nl/>


# Curatoren Kantoren
- kantorenlijst <http://www.curatoren.nl/fo/handig_kantoren.php>
- vorige versie insolad scrape lijst

# Rechter-Commissaris
De RC wordt in de CIR data genoemd als onderdeel van de insolvent. 
De naam van de RC is een vrij text veld en dezelfde naam komt vaak in vele variaties voor.

## rechtspraak register
Een betrouwbare bron voor de naam is het register van nevenfuncties van rechters: <http://namenlijst.rechtspraak.nl/>
Dit register levert de volgende datavelden:

- geslacht
- titel
- naam
- historie beroepsgegevens (functie, instantie, datum ingang, datum eind) .. - niet relevant nu
- nevenbetrekkingen - niet relevant nu

## open state foundation

Open State Foundation (<https://openstate.eu/>) maakt publieke data bruikbaar voor derden.
Deze data is ook verkrijgbaar via de rest API van openstate:

- <http://ors.openstate.eu/index.php/content/page/opendata>
- <http://ors.openstate.eu/index.php/relations/json> (set, name, uri)
- uri bv: <http://ors.openstate.eu/relations/instantie/Rechtbank+Amsterdam/mw.+mr.+J.F.+Aalders+/json> (bevat data per persoon)

namen, titel en geslacht en is genoeg voor nu)

De gehele van rechtspraak gescrapte dataset is er verkrijgbaar van datum 20-01-2016. Voor recentere informatie zal openstate om een update gevraagd kunnen worden of zelf te gaan scrapen.
