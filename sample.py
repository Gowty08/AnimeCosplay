from pymongo import MongoClient
from bson.objectid import ObjectId

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['Anime']
products_collection = db['Products']

# Sample products data
sample_products = [
    {
        "name": "Naruto Uzumaki Costume",
        "description": "Complete outfit with headband and kunai pouch",
        "price": 89.99,
        "image_url": "https://images.unsplash.com/photo-1633332755192-727a05c4013d?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=500&q=80",
        "category": "Costume",
        "series": "Naruto",
        "rating": 4.5,
        "featured": True,
        "in_stock": True,
        "inventory_count": 25
    },
    {
        "name": "Survey Corps Uniform",
        "description": "Authentic Attack on Titan military uniform",
        "price": 129.99,
        "image_url": "https://images.unsplash.com/photo-1519162584292-56dfc9eb5db4?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=500&q=80",
        "category": "Costume",
        "series": "Attack on Titan",
        "rating": 4.0,
        "featured": True,
        "in_stock": True,
        "inventory_count": 15
    },
    {
        "name": "Izuku Midoriya Costume",
        "description": "UA High School uniform with mask",
        "price": 79.99,
        "image_url": "https://images.unsplash.com/photo-1561047029-3000c68339ca?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=500&q=80",
        "category": "Costume",
        "series": "My Hero Academia",
        "rating": 4.2,
        "featured": True,
        "in_stock": True,
        "inventory_count": 20
    },
    {
        "name": "Tanjiro Kamado Outfit",
        "description": "Complete Demon Slayer Corps uniform with sword",
        "price": 149.99,
        "image_url": "https://images.unsplash.com/photo-1516633630673-67bbad747022?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=500&q=80",
        "category": "Costume",
        "series": "Demon Slayer",
        "rating": 4.7,
        "featured": True,
        "in_stock": True,
        "inventory_count": 10
    }
]

# Insert sample data
products_collection.insert_many(sample_products)

print("Sample data inserted successfully!")