
from langchain_core.output_parsers import PydanticOutputParser
from pprint import pp
import re

from ..schemas import schemas

import re

import json
import re
from langchain.output_parsers import PydanticOutputParser

class ResponseParser:
   def parse_raw_response(self, raw_response, section: str):
       try:
           raw_output = raw_response.get("output", "")
           if not raw_output:
               return None
           
           # Find complete JSON by tracking braces
           first_brace = raw_output.find('{')
           if first_brace == -1:
               return None
           
           brace_count = 0
           i = first_brace
           in_string = False
           escape_next = False
           
           while i < len(raw_output):
               char = raw_output[i]
               
               if escape_next:
                   escape_next = False
               elif char == '\\':
                   escape_next = True
               elif char == '"' and not escape_next:
                   in_string = not in_string
               elif not in_string:
                   if char == '{':
                       brace_count += 1
                   elif char == '}':
                       brace_count -= 1
                       if brace_count == 0:
                           json_content = raw_output[first_brace:i + 1]
                           break
               i += 1
           else:
               return None
           
           # Try Pydantic first, fallback to plain JSON
           try:
               parser = PydanticOutputParser(pydantic_object=schemas[section])
               structured_response = parser.parse(json_content)
               
               if hasattr(structured_response, 'model_dump'):
                   return structured_response.model_dump()
               elif hasattr(structured_response, 'dict'):
                   return structured_response.dict()
               else:
                   return structured_response
           except:
               return json.loads(json_content)
               
       except Exception as e:
           print(f"Error parsing {section}: {e}")
           return None