import pytest
from unittest.mock import patch
from app.services.celery.celery_task import fetch_contextual_information  # Adjust this import based on your project structure

class TestFetchContextualInformation:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.prediction = "fire"
        self.sensitive_structures = ["house", "tree"]

    @patch('app.celery_task.get_response')  # Adjust this based on your project structure
    def test_fetch_contextual_information(self, mock_get_response):
        mock_get_response.side_effect = ["Context about fire", "Impact of fire", "Possible solutions"]
        
        result = fetch_contextual_information(self.prediction, self.sensitive_structures)
        
        assert isinstance(result, tuple)
        assert result == ("Context about fire", "Impact of fire", "Possible solutions")