from bs4 import BeautifulSoup

def safe_xss(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    for tag in ["script", "iframe", "frame", "style", "link", "meta"]:
        for match in soup.find_all(tag):
            match.decompose()
    
    return str(soup)