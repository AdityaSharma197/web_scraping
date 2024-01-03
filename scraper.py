import requests
from lxml import html
import validators


def error_reason(issue):
    if issue == "empty url":
        print("Please enter URL: ")
    elif issue == "invalid url":
        print("Invalid URL. Please try again.")
    else:
        print("Error accessing the website.")


def scrape_project(url):
    try:
        # Validate URL format
        if not validators.url(url):
            error_reason("invalid url")
            return

        # Fetch content
        project_page = requests.get(url)

        # Check for successful response
        if project_page.status_code != 200:
            error_reason("error accessing the website")
            return

        # Parse HTML structure
        structure = html.fromstring(project_page.content)

        # Extract information
        creator = str(structure.xpath(".//*[@id='content-wrap']/section/div/div[2]/div/div/div[2]/span[1]/a/text()")[0]).strip()
        title = str(structure.xpath(".//*[@id='content-wrap']/section/div/div[2]/div/div/div[3]/h2/text()")[0]).strip()
        description = str(structure.xpath(".//*[@id='content-wrap']/section/div/div[2]/div/div/div[3]/p/text()")[0]).strip()
        backers = str(structure.xpath(".//*[@id='backers_count']/text()")[0]).strip()
        backed_amount = str(
            structure.xpath(".//*[@id='content-wrap']/section/div/div[1]/div[2]/div[1]/div[3]/div[1]/span[1]/text()")[0]).strip()
        pledged_amount = str(
            structure.xpath(".//*[@id='content-wrap']/section/div/div[1]/div[2]/div[1]/div[3]/div[1]/span[3]/span[1]/text()")[0]).strip()

        # Calculate and format values
        backed_amount = int(backed_amount[1:].replace(",", ""))
        pledged_amount = int(pledged_amount[1:].replace(",", ""))
        backed_percentage = str(int((backed_amount / pledged_amount) * 100)) + "%"

        # Print results
        print("CREATOR: " + creator)
        print("TITLE: " + title)
        print("DESCRIPTION: " + description)
        print("BACKED AMOUNT: " + backed_amount)
        print("PLEDGED AMOUNT: " + pledged_amount)
        print(backed_percentage + " FUNDED")
        print("BACKED BY: " + backers + " PEOPLE")

    except Exception as e:
        print("Unexpected error:", e)


# Get URL from user
url = input("Enter the URL: ")

# Scrape project information
scrape_project(url)
