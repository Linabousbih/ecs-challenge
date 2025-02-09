from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["ResearchDay"]
judges_collection = db["judges"]
posters_collection = db["posters"]

def fetch_judges():
    """
    Fetch all judges from the 'judges' collection.
    """
    judges = list(judges_collection.find())
    return judges

def fetch_posters():
    """
    Fetch all posters from the 'posters' collection.
    """
    posters = list(posters_collection.find())
    return posters

if __name__ == "__main__":
    # Fetch all judges and posters
    judges = fetch_judges()
    posters = fetch_posters()

    # Print the fetched data (you can adjust this part as needed)
    print("Judges:")
    for judge in judges:
        print(judge)

    print("\nPosters:")
    for poster in posters:
        print(poster)
