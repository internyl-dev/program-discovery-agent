
from .response_model import *

schemas = {
    "overview": Overview,
    "eligibility": Eligibility,
    "dates": Dates,
    "locations": Locations,
    "costs": Costs,
    "contact": Contact,
    "all": RootSchema
}

print("Root schema initialized")