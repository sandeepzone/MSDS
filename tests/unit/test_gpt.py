import pytest
from unittest.mock import Mock, patch
from service.gpt_service import GptService, MSDSConfig  # Replace 'your_module' with the actual module name
import json

from openai import (OpenAI, APIConnectionError, AuthenticationError,
                     RateLimitError, APIError)
from exception.service_exception import OpenAiRateLimitError, \
                OpenAiAuthenticationError, OpenAIError, OpenAiTimeoutError
import pytest
from unittest.mock import Mock, patch
from service.gpt_service import GptService, MSDSConfig
import json

@pytest.fixture
def mock_config():
    return MSDSConfig(
        OPENAI_KEY='dummy_key',
        MODEL_NAME='dummy_model',
        MODEL_TEMP=0.5,
        GPT_PROMPT='dummy_prompt',
        MSDS_SHEETS_PATH='/dummy/path'
    )

@pytest.fixture
def gpt_service(mock_config):
    return GptService(config=mock_config)

# Test get_input_format
def test_get_input_format(gpt_service):
    assert gpt_service.get_input_format('123-45-6') == 'CAS Number'
    assert gpt_service.get_input_format('Water') == 'Chemical Name'

# Test get_json_from_gpt
@patch('service.gpt_service.OpenAI')
def test_get_json_from_gpt(mock_openai, gpt_service):
    # Example JSON response content
    mock_response_content = '{"Chemical1": "Data1", "Chemical2": "Data2"}'

    # Set up the mock to return this content in the expected structure
    mock_message = Mock()
    mock_message.content = mock_response_content
    mock_choice = Mock()
    mock_choice.message = mock_message
    mock_openai.chat.completions.create.return_value = Mock(choices=[mock_choice])
    
    # Test normal operation
    result = gpt_service.get_json_from_gpt(['Chemical1', 'Chemical2'])
    # Ensure result is a string that can be loaded by json.loads
    assert isinstance(result, str)
    data = json.loads(result)
    assert 'Chemical1' in data['Chemicals']
    assert 'Chemical2' in data['Chemicals']
    assert data['Chemicals']['Chemical1'] == 'Data1'
    assert data['Chemicals']['Chemical2'] == 'Data2'
    
    # Test for AuthenticationError
    mock_openai.chat.completions.create.side_effect = AuthenticationError
    with pytest.raises(OpenAiAuthenticationError):
        gpt_service.get_json_from_gpt(['123-45-6'])


# Test generate_document
@patch('service.gpt_service.GptService.get_json_from_gpt', return_value='{"Chemicals": {"Water": "H2O"}}')
@patch('service.gpt_service.DocumentGenerator')
def test_generate_document(mock_doc_generator, mock_get_json_from_gpt, gpt_service, mock_config):
    result = gpt_service.generate_document(['Water'])
    mock_doc_generator.return_value.save_doc.assert_called_once_with('{"Chemicals": {"Water": "H2O"}}', f'{mock_config.MSDS_SHEETS_PATH}/Water.docx')
    assert result == 'SUCCESS'
