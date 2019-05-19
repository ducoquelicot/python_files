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