""" Parse Horizons """

import re
import pandas as pd

def parse_horizons_ephemeris_string(text):
    entries = []
    
    # Split into blocks by Julian date lines
    blocks = re.split(r'(?=\d+\.\d+\s+=)', text.strip())
    
    for block in blocks:
        if not block.strip():
            continue
        
        # Extract Julian date
        jd_match = re.search(r'(\d+\.\d+)\s+=', block)
        jd = float(jd_match.group(1)) if jd_match else None
        
        # Extract calendar date/time
        date_match = re.search(r'A\.D\.\s+([^\n]+)', block)
        date_str = date_match.group(1).strip() if date_match else None
        
        # Extract vectors and scalar values
        def get_val(label):
            m = re.search(rf'{label}\s*=\s*([-\d\.E\+]+)', block)
            return float(m.group(1)) if m else None
        
        entry = {
            "jd": jd,
            "datetime": date_str,
            "X": get_val("X"),
            "Y": get_val("Y"),
            "Z": get_val("Z"),
            "VX": get_val("VX"),
            "VY": get_val("VY"),
            "VZ": get_val("VZ"),
            "LT": get_val("LT"),
            "RG": get_val("RG"),
            "RR": get_val("RR"),
        }
        
        if any(entry.values()):
            entries.append(entry)
        
        ephemeris = pd.DataFrame(entries)
    
    return ephemeris


def parse_horizons(filepath):
    with open(filepath, "r") as ephemeris:
        lines = ephemeris.read()
    # Extract ephemeris data as string
    ephemeris_string = re.search(
        r"\$\$SOE\s*(.*?)\s*\$\$EOE",
        lines,
        re.S
    ).group(1)
    # Parse ephemeris string to dataframe
    ephemeris_data = parse_horizons_ephemeris_string(
        ephemeris_string
    )
    physical_data = None
    return ephemeris_data, physical_data
