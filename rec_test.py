import urllib.request
from bs4 import BeautifulSoup


goto = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
body = urllib.request.urlopen(goto)
soup = BeautifulSoup(body, from_encoding=body.info().get_param('charset'))
recommended_urls =[]
for link in soup.find_all('a', href=True):
    print(link)
    if "/watch?" in link['href']:
        recommended_urls.append(link['href'])
print(list(set(recommended_urls)))