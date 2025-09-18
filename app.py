from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(_name_)
CORS(app)  # Enable CORS for all routes

# File to store orders
ORDERS_FILE = 'orders.json'

# Initialize orders file if it doesn't exist
if not os.path.exists(ORDERS_FILE):
    with open(ORDERS_FILE, 'w') as f:
        json.dump([], f)

@app.route('/')
def home():
    return "STAR TECHNOLOGIES Backend API"

@app.route('/api/products')
def get_products():
    # Product data for STAR TECHNOLOGIES
    products = [
        {
            "id": 1,
            "name": "Wireless Headphones",
            "price": 129.99,
            "currency": "GHc",
            "description": "Premium sound quality with excellent noise cancellation",
            "image": "https://images.unsplash.com/photo-1546868871-7041f2a55e12?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80"
        },
        {
            "id": 2,
            "name": "Smart Watch",
            "price": 199.99,
            "currency": "GHc",
            "description": "Track your fitness and receive quick notifications",
            "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80"
        },
        {
            "id": 3,
            "name": "Ultra-Thin Laptop",
            "price": 8999.99,
            "currency": "GHc",
            "description": "Powerful performance in a lightweight design",
            "image": "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80"
        },
        {
            "id": 4,
            "name": "Wireless Earbuds",
            "price": 89.99,
            "currency": "GHc",
            "description": "Crystal clear audio with long battery life",
            "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80"
        },
        {
            "id": 5,
            "name": "Iphone 17 Pro Max",
            "price": 16999.99,
            "currency": "GHc",
            "description": "High-resolution camera and fast processor and smart AI",
            "image": "https://images.unsplash.com/photo-1485955900006-10f4d324d411?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80"
        },
        {
            "id": 6,
            "name": "Gaming Mouse",
            "price": 79.99,
            "currency": "GHc",
            "description": "Precision control for professional gamers",
            "image": "https://images.unsplash.com/photo-1531297484001-80022131f5a1?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80"
        },
        {
            "id": 7,
            "name": "VR Headset",
            "price": 2999.99,
            "currency": "GHc",
            "description": "Immersive virtual reality experience",
            "image": "https://images.unsplash.com/photo-1585386959984-a4155224a1ad?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80"
        },
        {
            "id": 8,
            "name": "Bluetooth Speaker",
            "price": 79.99,
            "currency": "GHc",
            "description": "360° surround sound with deep bass",
            "image": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80"
        }
    ]
    return jsonify(products)

@app.route('/api/orders', methods=['GET', 'POST'])
def handle_orders():
    if request.method == 'GET':
        # Return all orders
        with open(ORDERS_FILE, 'r') as f:
            orders = json.load(f)
        return jsonify(orders)
    
    elif request.method == 'POST':
        # Create a new order
        order_data = request.json
        
        # Validate required fields
        required_fields = ['customer_name', 'customer_email', 'customer_address', 'customer_phone', 'items']
        for field in required_fields:
            if field not in order_data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Read existing orders
        with open(ORDERS_FILE, 'r') as f:
            orders = json.load(f)
        
        # Add new order
        order_id = len(orders) + 1
        new_order = {
            'id': order_id,
            'status': 'received',
            'order_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            **order_data
        }
        orders.append(new_order)
        
        # Save updated orders
        with open(ORDERS_FILE, 'w') as f:
            json.dump(orders, f, indent=2)
        
        return jsonify({'message': 'Order created successfully', 'order_id': order_id}), 201

@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    with open(ORDERS_FILE, 'r') as f:
        orders = json.load(f)
    
    order = next((o for o in orders if o['id'] == order_id), None)
    
    if order:
        return jsonify(order)
    else:
        return jsonify({'error': 'Order not found'}), 404

if _name_ == '_main_':
    app.run(debug=True, port=5000)