# main.py
from data_loader import load_data, group_judges, divide_posters
from judge_assignment import assign_judges
from optimizer import simulated_annealing_swap
import pandas as pd

# File paths
judges_file = "data/Example_list_judges.xlsx"
posters_file = "data/Sample_input_abstracts.xlsx"

# Load data
judges_df, posters_df, judge_full_names = load_data(judges_file, posters_file)
first_primary, first_backup, second_primary, second_backup = group_judges(judges_df)
first_hour_posters, second_hour_posters = divide_posters(posters_df)

# Assign judges
first_assignments = assign_judges(first_hour_posters, first_primary, first_backup, judge_full_names)
second_assignments = assign_judges(second_hour_posters, second_primary, second_backup, judge_full_names)
assignments = {**first_assignments, **second_assignments}

# Optimize assignments
final_assignments = simulated_annealing_swap(assignments)

# Save results
posters_df["Judge1"] = [judge_full_names.get(assignments.get(p, ["N/A", "N/A"])[0], "N/A") for p in posters_df["Poster #"]]
posters_df["Judge2"] = [judge_full_names.get(assignments.get(p, ["N/A", "N/A"])[1], "N/A") for p in posters_df["Poster #"]]
posters_df.to_excel("data/final_assignments.xlsx", index=False)

print("Final assignments saved to data/final_assignments.xlsx")

# ----- 2️⃣ Save Judges with Assigned Posters -----
# Create 6 new columns (Poster1 to Poster6) in judges_df
poster_columns = ["Poster1", "Poster2", "Poster3", "Poster4", "Poster5", "Poster6"]
for col in poster_columns:
    judges_df[col] = ""

# Populate poster assignments for each judge
for judge_id in judges_df["Judge"]:
    assigned_posters = []
    for poster, judges in final_assignments.items():
        if judge_id in judges:
            assigned_posters.append(poster)
    
    # Fill the first 6 poster assignment slots
    for i in range(min(len(assigned_posters), 6)):
        judges_df.loc[judges_df["Judge"] == judge_id, poster_columns[i]] = assigned_posters[i]

# Save the updated judges file
judges_df.to_excel("data/judges_with_posters.xlsx", index=False)
print("✅ Judges with assigned posters saved to data/judges_with_posters.xlsx")

# ----- 3️⃣ Create and Save Poster-Judge Binary Matrix -----
# Get unique judge IDs and poster numbers
judge_ids = sorted(judges_df["Judge"].unique())
poster_numbers = sorted(posters_df["Poster #"].unique())

# Create an empty DataFrame with judges as columns and posters as rows
binary_matrix = pd.DataFrame(0, index=poster_numbers, columns=judge_ids)

# Fill the matrix: 1 if a judge was assigned to a poster, 0 otherwise
for poster, judges in final_assignments.items():
    for judge in judges:
        binary_matrix.loc[poster, judge] = 1

# Save the binary matrix
binary_matrix.to_excel("data/poster_judge_matrix.xlsx")
print("✅ Poster-Judge matrix saved to data/poster_judge_matrix.xlsx")