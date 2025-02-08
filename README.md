# Research Day Judge Assignment

## Explanation
We start with two lists: **primary** and **backup**. The primary list contains the main pool of judges, while the backup list serves as a reserve. The assignment process follows a recursive logic where, if the primary list is empty, we swap it with the backup list and continue. At the end, an AI-based match swapping optimization is performed to improve assignments.

## Loading and Grouping
The judges and posters are loaded from Excel. Judges are grouped by their availability (first or second hour) and stored in dictionaries keyed by JudgeID. Each judge is associated with a list (initially empty) that will store the line numbers of the assigned posters.

## Assignment Logic
For each poster, we first try to pick two judges from the primary dictionary whose match score (using F()) is at least 0.5.

- If there are at least two such judges:
  - We choose the top two based on the match score.
- Otherwise:
  - We then evaluate the backup list (and, if needed, relax the threshold to include all available candidates).

### Flipping Primary and Backup
If the primary list has fewer than 2 judges available, we swap primary and backup and repeat the process. Once judges are assigned, we update their list of assigned poster indices and remove them if they reach 6 assignments. Also, judges selected from primary are moved into the backup list.

## Swapping Phase
A second round iterates over pairs of posters. For each pair, it checks if swapping one judge from each poster would yield a better combined match score. If so, the swap is made. This phase is iterative (up to a fixed number of iterations) and helps fine-tune the initial assignments.

## Logic
1. If primary has fewer than 2 judges, then:
   - If primary is empty, let backup become primary and reset backup.
   - If primary has exactly one judge, merge it into backup and then let backup become primary.
2. Evaluate candidates in primary using F() (consider only those with score >= 0.5)
   - Skip any candidate whose full name equals the poster's advisor.
3. If fewer than 2 primary candidates meet the threshold, then evaluate candidates from backup.
   - If still fewer than 2, relax the threshold by considering all candidates.
4. Record the assignment and update the judge's list with the poster row index.
5. Once a judge is assigned, if from primary, move the judge into backup.
6. Remove any judge (from either dictionary) if they reach 6 assignments.

## Loading and Grouping
Judges and posters are loaded from Excel. Judges are grouped into two dictionaries (primary and backup) by availability for first and second hour using their JudgeID as keys. Each judge’s value is a list that will store poster indices (i.e., the row numbers in the poster file) up to 6 assignments.

## Assignment Logic
For each poster:

1. Check if the primary candidate pool has fewer than 2 judges.
   - If primary is empty, let backup become primary and reset backup.
   - If primary has one judge, add that judge into backup (effectively combining the pools), then set that combined pool as primary and clear backup.
2. Evaluate candidates from primary using the matching function F() (only considering those with a score ≥ 0.5).
3. If there are at least two primary candidates meeting the threshold, select the top two. Otherwise, evaluate candidates from backup (or relax the threshold if needed) to ensure two judges are chosen.
4. After assignment, update each judge’s list. Judges are removed once they reach 6 assignments.
5. Judges assigned from primary are moved to backup.

## Swapping Phase
In a second round, the algorithm iterates over pairs of posters and, for each pair of assigned judges, checks if swapping would improve the combined matching score. If so, the swap is performed.
