import requests

URL = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
HEADERS = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

def emotion_detector(text_to_analyse):

    try:
        # Check if input is empty before making API call
        if not text_to_analyse.strip():
            return {
                "anger": None,
                "disgust": None,
                "fear": None,
                "joy": None,
                "sadness": None,
                "dominant_emotion": None
            }

        response = requests.post(
            URL,
            headers=HEADERS,
            json={"raw_document": { "text": text_to_analyse }}
        )

        if response.status_code == 200:
            emotions = response.json()
            emotions_scores = emotions['emotionPredictions'][0]['emotion']

            # Determine dominant emotion
            dominant_emotion = max(emotions_scores, key=emotions_scores.get)
            emotions_scores.update({'dominant_emotion': dominant_emotion})

            return emotions_scores

        elif response.status_code == 400:
            # Return all None values if API returns bad request
            return {
                "anger": None,
                "disgust": None,
                "fear": None,
                "joy": None,
                "sadness": None,
                "dominant_emotion": None
            }

        else:
            return {"error": f"API request failed with status code {response.status_code}"}

    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
