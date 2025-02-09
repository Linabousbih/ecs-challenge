from data_loader import load_data, group_judges, divide_posters
from judge_assignment import assign_judges
from optimizer import simulated_annealing_swap
from db_handler import populate_db  # Import the DB population function
from matching import scrape_professor_data, compute_match_score  # Import matching functions
import pandas as pd
import torch  # ✅ Add missing import
from sentence_transformers import SentenceTransformer  # ✅ Import model

# File paths
# judges_file = "data/Example_list_judges.xlsx"
# posters_file = "data/Sample_input_abstracts.xlsx"

# Load data
judges_df, posters_df, judge_full_names = load_data("data/Example_list_judges.xlsx", "data/Sample_input_abstracts.xlsx")
first_primary, first_backup, second_primary, second_backup = group_judges(judges_df)
first_hour_posters, second_hour_posters = divide_posters(posters_df)

# Scrape Professor Research Interests
professor_data = scrape_professor_data(judge_full_names)
if not professor_data:
    print("No professor data found. Exiting process.")
    exit()

# Precompute Professor Embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')
professor_names = list(professor_data.keys())
professor_texts = list(professor_data.values())
professor_embeddings = model.encode(professor_texts, convert_to_tensor=True)

# Assign Judges Using AI-Based Matching
first_assignments = assign_judges(first_hour_posters, first_primary, first_backup, judge_full_names, professor_embeddings, professor_names)
second_assignments = assign_judges(second_hour_posters, second_primary, second_backup, judge_full_names, professor_embeddings, professor_names)
assignments = {**first_assignments, **second_assignments}

# Optimize Assignments
final_assignments = simulated_annealing_swap(assignments)

# Populate MongoDB
populate_db(final_assignments, judge_full_names)

# -------------------------------
# ✅ Save Final Assignments to Excel
# -------------------------------
posters_df["Judge1"] = [judge_full_names.get(final_assignments.get(p, ["N/A", "N/A"])[0], "N/A") for p in posters_df["Poster #"]]
posters_df["Judge2"] = [judge_full_names.get(final_assignments.get(p, ["N/A", "N/A"])[1], "N/A") for p in posters_df["Poster #"]]
posters_df.to_excel("data/final_assignments.xlsx", index=False)

print("✅ Final assignments saved to data/final_assignments.xlsx")

# -------------------------------
# ✅ Save Judges with Assigned Posters
# -------------------------------
poster_columns = ["Poster1", "Poster2", "Poster3", "Poster4", "Poster5", "Poster6"]
for col in poster_columns:
    judges_df[col] = ""

for judge_id in judges_df["Judge"]:
    assigned_posters = [poster for poster, judges in final_assignments.items() if judge_id in judges]

    for i in range(min(len(assigned_posters), 6)):
        judges_df.loc[judges_df["Judge"] == judge_id, poster_columns[i]] = assigned_posters[i]

judges_df.to_excel("data/judges_with_posters.xlsx", index=False)
print("✅ Judges with assigned posters saved to data/judges_with_posters.xlsx")

# -------------------------------
# ✅ Create and Save Poster-Judge Binary Matrix
# -------------------------------
judge_ids = sorted(judges_df["Judge"].unique())
poster_numbers = sorted(posters_df["Poster #"].unique())

binary_matrix = pd.DataFrame(0, index=poster_numbers, columns=judge_ids)

for poster, judges in final_assignments.items():
    for judge in judges:
        binary_matrix.loc[poster, judge] = 1

binary_matrix.to_excel("data/poster_judge_matrix.xlsx")
print("✅ Poster-Judge matrix saved to data/poster_judge_matrix.xlsx")
