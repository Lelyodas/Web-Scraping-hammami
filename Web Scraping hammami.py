import requests
from bs4 import BeautifulSoup

def get_html(url):
    response = requests.get(url)
    return BeautifulSoup(response.content, 'html.parser')

def get_title(soup):
    return soup.find('h1').text

def get_text(soup):
    result = {}
    headings = soup.find_all(['h2', 'h3'])
    for heading in headings:
        heading_text = heading.text.strip()
        paragraphs = []
        for tag in heading.find_next_siblings():
            if tag.name in ['h2', 'h3']:
                break
            if tag.name == 'p':
                paragraphs.append(tag.text.strip())
        if paragraphs:
            result[heading_text] = paragraphs
    return result

def get_links(soup):
    links = []
    for tag in soup.find_all('a', href=True):
        if tag['href'].startswith('/wiki/') and not tag['href'].startswith('/wiki/Special:'):
            links.append("https://en.wikipedia.org" + tag['href'])
    return links

def scrape_wikipedia(url):
    soup = get_html(url)
    title = get_title(soup)
    text = get_text(soup)
    links = get_links(soup)
    return {"title": title, "text": text, "links": links}

url = "https://en.wikipedia.org/wiki/History_of_anime"
result = scrape_wikipedia(url)

print("Title:", result['title'])
print("\nHeadings and Text:")
for heading, paragraphs in result['text'].items():
    print(f"\n{heading}:")
    for paragraph in paragraphs:
        print(f"- {paragraph}")
print("\nInternal Links:")
for link in result['links'][:10]:
    print(link)
