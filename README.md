# lite_llm_json

## Description

The library has functionality to cleanly extract JSON from LLM responses and generate prompts for LLM that return JSON. It features a simple yet versatile implementation.

## Installation

`pip install git+https://github.com/HawkClaws/lite_llm_json.git`

## HowToUse

```python
import openai
from lite_llm_json import LiteLLMJson

# Set the OpenAI API key
api_key = "YOUR_API_KEY"
openai.api_key = api_key

# Define the JSON schema
json_schema = {
    "type": "object",
    "properties": {"name": {"type": "string"}, "age": {"type": "integer"}},
    "required": ["name", "age"],
}
# Instantiate the LiteLLMJson class
llm_json = LiteLLMJson(json_schema)

# Define the query prompt
query_prompt = """## Instructions:
Provide information about a person."""

# Get the generated prompt
generated_prompt = llm_json.generate_prompt(query_prompt)

# Use the OpenAI API to get a completion
response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=generated_prompt
)

# Get the output text
output_text = response["choices"][0]["text"]

# Parse the output text to obtain JSON data
json_data = llm_json.parse_response(output_text)

# Display the JSON data
print(json_data)


```