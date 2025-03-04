from decouple import config
from protocols.clients import OllamaClient, OpenAIClient
from protocols.privacy_protocol import PrivacyProtocol_v1

# Initialize clients
local_llm = OllamaClient(
    model="llama-3",
    temperature=0.6,
)

remote_llm = OpenAIClient(
    model="gpt-4o",
    temperature=0.6,
    api_key=config('OPENAI_API_KEY'),
)

# Set up protocol
protocol = PrivacyProtocol_v1(
    local_llm=local_llm,
    remote_llm=remote_llm,
    sensitivity_threshold=0.6
)

# Example usage
sensitive_query = "My social security number is 123-45-6789. Should I share this?"
normal_query = "Explain quantum computing in simple terms"

print("Sensitive query response:", protocol.process_query(sensitive_query))
print("Normal query response:", protocol.process_query(normal_query))
print("Hybrid response:", protocol.hybrid_generation(sensitive_query))
