import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get('GEMINI_API_KEY')
client = genai.Client(api_key=api_key)
parser = argparse.ArgumentParser()
parser.add_argument('user_prompt', type=str)
parser.add_argument('--verbose', action='store_true')
args = parser.parse_args()

if not args.user_prompt:
    print('ERROR: A prompt must be passed as a positional argument')
    sys.exit(1)

messages = [
    types.Content(role='user', parts=[types.Part(text=args.user_prompt)])
]

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=messages
)

if args.verbose:
    print(f'User prompt: {args.user_prompt}')
    print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
    print(response.text)
    print(f'Response tokens: ${response.usage_metadata.candidates_token_count}')
else:
    print(response.text)