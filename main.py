from data_loader import load_data, group_judges, divide_posters
from judge_assignment import assign_judges
from optimizer import simulated_annealing_swap
from db_handler import populate_db  # Import the DB population function
from matching import scrape_professor_data, compute_match_score  # Import matching functions
import pandas as pd
import torch  # ✅ Add missing import
from outputs import save_final_assignments, save_judges_with_posters, save_poster_judge_matrix
from sentence_transformers import SentenceTransformer  # ✅ Import model

# File paths
# judges_file = "data/Example_list_judges.xlsx"
# posters_file = "data/Sample_input_abstracts.xlsx"

# Load data
print("Loading data, please wait...")
judges_df, posters_df, judge_full_names = load_data("data/Example_list_judges.xlsx", "data/Sample_input_abstracts.xlsx")
first_primary, first_backup, second_primary, second_backup = group_judges(judges_df)
first_hour_posters, second_hour_posters = divide_posters(posters_df)

# Scrape Professor Research Interests
print("Matching professors, please wait...")
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
print("Optimizing match, please wait...")
final_assignments = simulated_annealing_swap(assignments)

# Debugging: Display final assignments
print("=== Final Assignments ===")
for poster_id, judges in final_assignments.items():
    print(f"Poster {poster_id}: Judges {judges}")

# Debugging: Display judge full names
print("\n=== Judge Full Names ===")
for key, name in judge_full_names.items():
    print(f"{key}: {name}")

# Check for any fallback judge entries
fallback_entries = [poster for poster, judges in final_assignments.items() if "Fallback Judge" in judges]
if fallback_entries:
    print("\nWARNING: Fallback Judge found in assignments for posters:", fallback_entries)
else:
    print("\nNo Fallback Judge entries found.")


# Populate MongoDB
# After computing final_assignments and precomputing professor_embeddings, professor_names, etc.
populate_db(final_assignments, judge_full_names, posters_df, professor_embeddings, professor_names)


# Export Excel files using our dedicated functions:
save_final_assignments(posters_df, final_assignments, judge_full_names)
save_judges_with_posters(judges_df, final_assignments, posters_df)
save_poster_judge_matrix(posters_df, judges_df, final_assignments)

