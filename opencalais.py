from bs4 import BeautifulSoup
import glob, json, os, re, requests, time

recalls = glob.glob(os.path.expanduser('~/Desktop/Python/Files/*.htm'))
calais_url = 'https://api.thomsonreuters.com/permid/calais'
user = os.environ['OPENCALAIS_API_USER']
key = os.environ['OPENCALAIS_API_KEY']

def main():
    for recall in recalls:
        filename = os.path.basename(recall)[:-4]
        soup = BeautifulSoup(open(recall), 'html.parser')
        reason = (soup.find_all(string=re.compile("is recalling")))
        
        header = {
            'X-AG-Access-Token' : key,
            'Content-Type' : 'text/raw',
            'outputformat' : 'application/json'
        }
        response = requests.post(
            url=calais_url,
            data=str(reason),
            headers=header,
            timeout=80
        )
        time.sleep(5)
        output = os.path.expanduser('~/Desktop/Python/Files/' +filename +'.json')
        with open(output, 'w') as out:
            if response.status_code == 200:
                print('Extraction successful. Writing response to {}'.format(output[-14:]))
                json.dump(response.json(), out, indent=4)
            else:
                print('Something went wrong with the extraction.')

if __name__ == '__main__':
    main()