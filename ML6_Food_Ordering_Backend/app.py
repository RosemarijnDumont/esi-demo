
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food_ordering.db'
db = SQLAlchemy(app)

# --- Database Models ---
class FoodItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    price = db.Column(db.Float, nullable=False)

class OfficeLocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)  # Assuming a simple user ID for now
    location_id = db.Column(db.Integer, db.ForeignKey('office_location.id'), nullable=False)
    order_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    total_amount = db.Column(db.Float, nullable=False)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    food_item_id = db.Column(db.Integer, db.ForeignKey('food_item.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_order = db.Column(db.Float, nullable=False) # Price at the time of order

# --- API Endpoints ---

@app.route('/api/food_items', methods=['GET'])
def get_food_items():
    items = FoodItem.query.all()
    return jsonify([{'id': item.id, 'name': item.name, 'description': item.description, 'price': item.price} for item in items])

@app.route('/api/locations', methods=['GET'])
def get_locations():
    locations = OfficeLocation.query.all()
    return jsonify([{'id': location.id, 'name': location.name, 'address': location.address} for location in locations])

@app.route('/api/order', methods=['POST'])
def submit_order():
    data = request.json

    # Basic validation
    if not all(key in data for key in ['user_id', 'location_id', 'items']):
        return jsonify({'error': 'Missing required fields'}), 400

    user_id = data['user_id']
    location_id = data['location_id']
    order_items_data = data['items']

    if not isinstance(order_items_data, list) or not order_items_data:
        return jsonify({'error': 'Items list cannot be empty'}), 400

    total_amount = 0
    items_to_add = []

    for item_data in order_items_data:
        if not all(key in item_data for key in ['food_item_id', 'quantity']):
            return jsonify({'error': 'Each item must have food_item_id and quantity'}), 400

        food_item_id = item_data['food_item_id']
        quantity = item_data['quantity']

        food_item = FoodItem.query.get(food_item_id)
        if not food_item:
            return jsonify({'error': f'Food item with ID {food_item_id} not found'}), 404
        if quantity <= 0:
            return jsonify({'error': 'Quantity must be positive'}), 400

        item_price = food_item.price * quantity
        total_amount += item_price
        items_to_add.append({
            'food_item_id': food_item_id,
            'quantity': quantity,
            'price_at_order': food_item.price
        })

    # Create new order
    new_order = Order(
        user_id=user_id,
        location_id=location_id,
        total_amount=total_amount
    )
    db.session.add(new_order)
    db.session.commit()
    db.session.refresh(new_order)

    # Add order items
    for item in items_to_add:
        order_item = OrderItem(
            order_id=new_order.id,
            food_item_id=item['food_item_id'],
            quantity=item['quantity'],
            price_at_order=item['price_at_order']
        )
        db.session.add(order_item)
    db.session.commit()

    # --- Vendor Integration (Placeholder) ---
    # In a real application, you would integrate with a vendor system here.
    # This could be a webhook, an email, or a direct API call.
    # For demonstration, we'll just log it.
    print(f"Submitting order {new_order.id} to vendor system. Details: {data}")

    return jsonify({'message': 'Order submitted successfully', 'order_id': new_order.id, 'total_amount': total_amount}), 201

# --- Initialization ---
@app.before_first_request
def create_tables_and_seed_data():
    db.create_all()
    # Seed data if tables are empty
    if not FoodItem.query.first():
        food_items = [
            FoodItem(name='Pizza Margherita', description='Classic cheese pizza', price=12.50),
            FoodItem(name='Vegan Burger', description='Plant-based burger with fries', price=14.00),
            FoodItem(name='Caesar Salad', description='Fresh salad with chicken and croutons', price=10.00),
            FoodItem(name='Sushi Combo', description='Assorted sushi rolls', price=18.75)
        ]
        db.session.add_all(food_items)

    if not OfficeLocation.query.first():
        locations = [
            OfficeLocation(name='Main Office - Floor 1', address='123 ML6 St, Floor 1'),
            OfficeLocation(name='Main Office - Floor 3', address='123 ML6 St, Floor 3'),
            OfficeLocation(name='Annex Building', address='456 ML6 Ave, Annex')
        ]
        db.session.add_all(locations)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)