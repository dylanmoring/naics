# naics

naics provides a convenient interface for working with NAICS codes.


Usage:
```
from naics import NAICS

# Instantiate NAICS for code 111 (Crop Production)
crop_production = NAICS(111)

# List all child codes
# e.g. 1111 - Oilseed and Grain Farming, 11111 - Soybean Farming
crop_production.child_codes

# List all parent codes
# e.g. 11 - Agriculture, Forestry, Fishing and Hunting
crop_production.parent_codes

# List all cross-reference codes
# Cross-reference codes are non-child codes that include businesses that could also fall
#   under the definition of the original code. Can be used to determine alternative search
#   codes
# e.g. 11251 - Aquaculture, 113210 - Forest Nurseries and Gathering of Forest Products
crop_production.cross_reference_codes

# List all potential subcodes
# This is all child codes as well as all cross-reference codes with more digits than the 
#   primary code
# e.g. 11111 - Soybean Farming, 11251 - Aquaculture
crop_production.all_potential_subcodes

# List all included index activities
# These are all economic activities that are included under this code. Useful for fine-tuning
# e.g. Agave farming, Almond farming
crop_production.included_activities


# Get next code in hierarchy
# Returns the next highest code in the same level
# e.g. 112 - Animal Production and Aquaculture
crop_production.next_code


# Get previous code in hierarchy
# Returns the next lowest code in the same level
# e.g. None (111 is the first 3-digit code)
crop_production.next_code
```

