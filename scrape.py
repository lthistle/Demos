from bs4 import BeautifulSoup
from requests_html import HTMLSession

news = "cnn"

# with open(f"{news}.html", "w") as f:
#     session = HTMLSession()
#     r = session.get(f'http://{news}.com/')
#     f.write(r.html.html)
#     #f.write(requests.get(f"https://www.{news}.com/").text)

with open(f"{news}.html") as f: page = f.read()

soup = BeautifulSoup(page, "html.parser")


print([x.text for x in soup.find_all("a")])
print([x.text for x in soup.find_all("article")])
