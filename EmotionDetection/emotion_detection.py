"""Watson Emotion Detection client (with error handling)."""
from typing import Dict, Union, Optional
import requests

WATSON_URL = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
HEADERS = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

Result = Dict[str, Union[float, str, None]]

EMPTY_RESULT: Result = {
    "anger": None,
    "disgust": None,
    "fear": None,
    "joy": None,
    "sadness": None,
    "dominant_emotion": None,
}

def emotion_detector(text_to_analyze: str) -> Result:
    """Return five emotions + 'dominant_emotion'. All None for blank/400/error."""
    # Blank input → immediately return all None
    if not text_to_analyze or not text_to_analyze.strip():
        return EMPTY_RESULT.copy()

    payload = {"raw_document": {"text": text_to_analyze}}
    resp = requests.post(WATSON_URL, headers=HEADERS, json=payload, timeout=10)

    # Per lab: if server returns 400, return all None
    if resp.status_code == 400:
        return EMPTY_RESULT.copy()

    # Parse JSON safely
    try:
        data = resp.json()
    except Exception:
        return EMPTY_RESULT.copy()

    preds = data.get("emotionPredictions", [])
    if not preds:
        return EMPTY_RESULT.copy()

    scores = preds[0].get("emotion", {})
    anger   = float(scores.get("anger", 0.0))
    disgust = float(scores.get("disgust", 0.0))
    fear    = float(scores.get("fear", 0.0))
    joy     = float(scores.get("joy", 0.0))
    sadness = float(scores.get("sadness", 0.0))

    dominant = max(
        ("anger", anger),
        ("disgust", disgust),
        ("fear", fear),
        ("joy", joy),
        ("sadness", sadness),
        key=lambda kv: kv[1],
    )[0]

    return {
        "anger": anger,
        "disgust": disgust,
        "fear": fear,
        "joy": joy,
        "sadness": sadness,
        "dominant_emotion": dominant,
    }
