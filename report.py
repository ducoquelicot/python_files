import csv, glob, json, os

reasons = glob.glob(os.path.expanduser('~/Desktop/Python/Files/*.json'))
socialtags = []

def main():
    try:
        os.makedirs(os.path.expanduser('~/Desktop/Python/Files'))
    except FileExistsError:
        print('This folder already exists.')
    for item in reasons:
        filename = os.path.basename(item)
        with open(item) as json_data:
            output = json.load(json_data)
            for row in output:
                if 'SocialTag' in row:
                    tag = filename, output[row]["name"]
                    socialtags.append(tag)

    with open(os.path.expanduser('~/Desktop/Python/Files/fda_tags.csv'), 'w') as fda_tags:
        writer = csv.writer(fda_tags)
        writer.writerow(["filename", "social_tag"])
        writer.writerows(socialtags)

    print('Tags successfully added.')

if __name__ == '__main__':
    main()