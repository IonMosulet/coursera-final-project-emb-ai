"""
Flask web application for Emotion Detection.
Route is exactly /emotionDetector and output matches customer's requested format.
"""

from flask import Flask, render_template, request
import json

from EmotionDetection.emotion_detection import emotion_detector

HOST: str = "0.0.0.0"
PORT: int = 5000

app = Flask("Emotion Detector")


@app.route("/emotionDetector")
def emotion_detection_route():
    """Return emotion detection result in the exact format requested by the customer."""
    text_to_analyze = request.args.get("textToAnalyze")

    if not text_to_analyze or not text_to_analyze.strip():
        return "No text provided. Please provide valid text (e.g., 'I love my life')."

    response = emotion_detector(text_to_analyze)

    if not isinstance(response, dict) or "dominant_emotion" not in response:
        return "Invalid input! Please try again."

    # 1. First part - "Let's say that you want to evaluate..." + pretty JSON
    json_output = json.dumps(response, indent=2)

    intro = (
        f"Let's say that you want to evaluate the statement {text_to_analyze}. "
        f"The statement is processed as follows:\n\n{json_output}"
    )

    # 2. Second part - summary sentence
    anger = response.get("anger", 0)
    disgust = response.get("disgust", 0)
    fear = response.get("fear", 0)
    joy = response.get("joy", 0)
    sadness = response.get("sadness", 0)
    dominant = response["dominant_emotion"]

    summary = (
        f"For the given statement, the system response is 'anger': {anger}, "
        f"'disgust': {disgust}, 'fear': {fear}, 'joy': {joy} and "
        f"'sadness': {sadness}. The dominant emotion is {dominant}."
    )

    # Combine both parts exactly as requested
    return f"{intro}\n\n{summary}"


@app.route("/")
def render_index_page():
    """Render the main homepage."""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)