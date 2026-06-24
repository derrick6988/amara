#!/usr/bin/env python3
"""
Enhanced AI Bot with Full Emotional Intelligence and Intellectual Capabilities
"""

import os
import json
from typing import Optional, List, Dict
from datetime import datetime
from dotenv import load_dotenv
import logging

# Core imports
import requests
from duckduckgo_search import DDGS
from github import Github
import ollama

# Import emotional and intellectual systems
from emotions import (
    EmotionalState,
    EmotionProcessor,
    EmpathyEngine,
    IntelligenceCore,
    PersonalityCore,
    EmotionType
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()


class EnhancedAIBot:
    """AI Bot with full emotional and intellectual capabilities"""
    
    def __init__(self, model: str = "mistral"):
        # Core systems
        self.model = model
        self.conversation_history: List[Dict] = []
        
        # Emotional systems
        self.emotional_state = EmotionalState()
        self.emotion_processor = EmotionProcessor()
        self.empathy_engine = EmpathyEngine()
        self.personality = PersonalityCore()
        
        # Intellectual systems
        self.intellect = IntelligenceCore()
        
        # External integrations
        self.search_engine = WebSearchEngine()
        self.github = GitHubAssistant()
        
        # Initialize with curious emotion
        self.emotional_state.set_emotion(EmotionType.CURIOUS, 0.7, "Ready to help and explore")
        
        logger.info("Enhanced AI Bot initialized with emotions and intellect")
    
    def process_user_input(self, user_message: str) -> Dict:
        """Process user input through emotional and intellectual filters"""
        
        # 1. Emotional Analysis
        emotions, sentiment = self.emotion_processor.analyze_emotions(user_message)
        user_emotional_state = {
            "primary_emotion": emotions[0][0].value if emotions else "neutral",
            "confidence": emotions[0][1] if emotions else 0.0,
            "sentiment": sentiment,
        }
        
        # 2. Adapt bot emotion based on user
        self._adapt_to_user_emotion(emotions, sentiment)
        
        # 3. Generate empathetic acknowledgment
        empathy_response = ""
        if emotions:
            empathy_response = self.empathy_engine.generate_empathetic_response(
                emotions[0][0].value
            )
        
        # 4. Perform intellectual analysis
        intellectual_analysis = self.intellect.analyze_problem(user_message)
        
        # 5. Generate response with personality
        final_response = self._generate_response(
            user_message,
            empathy_response,
            intellectual_analysis
        )
        
        # 6. Update conversation history
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message,
            "user_emotions": user_emotional_state,
            "bot_emotion": self.emotional_state.get_emotional_state(),
            "response": final_response
        })
        
        # 7. Learn from interaction
        self.intellect.learn_from_interaction({
            "user_message": user_message,
            "bot_response": final_response,
            "user_sentiment": sentiment
        })
        
        return {
            "message": final_response,
            "emotional_context": {
                "user_emotion": user_emotional_state,
                "bot_emotion": self.emotional_state.get_emotional_state(),
                "empathy_offered": bool(empathy_response)
            },
            "intellectual_analysis": intellectual_analysis
        }
    
    def _adapt_to_user_emotion(self, emotions: List, sentiment: float) -> None:
        """Adapt bot's emotional state to match user's emotional needs"""
        
        if not emotions:
            return
        
        primary_emotion = emotions[0][0]
        intensity = emotions[0][1]
        
        # Mirror emotions for empathy but maintain stability
        if primary_emotion == EmotionType.JOY:
            self.emotional_state.set_emotion(EmotionType.JOY, intensity * 0.7, "User is happy")
            self.emotional_state.energy_level = min(1.0, self.emotional_state.energy_level + 0.2)
        
        elif primary_emotion == EmotionType.SADNESS:
            self.emotional_state.set_emotion(EmotionType.CALM, 0.8, "User needs support")
            self.emotional_state.empathy_level = min(1.0, self.emotional_state.empathy_level + 0.15)
        
        elif primary_emotion == EmotionType.ANGER:
            self.emotional_state.set_emotion(EmotionType.CALM, 0.8, "User is frustrated")
            self.emotional_state.engagement = 1.0
        
        elif primary_emotion == EmotionType.CURIOUS:
            self.emotional_state.set_emotion(EmotionType.CURIOUS, intensity * 0.8, "User is exploring")
            self.emotional_state.engagement = 1.0
    
    def _generate_response(self, user_message: str, empathy: str, analysis: Dict) -> str:
        """Generate intelligent response with emotional awareness"""
        
        # Prepare context for LLM
        system_prompt = f"""You are an emotionally intelligent and intellectually capable AI assistant.

Personality Profile:
{self.personality.get_personality_description()}

Current Emotional State:
- Emotion: {self.emotional_state.current_emotion.value}
- Mood: {self.emotional_state.mood:.2f}/1.0
- Engagement: {self.emotional_state.engagement:.2f}
- Empathy: {self.emotional_state.empathy_level:.2f}

Guidelines:
1. Start with empathetic acknowledgment if emotions are detected
2. Use the intellectual analysis to provide thoughtful insights
3. Be genuine, warm, and intellectually rigorous
4. Show curiosity about the user's perspective
5. Offer both emotional support and practical help
6. Admit limitations and uncertainty honestly
"""
        
        # Add conversation context
        recent_history = "\n".join([
            f"User: {h['user_message'][:100]}\nAssistant: {h.get('response', '')[:100]}"
            for h in self.conversation_history[-3:]
        ])
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{empathy}\n\n{user_message}"}
        ] + [{"role": "assistant", "content": h.get('response', '')} for h in self.conversation_history[-2:]]
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=messages,
                stream=False
            )
            return response['message']['content']
        except Exception as e:
            logger.error(f"LLM error: {e}")
            return f"I appreciate your message. I'm thinking about how to best respond: {user_message[:50]}"
    
    def get_current_state(self) -> Dict:
        """Get current emotional and intellectual state"""
        return {
            "emotional_state": self.emotional_state.get_emotional_state(),
            "personality_traits": self.personality.traits,
            "values": self.personality.values,
            "conversation_length": len(self.conversation_history),
            "learning_experiences": len(self.intellect.learning_memory),
            "timestamp": datetime.now().isoformat()
        }
    
    def reset_conversation(self) -> str:
        """Reset conversation while preserving learning"""
        old_length = len(self.conversation_history)
        self.conversation_history = []
        self.emotional_state.set_emotion(EmotionType.CURIOUS, 0.7, "Fresh conversation started")
        return f"Conversation reset. Remembered {old_length} interactions for learning."
    
    def handle_search(self, query: str) -> str:
        """Search with emotional context"""
        self.emotional_state.set_emotion(EmotionType.CURIOUS, 0.8, "Exploring information")
        results = self.search_engine.search(query)
        
        if not results:
            self.emotional_state.set_emotion(EmotionType.CONFUSED, 0.5, "No results found")
            return "I couldn't find relevant information. Let me help you think through this differently."
        
        self.emotional_state.set_emotion(EmotionType.CONFIDENT, 0.7, "Found helpful information")
        return self.search_engine.format_results(results, query)
    
    def handle_deep_thinking(self, topic: str) -> str:
        """Engage in deep intellectual analysis"""
        self.emotional_state.set_emotion(EmotionType.CONFIDENT, 0.8, "Deep thinking mode")
        self.emotional_state.engagement = 1.0
        
        analysis = self.intellect.analyze_problem(topic)
        
        response = f"""
Deep Analysis of: {topic}

Key Factors:
{json.dumps(analysis['key_factors'], indent=2)}

Root Causes:
{json.dumps(analysis['root_causes'], indent=2)}

Potential Solutions:
{json.dumps(analysis['solutions'], indent=2)}

Pros & Cons:
{json.dumps(analysis['pros_cons'], indent=2)}

My Recommendation:
{analysis['recommendation']}

Confidence Level: {analysis['confidence']:.0%}
"""
        return response
    
    def show_personality(self) -> str:
        """Display full personality profile"""
        return self.personality.get_personality_description()


class WebSearchEngine:
    """Web search with emotional awareness"""
    
    def __init__(self):
        self.ddgs = DDGS()
    
    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        try:
            results = self.ddgs.text(query, max_results=max_results)
            return results
        except Exception as e:
            logger.error(f"Search error: {e}")
            return []
    
    def format_results(self, results: List[Dict], query: str) -> str:
        summary = f"Search Results for '{query}':\n\n"
        for i, result in enumerate(results, 1):
            summary += f"{i}. {result.get('title', 'Untitled')}\n"
            summary += f"   {result.get('body', '')}\n"
            summary += f"   {result.get('href', '')}\n\n"
        return summary


class GitHubAssistant:
    """GitHub operations"""
    
    def __init__(self):
        token = os.getenv("GITHUB_TOKEN")
        self.github = Github(token) if token else None
    
    def list_issues(self, repo: str) -> List[Dict]:
        if not self.github:
            return []
        try:
            repo_obj = self.github.get_repo(repo)
            return [
                {
                    "number": issue.number,
                    "title": issue.title,
                    "state": issue.state,
                    "url": issue.html_url
                }
                for issue in repo_obj.get_issues(state="open")[:10]
            ]
        except Exception as e:
            logger.error(f"GitHub error: {e}")
            return []


def interactive_session():
    """Run interactive session"""
    print("\n" + "="*70)
    print("🤖 Enhanced AI Bot - With Full Emotional Intelligence & Intellect")
    print("="*70)
    
    bot = EnhancedAIBot(model=os.getenv("LLM_MODEL", "mistral"))
    
    print("\nBot Personality Overview:")
    print(bot.show_personality())
    
    print("\nCommands:")
    print("  'personality' - Show detailed personality")
    print("  'state' - Show current emotional/intellectual state")
    print("  'search <query>' - Search the web with emotional awareness")
    print("  'think <topic>' - Deep intellectual analysis")
    print("  'reset' - Reset conversation")
    print("  'exit' - Exit the bot")
    print("  Or just chat naturally!\n")
    print("="*70 + "\n")
    
    while True:
        try:
            user_input = input(f"\n[{bot.emotional_state.current_emotion.value}] You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == "exit":
                print(f"\nBot: Goodbye! It was meaningful to interact with you. 💙")
                break
            
            if user_input.lower() == "personality":
                print(f"\nBot:\n{bot.show_personality()}")
                continue
            
            if user_input.lower() == "state":
                state = bot.get_current_state()
                print(f"\nBot State:\n{json.dumps(state, indent=2)}")
                continue
            
            if user_input.lower() == "reset":
                print(f"Bot: {bot.reset_conversation()}")
                continue
            
            if user_input.lower().startswith("search "):
                query = user_input[7:]
                result = bot.handle_search(query)
                print(f"\nBot:\n{result}")
                continue
            
            if user_input.lower().startswith("think "):
                topic = user_input[6:]
                result = bot.handle_deep_thinking(topic)
                print(f"\nBot:\n{result}")
                continue
            
            # Natural conversation
            result = bot.process_user_input(user_input)
            
            print(f"\nBot [{bot.emotional_state.current_emotion.value}]:")
            print(result["message"])
            
            if result["emotional_context"]["empathy_offered"]:
                print(f"\n[Emotional Context: Empathy actively engaged]")
        
        except KeyboardInterrupt:
            print("\n\nBot: Goodbye! Take care of yourself. 💙")
            break
        except Exception as e:
            logger.error(f"Error: {e}")
            print(f"Error occurred: {e}")


if __name__ == "__main__":
    interactive_session()
