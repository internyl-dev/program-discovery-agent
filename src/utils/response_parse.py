
from langchain_core.output_parsers import PydanticOutputParser
from pprint import pp

from ..schemas.response_model import RootSchema

parser = PydanticOutputParser(pydantic_object=RootSchema)

def parse_raw_response(raw_response):
    try:
        # The output is already a string, not a list with a text field
        raw_output = raw_response.get("output")
        
        # Remove the 'json' prefix if it exists
        if raw_output.startswith('json\n'):
            raw_output = raw_output[5:]  # Remove 'json\n'
        
        structured_response = parser.parse(raw_output)
        pp(structured_response)
        
    except Exception as e:
        print("Error parsing response", e)
        print("Raw Response - ", raw_response)
        print("Output content - ", raw_response.get("output"))