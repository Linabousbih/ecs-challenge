# data_loader.py
import pandas as pd

def load_data(judges_file, posters_file):
    """Load judges and posters from Excel files."""
    judges_df = pd.read_excel(judges_file)
    posters_df = pd.read_excel(posters_file)

    # Build a dictionary mapping JudgeID to full name
    judge_full_names = {row["Judge"]: f"{row['Judge FirstName'].strip()} {row['Judge LastName'].strip()}"
                        for _, row in judges_df.iterrows()}

    return judges_df, posters_df, judge_full_names

def group_judges(judges_df):
    """Group judges by availability into primary and backup pools."""
    first_hour_judges_df = judges_df[judges_df["Hour available"].isin([1, "both"])].copy()
    second_hour_judges_df = judges_df[judges_df["Hour available"].isin([2, "both"])].copy()

    def initialize_judge_map(judges):
        return {row["Judge"]: [] for _, row in judges.iterrows()}

    return (
        initialize_judge_map(first_hour_judges_df), {},  # first_primary, first_backup
        initialize_judge_map(second_hour_judges_df), {}  # second_primary, second_backup
    )

def divide_posters(posters_df):
    """Split posters into first and second hour based on odd/even numbering."""
    return (posters_df[posters_df["Poster #"] % 2 == 1].copy(),
            posters_df[posters_df["Poster #"] % 2 == 0].copy())

if __name__ == "__main__":
    print("Data loading functions ready.")
