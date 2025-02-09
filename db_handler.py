from pymongo import MongoClient
from matching import compute_match_score  # Your matching function
import pandas as pd

def populate_db(final_assignments, judge_full_names, posters_df, professor_embeddings, professor_names):
    """
    Populates MongoDB with judges and posters after final assignments.
    Ensures only assigned judges' match scores are stored and no judge exceeds 6 posters.
    """
    client = MongoClient("mongodb://localhost:27017/")
    db = client["ResearchDay"]
    judges_collection = db["judges"]
    posters_collection = db["posters"]

    try:
        # Clear existing collections
        judges_collection.delete_many({})
        posters_collection.delete_many({})

        # Track the number of posters assigned to each judge (to enforce the 6-poster limit)
        judge_poster_count = {judge: 0 for judge in judge_full_names.values()}

        # Filter out Fallback Judges and enforce 6-poster limit
        filtered_assignments = {}
        for poster_id, judges in final_assignments.items():
            valid_judges = []
            for judge in judges:
                if judge != "Fallback Judge" and judge_poster_count.get(judge, 0) < 6:
                    valid_judges.append(judge)
                    judge_poster_count[judge] += 1  # Increment count
                    if judge_poster_count[judge] == 6:
                        print(f"🔴 Judge {judge} has reached the 6-poster limit and will no longer be assigned.")
            
            # Ensure at most 2 judges per poster
            filtered_assignments[poster_id] = valid_judges[:2]

        # Populate the judges collection
        for judge, full_name in judge_full_names.items():
            assigned_posters = [
                poster_id for poster_id, judges in filtered_assignments.items()
                if full_name in judges
            ]
            judge_data = {
                "username": full_name,
                "password": None,  # Password will be set on first login
                "assigned_posters": assigned_posters
            }
            judges_collection.insert_one(judge_data)

        # Populate the posters collection with **only** final match scores of assigned judges
        for poster_id, judges in filtered_assignments.items():
            # Get the abstract for this poster
            abstract_values = posters_df.loc[posters_df["Poster #"] == poster_id, "Abstract"].values
            abstract = abstract_values[0] if len(abstract_values) > 0 else "No abstract available"

            # Compute match scores **only for assigned judges**
            final_matching_scores = {}
            for judge in judges:
                score = next(
                    (s for j, s in compute_match_score(abstract, professor_embeddings, professor_names) if j == judge),
                    None
                )
                final_matching_scores[judge] = score

            poster_data = {
                "poster_id": poster_id,
                "judges": judges,
                "matching_scores": final_matching_scores,  # Only store final scores
                "grades": {judge: None for judge in judges}  # Grades to be filled later
            }
            posters_collection.insert_one(poster_data)

        print("✅ MongoDB populated with final assignments and match scores.")

    except Exception as e:
        print(f"❌ Error populating database: {e}")

    finally:
        client.close()

if __name__ == "__main__":
    populate_db({}, {}, pd.DataFrame(), None, [])
