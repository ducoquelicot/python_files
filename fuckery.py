from bs4 import BeautifulSoup
import csv
import os
import requests

pa_agenda = {2019: 'https://www.cityofpaloalto.org/gov/depts/cou/council_agendas.asp', 2018:'https://www.cityofpaloalto.org/gov/agendas/council/2018.asp'}

for year in pa_agenda.keys():
    print(pa_agenda[2019])

for i in range(2002,2019):
    print(i)
