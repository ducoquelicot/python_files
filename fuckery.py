from bs4 import BeautifulSoup
import csv
import os
import requests

pa_agenda = {2019: 'https://www.cityofpaloalto.org/gov/depts/cou/council_agendas.asp', 2018:'https://www.cityofpaloalto.org/gov/agendas/council/2018.asp'}

for year in pa_agenda.keys():
    print(pa_agenda[2019])

for i in range(2002,2019):
    print(i)

from bs4 import BeautifulSoup
import os, urllib.request
import fitz

# cmd = 'pdftohtml -c -s /home/fabienne/Desktop/Python/Files/pdfs_2019_37.pdf  /home/fabienne/Desktop/Python/html/pdfs_2019_37'
# os.system(cmd)

# response = urllib.request.urlopen('file:///home/fabienne/Desktop/Python/html/pdfs_2019_37-html.html', timeout=1)
# html = response.read()
# soup = BeautifulSoup(html, 'html.parser')
# links = soup.select('a')

# for row in links:
#     if '31-18' or '07-19' in row.getText():
#         print(row)

doc = fitz.open('/home/fabienne/Desktop/Python/Files/pdfs_2019_37.pdf')
page = doc[2]
links = page.getLinks()
print(len(doc))

lastnum = range(len(doc))[-1]
print(lastnum)

for row in links:
    print(row['uri'])

'/home/fabienne/Desktop/Python/PDF/pdfs_2019_37.pdf'

# for recall in recalls:
#     filename = os.path.basename(recall)[:-4]
#     soup = BeautifulSoup(open(recall), 'html.parser')
#     with open(os.path.expanduser('~/Desktop/Python/Files/' +filename +'_soup.html'), 'w') as file:
#         file.write(str(soup))