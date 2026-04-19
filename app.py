import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///titan_final.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- DATABASE MODELS ---
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    addr = db.Column(db.String(200))
    prefix = db.Column(db.String(10))
    counter = db.Column(db.Integer, default=100)
    items = db.relationship('Item', backref='company', lazy=True)
    sales = db.relationship('Sale', backref='company', lazy=True)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    cost = db.Column(db.Float)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bill_no = db.Column(db.String(50))
    date = db.Column(db.String(20), default=datetime.now().strftime("%Y-%m-%d"))
    grand_total = db.Column(db.Float)
    profit = db.Column(db.Float)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

@app.route('/')
def index():
    if Company.query.count() == 0:
        c = Company(name="TITAN BIZ", addr="Murshidabad", prefix="TTN")
        db.session.add(c)
        db.session.commit()
    
    active_co = Company.query.first()
    today = datetime.now().strftime("%Y-%m-%d")
    today_sales = Sale.query.filter_by(company_id=active_co.id, date=today).all()
    
    stats = {
        "revenue": sum(s.grand_total for s in today_sales),
        "profit": sum(s.profit for s in today_sales),
        "total_sales": len(today_sales)
    }
    return render_template('index.html', co=active_co, all_cos=Company.query.all(), stats=stats)

@app.route('/add-item', methods=['POST'])
def add_item():
    data = request.json
    new_it = Item(name=data['name'], price=data['price'], cost=data['cost'], company_id=data['co_id'])
    db.session.add(new_it)
    db.session.commit()
    return jsonify({"success": True})

@app.route('/save-bill', methods=['POST'])
def save_bill():
    data = request.json
    co = Company.query.get(data['company_id'])
    sale = Sale(bill_no=f"{co.prefix}-{co.counter}", grand_total=data['total'], profit=data['profit'], company_id=co.id)
    co.counter += 1
    db.session.add(sale)
    db.session.commit()
    return jsonify({"success": True})

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
