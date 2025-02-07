# judge_assignment.py
from matching import compute_match_score

def assign_judges(posters, primary, backup, judge_full_names):
    """Assigns judges to posters while ensuring advisors are not assigned."""
    assignments = {}

    for _, poster in posters.iterrows():
        poster_id = poster["Poster #"]
        advisor_full = f"{poster['Advisor FirstName'].strip()} {poster['Advisor LastName'].strip()}"

        # Ensure enough judges in primary list
        if len(primary) < 2:
            if len(primary) == 0:
                primary = backup.copy()
                backup.clear()
            elif len(primary) == 1:
                backup.update(primary)
                primary = backup.copy()
                backup.clear()

        # Filter out advisor and sort by match score
        primary_candidates = sorted(
            [(j, compute_match_score(j, poster_id)) for j in primary if judge_full_names[j].lower() != advisor_full.lower()],
            key=lambda x: x[1], reverse=True
        )

        if len(primary_candidates) >= 2:
            selected = [primary_candidates[0][0], primary_candidates[1][0]]
        else:
            backup_candidates = sorted(
                [(j, compute_match_score(j, poster_id)) for j in backup if judge_full_names[j].lower() != advisor_full.lower()],
                key=lambda x: x[1], reverse=True
            )
            selected = primary_candidates + backup_candidates

            if len(selected) < 2:
                selected += sorted(
                    [(j, compute_match_score(j, poster_id)) for j in (primary | backup) if judge_full_names[j].lower() != advisor_full.lower()],
                    key=lambda x: x[1], reverse=True
                )

            selected = [selected[0][0], selected[1][0]]

        assignments[poster_id] = selected

        # Update lists
        for j in selected:
            if j in primary:
                primary[j].append(poster_id)
                if len(primary[j]) >= 6:
                    del primary[j]
            elif j in backup:
                backup[j].append(poster_id)
                if len(backup[j]) >= 6:
                    del backup[j]
            if j in primary:
                backup[j] = primary.pop(j)

    return assignments

if __name__ == "__main__":
    print("Judge assignment functions ready.")
