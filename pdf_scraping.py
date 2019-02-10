import fitz, os, urllib.request

agenda = fitz.open('/home/fabienne/Desktop/Python/PDF/pdfs_2019_37.pdf')
lastpage = agenda[range(len(agenda))[-1]]
links = lastpage.getLinks()

letters = []

for row in links:
    letters.append(row['uri'])

for row in range(len(letters))[-2:]:
    urllib.request.urlretrieve(letters[row], os.path.expanduser('~/Desktop/Python/Letters/letters_' +str(row) + '.pdf'))

letter = fitz.open('/home/fabienne/Desktop/Python/Letters/letters_2.pdf')
pages = len(letter)

lettertotext = 'pdftotext -layout /home/fabienne/Desktop/Python/Letters/letters_2.pdf'
os.system(lettertotext)

with open('/home/fabienne/Desktop/Python/Letters/letters_2.txt') as council_letters:
    contents = council_letters.read()
    if 'President' in contents:
        print('Keyword found')
    else:
        print('Keyword not found')