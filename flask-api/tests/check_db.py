from pymongo import MongoClient

# Replace the MONGODB_URI with your own MongoDB URI
MONGODB_URI = "mongodb+srv://dsti-devops:dsti-devops@cluster0.piza0cu.mongodb.net/?retryWrites=true&w=majority"

# Create a MongoClient object and connect to the MongoDB server
client = MongoClient(MONGODB_URI)

# Get a reference to the database where the user is defined
db = client.get_database("test_db")

# Get a reference to the user
user = db.command("usersInfo", "dsti-devops")

# Check the roles assigned to the user
for role in user["users"][0]["roles"]:
    print(f"Role: {role['role']}, Database: {role['db']}")
