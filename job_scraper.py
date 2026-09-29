import csv
import requests
from bs4 import BeautifulSoup

URL = "https://realpython.github.io/fake-jobs/"
OUTPUT_FILE = "jobs.csv"


def fetch_page(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.content, "html.parser")
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None


def extract_job(job_element):
    title_el = job_element.find("h2", class_="title")
    company_el = job_element.find("h3", class_="company")
    location_el = job_element.find("p", class_="location")
    links = job_element.find_all("a")

    title = title_el.text.strip() if title_el else ""
    company = company_el.text.strip() if company_el else ""
    location = location_el.text.strip() if location_el else ""
    url = links[1]["href"] if len(links) >= 2 else ""

    if not title:
        return None

    return {
        "title": title,
        "company": company,
        "location": location,
        "url": url
    }


def scrape_jobs(soup):
    results = soup.find(id="ResultsContainer")
    if not results:
        return []

    jobs = []
    for job_el in results.find_all("div", class_="card-content"):
        data = extract_job(job_el)
        if data:
            jobs.append(data)
    return jobs


def save_to_csv(jobs, filename):
    if not jobs:
        print("Tidak ada data")
        return

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "company", "location", "url"])
        writer.writeheader()
        writer.writerows(jobs)

    print(f"Berhasil menyimpan {len(jobs)} job ke {filename}")


if __name__ == "__main__":
    print("Mengambil data...")
    soup = fetch_page(URL)
    if soup:
        jobs = scrape_jobs(soup)
        print(f"Ditemukan {len(jobs)} job")
        save_to_csv(jobs, OUTPUT_FILE)
