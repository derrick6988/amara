import pytest
from unittest.mock import patch, MagicMock
from main_enhanced import WebSearchEngine


class TestWebSearchEngine:
    
    @pytest.fixture
    def search_engine(self):
        return WebSearchEngine()
    
    def test_search_initialization(self, search_engine):
        """Test WebSearchEngine initializes correctly"""
        assert search_engine is not None
        assert hasattr(search_engine, 'ddgs')
    
    @patch('main_enhanced.DDGS')
    def test_search_returns_results(self, mock_ddgs_class, search_engine):
        """Test search returns results"""
        mock_instance = MagicMock()
        mock_ddgs_class.return_value = mock_instance
        mock_results = [
            {'title': 'Test 1', 'body': 'Body 1', 'href': 'http://test1.com'},
            {'title': 'Test 2', 'body': 'Body 2', 'href': 'http://test2.com'},
        ]
        mock_instance.text.return_value = mock_results
        
        search_engine = WebSearchEngine()
        results = search_engine.search('test query')
        
        assert len(results) == 2
        assert results[0]['title'] == 'Test 1'
    
    @patch('main_enhanced.DDGS')
    def test_search_handles_exceptions(self, mock_ddgs_class, search_engine):
        """Test search handles exceptions gracefully"""
        mock_instance = MagicMock()
        mock_ddgs_class.return_value = mock_instance
        mock_instance.text.side_effect = Exception('Search failed')
        
        search_engine = WebSearchEngine()
        results = search_engine.search('test query')
        
        assert results == []
    
    def test_format_results_creates_summary(self, search_engine):
        """Test format_results creates a proper summary"""
        results = [
            {'title': 'Python Tutorial', 'body': 'Learn Python basics', 'href': 'http://example.com'},
            {'title': 'Python Docs', 'body': 'Official documentation', 'href': 'http://python.org'},
        ]
        
        summary = search_engine.format_results(results, 'python tutorial')
        
        assert 'Search Results for' in summary
        assert 'Python Tutorial' in summary
        assert 'http://example.com' in summary
        assert '1.' in summary  # Numbered list
        assert '2.' in summary
    
    def test_format_results_handles_empty_results(self, search_engine):
        """Test format_results handles empty results"""
        summary = search_engine.format_results([], 'test query')
        
        assert 'Search Results for' in summary
        assert 'test query' in summary
    
    def test_format_results_handles_missing_fields(self, search_engine):
        """Test format_results handles missing fields gracefully"""
        results = [
            {'title': 'Missing body'},
            {'body': 'Missing title'},
            {'href': 'Missing both'},
        ]
        
        summary = search_engine.format_results(results, 'test')
        
        # Should still format even with missing fields
        assert 'Search Results for' in summary
        assert isinstance(summary, str)
