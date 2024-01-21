from unittest.mock import Mock, patch
import pytest
from models.gpt import get_json_from_gpt
import json
@pytest.fixture
def mock_openai_response():
    response = Mock()
    response.choices = [Mock()]
    response.choices[0].message.content = '{"H2O": "Water"}'  # Example response
    return response

@patch('models.gpt.OpenAI')
def test_get_json_from_gpt(mock_openai, mock_openai_response):
    mock_openai.return_value.chat.completions.create.return_value = mock_openai_response

    result = get_json_from_gpt(["H2O"])
    assert json.loads(result) == {"Chemicals": {"H2O": "Water"}}
