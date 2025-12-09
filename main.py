import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import MAX_ITERATIONS, MODEL
from prompts import SYSTEM_PROMPT

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

def main():
    load_dotenv()
    api_key = os.environ.get('GEMINI_API_KEY')
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Prompt the Gemini model.")
    parser.add_argument('prompt', type=str, help='User prompt')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    args = parser.parse_args()

    user_prompt = args.prompt
    verbose = args.verbose

    if verbose:
        print(f"User prompt: {user_prompt}")

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info, 
            schema_get_file_content, 
            schema_run_python_file, 
            schema_write_file
        ],
    )

    iteration = 0
    while iteration < MAX_ITERATIONS:
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=SYSTEM_PROMPT)
                )

            if response is None or response.usage_metadata is None:
                raise RuntimeError("No response from the model.")
            
            if verbose:
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")

            response_wants_function_call = False

            for candidate in response.candidates:
                if candidate.content.parts[0].function_call is not None:
                    response_wants_function_call = True
                messages.append(candidate.content)

            if not response_wants_function_call:
                print(response.text)
                iteration = MAX_ITERATIONS
                break

            function_call_responses = []
            if response.function_calls is not None and len(response.function_calls) > 0:
                for function_call_part in response.function_calls:
                    function_call_response = call_function(function_call_part, verbose=verbose)
                    if function_call_response is None or function_call_response.parts[0].function_response.response is None:
                        raise Exception("No function response from the model.")
                    else:
                        function_call_responses.append(function_call_response.parts[0])
                        if verbose:
                            print(f"-> {function_call_response.parts[0].function_response.response}")        

                function_call_message = types.Content(
                    role="user",
                    parts=function_call_responses,
                )

                messages.append(function_call_message)
        except Exception as e:
            print(f"Error during iteration {iteration}: {str(e)}")
            break
        
        iteration += 1

if __name__ == "__main__":
    main()