from pymongo import MongoClient
from matching import compute_match_score  # Import matching function

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["ResearchDay"]
judges_collection = db["judges"]
posters_collection = db["posters"]

def populate_db(final_assignments, judge_full_names):
    """
    Populates MongoDB with judges and posters after final assignments.
    Stores matching scores in the process.
    """
    # Clear existing collections
    judges_collection.delete_many({})
    posters_collection.delete_many({})

    # Store judges
    for judge, full_name in judge_full_names.items():
        assigned_posters = [
            poster_id for poster_id, judges in final_assignments.items() 
            if any(full_name.strip().lower() == judge_full_names[judge].strip().lower() for judge in judges)
        ]

        # Print the assigned posters for debugging
        print(f"Judge: {full_name}, Assigned Posters: {assigned_posters}")

        judge_data = {
            "username": full_name,
            "password": None,  # Password will be set on first login
            "assigned_posters": assigned_posters
        }
        judges_collection.insert_one(judge_data)

    # Store posters with matching scores
    for poster_id, judges in final_assignments.items():
        matching_scores = {str(judge): compute_match_score(judge, poster_id) for judge in judges}
        grades = {str(judge): None for judge in judges}  # Grades will be added later

        poster_data = {
            "poster_id": poster_id,
            "judges": judges,
            "matching_scores": matching_scores,
            "grades": grades
        }
        posters_collection.insert_one(poster_data)

    print("✅ MongoDB populated with assignments and matching scores.")
