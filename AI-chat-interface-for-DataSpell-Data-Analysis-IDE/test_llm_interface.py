from Task1.Layer2.llm_interface import LLMInterface


base_url = "http://192.168.1.139:1234"
model_name = "llama-3.2-1b-instruct"

llm = LLMInterface(base_url, model_name)


# Simple prompt
prompt = "What is the capital of France?"
response = llm.send_prompt(prompt)
print("Response:", response)

# Prompt with structured schema
structured_prompt = "Give me a JSON object with a fact about the Eiffel Tower."
schema = {
    "type": "object",
    "properties": {
        "fact": {"type": "string"}
    },
    "required": ["fact"]
}
structured_response = llm.send_prompt(structured_prompt, schema=schema)
print("Structured Response:", structured_response)