
import json

with open("src/prompts/assets/schemas.json", 'r', encoding="utf-8") as file:
    SCHEMA = json.load(file)

REPEAT_INSTRUCTIONS = """
Return this schema with the data completely populated (no section has "not provided" and all lists have entries)

SEARCH INSTRUCTIONS:
You will be responsible yourself to think of ways to find the information with the tools given to you.
If you are stuck however, the following tips are a starting point to get the information that is needed.
Get started by searching: "[title of program] [program provider] [missing section name]" (with underscores and dashes replaced by spaces to get the most search results)

Core rules:
- Do NOT change the structure of the given schema.
"""

PROMPTS = {
    "overview": f"""
SCHEMA:
"overview": {SCHEMA["overview"]}

{REPEAT_INSTRUCTIONS}

Fill:
- "title": Full program name.
- "provider": Organization offering the program.
- "description": A summary or mission statement.
- "subject": List of academic topics.
  - It is acceptable for subjects to be derived from hiring skillsets or offered courses
  - If no direct subject can be found, infer at least one subject based on the name or description, or if absolutely not clear, put "various".
- "tags": Keywords like "free", "residential", or "virtual".

In the schema there may be a "link" key; that is only for the program, so don't change it.
""",



    "eligibility": f"""
SCHEMA:
"eligibility": {SCHEMA["eligibility"]}

{REPEAT_INSTRUCTIONS}

ADDITIONAL SEARCH INSTRUCTIONS:
For eligiblity specifically, search for the form where you apply for the program and look through the requirements.
Also search for requirements like essays with double quotes around the search term to return search results always including the search term.
Eg. 'brainyac rutgers "recommendation"' returns results that have to have the word "recommendation" in the contents.

Fill:
- "essay_required", "recommendation_required", "transcript_required": Use true, false, or "not provided".
- "other": List any extra requirements mentioned like "An interview is required" or "A portfolio is required".
- "grades": Convert phrases like "rising 11th and 12th graders" to "Rising Junior" and "Rising Senior". Don't include "Rising" if not specified.
- "age": Fill "minimum" or "maximum" only if exact numbers are provided.

Be literal and precise — convert 9th, 10th, 11th, and 12th grade to freshman, sophomore, junior, and senior respectively.
""",



    "dates": f"""
SCHEMA:
"dates": {SCHEMA["dates"]}

{REPEAT_INSTRUCTIONS}

Update deadlines:
- Add each deadline as a separate object.
- Fields: "name", "priority" ("high" only for the most important application deadline, rank other priorities yourself based on context), "term", "date", "rolling_basis", "time".

Update program dates:
- Include term (Summer, Winter, Spring, Fall), start, and end dates only if both are clearly stated.
- Use mm-dd-yyyy format.
  - Providing only the month for dates where the days aren't given is acceptable (e.g. "September 2026")
  - If the year isn't provided, it is safe to assume that it refers to the current year

Update duration_weeks:
- Use a number only if the duration is clearly stated (e.g., "6-week program").
- Otherwise, use "not provided".

Do not infer dates or duration from vague phrases or context.
""",



    "locations": f"""
SCHEMA:
"locations": {SCHEMA["locations"]}

{REPEAT_INSTRUCTIONS}

Fill:
- "virtual": true if clearly online, false if clearly in-person, "hybrid" if both, "both available" if both are available, "not provided" if unclear.
- "state", "city", "address": Use only if directly stated.

Include only the main residential/instructional site — ignore travel destinations or event locations.
""",



    "costs": f"""
SCHEMA:
"costs": {SCHEMA["costs"]}

{REPEAT_INSTRUCTIONS}

Cost objects (tuition, fees, etc.):
- "free": Set to true only if explicitly stated. If true, set "lowest" and "highest" to null.
- "lowest"/"highest": Use numbers only if directly stated; if not stated and not free, leave as "not provided".
- "financial-aid-available": Use true, false, or "not provided".

Stipend:
- "available": true only if explicitly mentioned, false if clearly absent.
- "amount": Use number if stated. If "available" is false, set to null.

Include each cost type as a separate object if multiple are mentioned.
""",



    "contact": f"""
SCHEMA:
"contact": {SCHEMA["contact"]}

{REPEAT_INSTRUCTIONS}

Core rules:
- Only include contact info shown directly in the webpage content.
- Do not infer or assume from context or page layout.
- Leave fields as "not provided" if missing.
- Only include the most important contact to an applicant.

Fill:
- "email": Must be a complete and valid address (e.g., contact@school.edu).
- "phone": Must be clearly formatted and complete (123-456-7890).

Do not copy from social links or headers unless the contact is fully visible in the content. 
"""
}