import requests
import jsondef emotion_detector(text_to_analyze):
    URL = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = { "raw_document": { "text": text_to_analyze } }

    try:
        response = requests.post(URL, json=input_json, headers=header)
        if response.status_code == 200:
            formated_response = json.loads(response.text)
            return formated_response
        elif response.status_code == 400:
            print("Error 400: Bad Request - The input was invalid.")
            return {
                'anger': None,
                'disgust': None, 
                'fear': None, 
                'joy': None, 
                'sadness': None, 
                'dominant_emotion': None
            }
        else:
            print(f"Error {response.status_code}: {response.text}")
            return {
                'anger': None,
                'disgust': None, 
                'fear': None, 
                'joy': None, 
                'sadness': None, 
                'dominant_emotion': None
            }
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return {
            'anger': None,
            'disgust': None, 
            'fear': None, 
            'joy': None, 
            'sadness': None, 
            'dominant_emotion': None
        }

def emotion_predictor(detected_text):
    try:
        if all(value is None for value in detected_text.values()):
            return detected_text
        
        if detected_text.get('emotionPredictions') is not None and len(detected_text['emotionPredictions']) > 0:
            emotions = detected_text['emotionPredictions'][0].get('emotion', {})

            anger = emotions.get('anger', None)
            disgust = emotions.get('disgust', None)
            fear = emotions.get('fear', None)
            joy = emotions.get('joy', None)
            sadness = emotions.get('sadness', None)

            max_emotion = max(emotions, key=emotions.get) if emotions else None

            formated_dict_emotions = {
                'anger': anger,
                'disgust': disgust,
                'fear': fear,
                'joy': joy,
                'sadness': sadness,
                'dominant_emotion': max_emotion
            }
            return formated_dict_emotions
        else:
            print("No emotion predictions found.")
            return {
                'anger': None,
                'disgust': None, 
                'fear': None, 
                'joy': None, 
                'sadness': None, 
                'dominant_emotion': None
            }

    except Exception as e:
        # Catch any other unexpected errors
        print(f"Error processing emotions: {e}")
        return {
            'anger': None,
            'disgust': None, 
            'fear': None, 
            'joy': None, 
            'sadness': None, 
            'dominant_emotion': None
        }
