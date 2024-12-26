import pandas as pd
from jsonschema import validate, ValidationError
from Layer1.transformations import apply_transformations
from Layer2.llm_interface import LLMInterface

# Initial Data
data = {
    'name': ['John', 'Jane', 'Bob', 'Alice'],
    'age': [17, 30, 35, 40],
    'salary': [50000, 60000, 70000, 80000],
    'department': ['HR', 'IT', 'Sales', 'Marketing']
}
df = pd.DataFrame(data)

# Initiate LLMInterface
base_url = "http://192.168.1.139:1234"
model_name = "llama-3.2-1b-instruct"
llm = LLMInterface(base_url, model_name)

def run():
    while True:
        user_input = input("Enter your query (or 'exit' to quit): ")

        if user_input.lower() == 'exit':
            print("Exiting the program.")
            break

        # Generate Transformations with LLM
        prompt = f"""
        Generate a sequence of transformations in JSON format to:

        {user_input}

        The output should be an array of transformation objects, where:
        - Each array should have at least one object.
        - Each object must have an "operation" field, which is either "filter" or "select".
        - For "filter" operations, include a "predicates" field with the filtering conditions.
        - For "select" operations, include a "columns" field with the names of the columns to select.
        """
        schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "operation": {"type": "string", "enum": ["select", "filter"]},
                    "columns": {"type": "array", "items": {"type": "string"}},
                    "predicates": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["operation"],
                "additionalProperties": False
            }
        }

        # Send Prompt and Validate Transformations
        transformations = llm.send_prompt(prompt, schema=schema)
        print("Transformations received from LLM:", transformations)

        # Validate LLM Response
        try:
            validate(instance=transformations, schema=schema)
        except ValidationError as e:
            print(f"LLM output validation failed: {e}")
            continue

        if not transformations or not isinstance(transformations, list):
            print("No valid transformations received from LLM.")
            continue

        # Apply Transformations
        try:
            transformed_df = apply_transformations(df, transformations)
            print(transformed_df)
        except ValueError as ve:
            print(f"ValueError: {ve}")
        except KeyError as ke:
            print(f"KeyError: {ke}")
        except Exception as e:
            print(f"Unexpected error: {e}")


run()