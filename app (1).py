
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/meal-planner')
def meal_planner():
    return render_template('meal_planner.html')

@app.route('/budget-buddy')
def budget_buddy():
    return render_template('budget_buddy.html')

@app.route('/food-games')
def food_games():
    return render_template('food_games.html')

@app.route('/food-chatbot')
def food_chatbot():
    return render_template('food_chatbot.html')
if __name__ == '__main__':
    app.run(debug=True)
