import requests
import json

def emotion_detector(text_to_analyze):
    """Calls the Watson Emotion Analysis API and returns the dominant emotion + score."""
    
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    
    myobj = {"raw_document": {"text": text_to_analyze}}
    
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    
    response = requests.post(url, json=myobj, headers=header)
    
    # Debug: Print status and response (very useful in Coursera labs)
    print(f"Status Code: {response.status_code}")
    print(f"Raw Response: {response.text[:500]}...")  # First 500 chars
    
    if response.status_code == 200:
        try:
            formatted_response = response.json()
            
            # Extract the emotions
            emotions = formatted_response['emotionPredictions'][0]['emotion']
            
            # Find the dominant emotion (highest score)
            dominant_emotion = max(emotions, key=emotions.get)
            score = emotions[dominant_emotion]
            
            return {
                'label': dominant_emotion,   # e.g., 'joy'
                'score': score
            }
            
        except Exception as e:
            print(f"Error parsing response: {e}")
            return {'label': None, 'score': None}
    else:
        print(f"API Error: {response.status_code}")
        return {'label': None, 'score': None}


# For testing when running directly
if __name__ == "__main__":
    import sys
    text = sys.argv[1] if len(sys.argv) > 1 else "I love this new technology."
    result = emotion_detector(text)
    print(result)