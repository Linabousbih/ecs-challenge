# optimizer.py
import math
import random
from matching import compute_match_score
import copy  # ✅ Use deep copy

def compute_total_score(assignments):
    """Compute total score based on judge-poster match quality (placeholder function)."""
    return sum(random.random() for _ in assignments)  # Replace with actual scoring function

def simulated_annealing_swap(assignments, iterations=1000, initial_temp=1.0, cooling_rate=0.995):
    """Optimize assignments using simulated annealing while ensuring no judge exceeds 6 assignments."""
    judge_poster_count = {judge: sum(judge in judges for judges in assignments.values()) for judge in set(sum(assignments.values(), []))}
    current_solution = assignments.copy()
    best_solution = assignments.copy()
    current_score = best_score = compute_total_score(assignments)
    T = initial_temp
    poster_ids = list(assignments.keys())

    for _ in range(iterations):
        p1, p2 = random.sample(poster_ids, 2)
        idx1, idx2 = random.choice([0, 1]), random.choice([0, 1])

        new_solution = current_solution.copy()
        judge1, judge2 = new_solution[p1][idx1], new_solution[p2][idx2]

        # Ensure the swap doesn't violate the 6-poster limit
        if judge_poster_count[judge1] >= 6 or judge_poster_count[judge2] >= 6:
            continue  # Skip this swap

        # Perform the swap
        new_solution[p1][idx1], new_solution[p2][idx2] = judge2, judge1
        new_score = compute_total_score(new_solution)
        delta = new_score - current_score

        if delta > 0 or math.exp(delta / T) > random.random():
            current_solution = new_solution
            current_score = new_score
            if new_score > best_score:
                best_solution = new_solution
                best_score = new_score

        T *= cooling_rate

    return best_solution
