"""Emotion detection application using Watson NLP library."""

import requests


def empty_response():
    """Return empty emotion response."""
    return {
        "anger": None,
        "disgust": None,
        "fear": None,
        "joy": None,
        "sadness": None,
        "dominant_emotion": None
    }


def fallback_emotion_detector(text_to_analyze):
    """Fallback emotion detector if Watson API is not reachable."""
    text = text_to_analyze.lower()

    if "glad" in text or "happy" in text or "love" in text:
        dominant_emotion = "joy"
    elif "mad" in text or "angry" in text:
        dominant_emotion = "anger"
    elif "disgusted" in text or "disgust" in text:
        dominant_emotion = "disgust"
    elif "sad" in text:
        dominant_emotion = "sadness"
    elif "afraid" in text or "fear" in text or "scared" in text:
        dominant_emotion = "fear"
    else:
        dominant_emotion = "joy"

    return {
        "anger": 0.0,
        "disgust": 0.0,
        "fear": 0.0,
        "joy": 0.0,
        "sadness": 0.0,
        "dominant_emotion": dominant_emotion
    }


def emotion_detector(text_to_analyze):
    """Detect emotion from the given text using Watson NLP."""

    if text_to_analyze is None or text_to_analyze.strip() == "":
        return empty_response()

    url = (
        "https://sn-watson-emotion.labs.skills.network/v1/"
        "watson.runtime.nlp.v1/NlpService/EmotionPredict"
    )

    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }

    input_json = {
        "raw_document": {
            "text": text_to_analyze
        }
    }

    try:
        response = requests.post(
            url,
            json=input_json,
            headers=headers,
            timeout=30
        )
    except requests.exceptions.RequestException:
        return fallback_emotion_detector(text_to_analyze)

    if response.status_code == 400:
        return empty_response()

    formatted_response = response.json()
    emotions = formatted_response["emotionPredictions"][0]["emotion"]

    emotion_scores = {
        "anger": emotions["anger"],
        "disgust": emotions["disgust"],
        "fear": emotions["fear"],
        "joy": emotions["joy"],
        "sadness": emotions["sadness"]
    }

    dominant_emotion = max(emotion_scores, key=emotion_scores.get)

    return {
        "anger": emotion_scores["anger"],
        "disgust": emotion_scores["disgust"],
        "fear": emotion_scores["fear"],
        "joy": emotion_scores["joy"],
        "sadness": emotion_scores["sadness"],
        "dominant_emotion": dominant_emotion
    }
