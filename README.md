# --------------------------------------
# Step 1: Set Up MongoDB using Docker
# --------------------------------------

# Ensure you have Docker installed. You can get Docker from: https://www.docker.com/get-started

# Run the following command to start a MongoDB container:
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -v mongodb_data:/data/db \
  mongo:8.0

# This will start MongoDB, bind it to port 27017, and persist the database in a volume called `mongodb_data`.

# --------------------------------------
# Step 2: Install Python Dependencies
# --------------------------------------

# Ensure that Python 3 and pip3 are installed. Then, install the required packages:
pip3 install -r requirements.txt

# Create a `requirements.txt` file with the following content:
# pandas
# numpy
# requests
# beautifulsoup4
# sentence-transformers
# torch
# pymongo
# openpyxl

# This will install necessary libraries such as pandas, numpy, requests, beautifulsoup4, and more.

# --------------------------------------
# Step 3: Running the Application
# --------------------------------------

# Once MongoDB is up and running, and the required Python packages are installed, you can run the application using:
python3 main.py

# --------------------------------------
# Step 4: Branches Overview
# --------------------------------------

# The project is organized into three branches:
# 1. **Main Branch (`main`)**: 
#    - Contains the logic for **Part 1** and **Part 3** of the project:
#      - **Part 1**: Judge assignment based on AI matching, web scraping, and assignment logic.
#      - **Part 3**: Final grading and ranking of posters based on matching scores and grades from judges.
# 2. **UI Branch (`UI`)**: 
#    - Dedicated to building the user interface for interacting with the application.
# 3. **Part 2 Branch (`part 2`)**: 
#    - Focuses on **Part 2**, which includes the **optimization phase** of matching judges to posters based on matching scores.

# --------------------------------------
# Part 1: Loading and Grouping
# --------------------------------------

# Judges and posters are loaded from Excel files. Judges are grouped by their availability (first or second hour) into two dictionaries (`primary` and `backup`).
# Each judge is associated with a list (initially empty) that stores the line numbers of the assigned posters.
# When a judge reaches 6 assignments, they are removed from the pool.

# --------------------------------------
# Part 2: Assignment Logic
# --------------------------------------

# For each poster, we evaluate the candidate judges:
# - First, from the **primary list**, if there are at least two candidates with a match score >= 0.5.
# - If fewer than two are available, we then check the **backup list**, and if necessary, relax the threshold to include all candidates.
# Once judges are assigned, the assignment is recorded, and their list of assigned poster indices is updated.

# If the **primary list** has fewer than 2 judges available, we swap it with the **backup list** and repeat the process.
# Once judges from the **primary list** are assigned, they are moved to the **backup list**.

# --------------------------------------
# Part 3: Swapping Phase
# --------------------------------------

# In a second round, we iterate over pairs of posters and evaluate whether swapping one judge from each poster improves the combined match score.
# If a swap results in a better match, we perform the swap. This process is iterative and helps fine-tune the initial assignments.

# --------------------------------------
# Part 4: Data Storage and Access
# --------------------------------------

# All assignments, posters, judges, and relevant data are stored in a MongoDB database for easy access and management.
# This allows for real-time access to judge assignments, poster details, and professor interactions.
# Using a MongoDB database helps keep track of assignments and makes the process more scalable.

# --------------------------------------
# Part 5: Professor Login and Poster Access
# --------------------------------------

# In addition to the judge assignment and grading system, the application includes a login page for professors. 
# Professors can log in to access only their assigned posters. This ensures that professors have secure access to their relevant data.
# The login page will verify their credentials, and upon successful authentication, it will display the posters assigned to them.

# The login system ensures that only professors can view and grade the posters assigned to them, maintaining confidentiality and access control.
