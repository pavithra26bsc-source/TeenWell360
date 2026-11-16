
from flask import Flask, render_template

app = Flask(__name__)

# Homepage
@app.route('/')
def home():
    return render_template('index.html')

# Meal Planner page
@app.route('/meal_planner')
def meal_planner():
    return render_template('meal_planner.html')

if __name__ == '__main__':
    app.run(debug=True)
