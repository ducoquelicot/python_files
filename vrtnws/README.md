# Uitleg bij opdrachten VRTNWS

## Opdracht 1: scraper 
```
Corresponding files and directories:
parliament_scrapers.py
parliament.questions.py
run_pipeline.py
/scraped_urls
```

Antwoorden:
1. 684
2. CD&V
3. Jos de Meyer

Scrapers zijn finnicky om mee te werken en dus is het handig om goed na te denken wat we precies willen weten voordat we de scraper maken. In dit geval zijn
we geinteresseerd in alles van maart 2019. Dus specificeren we in de zoekvelden van 1-03-2019 tot 31-03-2019. We specificeren ook dat we op zoek zijn naar
alle schriftelijke vragen. Dit geeft 28 pagina's aan resultaten. Aan de url ```https://www.vlaamsparlement.be/parlementaire-documenten/zoekresultaten?query=&sort=date&aggregaat%5B0%5D=schriftelijke%20vraag&publicatiedatum%5Bvan%5D%5Bdate%5D=01-03-2019&publicatiedatum%5Btot%5D%5Bdate%5D=31-03-2019&zittingsjaar=all&legislatuur=all&aggregatedstatus%5Btype%5D=none&aggregatedstatus%5Bvan%5D%5Bdate%5D=&aggregatedstatus%5Btot%5D%5Bdate%5D=&vraagsteller=all&indiener=all&nummer=&volgnummer=&titel=&commissie=&page=27``` kunnen we door ```page=27``` zien dat we te maken hebben met een lijst die bij 0 begint met tellen. Als we testen met 
```page=0``` komen we inderdaad bij pagina 1 uit. Dat betekent dat we logica hebben in de url's en dat maakt het scrapen makkelijker.

Vervolgens genereren we een python dictionary met alle links. Deze scrapen we met BeautifulSoup, we zoeken naar alle 'a' oftewel alle links op de pagina. Als we de
pagina's inspecteren zien we dat we altijd via dezelfde tekst 'Bekijk de documentenfiche' bij de link kunnen komen waar we de partij van de vragensteller kunnen vinden. Deze gebruiken we dus in het volgende stukje:

```
def save_html(output):
    for row in output:
        if 'Bekijk de documentenfiche' in row.getText():
            row['href'] = 'https://www.vlaamsparlement.be{}'.format(row['href'])
            filename = row['href'][-7:]
            if not os.path.isfile('vrtnws/scraped_urls/{}.html'.format(filename)):
                urllib.request.urlretrieve(row['href'], 'vrtnws/scraped_urls/{}.html'.format(filename))
                time.sleep(2)
                print('File {} successfully saved.'.format(filename))

```

De line ```if not os.path.isfile('vrtnws/scraped_urls/{}.html'.format(filename))``` is ingevoegd om te zorgen dat we geen files dubbel downloaden, dat is erg belastend voor de server van de partij waar we de links vanaf trekken - en je wil een website niet per ongeluk dDossen. We voegen hier ook de basis-url in om te zorgen dat we de webpagina's daadwerkelijk kunnen downloaden. We doen dit om dezelfde reden als zojuist: voorkomen dat we de website per ongeluk overbelasten met onze verzoeken.

Als dit allemaal gelukt is, kunnen we naar het volgende script: ```parliament_questions.py```. Allereerst - dit is later in de code teruggekomen maar is het eerste wat ik gedaan heb - checken we of het aantal gescrapete documenten overeenkomt met wat er op de site staat. Dit blijkt niet zo te zijn: 684 tegenover 686. Om de oorzaak te achterhalen voeren we een aantal tests uit, zoals controleren hoeveel links we terugkrijgen van het eerste script. We komen erachter dat op ten minste een (1) pagina een link naar een document twee keer is geplaatst. Dit lijkt, gezien andere tests op niets bijzonders uitkomen, de meest waarschijnlijke verklaring.

In het tweede bestand halen we, wederom met BeautifulSoup, de tekst uit de pagina waar de naam en de partij van de vragensteller op staat. Die is te vinden door alle links te zoeken waar 'volksvertegenwoordigers'  in staat. Om te zorgen dat we niet de standaard links in het menu en de footer meenemen, voegen we de tekst alleen toe aan de lijst als ```row.getText()``` geen 'Volksvertegenwoordiger' bevat. 

Vervolgens is het een kwestie van de boel sorteren en netjes maken. Eerst halen we de partij uit de tekst met een regex en zetten deze in een aparte lijst. Sorteren doen we met ```Counter```, en vervolgens maken we alles netjes door het in strings om te zetten en de [] eraf te strippen. Dit alles printen we uiteindelijk netjes.

Om te zorgen dat je allebei de scripts achter elkaar kunt runnen heb ik de ```run_pipeline.py``` gemaakt. 

## Opdracht 2: data-analyse
```
Corresponding files:
terrorism_data.ipynb
(external) vrtnws_story
(external) vrtnws_pivot
```

Het eerste wat opvalt is dat de dataset geen bron heeft, wat het lastig maakt de kwaliteit van de data te verifieren. Daarnaast is er geen data dictionary aanwezig, wat het lastig maakt de betekenis van verschillende column headers te ontcijferen.

Desondanks kunnen we zeker wel wat analyse doen. Allereerst openen we het bestand in Excel, om een overview te krijgen van de datatypes en of bepaalde zaken meteen opvallen. Na het bekijken en filteren van de data in Excel kunnen we een aantal vragen opschrijven die we in Python Pandas kunnen beantwoorden.

Een paar voorbeeldvragen:
- Welke landen kregen de meeste aanslagen te verduren tussen 1970 en 2017?
- Wat waren de tien aanslagen met de meeste slachtoffers?
- In welke landen opereren de terreurgroepen het meest?
- Hoeveel dodelijke slachtoffers waren er per jaar en hoe ontwikkelt zich dat?
- Welk type aanslag komt het vaakst voor?
- Wie is het vaakst doelwit van een aanslag?
- Wat waren de dodelijkste aanslagen in Belgie?

(Zie ```terrorism_data.ipynb``` voor een uitgebreide stap voor stap uitleg bij de gestelde vragen en gedane handelingen)

Nu we een overzicht hebben van de vragen die we hebben beantwoord, kunnen we verder werken in Tableau (zie: https://public.tableau.com/profile/fabienne.meijer#!/vizhome/vrtnws_story/deaths_overtime, schakel tussen de twee tabbladen om de twee visualisaties te zien) om visualisaties te maken die bij het verhaal zouden passen.

- Viz 1: lijngrafiek van het aantal slachtoffers per jaar
Deze grafiek is handig omdat duidelijk te zien is hoe het aantal slachtoffers per jaar zich ontwikkelt door de jaren heen.

- Viz 2: kaart met ingekleurd voor aantal aanslagen, gecombineerd met bar chart
Deze kaart laat in een (1) oogopslag zien in welke landen de meeste aanslagen worden gepleegd. Als je klikt op een land, zie je in de tabel eronder in een bar hoeveel aanslagen er gepleegd zijn. 

Als laatste de pivottabel. Deze had ik in pandas kunnen maken, maar Excel is hier gewoon ontzettend handig voor. Dus heb ik in een Excel werkblad een draaitabel gemaakt waar je per terroristische groep het aantal dodelijke slachtoffers per jaar kunt zien. Elke rij eindigt met het totaal aantal slachtoffers per groep, elke kolom eindigt met het totaal aantal slachtoffers voor dat jaar.

Om het stuk te schrijven kunnen we nu alle gevonden waarden makkelijk combineren om tot de conclusie te komen dat het vrij opmerkelijk is dat ISIL, een groep die nog maar 'relatief kort' actief is, een enorme hoeveelheid aanslagen heeft geclaimd en daarmee ook een heleboel slachtoffers. 

Om het verhaal in perspectief te plaatsen, vind ik het belangrijk om te melden dat hoewel er veel aandacht is voor de aanslagen in het Westen, we niet moeten vergeten dat met name het Midden-Oosten de laatste paar jaar onevenredig getroffen wordt door aanslagen, die bovendien nog eens veel dodelijker zijn dan aanslagen vroeger.

## Opdracht 5: Belgische YT-verhalen
Dimitri Tokmetzis schrijft in een artikel op de Correspondent over verschillende gebruiksmogelijkheden die er zijn voor de code die ze geschreven hebben. Je kan bijvoorbeeld een gebruikersgemeenschap onderzoek of een landenanalyse doen.

Uit de code op GitHub blijkt dat je bijvoorbeeld makkelijk het land kan vinden waar het kanaal mee geassocieerd is. Dat betekent dat je met de code van DC met een paar kleine aanpassingen een verzameling moet kunnen maken van Belgische kanalen en die verder kan analyseren op bijvoorbeeld extreme onderwerpen en bekende extreemrechtse gebruikers.

Een andere optie is een lijst op te vragen van de meest populaire video's in de Vlaamse of Franstalige regio te zoeken en deze met elkaar te vergelijken. Dit is extra interessant als wordt gekeken naar een lijst van de meest populaire video's met extreme topics. 

Verder uitzoeken: na het vinden van video's in Belgie en deze verder uitpluizen voor extreme video's is het wellicht een goed idee om ook naar de comments onder deze video's te kijken, aangezien deze waarschijnlijk van Belgen zijn. De accounts achter deze comments zijn mogelijk ook interessant.

## Opdracht 6: Een verhaal voor de VRT
Een interessant verhaal dat ik zou willen onderzoeken is de impact van het gebrek aan diversiteit in het Europese parlement op de beleidsvoering en de wetten die gemaakt worden. Een speciale hoofdrol kan hier natuurlijk spelen voor de Belgische nationale politici die actief zijn op het Europese toneel en welke veranderingen er mogelijk op handen zijn na de Europese verkiezingen.

Data speelt hierbij natuurlijk een belangrijke rol in het analyseren ten eerste van de diversiteit van het parlement: een mogelijk interessante vergelijking is bijvoorbeeld om de diversiteit van nationale parlementen te vergelijken met de afspiegeling op Europees niveau. Daarnaast kan data verzameld worden over het soort vragen en moties die worden ingediend door Europarlementariers die behoren tot een minderheidsgroep, en of zij inhoudelijk verschillen van de vragen en moties van parlementariers uit meerderheidsgroepen. 
