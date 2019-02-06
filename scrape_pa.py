from bs4 import BeautifulSoup
from itertools import count
import csv, fnmatch, os, requests, time, urllib.request

def main():
    pa_agenda = {2019: 'https://www.cityofpaloalto.org/gov/depts/cou/council_agendas.asp'}

    for year in range(2002,2019):
        pa_agenda[year] = 'https://www.cityofpaloalto.org/gov/agendas/council/' + str(year) +'.asp'
    
    for year in pa_agenda.keys():
        output = scrape(pa_agenda[year])
        get_links(output, year)

def scrape(html_link):
    # get all links within parameters from provided html
    agenda = requests.get(html_link)
    soup = BeautifulSoup(agenda.text, 'lxml')
    relevant_soup = soup.select('a')
    return relevant_soup

def get_links(links, years):
    # filter for Agenda and packet only, append to list and download pdf
    agendas = []
    for row in range(len(links)):
        if links[row].getText()== 'Agenda and Packet':
            if fnmatch.fnmatch(links[row]['href'], '*://www.cityofpaloalto.org/*'):
                agendas.append([links[row]['href']])
                time.sleep(2)
                urllib.request.urlretrieve(links[row]['href'], os.path.expanduser('~/Desktop/Python/Files/pdfs_' +str(years) + '_' +str(row) + '.pdf'))
                time.sleep(5)
            else:
                links[row]['href'] = 'https://www.cityofpaloalto.org' + links[row]['href']
                agendas.append([links[row]['href']])
                time.sleep(2)
                urllib.request.urlretrieve(links[row]['href'], os.path.expanduser('~/Desktop/Python/Files/pdfs_' +str(years) + '_' +str(row) + '.pdf'))
                time.sleep(5)

    # Write list into .csv file
    with open(os.path.expanduser('~/Desktop/Python/Files/agendas_' +str(years) + '.csv'), 'w') as agenda:
        writer = csv.writer(agenda)
        writer.writerow(["Agenda and Packet"])
        writer.writerows(agendas)

if __name__ == '__main__':
    main()