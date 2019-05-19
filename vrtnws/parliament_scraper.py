from bs4 import BeautifulSoup
import os, requests, time, urllib.request

def main():
    urls = {}

    for page in range(0, 28):
        urls[page] = 'https://www.vlaamsparlement.be/parlementaire-documenten/zoekresultaten?query=&sort=date&aggregaat%5B0%5D=schriftelijke%20vraag&publicatiedatum%5Bvan%5D%5Bdate%5D=01-03-2019&publicatiedatum%5Btot%5D%5Bdate%5D=31-03-2019&zittingsjaar=all&legislatuur=all&aggregatedstatus%5Btype%5D=none&aggregatedstatus%5Bvan%5D%5Bdate%5D=&aggregatedstatus%5Btot%5D%5Bdate%5D=&vraagsteller=all&indiener=all&nummer=&volgnummer=&titel=&commissie=&page={}'.format(page)
        os.makedirs('vrtnws/scraped_urls', exist_ok=True)

    for link in urls.keys():
        output = scrape(urls[link])
        save_html(output)

def scrape(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')
    time.sleep(5)
    output = soup.select('a')
    return output

def save_html(output):
    for row in output:
        if 'Bekijk de documentenfiche' in row.getText():
            row['href'] = 'https://www.vlaamsparlement.be{}'.format(row['href'])
            filename = row['href'][-7:]
            if not os.path.isfile('vrtnws/scraped_urls/{}.html'.format(filename)):
                urllib.request.urlretrieve(row['href'], 'vrtnws/scraped_urls/{}.html'.format(filename))
                time.sleep(2)
                print('File {} successfully saved.'.format(filename))

if __name__ == '__main__':
    main()