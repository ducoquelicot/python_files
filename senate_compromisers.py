import os
import requests

def main():
    url = 'https://api.propublica.org/congress/v1/116/senate/members.json'
    key = {"X-API-Key": os.environ['pp_api']}
    response = requests.get(url, headers=key)
    members = response.json()

    senators = []

    for row in members['results']:
        for member in row['members']:
            senators.append(member)

    for row in senators:
        dems_five = sorted(senators, key = sort_dems)[:5]
        reps_first = sorted(senators, key = sort_reps)
        reps_five = sorted(reps_first, key = reps_vote, reverse = True)[:5]

    print("Democrats lowest party vote:")
    for row in dems_five:
        print([row['first_name'] + ' ' + row['last_name'], row['state'], row['votes_with_party_pct']])

    print()
    print("Republicans lowest party vote:")
    for row in reps_five:
        print([row['first_name'] + ' ' + row['last_name'], row['state'], row['votes_with_party_pct']])

def sort_dems(senator):
    return senator['party'], senator['votes_with_party_pct']

def sort_reps(senator):
    return senator['votes_with_party_pct']

def reps_vote(senator):
    return senator['party']

main()