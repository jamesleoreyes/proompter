import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from helpers.call_function import call_function
from config.gemini import GeminiConfig

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

for _ in range(51):
    try: 
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[GeminiConfig().FUNCTIONS],
                system_instruction=GeminiConfig().SYSTEM_PROMPT
            )
        )
            
        if not response.candidates or not response.candidates[0].content:
            print('ERROR: Received invalid response from API')
            break
            
        if response.text and not response.function_calls:
            print(f'Final Response:\n{response.text}')
            break

        model_content = response.candidates[0].content
        if model_content and model_content.parts:
            messages.append(model_content)
        else:
            print('WARNING: Response has no parts, skipping append')
            if args.verbose:
                print(f'Response object: {response}')
            break

        if response.function_calls:
            function_response_parts = []
            for function_call in response.function_calls:
                function_call_result = call_function(function_call)
                if not function_call_result.parts[0].function_response.response:
                    raise Exception('Error: Function call did not return a valid response')
                elif args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            
                function_response_parts.extend(function_call_result.parts)
                
            messages.append(types.Content(
                role='user',
                parts=function_response_parts
            ))
        else:
            print(response.text or "")
            
        if args.verbose:
            print(f'User prompt: {args.user_prompt}')
            print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
            print(f'Response tokens: ${response.usage_metadata.candidates_token_count}')
    except Exception as e:
        raise RuntimeError(f'An error occurred while generating a response: {e}')