import requests
import json

def emotion_detector(text_to_analyze):
    """Calls the Watson Emotion Analysis API and returns emotions with dominant emotion."""
    
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    
    myobj = {"raw_document": {"text": text_to_analyze}}
    
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    
    response = requests.post(url, json=myobj, headers=header)
    
    # Debug prints (helpful during development)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        try:
            # Convert response text to dictionary using json library (as requested)
            formatted_response = json.loads(response.text)
            
            # Extract emotions from the response
            emotions = formatted_response['emotionPredictions'][0]['emotion']
            
            anger = emotions.get('anger', 0)
            disgust = emotions.get('disgust', 0)
            fear = emotions.get('fear', 0)
            joy = emotions.get('joy', 0)
            sadness = emotions.get('sadness', 0)
            
            # Find dominant emotion (highest score)
            emotion_scores = {
                'anger': anger,
                'disgust': disgust,
                'fear': fear,
                'joy': joy,
                'sadness': sadness
            }
            dominant_emotion = max(emotion_scores, key=emotion_scores.get)
            
            return {
                'anger': anger,
                'disgust': disgust,
                'fear': fear,
                'joy': joy,
                'sadness': sadness,
                'dominant_emotion': dominant_emotion
            }
            
        except Exception as e:
            print(f"Error parsing response: {e}")
            return {
                'anger': 0, 'disgust': 0, 'fear': 0, 'joy': 0, 'sadness': 0,
                'dominant_emotion': None
            }
    else:
        print(f"API Error: {response.status_code} - {response.text[:300]}")
        return {
            'anger': 0, 'disgust': 0, 'fear': 0, 'joy': 0, 'sadness': 0,
            'dominant_emotion': None
        }


# For testing when running directly from terminal
if __name__ == "__main__":
    import sys
    text = sys.argv[1] if len(sys.argv) > 1 else "I love this new technology."
    result = emotion_detector(text)
    print(result)