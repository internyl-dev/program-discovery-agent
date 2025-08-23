
from src.firebase import firebase


def read_overviews(collection:str):
    docs = list(firebase.read_documents(collection).values())

    i=0
    while i < len(docs):
        docs[i] = docs[i]["overview"]
        i+=1

    return docs

PROMPT = f"""
You are given a dictionary of program information including links below.
{read_overviews("programs-display")}
Analyze the programs to understand what is being looked for. 
Find extracurricular programs of any subject, any due date, any institution, etc. on the web that are not already on the given dictionarty.
Return just the links for the program overview page found as a list.

Search for extracurricular programs, internships, fellowships, summer programs, or research opportunities for high school or undergraduate students across any subject and provider. Use query variations such as: "high school internship", "summer program for high school students", "undergraduate research program", "pre-college program", "STEM summer program", "humanities summer program", "college readiness summer program", and "paid high school internships". Do not limit to .edu sites—also include .org, .gov, and reputable .com domains.

Prioritize official overview or landing pages for programs (URLs often contain /internship/, /programs/, /precollege/, /summer/, /opportunities/, but don't limit your search to this).

Skip:
- PDFs
- News articles
- Blog posts
- Event calendars
- Generic directory listings

Before returning, compare against {read_overviews("programs-display")} and exclude duplicates. Return only a clean list of unique links to program overview pages.

"""