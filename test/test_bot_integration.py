import pytest
from unittest.mock import patch, MagicMock
from main_enhanced import EnhancedAIBot
from emotions import EmotionType


class TestEnhancedAIBot:
    
    @pytest.fixture
    def bot(self):
        with patch('main_enhanced.ollama.chat'):
            return EnhancedAIBot(model='mistral')
    
    def test_bot_initialization(self, bot):
        """Test bot initializes with all systems"""
        assert bot is not None
        assert bot.model == 'mistral'
        assert bot.emotional_state is not None
        assert bot.emotion_processor is not None
        assert bot.empathy_engine is not None
        assert bot.intellect is not None
        assert bot.personality is not None
        assert len(bot.conversation_history) == 0
    
    def test_bot_initial_emotion(self, bot):
        """Test bot starts with curious emotion"""
        state = bot.emotional_state.get_emotional_state()
        assert state['current_emotion'] == EmotionType.CURIOUS.value
    
    @patch('main_enhanced.ollama.chat')
    def test_process_user_input_happy(self, mock_chat, bot):
        """Test processing happy user input"""
        mock_chat.return_value = {'message': {'content': 'That is wonderful!'}}
        
        result = bot.process_user_input("I'm so happy!")
        
        assert result is not None
        assert 'message' in result
        assert 'emotional_context' in result
        assert 'intellectual_analysis' in result
        assert len(bot.conversation_history) == 1
    
    @patch('main_enhanced.ollama.chat')
    def test_process_user_input_sad(self, mock_chat, bot):
        """Test bot adapts to sad user input"""
        mock_chat.return_value = {'message': {'content': 'I understand'}}
        
        result = bot.process_user_input("I'm feeling really sad")
        
        assert result is not None
        # Bot should show empathy for sadness
        assert result['emotional_context']['empathy_offered'] is True
    
    @patch('main_enhanced.ollama.chat')
    def test_process_user_input_curious(self, mock_chat, bot):
        """Test bot responds to curious questions"""
        mock_chat.return_value = {'message': {'content': 'Let me explore that...'}}
        
        result = bot.process_user_input("How does this work?")
        
        assert result is not None
        # Question should be detected as curiosity
        assert result['emotional_context']['user_emotion']['primary_emotion'] == EmotionType.CURIOUS.value
    
    def test_get_current_state(self, bot):
        """Test getting bot's current state"""
        state = bot.get_current_state()
        
        assert 'emotional_state' in state
        assert 'personality_traits' in state
        assert 'values' in state
        assert 'conversation_length' in state
        assert 'learning_experiences' in state
        assert 'timestamp' in state
    
    @patch('main_enhanced.ollama.chat')
    def test_reset_conversation(self, mock_chat, bot):
        """Test resetting conversation"""
        # Add some history
        mock_chat.return_value = {'message': {'content': 'Response'}}
        bot.process_user_input("Hello")
        assert len(bot.conversation_history) == 1
        
        # Reset
        message = bot.reset_conversation()
        assert len(bot.conversation_history) == 0
        assert "reset" in message.lower()
        assert bot.emotional_state.current_emotion == EmotionType.CURIOUS
    
    @patch('main_enhanced.WebSearchEngine')
    def test_handle_search(self, mock_search_class, bot):
        """Test search functionality"""
        mock_search = MagicMock()
        mock_search_class.return_value = mock_search
        mock_search.search.return_value = [
            {'title': 'Result', 'body': 'Found something', 'href': 'http://example.com'}
        ]
        mock_search.format_results.return_value = "Search results..."
        
        bot.search_engine = mock_search
        result = bot.handle_search('python')
        
        assert result is not None
        assert 'Search results' in result
    
    @patch('main_enhanced.WebSearchEngine')
    def test_handle_search_no_results(self, mock_search_class, bot):
        """Test search with no results"""
        mock_search = MagicMock()
        mock_search_class.return_value = mock_search
        mock_search.search.return_value = []
        
        bot.search_engine = mock_search
        result = bot.handle_search('gibberish xyz 123')
        
        assert "couldn't find" in result.lower()
    
    def test_show_personality(self, bot):
        """Test personality display"""
        personality = bot.show_personality()
        
        assert personality is not None
        assert isinstance(personality, str)
        assert 'Amara' in personality or 'warm' in personality
    
    @patch('main_enhanced.ollama.chat')
    def test_conversation_learning(self, mock_chat, bot):
        """Test bot learns from conversations"""
        mock_chat.return_value = {'message': {'content': 'Response'}}
        
        initial_memories = len(bot.intellect.learning_memory)
        bot.process_user_input("Tell me about AI")
        final_memories = len(bot.intellect.learning_memory)
        
        assert final_memories > initial_memories
    
    @patch('main_enhanced.ollama.chat')
    def test_multiple_interactions_history(self, mock_chat, bot):
        """Test conversation history grows with interactions"""
        mock_chat.return_value = {'message': {'content': 'Response'}}
        
        bot.process_user_input("First message")
        assert len(bot.conversation_history) == 1
        
        bot.process_user_input("Second message")
        assert len(bot.conversation_history) == 2
        
        bot.process_user_input("Third message")
        assert len(bot.conversation_history) == 3
