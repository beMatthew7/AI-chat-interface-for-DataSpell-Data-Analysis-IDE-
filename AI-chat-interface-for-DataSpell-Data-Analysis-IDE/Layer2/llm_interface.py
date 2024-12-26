import requests
import json

class LLMInterface:
    """
    Interface for interacting with a locally hosted LLM API.
    """
    def __init__(self, base_url: str, model_name: str):
        self.base_url = base_url
        self.model_name = model_name
        self.headers = {"Content-Type": "application/json"}

    def send_prompt(self, prompt: str, schema: dict = None, temperature: float = 0.7, max_tokens: int = 100):
        """
        Send a custom prompt to the LLM and receive the response.

        Args:
            prompt (str): The user-provided prompt to send to the LLM.
            schema (dict, optional): A JSON schema to enforce structured output. Defaults to None.
            temperature (float): Sampling temperature for randomness. Defaults to 0.7.
            max_tokens (int): Maximum number of tokens to generate. Defaults to 100.

        Returns:
            str or dict: The generated response from the LLM. If a schema is provided, it returns a dictionary.
        """
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"""
                You are generating JSON transformations for a DataFrame. These transformations should follow the structure:
                [
                    {{"operation": "select", "columns": ["column1", "column2"]}},
                    {{"operation": "filter", "predicates": ["column1 > 10", "column2 == 'value'"]}}
                ]
                Only include "select" if the user requests it, without adding "filter".
                Example:
                Input: "Select columns 'A', 'B' and filter rows where 'A' > 5."
                Output: [
                    {{"operation": "select", "columns": ["A", "B"]}},
                    {{"operation": "filter", "predicates": ["A > 5"]}}
                ]
                Input: "Select columns 'A', 'B'."
                Output: [
                    {{"operation": "select", "columns": ["A", "B"]}}
                ]
                Now, generate a transformation for the following request:
                {prompt}
                """}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }

        if schema:
            payload["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": "custom_response",
                    "strict": "true",
                    "schema": schema
                }
            }

        try:
            response = requests.post(f"{self.base_url}/v1/chat/completions", headers=self.headers, json=payload)
            if response.status_code == 200:
                data = response.json()
                if schema:
                    # Parse and return structured JSON response
                    return json.loads(data["choices"][0]["message"]["content"])
                else:
                    # Return plain text response
                    return data["choices"][0]["message"]["content"]
            else:
                raise Exception(f"Error: {response.status_code}, {response.text}")
        except Exception as e:
            raise Exception(f"Failed to send prompt: {str(e)}")
