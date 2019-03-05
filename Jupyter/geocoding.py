import os, requests

address = '380 New York St.' + ', Redlands, CA'
url = 'http://locator.stanford.edu/arcgis/rest/services/geocode/Composite_NorthAmerica/GeocodeServer/geocodeAddresses?addresses={"records":[{"attributes":{"OBJECTID":1,"SingleLine":"' + address + '"}' + '}]}'
token = '&token={}'.format(os.environ['arcgis'])
form = '&f=pjson'
request = url +token +form
response = requests.get(request)
geocode = response.json()

print(geocode)