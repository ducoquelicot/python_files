from bs4 import BeautifulSoup
import glob, os, requests, time, urllib.request

def main():
    fda = 'https://www.fda.gov/MedicalDevices/Safety/ListofRecalls/ucm629347.htm'
    try:
        os.makedirs(os.path.expanduser('~/Desktop/Python/Files'))
    except FileExistsError:
        print('This folder already exists.')
    output = scrape(fda)
    save_files(output)

def scrape(html_link):
    fda = requests.get(html_link)
    soup = BeautifulSoup(fda.text, 'lxml')
    relevant_soup = soup.select('tbody tr td a')
    return relevant_soup

def save_files(links):
    for row in links:
        # append https://fda.gov to links
        # save file as cache 
        filename = row['href'][-13:]
        row['href'] = 'https://www.fda.gov' + row['href']
        urllib.request.urlretrieve(row['href'], os.path.expanduser('~/Desktop/Python/Files/' +filename))
        time.sleep(2)
        print('File ' +filename +' successfully saved.')

if __name__ == '__main__':
    main()

    