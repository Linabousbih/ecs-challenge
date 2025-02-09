import pandas as pd
import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer, util
import re

url = "https://ecs.syracuse.edu/faculty-staff"

def scrape_professor_data(url):
    """
    Scrape professor data (name and research interests) from the provided URL.
    """
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an error for bad HTTP responses
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    professors = []
    faculty_profiles = soup.find_all('div', class_=re.compile(r'(faculty|profile)', re.IGNORECASE))

    for profile in faculty_profiles:
        name_tag = profile.find(re.compile(r'(h3|h2|h4)'))  # Trying multiple header tags
        name = name_tag.get_text(strip=True) if name_tag else "Unknown"

        # Improve the extraction of research interests by searching for better indicators
        interests_section = profile.find('p')  # Look for paragraph tags after name
        interests = interests_section.get_text(strip=True) if interests_section else "No interests listed"

        professors.append((name, interests))

    return professors


def compute_match_score(abstract, professor_data):
    """
    Compute text similarity between poster abstract and professor research interests using Sentence Transformers.
    """
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Combine abstract and professor interests for embedding
    texts = [abstract] + [prof[1] for prof in professor_data]
    embeddings = model.encode(texts, convert_to_tensor=True)

    # Compute similarity scores between abstract and each professor
    similarity_scores = util.pytorch_cos_sim(embeddings[0], embeddings[1:]).flatten()

    return list(zip([prof[0] for prof in professor_data], similarity_scores.tolist()))


def fetch_abstract_from_excel(file_path, sheet_name='Sheet1', column_name='abstract_text'):
    """
    Fetch the abstract from the Excel file.
    :param file_path: Path to the Excel file.
    :param sheet_name: Name of the sheet containing the abstract.
    :param column_name: Column name containing the abstract.
    :return: The abstract text.
    """
    try:
        # Read Excel file
        df = pd.read_excel(file_path, sheet_name=sheet_name)

        # Fetch abstract text (assuming only one row and column)
        abstract = df[column_name].iloc[0]  # Adjust the row index as necessary

        return abstract if pd.notna(abstract) else "No abstract found."
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return "No abstract found."


if __name__ == "__main__":
    # Path to the Excel file
    file_path = 'abstracts.xlsx'  # Replace with the actual path to your Excel file

    # Fetch the abstract from the Excel file
    abstract = fetch_abstract_from_excel(file_path)

    if abstract == "No abstract found.":
        print(abstract)
    else:
        # Scrape professor data
        professor_data = scrape_professor_data(url)

        if professor_data:
            # Compute match scores between the abstract and professor research interests
            match_scores = compute_match_score(abstract, professor_data)
            sorted_matches = sorted(match_scores, key=lambda x: x[1], reverse=True)

            # Print top matches
            print("Top Matches:")
            for name, score in sorted_matches[:5]:
                print(f"Professor: {name}, Score: {score:.2f}")
        else:
            print("No professor data found.")
