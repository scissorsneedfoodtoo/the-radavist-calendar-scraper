# /usr/bin/python3
# theRadavistCalScraper - Downloads the current month's calendar from theradavist.com

import requests, os, bs4

url = 'https://theradavist.com/?s=calendar' # base URL for most recent calendars
header = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1'}
os.makedirs('cals', exist_ok=True) # stores pics in local file

print('Downloading page {}...'.format(url))
res = requests.get(url, headers=header)
try:
    res.raise_for_status()
except Exception as exc:
    print('There was a problem: {}'.format(exc))

soup = bs4.BeautifulSoup(res.text, 'lxml')

# Check that most current post is a monthly calendar,
# rather than a promotion for a yearly calendar

firstArticle = soup.find('article')

def downloadCals(article):
    articleHeader = article.find('header').get_text()
    if 'The Radavist' and 'Calendar:' in articleHeader:
        # Isolate the image elements
        paragraphs = article.find_all('p')
        imageElems = []
        for p in paragraphs:
            if p.find('a'):
                imageElems.append(p.find('a'))
        imageNames = []
        for link in imageElems:
            imageNames.append(link.get_text()) # TODO: Clean up the names with regex and joins

        if imageElems == []:
            print('Could not find calendars.')
        else:
            for i in range(len(imageElems)):
                imageURL = imageElems[i].get('href')

                # Download the imageURL
                print('Downloading image from {}...'.format(imageURL))
                res = requests.get(imageURL) # stores calendar image in res
                try:
                    res.raise_for_status()
                except Exception as exc:
                    print('There was a problem: {}'.format(exc))

                # Save the calendar images to ./cals
                imageFile = open(os.path.join('cals', imageNames[i]), 'wb')
                for chunk in res.iter_content(100000):
                    imageFile.write(chunk)
                imageFile.close()
        return # break out of the function

    else:
        print('The current post has no calendars. Moving to the next.')
        nextArticle = article.find_next_sibling('article')
        downloadCals(nextArticle)

downloadCals(firstArticle)

print('Finished!')
