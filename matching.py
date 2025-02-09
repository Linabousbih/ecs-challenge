import requests
from bs4 import BeautifulSoup
import re
import concurrent.futures
from sentence_transformers import SentenceTransformer, util

PROFESSOR_URL_TEMPLATE = "https://ecs.syracuse.edu/faculty-staff/{first_name}-{last_name}"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

def fetch_professor_page(professor_url):
    """Fetch a professor's individual page and extract research interests."""
    try:
        response = requests.get(professor_url, headers=HEADERS, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract research interests
        interests = "No research interests listed."
        for p in soup.find_all('p'):
            if "research" in p.get_text().lower():
                interests = p.get_text(strip=True)
                break
        return interests
    except requests.RequestException:
        return "No research interests listed."

def scrape_professor_data(judge_full_names):
    """Scrape research interests from the faculty webpage."""
    professors = {}

    try:
        response = requests.get("https://ecs.syracuse.edu/faculty-staff", headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return professors

    soup = BeautifulSoup(response.text, 'html.parser')
    faculty_profiles = soup.find_all('div', class_=re.compile(r'(faculty|profile)', re.IGNORECASE))

    professor_urls = {}
    for profile in faculty_profiles:
        name_tag = profile.find('div', class_='profile-name')
        if not name_tag:
            continue

        name = name_tag.find('a').get_text(strip=True)
        name_parts = name.split()
        if len(name_parts) >= 2:
            first_name = name_parts[0].lower()
            last_name = name_parts[-1].lower()
            professor_url = PROFESSOR_URL_TEMPLATE.format(first_name=first_name, last_name=last_name)
            professor_urls[name] = professor_url

    # Fetch all professor pages in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(fetch_professor_page, professor_urls.values())

    # Assign research interests to professors
    for name, interests in zip(professor_urls.keys(), results):
        if name.lower() in [j.lower() for j in judge_full_names.values()]:
            professors[name] = interests

    return professors





def scrape_research_interests(professor_url):
    """
    Scrape the research interests from a professor's individual page.
    """
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    try:
        response = requests.get(professor_url, headers=headers, timeout=10)
        response.raise_for_status()
        print(f"Successfully fetched {professor_url}")
    except requests.RequestException as e:
        print(f"Error fetching the professor's page {professor_url}: {e}")
        return "No research interests listed."

    soup = BeautifulSoup(response.text, 'html.parser')

    # Print the entire HTML content of the page for inspection (first 2000 characters)
    print(f"Page content for {professor_url}:\n", soup.prettify()[:2000])  # Increased content length for better inspection

    # Try to extract research interests from the page
    interests_section = soup.find_all('p')  # Look for research interests in paragraph tags
    interests = ""
    for p in interests_section:
        print(f"Checking paragraph text: {p.get_text()}")  # Debug: Print paragraph content
        if "research" in p.get_text().lower():  # Searching for research keywords
            interests = p.get_text(strip=True)
            break

    return interests if interests else "No research interests listed."


model = SentenceTransformer('all-MiniLM-L6-v2')

def compute_match_score(abstract, professor_embeddings, professor_names):
    """Compute cosine similarity between poster abstract and professor research interests."""
    abstract_embedding = model.encode(abstract, convert_to_tensor=True)
    similarity_scores = util.pytorch_cos_sim(abstract_embedding, professor_embeddings).flatten()
    return list(zip(professor_names, similarity_scores.tolist()))


