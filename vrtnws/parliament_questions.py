from bs4 import BeautifulSoup
import os, fnmatch, glob, re
from collections import Counter

def main():
    questions = glob.glob('vrtnws/scraped_urls/*')
    politicians = []
    for row in questions:
        output = scrape(row)
        pol = get_polit(output)
        politicians.append(pol)

    flat = [val for sublist in politicians for val in sublist]
    parties = []
    for item in flat:
        p = item[item.index("(") +1:item.rindex(")")]
        parties.append(p)

    count_pols = Counter(flat)
    count_party = Counter(parties)
    cpo = str(sorted(count_pols, key=count_pols.get, reverse=True)[:1])
    cpy = str(sorted(count_party, key=count_party.get, reverse=True)[:1])
    politician = cpo.strip('[]')
    party = cpy.strip('[]')
    total_questions = len(fnmatch.filter(os.listdir('vrtnws/scraped_urls'), '*html'))

    print('The total number of questions asked to the Flemish parliament in March 2019 is {}.\nThe politician who asked the most questions is {}.\nThe party that asked the most questions is {}.'.format(total_questions, politician, party))

def scrape(question):
        # filename = os.path.basename(row)
        soup = BeautifulSoup(open(question), 'html.parser')
        output = soup.find_all('a', href=re.compile('volksvertegenwoordigers'))
        return output

def get_polit(output):
    pol = []
    for row in output:
        if 'Volksvertegenwoordiger' not in row.getText():
            pol.append(row.getText())
    return pol

if __name__ == '__main__':
    main()
