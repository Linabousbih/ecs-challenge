import pandas as pd
from pymongo import MongoClient

# Weights for the components
w1, w2, w3 = 0.4, 0.4, 0.2  # Adjust these as needed

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["ResearchDay"]
posters_collection = db["posters"]

def calculate_final_grades_and_ranking():
    """
    Calculate the final grades for each poster based on judge grades and matching scores,
    and generate a ranking. Save the results in an Excel file.
    """
    posters = list(posters_collection.find())  # Fetch all posters from the database

    final_grades = []

    for poster in posters:
        poster_id = poster['poster_id']
        judges = poster['judges']
        matching_scores = poster['matching_scores']
        grades = poster['grades']

        # Ensure we have both grades for the poster and both judges
        if len(judges) != 2 or len(grades) != 2:
            continue  # Skip posters with missing judges or grades
        
        judge_1, judge_2 = judges
        grade_1, grade_2 = grades[judge_1], grades[judge_2]
        match_1, match_2 = matching_scores[judge_1], matching_scores[judge_2]

        # Calculate the average matching rate (M)
        average_matching = (match_1 + match_2) / 2

        # Calculate the final grade (G_final) using the formula
        G_final = w1 * grade_1 + w2 * grade_2 + w3 * average_matching

        # Store the final grade and other details
        final_grades.append({
            'poster_id': poster_id,
            'judge_1': judge_1,
            'judge_2': judge_2,
            'G1': grade_1,
            'G2': grade_2,
            'M': average_matching,
            'G_final': G_final
        })

    # Create DataFrame with all final grades and details
    df = pd.DataFrame(final_grades)

    # Sort the posters by final grade (G_final) in descending order to create the ranking
    df['Rank'] = df['G_final'].rank(method='dense', ascending=False).astype(int)

    # Save to Excel
    df.to_excel("data/poster_rankings.xlsx", index=False)
    print("✅ Rankings and final grades saved to data/poster_rankings.xlsx")

# Call the function to calculate final grades, rankings, and save them to Excel
calculate_final_grades_and_ranking()
