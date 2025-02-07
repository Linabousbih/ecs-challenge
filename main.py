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
