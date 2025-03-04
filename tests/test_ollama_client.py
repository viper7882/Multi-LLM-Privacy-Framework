import pytest
from unittest.mock import MagicMock, patch
from protocols.clients import OllamaClient

ollama_model = "deepscaler:latest"


@pytest.fixture
def mock_ollama_client():
    """Fixture to mock the Ollama client entirely."""
    with patch("protocols.clients.ollama_client.ollama.Client") as mock_ollama_client:
        mock_instance = MagicMock()
        mock_ollama_client.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def ollama_client(mock_ollama_client):
    """Fixture to initialize OllamaClient with mocked dependencies."""
    # Configure default mock response
    mock_ollama_client.generate.return_value = {"response": "Default response"}
    return OllamaClient(
        model=ollama_model,
        temperature=0.7,
        top_p=0.9,
        base_url="http://mock-url:11434"
    )


def test_ollama_client_initialization(mock_ollama_client, ollama_client):
    """Test initialization with custom parameters."""
    assert ollama_client.model == ollama_model
    assert ollama_client.temperature == 0.7
    assert ollama_client.top_p == 0.9
    assert ollama_client.max_tokens is None

    # Verify the client was never actually initialized with real connection
    mock_ollama_client.assert_not_called()  # Client is lazy-initialized


def test_ollama_client_generate(mock_ollama_client, ollama_client):
    """Test generate() with full isolation."""
    # Configure mock response
    mock_ollama_client.generate.return_value = {"response": "Mocked response"}

    # Execute test call
    prompt = "Test prompt"
    response = ollama_client.generate(prompt)

    # Verify response and API call
    assert response == "Mocked response"
    mock_ollama_client.generate.assert_called_once_with(
        model=ollama_model,
        prompt=prompt,
        options={
            "temperature": 0.7,
            "top_p": 0.9,
            "max_tokens": None,
            "stop": None
        }
    )


def test_ollama_client_stream(mock_ollama_client, ollama_client):
    """Test streaming with full isolation."""
    # Configure streaming response
    mock_ollama_client.generate.return_value = [
        {"response": "Chunk1 "},
        {"response": "Chunk2"}
    ]

    # Execute streaming test
    prompt = "Stream prompt"
    stream_response = ollama_client.stream(prompt)
    assert "".join(stream_response) == "Chunk1 Chunk2"

    # Verify streaming parameters
    mock_ollama_client.generate.assert_called_once_with(
        model=ollama_model,
        prompt=prompt,
        options={
            "temperature": 0.7,
            "top_p": 0.9,
            "max_tokens": None,
            "stop": None
        },
        stream=True
    )
