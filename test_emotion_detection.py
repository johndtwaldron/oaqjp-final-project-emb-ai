from EmotionDetection import emotion_detector

CASES = [
    ("I am glad this happened", "joy"),
    ("I am really mad about this", "anger"),
    ("I feel disgusted just hearing about this", "disgust"),
    ("I am so sad about this", "sadness"),
    ("I am really afraid that this will happen", "fear"),
]

def test_dominant_emotions():
    for text, expected in CASES:
        res = emotion_detector(text)
        assert res["dominant_emotion"] == expected, f"{text} -> {res}"
