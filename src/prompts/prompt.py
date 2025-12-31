
from src.io.firebase import FirebaseClient
from pprint import pp

db = FirebaseClient.get_instance()
def read_overviews(collection:str) -> list[str]:
   docs = db.get_all_latest_entries("programs-display")

   overviews = []
   for doc in docs:
      overview = docs[doc]["overview"]
      title = overview["title"]
      provider = overview["provider"]
      link = overview["link"]

      info = f"Title: {title}. Provider: {provider}. Link: {link}\n"
      overviews.append(info)

   return overviews

PROMPT = f"""
You are given a dictionary of program information including links below.
{read_overviews("programs-display")}
Analyze the programs to understand what types of opportunities are being collected.

Your task: Find extracurricular programs (internships, fellowships, summer programs, research opportunities) for high school or undergraduate students that are NOT already in the given dictionary.

## Search Strategy

Use diverse, specific queries:
- Subject-specific: "biology research internship high school", "creative writing summer program undergraduates"
- Institution-specific: "MIT summer program high school", "NASA internship high school students"
- Location-specific: "STEM internship high school students California", "humanities program teenagers Boston"
- Program-type specific: "paid research internship high school", "residential summer program", "virtual internship high school"
- Combine filters: "biomedical research internship high school paid summer"

Search across all domains (.edu, .org, .gov, .com) from universities, research institutions, nonprofits, government agencies, museums, hospitals, and corporations.

## Critical: Find INDIVIDUAL Program Pages

For each potential program you discover:

1. **Initial page analysis**: If you land on a LIST page (e.g., "Top 10 Internships", "Summer Programs Directory", aggregator sites), you MUST:
   - Extract individual program links from that page
   - Visit each individual program's website
   - Navigate to find the specific program's dedicated overview/landing page

2. **Navigate to the most specific overview page**: Look for links containing:
   - /about/, /overview/, /details/, /description/
   - /[program-name]/ (specific program slug)
   - Follow "Learn More", "Program Details", "About This Program" buttons
   - DO NOT prioritize /apply/, /application/, or /admissions/ pages (these often lack overview info)

3. **Verify it's a single-program page** by checking if the page:
   ✓ Has ONE program name as the main heading
   ✓ Contains specific details (dates, eligibility, curriculum, description) for ONE program
   ✓ Describes what participants will do/learn in ONE specific program
   ✗ Lists multiple programs with different names
   ✗ Is a department page showing "Our Programs" with multiple options
   ✗ Is a generic "Opportunities" or "Get Involved" page

4. **Multi-program pages**: If a page lists multiple distinct programs (e.g., "Summer Program A", "Summer Program B", "Fall Fellowship"), check if each has its own dedicated page:
   - YES: Return the individual program overview pages, not the parent page
   - NO: Only then return the multi-program page as a last resort

5. **Determine the canonical URL**: Return the most specific, stable overview URL:
   - Prefer: https://example.edu/summer-programs/stem-research-internship (program overview)
   - Over: https://example.edu/summer-programs (parent directory)
   - Over: https://example.edu/summer-programs/stem-research-internship/apply (application page)
   - Over: https://example.edu/summer-programs/stem-research-internship?utm_source=google (with tracking params)

## Skip These Pages

- PDFs, downloadable brochures, application forms
- News articles, press releases, blog posts about programs
- Event calendars, academic calendars
- Generic directory/aggregator listings (unless you extract individual links from them)
- Social media posts
- Application portals or "How to Apply" pages (unless they contain the main overview)
- "Contact", "FAQ" pages (unless the FAQ IS the main program page)
- Pages that say "applications closed" or "program discontinued" without future info
- Student testimonial pages (unless they're part of the main program page)
- Pages listing past participants or alumni

## Before Returning Results

1. **Check every link** you plan to return:
   - Does it describe exactly ONE specific program with overview information?
   - Is it the most specific overview/landing page available for that program?
   - Is it a stable, official URL (not a cached/archived/proxy version)?

2. **Deduplicate against existing programs**:
   - Compare program NAME and HOST INSTITUTION, not just URLs
   - If "MIT Biology Internship" is already in the dictionary at ANY URL, don't return it
   - Even if you find a different URL for an existing program, DON'T include it (we already have it)

3. **Deduplicate within your results**:
   - Don't return multiple URLs for the same program
   - If you found both the parent page and specific page, return only the specific page
   - Remove any tracking parameters (?utm_source=, ?ref=, etc.) from URLs

4. **Final verification**: For each URL in your list, confirm:
   - [ ] Single program only (or multi-program only if no individual pages exist)
   - [ ] Most specific overview/landing page available (not application page)
   - [ ] Not a duplicate of existing programs (same program name + institution)
   - [ ] Not a duplicate within your new list
   - [ ] Official, stable URL

## Output Format

Return ONLY a clean Python list of URLs, one per line.
Example:
```python
[
    "https://example.edu/programs/summer-research-internship",
    "https://research-org.org/high-school-fellowship",
    ...
]
 CRITICAL: DO NOT RETURN ANYTHING BUT A LIST OF URLs. DO NOT RETURN ANY EXTRA COMMENTARY OR SITE CONTENTS.
"""