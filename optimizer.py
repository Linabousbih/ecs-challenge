# optimizer.py
import math
import random
from matching import compute_match_score
import copy  # ✅ Use deep copy

def compute_total_score(assignments):
    """Compute total score based on judge-poster match quality (placeholder function)."""
    return sum(random.random() for _ in assignments)  # Replace with actual scoring function

def simulated_annealing_swap(assignments, iterations=1000, initial_temp=1.0, cooling_rate=0.995):
    """Optimize assignments using simulated annealing."""
    current_solution = copy.deepcopy(assignments)  # ✅ Use deep copy to avoid modifying original lists
    best_solution = copy.deepcopy(assignments)
    current_score = best_score = compute_total_score(assignments)
    T = initial_temp
    poster_ids = list(assignments.keys())

    for _ in range(iterations):
        # Select two distinct posters
        p1, p2 = random.sample(poster_ids, 2)

        # ✅ Ensure both posters have at least 2 judges before swapping
        if len(current_solution[p1]) < 2 or len(current_solution[p2]) < 2:
            continue  # Skip iteration if either poster has fewer than 2 judges

        # Select random judge index (0 or 1) in each poster
        idx1, idx2 = random.choice([0, 1]), random.choice([0, 1])

        # ✅ Perform a deep copy before swapping
        new_solution = copy.deepcopy(current_solution)
        new_solution[p1][idx1], new_solution[p2][idx2] = new_solution[p2][idx2], new_solution[p1][idx1]

        # Compute new score
        new_score = compute_total_score(new_solution)
        delta = new_score - current_score

        # Accept better solutions or probabilistically accept worse solutions
        if delta > 0 or math.exp(delta / T) > random.random():
            current_solution = new_solution
            current_score = new_score
            if new_score > best_score:
                best_solution = new_solution
                best_score = new_score

        # Cool down temperature
        T *= cooling_rate

    return best_solution

