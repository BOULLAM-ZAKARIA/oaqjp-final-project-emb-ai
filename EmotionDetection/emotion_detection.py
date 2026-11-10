"""Emotion detection using Watson NLP."""

import json
import requests


def emotion_detector(text_to_analyze):
    """Return emotion scores and dominant emotion."""

    url = (
        "https://sn-watson-emotion.labs.skills.network/"
        "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    )

    headers = {
        "grpc-metadata-mm-model-id":
        "emotion_aggregated-workflow_lang_en_stock"
    }

    emotions = ["anger", "disgust", "fear", "joy", "sadness"]

    if not text_to_analyze or not text_to_analyze.strip():
        return {
            **dict.fromkeys(emotions),
            "dominant_emotion": None
        }

    payload = {
        "raw_document": {"text": text_to_analyze}
    }

    response = requests.post(
        url, headers=headers, json=payload, timeout=30
    )

    if response.status_code == 400:
        return {
            **dict.fromkeys(emotions),
            "dominant_emotion": None
        }

    response.raise_for_status()

    data = json.loads(response.text)

    scores = data["emotionPredictions"][0]["emotion"]

    result = {
        "anger": scores["anger"],
        "disgust": scores["disgust"],
        "fear": scores["fear"],
        "joy": scores["joy"],
        "sadness": scores["sadness"]
    }

    result["dominant_emotion"] = max(
        result, key=result.get
    )

    return result
