from matching import compute_match_score
def assign_judges(posters, primary, backup, judge_full_names, professor_embeddings, professor_names):
    """Assigns judges to posters while ensuring advisors are not assigned and no judge exceeds 6 assignments."""
    assignments = {}
    judge_poster_count = {judge: 0 for judge in judge_full_names.values()}  # Track poster count per judge

    for _, poster in posters.iterrows():
        poster_id = poster["Poster #"]
        advisor_full = f"{poster['Advisor FirstName'].strip()} {poster['Advisor LastName'].strip()}"

        match_scores = compute_match_score(poster["Abstract"], professor_embeddings, professor_names)

        # Filter out advisor and judges who already have 6 posters
        filtered_candidates = [
            (j, score) for j, score in match_scores 
            if judge_full_names.get(j.lower(), "") != advisor_full and judge_poster_count.get(j, 0) < 6
        ]

        # Sort candidates by highest match score
        sorted_candidates = sorted(filtered_candidates, key=lambda x: x[1], reverse=True)

        # Select top 2 judges (if available)
        selected = []
        for judge, _ in sorted_candidates:
            if len(selected) < 2:
                selected.append(judge)
                judge_poster_count[judge] += 1
                if judge_poster_count[judge] == 6:
                    print(f"🔴 Judge {judge} has reached the 6-poster limit and will no longer be assigned.")

        # If no valid judges, assign fallback
        if len(selected) < 2:
            selected.append("Fallback Judge")
        if len(selected) < 2:
            selected.append("Fallback Judge")

        assignments[poster_id] = selected[:2]  # Ensure we return exactly 2 judges

    return assignments
