# Judge-Poster Assignment and Grading System

This project automates the process of assigning judges to posters, optimizing the assignments based on matching scores, and facilitating the grading process.  It leverages AI-driven matching, web scraping, and a user-friendly interface.

## Table of Contents

* [1. Getting Started](#getting-started)
    * [1.1. Prerequisites](#prerequisites)
    * [1.2. Setting up MongoDB with Docker](#setting-up-mongodb-with-docker)
    * [1.3. Installing Python Dependencies](#installing-python-dependencies)
* [2. Running the Application](#running-the-application)
* [3. Project Structure and Branches](#project-structure-and-branches)
* [4. Core Functionality](#core-functionality)
    * [4.1. Part 1: Loading and Grouping Data](#part-1-loading-and-grouping-data)
    * [4.2. Part 2: Initial Assignment Logic](#part-2-initial-assignment-logic)
    * [4.3. Part 3: Optimization Phase (Swapping)](#part-3-optimization-phase-swapping)
    * [4.4. Part 4: Data Storage (MongoDB)](#part-4-data-storage-mongodb)
    * [4.5. Part 5: Professor Login and Poster Access](#part-5-professor-login-and-poster-access)


## 1. Getting Started <a name="getting-started"></a>

### 1.1. Prerequisites <a name="prerequisites"></a>

Before you begin, ensure you have the following installed:

* **Docker:**  [https://www.docker.com/get-started](https://www.docker.com/get-started)
* **Python 3:**  (Check your system's Python version with `python3 --version`)
* **pip3:** (Usually included with Python 3)

### 1.2. Setting up MongoDB with Docker <a name="setting-up-mongodb-with-docker"></a>

1.  Run the following command to start a MongoDB container:

    ```bash
    docker run -d \
      --name mongodb \
      -p 27017:27017 \
      -v mongodb_data:/data/db \
      mongo:8.0
    ```

    This command does the following:
    *   `-d`: Runs the container in detached mode (background).
    *   `--name mongodb`: Gives the container the name "mongodb".
    *   `-p 27017:27017`: Maps port 27017 on the host to port 27017 in the container.
    *   `-v mongodb_data:/data/db`: Creates a volume named `mongodb_data` and mounts it to `/data/db` inside the container, ensuring data persistence.
    *   `mongo:8.0`: Specifies the MongoDB image version 8.0.

### 1.3. Installing Python Dependencies <a name="installing-python-dependencies"></a>

1.  Create a file named `requirements.txt` in the project directory with the following content:

    ```
    pandas
    numpy
    requests
    beautifulsoup4
    sentence-transformers
    torch
    pymongo
    openpyxl
    ```

2.  Install the required packages using pip:

    ```bash
    pip3 install -r requirements.txt
    ```

## 2. Running the Application <a name="running-the-application"></a>

Once MongoDB is running and the Python dependencies are installed, you can run the application:

```bash
python3 main.py
```  <-- **Crucially, there is a newline here now.**

## 3. Project Structure and Branches <a name="project-structure-and-branches"></a>

This project uses a branching strategy for development:

*   **`main` branch:** Contains the core logic for:
    *   Part 1: Judge assignment.
    *   Part 3: Final grading and ranking.
*   **`UI` branch:** Dedicated to user interface development.
*   **`part 2` branch:** Focuses on the optimization phase (Part 2) of matching judges to posters.

## 4. Core Functionality <a name="core-functionality"></a>

### 4.1. Part 1: Loading and Grouping Data <a name="part-1-loading-and-grouping-data"></a>

*   Judges and posters are loaded from Excel files.
*   Judges are grouped by availability (first or second hour) into `primary` and `backup` dictionaries.
*   Each judge has an initially empty list to store assigned poster indices.
*   Judges are removed from the assignment pool after reaching 6 assignments.

### 4.2. Part 2: Initial Assignment Logic <a name="part-2-initial-assignment-logic"></a>

For each poster:

*   Check the `primary` judge list for at least two candidates with a match score >= 0.5.
*   If fewer than two are available, check the `backup` list, potentially relaxing the threshold.
*   Assign available judges and update their assigned poster indices.
*   If the `primary` list has fewer than 2 judges available, swap it with the `backup` list and repeat.
*   After assigning judges from the `primary` list, move them to the `backup` list.

### 4.3. Part 3: Optimization Phase (Swapping) <a name="part-3-optimization-phase-swapping"></a>

*   Iterate through pairs of posters and evaluate if swapping a judge between them improves the combined match score.
*   Perform swaps that result in better matches. This process refines the initial assignments.

### 4.4. Part 4: Data Storage (MongoDB) <a name="part-4-data-storage-mongodb"></a>

*   Assignments, posters, judges, and related data are stored in a MongoDB database.
*   This facilitates data access, management, and scalability.

### 4.5. Part 5: Professor Login and Poster Access <a name="part-5-professor-login-and-poster-access"></a>

*   The application includes a professor login page.
*   Professors can access only their assigned posters after successful authentication.
*   This ensures data confidentiality and access control.