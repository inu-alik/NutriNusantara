from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nutrinusantara.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    activity_level = db.Column(db.String(32), nullable=False)
    goal = db.Column(db.String(32), nullable=False)
    calorie_target = db.Column(db.Integer, nullable=True)

class FoodLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.Date, default=datetime.utcnow)
    food_name = db.Column(db.String(128))
    calories = db.Column(db.Float)
    carbs = db.Column(db.Float)
    protein = db.Column(db.Float)
    fat = db.Column(db.Float)

class WeightLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.Date, default=datetime.utcnow)
    weight = db.Column(db.Float)

db.create_all()

def calculate_tdee(gender, weight, height, age, activity_level):
    if gender.lower() == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    activity_factors = {
        "sedentari": 1.2,
        "ringan": 1.375,
        "sedang": 1.55,
        "berat": 1.725
    }
    return int(bmr * activity_factors.get(activity_level.lower(), 1.2))

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    user = User(
        username=data['username'],
        gender=data['gender'],
        age=data['age'],
        weight=data['weight'],
        height=data['height'],
        activity_level=data['activity_level'],
        goal=data['goal']
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Registered successfully", "user_id": user.id}), 201

@app.route('/calorie_target/<int:user_id>', methods=['GET'])
def get_calorie_target(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    tdee = calculate_tdee(user.gender, user.weight, user.height, user.age, user.activity_level)
    if user.goal.lower() == "menurunkan":
        target = tdee - 500
    elif user.goal.lower() == "menaikkan":
        target = tdee + 300
    else:
        target = tdee
    user.calorie_target = target
    db.session.commit()
    return jsonify({"calorie_target": target})

@app.route('/food_log', methods=['POST'])
def add_food_log():
    data = request.json
    food = FoodLog(
        user_id=data['user_id'],
        date=datetime.strptime(data['date'], "%Y-%m-%d"),
        food_name=data['food_name'],
        calories=data['calories'],
        carbs=data.get('carbs', 0),
        protein=data.get('protein', 0),
        fat=data.get('fat', 0)
    )
    db.session.add(food)
    db.session.commit()
    return jsonify({"message": "Food logged"}), 201

@app.route('/food_log/<int:user_id>', methods=['GET'])
def get_food_log(user_id):
    logs = FoodLog.query.filter_by(user_id=user_id).all()
    result = [{
        "date": log.date.strftime("%Y-%m-%d"),
        "food_name": log.food_name,
        "calories": log.calories,
        "carbs": log.carbs,
        "protein": log.protein,
        "fat": log.fat
    } for log in logs]
    return jsonify(result)

@app.route('/weight_log', methods=['POST'])
def add_weight_log():
    data = request.json
    log = WeightLog(
        user_id=data['user_id'],
        date=datetime.strptime(data['date'], "%Y-%m-%d"),
        weight=data['weight']
    )
    db.session.add(log)
    db.session.commit()
    return jsonify({"message": "Weight logged"}), 201

@app.route('/weight_log/<int:user_id>', methods=['GET'])
def get_weight_log(user_id):
    logs = WeightLog.query.filter_by(user_id=user_id).all()
    result = [{
        "date": log.date.strftime("%Y-%m-%d"),
        "weight": log.weight
    } for log in logs]
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
