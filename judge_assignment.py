from matching import compute_match_score

def assign_judges(posters, primary, backup, judge_full_names, professor_embeddings, professor_names):
    """Assign judges to posters while ensuring advisors are not assigned."""
    assignments = {}

    # Normalize judge names for comparison
    judge_full_names = {str(k).strip().lower(): str(v).strip() for k, v in judge_full_names.items()}

    for _, poster in posters.iterrows():
        poster_id = poster["Poster #"]
        advisor_full = f"{poster['Advisor FirstName'].strip().lower()} {poster['Advisor LastName'].strip().lower()}"

        # Compute match scores
        match_scores = compute_match_score(poster["Abstract"], professor_embeddings, professor_names)

        # Filter out the advisor and judges who already reached 6 assignments
        filtered_candidates = [
            (j, score) for j, score in match_scores 
            if judge_full_names.get(j.lower(), "") != advisor_full and j in primary and len(primary[j]) < 6
        ]
        
        # Sort by highest match score
        sorted_candidates = sorted(filtered_candidates, key=lambda x: x[1], reverse=True)

        # If not enough candidates, pull from backup
        if len(sorted_candidates) < 2:
            backup_candidates = [
                (j, score) for j, score in match_scores 
                if judge_full_names.get(j.lower(), "") != advisor_full and j in backup and len(backup[j]) < 6
            ]
            sorted_candidates += sorted(backup_candidates, key=lambda x: x[1], reverse=True)

        # Ensure exactly 2 judges are assigned
        while len(sorted_candidates) < 2:
            sorted_candidates.append(("Fallback Judge", 0.0))  # Add a dummy fallback judge if needed

        selected = [sorted_candidates[0][0], sorted_candidates[1][0]]

        # Assign judges and update their lists
        assignments[poster_id] = selected
        for judge in selected:
            if judge in primary:
                primary[judge].append(poster_id)
                if len(primary[judge]) >= 6:
                    del primary[judge]  # Remove from primary when full
            elif judge in backup:
                backup[judge].append(poster_id)
                if len(backup[judge]) >= 6:
                    del backup[judge]  # Remove from backup when full

        # If primary is empty, swap with backup
        if len(primary) == 0:
            primary, backup = backup, {}  # Backup becomes primary, reset backup

    return assignments
