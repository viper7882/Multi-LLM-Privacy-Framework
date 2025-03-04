import pytest
from unittest.mock import MagicMock, patch
from protocols.clients import OpenAIClient

openai_model = "gpt-4o"


@pytest.fixture
def mock_openai_client():
    """Fixture to mock the OpenAI client with proper response structure."""
    with patch("protocols.clients.openai_client.openai.OpenAI") as mock_client:
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def openai_client(mock_openai_client):
    """Fixture to initialize OpenAIClient with mocked dependencies."""
    # Configure default mock response
    mock_completion = MagicMock()
    mock_completion.choices = [MagicMock(message=MagicMock(content="Default response"))]
    mock_openai_client.chat.completions.create.return_value = mock_completion

    return OpenAIClient(
        model=openai_model,
        temperature=0.7,
        api_key="mock-api-key",
    )


def test_openai_client_initialization(openai_client, mock_openai_client):
    """Verify client initialization with correct parameters."""
    assert openai_client.model == openai_model
    assert openai_client.temperature == 0.7
    assert openai_client.api_key == "mock-api-key"

    # Verify the client was never actually initialized with real connection
    mock_openai_client.assert_not_called()  # Client is lazy-initialized


def test_openai_client_generate(openai_client, mock_openai_client):
    """Test text generation with properly structured mock response."""
    # Configure mock response
    mock_completion = MagicMock()
    mock_completion.choices = [MagicMock(message=MagicMock(content="Mocked response"))]
    mock_openai_client.chat.completions.create.return_value = mock_completion

    # Execute test call
    prompt = "Test prompt"
    response = openai_client.generate(prompt)

    # Verify response and API call
    assert response == "Mocked response"
    mock_openai_client.chat.completions.create.assert_called_once_with(
        model=openai_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=None,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=None
    )


def test_openai_client_stream(openai_client, mock_openai_client):
    """Test streaming with chunked mock responses."""
    # Configure streaming response
    mock_chunks = [
        MagicMock(choices=[MagicMock(delta=MagicMock(content="Chunk1 "))]),
        MagicMock(choices=[MagicMock(delta=MagicMock(content="Chunk2"))])
    ]
    mock_openai_client.chat.completions.create.return_value = mock_chunks

    # Execute streaming test
    prompt = "Stream prompt"
    stream_response = openai_client.stream(prompt)
    assert "".join(stream_response) == "Chunk1 Chunk2"

    # Verify streaming parameters
    mock_openai_client.chat.completions.create.assert_called_once_with(
        model=openai_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=None,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=None,
        stream=True
    )


@patch("protocols.clients.openai_client.tiktoken")
def test_openai_client_get_num_tokens(mock_tiktoken, openai_client):
    """Test token counting with mocked tokenizer."""
    assert mock_tiktoken is not None, "Mock tiktoken is not applied"

    # Configure mock tokenizer
    mock_encoder = MagicMock()
    mock_encoder.encode.return_value = [1, 2, 3, 4, 5, 6]
    mock_tiktoken.get_encoding.return_value = mock_encoder

    # Test token count
    text = "This is a test sentence."
    assert openai_client.get_num_tokens(text) == 6
    mock_encoder.encode.assert_called_once_with(text)
