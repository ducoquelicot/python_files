import requests
import smtplib

def main():
    url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson'
    response = requests.get(url)
    earthquakes = response.json()

    quakes = []

    for dictionary in earthquakes['features']:
        quake = dictionary['properties']['place'], dictionary['properties']['mag']
        quakes.append(quake)

    for row in quakes:
        magnitude = sorted(quakes, key = sort_quakes, reverse = True)[:10]

    email = "in the past 24 hours, there were {} earthquakes. The top ten, by magnitude:\n\n".format(len(quakes))

    for quake in magnitude:
        row = "- {} ({})\n".format(quake[0], quake[1])
        email += row

    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login('fabienne.rosina.nicole@gmail.com', 'pythoncode123')
    smtpObj.sendmail('fabienne.rosina.nicole@gmail.com', 'fmeijer@stanford.edu', 'Subject: Earthquakes in the last 24 hours\nHi Fabienne, {}'.format(email))
    smtpObj.quit()

def sort_quakes(quakes):
    return quakes[1]

if __name__ == '__main__':
    main()