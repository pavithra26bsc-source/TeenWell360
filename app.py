
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types
import os

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


@app.route('/ask-food-buddy', methods=['POST'])
def ask_food_buddy():

    data = request.get_json(silent=True) or {}
    message = (data.get('message') or '').strip()

    if not message:
        return jsonify({
            "reply": "Please type a question first."
        }), 400

    if len(message) > 1000:
        return jsonify({
            "reply": "Please keep your question under 1000 characters."
        }), 400

    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        return jsonify({
            "reply": "Food Buddy is not connected yet. Please ask the website administrator to configure it."
        }), 503

    client = None

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=message,
            config=types.GenerateContentConfig(
                system_instruction="""
                You are Food Buddy, the nutrition education assistant
                for TeenWell360, a website for adolescents.

                Answer general questions about food, nutrition,
                cooking, food groups and food safety.

                Use simple, friendly and age-appropriate English.
                Keep answers clear and helpful.

                Encourage balanced meals and variety.
                Never encourage skipping meals, restrictive diets,
                weight-loss plans or unhealthy food rules.

                Do not diagnose diseases or prescribe treatment.
                For medical symptoms, allergies or health concerns,
                recommend speaking with a parent or guardian and
                a qualified healthcare professional.

                If a question is unrelated to food or nutrition,
                politely explain that Food Buddy focuses on nutrition.

                Do not invent exact food prices or nutritional values.
                """
            )
        )

        reply = (response.text or "").strip()

        if not reply:
            reply = "Sorry, I couldn't prepare an answer. Please try again."

        return jsonify({"reply": reply})

    except Exception:
        app.logger.exception("Food Buddy Gemini request failed")
        return jsonify({
            "reply": "Sorry! Food Buddy is temporarily unavailable. Please try again later."
        }), 502

    finally:
        if client is not None:
            client.close()


if __name__ == '__main__':
    app.run(debug=False)
    
    
