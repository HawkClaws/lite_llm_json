import json
import re
import jsonschema
from jsonschema.exceptions import SchemaError, ValidationError
from typing import Dict


class LiteLLMJson:
    BASE_PROMPT = """{query_prompt}

## Response Format:

Respond strictly in **JSON**. The response should adhere to the following JSON schema:

```JSON schema
{json_schema}
```

"""

    def __init__(self, json_schema: dict) -> None:
        """
        Initialize the class with a JSON schema.

        Args:
            json_schema (dict): The JSON schema.

        Returns:
            None
        """

        # Validate the JSON schema
        try:
            jsonschema.validate({}, json_schema)
        except SchemaError as e:
            raise e
        except ValidationError:
            pass

        # Set the JSON schema attribute
        self.json_schema = json_schema

    def generate_prompt(self, query_prompt: str) -> str:
        """
        Generate a prompt for the given query prompt.

        Args:
            query_prompt (str): The query prompt.

        Returns:
            str: The generated prompt.
        """
        # Convert the JSON schema to a string
        json_schema_str = json.dumps(self.json_schema, ensure_ascii=False, indent=2)

        # Format the prompt string with the query prompt and JSON schema
        return self.BASE_PROMPT.format(
            query_prompt=query_prompt, json_schema=json_schema_str
        )

    def parse_response(self, response: str) -> Dict:
        """
        Parse the response string and validate it against the JSON schema.

        Args:
            response (str): The response string to parse.

        Returns:
            Dict: The parsed response as a dictionary.

        """
        json_data = self._extract_data_from_response(response)
        jsonschema.validate(json_data, self.json_schema)
        return json_data

    def _extract_data_from_response(self, text: str, decoder=json.JSONDecoder(strict=False), symbols=('{', '[')):
        """Find JSON objects and arrays in text, load the JSON data, and return the loaded data as a list"""
        pos = 0
        while True:
            matches = {symbol: text.find(symbol, pos) for symbol in symbols}
            matches = {k: v for k, v in matches.items() if v != -1}
            if not matches:
                break
            match_symbol, match_pos = min(matches.items(), key=lambda item: item[1])
            try:
                result, index = decoder.raw_decode(text[match_pos:])
                if match_symbol == '{':
                    return json.loads(json.dumps(result))
                elif match_symbol == '[':
                    return json.loads(json.dumps(result))
                pos = match_pos + index
            except ValueError:
                pos = match_pos + 1
        return {}
