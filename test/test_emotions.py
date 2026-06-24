import pytest
from emotions import EmotionProcessor, EmotionType

def test_detects_curious():
    ep = EmotionProcessor()
    emotions, sentiment = ep.analyze_emotions("How does this work?")
    assert emotions[0][0] == EmotionType.CURIOUS

def test_detects_joy():
    ep = EmotionProcessor()
    emotions, sentiment = ep.analyze_emotions("I'm so happy about this!")
    assert emotions[0][0] == EmotionType.JOY
