# Commentaar op scriptie opzet Tom Akkermans 

* maarten
*  3 April 2018

1. Prima vragen. Ze zijn inhoudelijk en dat is leuk, maar geven aanleiding tot technische deelvragen. 
	2. Je zou het ook zo kunnen inrichten: "With which level of correctness and completeness can an automatic text extraction system answer the following questions based on insolvency data?"
	3. En dan noem je die vragen die je al had.
	4. Dan is je uiteindelijke doel helder, en passen de deelvragen er ook goed bij. 
	5. En je hebt 2 duidelijke (en elkaar tegenwerkende) doelen: precisie en recall, die je steeds ind e gaten moet houden.
2. **Resources/data** _Hoeveel heb je al binnen gehaald?_ Hoeveel heb je al omgezet naar jouw DB formaat? Zorg je voor _provenance_ van de data in jouw DB? Dus dat je van een relatie die je in je DB vindt/aangeeft steeds makkelijk kunt herleiden waar die van daan is gekomen en hoe? Dat is belangrijk want dit is allemaal juridisch.
	3. 3.2 Prima om dit nog in het midden te houden.  Je spendeert hier (de deduplicatie, etc) een paar dagen aan, haalt 85-90% , doet een snelle evaluatie en laat het daarbij. De rest is meestal toch handwerk, of een nieuwe neural network scriptie ;-). Dit is niet jouw focus punt.
	4. 3.3 Prima. Ik zou ook de totalen in de tabel erbij zetten. Je kan voor jezelf nu alvast een geordende lijst maken van dingen die je graag uit die rapprten wilt halen. Geef dan in dat lijstje ook steeds aan _hoe_ je denkt dat te doen, en _hoe lastig_ je denkt dat het zal zijn, en ook _wat je er later mee wilt doen_. 
		* Dit lijstje kan je hele onderzoek enorm structurene ne dwingt je tot het maken van keuzes.
4. **4** Prima die query interface. Dat kan als prototype ook heel simpel in een IPython notebook. Dat zou ik eerst doen. Dan kan je daar de functionaliteit al heel goed opmeten met  een paar proefpersonen. Een typische evaluatie is om een paar mensen wat taakjes te laten doen, eerst op de 'bestaande databses", ne dan via jouw systeem.  Die taakjes kunnen bijvoorbeeld jouw RQ's zijn. Of simpele dingen als "Heeft curator X iets gedaan met het faiilissement van bedrijf Y?" Zo ja, wat was het bedrag dat er mee gemoeid was. Zo nee, welke curator deed dat bedrijf dan?
	5. En dan meet je de tijd op, en bekijkt later of het antwoord goed is. 
		* Een paar van die vragen en 2-3 proefpersonen levert al heel wat op.
6. **tecnisch** Ik denk dat het netwerk model makkelijk in een sql lite db past, en dat zou ik dus ook gebruiken. Dat werkt heel makkelijk met pandas en networkx, waarmee je je protoptype query inerface kunt maken. 
	7. **In je schema zie ik dus nog geen dingen over de tijd, en over provenance, dus het linken naar bronnen, en technieken.
	8. In een groter schema zou je dus ook relaties hebben als <surfaceform, occurs_in, document, positie in document> en <surfaceform, mapped_on, entity, by technique/evidence/....>	
	9. Je zou je kunnen voorstellen dat je de entities die waarschijnlijk horen bij de surface forms die voorkomen in een document als metadata toevoegt aan dat document en dat oplstaatin je elastic search, en dat ook gebruikt in een zoekinterface (dan kan je dus heel makkelijk met facetten gaan werken,e n mooi uitsnedes maken).	
