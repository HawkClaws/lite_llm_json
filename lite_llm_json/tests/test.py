
import unittest
from lite_llm_json import LiteLLMJson

class TestLiteLLMJson(unittest.TestCase):
    def test_generate_prompt(self):
        json_schema = {
            "type": "object",
            "properties": {"name": {"type": "string"}, "age": {"type": "integer"}},
            "required": ["name", "age"],
        }
        llm_json = LiteLLMJson(json_schema)
        query_prompt = "Provide information about a person."
        generated_prompt = llm_json.generate_prompt(query_prompt)
        print(generated_prompt)
        # Add your assertion here based on the expected output of generate_prompt

    def test_parse_response(self):
        json_schema = {
            "type": "object",
            "properties": {"name": {"type": "string"}, "age": {"type": "integer"}},
            "required": ["name", "age"],
        }
        llm_json = LiteLLMJson(json_schema)
        valid_response = '{"name": "John Doe", "age": 30}'
        print(llm_json.parse_response(valid_response))
        # Add your assertion here based on the expected output of parse_response

        invalid_response = '{"name": "John Doe", "age": "thirty"}'
        print(llm_json.parse_response(invalid_response))
        # Add your assertion here based on the expected behavior when parsing an invalid response


if __name__ == "__main__":
    unittest.main()
