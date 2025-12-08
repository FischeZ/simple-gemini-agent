import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    parser = argparse.ArgumentParser(description="Prompt the Gemini model.")
    parser.add_argument('prompt', type=str, help='User prompt')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    args = parser.parse_args()

    user_prompt = args.prompt
    verbose = args.verbose

    if verbose:
        print(f"User prompt: {user_prompt}")

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    load_dotenv()
    api_key = os.environ.get('GEMINI_API_KEY')
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages
    )

    if response is None or response.usage_metadata is None:
        raise RuntimeError("No response from the model.")
    
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")
    
    print(response.text)

if __name__ == "__main__":
    main()
