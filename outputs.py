import pandas as pd

def save_final_assignments(posters_df, final_assignments, judge_full_names, output_path="data/final_assignments.xlsx"):
    """
    Saves the final assignments to an Excel file.
    Adds two columns ('Judge1' and 'Judge2') to the posters_df based on final_assignments.
    """
    # Create two new columns for the first and second judge assignment
    posters_df["Judge1"] = [
        judge_full_names.get(final_assignments.get(p, ["N/A", "N/A"])[0], "N/A") 
        for p in posters_df["Poster #"]
    ]
    posters_df["Judge2"] = [
        judge_full_names.get(final_assignments.get(p, ["N/A", "N/A"])[1], "N/A") 
        for p in posters_df["Poster #"]
    ]
    
    posters_df.to_excel(output_path, index=False)
    print(f"✅ Final assignments saved to {output_path}")


def save_judges_with_posters(judges_df, final_assignments, posters_df, output_path="data/judges_with_posters.xlsx"):
    """
    Saves judges with assigned posters to Excel.
    Creates up to 6 columns ('Poster1' ... 'Poster6') for each judge.
    """
    poster_columns = ["Poster1", "Poster2", "Poster3", "Poster4", "Poster5", "Poster6"]
    
    # Initialize poster columns to empty for all judges
    for col in poster_columns:
        judges_df[col] = ""
    
    # Now, assign posters to judges based on final_assignments
    for judge in judges_df["Judge"]:
        # Find posters assigned to this judge
        assigned_posters = [poster for poster, judges in final_assignments.items() if judge in judges]
        
        # Debugging: print the assigned posters for each judge
        print(f"Judge: {judge}, Assigned Posters (IDs): {assigned_posters}")
        
        # Ensure that no more than 6 posters are assigned to a judge
        for i in range(min(len(assigned_posters), 6)):  # Ensure no more than 6 posters per judge
            judges_df.loc[judges_df["Judge"] == judge, poster_columns[i]] = assigned_posters[i]
    
    # Save the updated judges DataFrame to Excel
    judges_df.to_excel(output_path, index=False)
    print(f"✅ Judges with assigned posters saved to {output_path}")




def save_poster_judge_matrix(posters_df, judges_df, final_assignments, output_path="data/poster_judge_matrix.xlsx"):
    """
    Creates a binary matrix with posters as rows and judges as columns,
    where each cell is 1 if the poster was assigned that judge, else 0.
    """
    # Extract unique judge names from the final assignments (these should be judge names, not IDs)
    judge_names = sorted(set(j for judges in final_assignments.values() for j in judges))

    # Create a binary matrix where rows are poster IDs and columns are judge names
    binary_matrix = pd.DataFrame(0, index=posters_df["Poster #"], columns=judge_names)

    # Populate matrix based on final assignments
    for poster, judges in final_assignments.items():
        for judge in judges:
            if judge in binary_matrix.columns:  # Check if the judge is a valid column (judge name)
                binary_matrix.loc[poster, judge] = 1

    # Save the matrix to Excel
    binary_matrix.to_excel(output_path)
    print(f"✅ Poster-Judge matrix saved to {output_path}")

