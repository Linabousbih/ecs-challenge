from pymongo import MongoClient
from matching import compute_match_score  # Your matching function that expects: abstract, professor_embeddings, professor_names
import pandas as pd

def populate_db(final_assignments, judge_full_names, posters_df, professor_embeddings, professor_names):
    """
    Populates MongoDB with judges and posters after final assignments.
    For each poster, uses its abstract (from posters_df) and the precomputed professor embeddings
    to compute a matching score for each assigned judge.
    """
    client = MongoClient("mongodb://localhost:27017/")
    db = client["ResearchDay"]
    judges_collection = db["judges"]
    posters_collection = db["posters"]

    # Clear existing collections
    judges_collection.delete_many({})
    posters_collection.delete_many({})

    # Create a filtered version of assignments that excludes any "Fallback Judge"
    filtered_assignments = {}
    for poster_id, judges in final_assignments.items():
        valid_judges = [j for j in judges if j != "Fallback Judge"]
        filtered_assignments[poster_id] = valid_judges

    # Populate the judges collection
    for judge, full_name in judge_full_names.items():
        # Use lower-case for matching to be consistent
        assigned_posters = [
            poster_id 
            for poster_id, judges in filtered_assignments.items()
            if full_name.strip().lower() in [j.strip().lower() for j in judges]
        ]
        judge_data = {
            "username": full_name,
            "password": None,  # Password will be set on first login
            "assigned_posters": assigned_posters
        }
        judges_collection.insert_one(judge_data)

    # Populate the posters collection with matching scores computed using the poster's abstract
    for poster_id, judges in filtered_assignments.items():
        # Look up the abstract for this poster from posters_df
        abstract_values = posters_df.loc[posters_df["Poster #"] == poster_id, "Abstract"].values
        abstract = abstract_values[0] if len(abstract_values) > 0 else "No abstract available"
        # Compute matching scores for each judge assigned to this poster
        matching_scores = {str(judge): compute_match_score(abstract, professor_embeddings, professor_names)
                            for judge in judges}
        poster_data = {
            "poster_id": poster_id,
            "judges": judges,
            "matching_scores": matching_scores,
            "grades": {str(judge): None for judge in judges}  # Grades to be filled later
        }
        posters_collection.insert_one(poster_data)

    print("✅ MongoDB populated with assignments and matching scores.")
    client.close()

if __name__ == "__main__":
    # For testing purposes only; you'll supply proper parameters in main.py
    populate_db({}, {}, pd.DataFrame(), None, [])
