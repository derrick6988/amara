from enum import Enum
from typing import List, Tuple, Dict

class EmotionType(Enum):
    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    CURIOUS = "curious"
    CONFUSED = "confused"
    CALM = "calm"
    NEUTRAL = "neutral"


class EmotionalState:
    def __init__(self):
        self.current_emotion = EmotionType.NEUTRAL
        self.mood = 0.5  # 0..1
        self.engagement = 0.5
        self.empathy_level = 0.5
        self.energy_level = 0.5

    def set_emotion(self, emotion: EmotionType, intensity: float = 0.5, reason: str = ""):
        try:
            self.current_emotion = emotion
            self.mood = max(0.0, min(1.0, intensity))
        except Exception:
            self.current_emotion = EmotionType.NEUTRAL

    def get_emotional_state(self) -> Dict:
        return {
            "current_emotion": self.current_emotion.value,
            "mood": self.mood,
            "engagement": self.engagement,
            "empathy_level": self.empathy_level,
            "energy_level": self.energy_level,
        }


class EmotionProcessor:
    """Very small heuristic-based emotion detector for demo purposes."""

    def analyze_emotions(self, text: str) -> Tuple[List[Tuple[EmotionType, float]], float]:
        t = text.lower() if text else ""
        emotions = []
        sentiment = 0.0
        if "?" in t or t.strip().endswith("?") or "how" in t or "what" in t:
            emotions.append((EmotionType.CURIOUS, 0.8))
            sentiment = 0.2
        if any(w in t for w in ("sad", "unhappy", "depressed", "down")):
            emotions = [(EmotionType.SADNESS, 0.9)]
            sentiment = -0.6
        if any(w in t for w in ("angry", "frustrat", "mad", "furious")):
            emotions = [(EmotionType.ANGER, 0.9)]
            sentiment = -0.7
        if any(w in t for w in ("yay", "happy", "joy", "excited", "love")):
            emotions = [(EmotionType.JOY, 0.9)]
            sentiment = 0.8
        if not emotions:
            emotions = [(EmotionType.NEUTRAL, 0.5)]
            sentiment = 0.0

        return emotions, sentiment


class EmpathyEngine:
    def generate_empathetic_response(self, emotion_value: str) -> str:
        # emotion_value is expected to be a string like 'joy' or 'sadness'
        if emotion_value == EmotionType.SADNESS.value:
            return "I'm sorry you're feeling that way — I'm here with you."
        if emotion_value == EmotionType.ANGER.value:
            return "I hear your frustration — let's try to unpack this together."
        if emotion_value == EmotionType.JOY.value:
            return "That's wonderful to hear — tell me more!"
        if emotion_value == EmotionType.CURIOUS.value:
            return "Nice question — let's explore that."
        return "Thanks for sharing — I'm listening."