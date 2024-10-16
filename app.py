from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    expiry_date = db.Column(db.Date, nullable=False)

@app.route('/')
def index():
    medications = Medication.query.all()
    return render_template('index.html', medications=medications)

@app.route('/add', methods=['GET', 'POST'])
def add_medication():
    if request.method == 'POST':
        name = request.form['name']
        stock = int(request.form['stock'])
        cost = float(request.form['cost'])
        expiry_date = datetime.strptime(request.form['expiry_date'], '%Y-%m-%d').date()

        new_medication = Medication(name=name, stock=stock, cost=cost, expiry_date=expiry_date)
        
        try:
            db.session.add(new_medication)
            db.session.commit()
            flash('Medication added successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding medication: {str(e)}', 'error')

    return render_template('add_medication.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_medication(id):
    medication = Medication.query.get_or_404(id)
    
    if request.method == 'POST':
        medication.name = request.form['name']
        medication.stock = int(request.form['stock'])
        medication.cost = float(request.form['cost'])
        medication.expiry_date = datetime.strptime(request.form['expiry_date'], '%Y-%m-%d').date()

        try:
            db.session.commit()
            flash('Medication updated successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating medication: {str(e)}', 'error')

    return render_template('edit_medication.html', medication=medication)

@app.route('/delete/<int:id>')
def delete_medication(id):
    medication = Medication.query.get_or_404(id)
    
    try:
        db.session.delete(medication)
        db.session.commit()
        flash('Medication deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting medication: {str(e)}', 'error')

    return redirect(url_for('index'))

@app.route('/view/<int:id>')
def view_medication(id):
    medication = Medication.query.get_or_404(id)
    return render_template('view_medication.html', medication=medication)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
