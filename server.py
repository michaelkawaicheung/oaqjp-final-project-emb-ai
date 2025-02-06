"""
Flask API for Emotion Detection.
This application processes text input and returns the dominant emotion.
"""
from flask import Flask, request, jsonify, render_template
from EmotionDetection.emotion_detection import emotion_detector  # Import function

app = Flask(__name__)

@app.route('/')
def index():
    """Render the frontend UI from index.html."""
    return render_template('index.html')  # Load the frontend UI

@app.route('/emotionDetector')
def detect_emotion():
    """Process the text input and return the detected emotions."""
    try:

        text_to_analyse = request.args.get("textToAnalyze")

        # Get emotion analysis
        emotions = emotion_detector(text_to_analyse)

        # Handle invalid text
        if emotions["dominant_emotion"] is None:
            return jsonify({"error": "Invalid text! Please try again!"})

        # Format output for frontend
        formatted_response = (
            f"For the given statement, the system response is "
            f"'anger': {emotions['anger']}, 'disgust': {emotions['disgust']}, "
            f"'fear': {emotions['fear']}, 'joy': {emotions['joy']} and "
            f"'sadness': {emotions['sadness']}. "
            f"The dominant emotion is {emotions['dominant_emotion']}."
        )

        return jsonify({"response": formatted_response})

    except KeyError as e:
        return jsonify({"error": f"Missing data in response: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
