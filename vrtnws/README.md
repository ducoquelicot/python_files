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

