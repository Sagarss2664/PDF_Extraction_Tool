import os
from openai import OpenAI
from pathlib import Path

# Load environment
env_path = Path(__file__).parent / '.env'
if env_path.exists():
    with open(env_path, 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key exists: {bool(api_key)}")
print(f"API Key length: {len(api_key) if api_key else 0}")

# Test OpenAI client
try:
    client = OpenAI(api_key=api_key)
    print("OpenAI client created successfully!")
    
    # Test a simple call
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say 'hello'"}],
        max_tokens=5
    )
    print(f"API call successful: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"Error: {e}")
    print(f"Error type: {type(e)}")