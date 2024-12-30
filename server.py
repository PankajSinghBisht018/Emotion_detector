from flask import Flask, render_template, request, jsonify
from emotiondetector.emotion_detection import emotion_detector, emotion_predictor

app = Flask("Emotion Detection")

def run_emotion_detection():
    app.run(host="0.0.0.0", port=5000)

@app.route("/emotionDetector")
def sent_detector():
    text_to_detect = request.args.get('textToAnalyze')
    if not text_to_detect:
        return jsonify({"error": "No text provided. Please provide some text to analyze."}), 400
    try:
        response = emotion_detector(text_to_detect)
        formated_response = emotion_predictor(response)

        if formated_response['dominant_emotion'] is None:
            return jsonify({"error": "Invalid text! Unable to detect emotions."}), 400
        

        return jsonify({
            "anger": formated_response['anger'],
            "disgust": formated_response['disgust'],
            "fear": formated_response['fear'],
            "joy": formated_response['joy'],
            "sadness": formated_response['sadness'],
            "dominant_emotion": formated_response['dominant_emotion']
        })

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route("/")
def render_index_page():
    return render_template('index.html')

if __name__ == "__main__":
    run_emotion_detection()
