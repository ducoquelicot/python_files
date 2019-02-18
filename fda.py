from bs4 import BeautifulSoup
import glob, os, requests, time, urllib.request
 
fda = requests.get('https://www.fda.gov/MedicalDevices/Safety/ListofRecalls/ucm629347.htm')
soup = BeautifulSoup(fda.text, 'lxml')
relevant_soup = soup.select('tbody tr td a')

for row in relevant_soup:
    # append https://fda.gov to links
    # save file as cache 
    filename = row['href'][-13:]
    row['href'] = 'https://www.fda.gov' + row['href']
    urllib.request.urlretrieve(row['href'], os.path.expanduser('~/Desktop/Python/Files/' +filename))
    time.sleep(2)

recalls = glob.glob(os.path.expanduser('~/Desktop/Python/Files/*.htm'))

# for recall in recalls:
#     filename = os.path.basename(recall)[:-4]
#     soup = BeautifulSoup(open(recall), 'html.parser')
#     with open(os.path.expanduser('~/Desktop/Python/Files/' +filename +'_soup.html'), 'w') as file:
#         file.write(str(soup))
    