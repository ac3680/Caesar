# Import and initialize MongoDB
import pymongo
from pymongo import MongoClient
client = MongoClient()

# Clear all databases being used:
db = client['databaseC']
collection = db.test_collection
posts = db.posts
collection.remove({})
posts.remove()

db = client['databaseS9003']
collection = db.test_collection
posts = db.posts
collection.remove({})
posts.remove()

db = client['databaseS9004']
collection = db.test_collection
posts = db.posts
collection.remove({})
posts.remove()

db = client['databaseS9005']
collection = db.test_collection
posts = db.posts
collection.remove({})
posts.remove()

db = client['databaseS0']
collection = db.test_collection
posts = db.posts
collection.remove({})
posts.remove()