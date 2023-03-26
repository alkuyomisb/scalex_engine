import requests
from bs4 import BeautifulSoup

# Define the Instagram account username
username = "gadgets_om"

# Make a request to the Instagram account page
url = f"https://www.instagram.com/{username}/"
response = requests.get(url)

# Parse the HTML response using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find all the links to posts on the account page
post_links = []
for link in soup.find_all("a"):
    href = link.get("href")
    if "/p/" in href:
        post_links.append(href)

# Print the list of post links
print(post_links)
