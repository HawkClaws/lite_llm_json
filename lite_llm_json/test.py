import unittest
import jsonschema
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
        self.assertIn("name", generated_prompt)
        self.assertIn("age", generated_prompt)

    def test_parse_response(self):
        json_schema = {
            "type": "object",
            "properties": {"name": {"type": "string"}, "age": {"type": "integer"}},
            "required": ["name", "age"],
        }
        llm_json = LiteLLMJson(json_schema)
        valid_response = '{"name": "John Doe", "age": 30}'
        parsed_response = llm_json.parse_response(valid_response)
        print(parsed_response)

        self.assertIsInstance(parsed_response, dict)
        self.assertEqual(parsed_response["name"], "John Doe")
        self.assertEqual(parsed_response["age"], 30)

        invalid_response = '{"name": "John Doe", "age": "thirty"}'
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            llm_json.parse_response(invalid_response)


class TestExtractDataFromResponse(unittest.TestCase):
    def setUp(self):
        json_schema = {
            "type": "object",
            "properties": {"name": {"type": "string"}, "age": {"type": "integer"}},
            "required": ["name", "age"],
        }
        self.llm_json = LiteLLMJson(json_schema)

    def test_extract_data_from_code_block(self):
        response_content = '```\n{"key": "value"}\n```'
        expected_data = {"key": "value"}
        data = self.llm_json._extract_data_from_response(response_content)
        self.assertEqual(data, expected_data)

    def test_extract_data_from_code_block_with_json_prefix(self):
        response_content = '```json\n{"key": "value"}\n```'
        expected_data = {"key": "value"}
        data = self.llm_json._extract_data_from_response(response_content)
        self.assertEqual(data, expected_data)

    def test_extract_data_from_json_string(self):
        response_content = '{"key": "value"}'
        expected_data = {"key": "value"}
        data = self.llm_json._extract_data_from_response(response_content)
        self.assertEqual(data, expected_data)

    def test_extract_data_from_json_list(self):
        response_content = '[{"key": "value"}]'
        expected_data = [{"key": "value"}]
        data = self.llm_json._extract_data_from_response(response_content)
        self.assertEqual(data, expected_data)

    def test_extract_data_from_invalid_json(self):
        response_content = "invalid json"
        expected_data = {}
        data = self.llm_json._extract_data_from_response(response_content)
        self.assertEqual(data, expected_data)

    def test_extract_data_with_extra_whitespace(self):
        response_content = '   {"key": "value"}   '
        expected_data = {"key": "value"}
        data = self.llm_json._extract_data_from_response(response_content)
        self.assertEqual(data, expected_data)

    def test_extract_data_with_simple_json(self):
        response_content = (
            '{"sentence": "The quick brown fox jumps over the lazy dog."}'
        )
        expected_data = {"sentence": "The quick brown fox jumps over the lazy dog."}
        data = self.llm_json._extract_data_from_response(response_content)
        self.assertEqual(data, expected_data)

    def test_extract_data_newline_text(self):
        response_content = """
        {
            "answer_impossible": false, 
            "text": "# Introduction
This is a simple example of a markdown-formatted text response."
        }
        """
        expected_data = {
            "answer_impossible": False,
            "text": "# Introduction\nThis is a simple example of a markdown-formatted text response.",
        }
        data = self.llm_json._extract_data_from_response(response_content)
        self.assertEqual(data, expected_data)


if __name__ == "__main__":
    unittest.main()
