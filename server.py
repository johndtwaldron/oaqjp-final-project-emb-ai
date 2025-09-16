"""Flask server for Emotion Detection app (Task 7 + GET/POST support)."""
from flask import Flask, request, render_template
from EmotionDetection import emotion_detector

app = Flask(__name__)

@app.get("/")
def index():
    """Render the provided index.html UI."""
    return render_template("index.html")

@app.route("/emotionDetector", methods=["GET", "POST"])
def emotion_detector_route():
    """
    Accept text via GET (?textToAnalyze=...) or POST (form field 'textToAnalyze').
    Return the formatted line required by the rubric, or an error message.
    """
    if request.method == "GET":
        text = (request.args.get("textToAnalyze") or "").strip()
    else:
        text = (request.form.get("textToAnalyze") or "").strip()

    result = emotion_detector(text)

    # Error condition per rubric
    if result["dominant_emotion"] is None:
        return "Invalid text! Please try again!", 200

    formatted = (
        f"For the given statement, the system response is "
        f"'anger': {result['anger']}, 'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, 'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. The dominant emotion is "
        f"{result['dominant_emotion']}."
    )
    return formatted, 200

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
