# optimizer.py
import math
import random
from matching import compute_match_score

def compute_total_score(assignments):
    """Compute the total match score of the current assignments."""
    return sum(compute_match_score(judge, poster) for poster, judges in assignments.items() for judge in judges)

def simulated_annealing_swap(assignments, iterations=1000, initial_temp=1.0, cooling_rate=0.995):
    """Optimize assignments using simulated annealing."""
    current_solution = assignments.copy()
    best_solution = assignments.copy()
    current_score = best_score = compute_total_score(assignments)
    T = initial_temp
    poster_ids = list(assignments.keys())

    for _ in range(iterations):
        p1, p2 = random.sample(poster_ids, 2)
        idx1, idx2 = random.choice([0, 1]), random.choice([0, 1])

        new_solution = current_solution.copy()
        new_solution[p1][idx1], new_solution[p2][idx2] = new_solution[p2][idx2], new_solution[p1][idx1]
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

if __name__ == "__main__":
    print("Optimizer functions ready.")
