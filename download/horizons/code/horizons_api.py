"""Access horizons api

https://ssd-api.jpl.nasa.gov/doc/horizons.html"""

import itertools
import re
import requests
import json
from datetime import datetime, timedelta
import pandas as pd

# FORMAT = "text"
# OBJECT = 199
# START = "2024-Nov-18"
# END = "2024-Nov-19"
# STEP = "1d"
# COORD_CENTER = "000@399"
# OBJ_DATA = "YES"
# MAKE_EPHEM = "YES"
# EPHEM_TYPE = "VECTORS"

def make_url(
    OBJECT:int,
    COORD_CENTER:str,
    START:str,
    END:str,
    STEP:str,
    OBJ_DATA:str,
    MAKE_EPHEM:str,
    EPHEM_TYPE:str,
    FORMAT:str,
):
    url = f"https://ssd.jpl.nasa.gov/api/horizons.api?\
format={FORMAT}&\
COMMAND={OBJECT}&\
OBJ_DATA={OBJ_DATA}&\
MAKE_EPHEM={MAKE_EPHEM}&\
EPHEM_TYPE={EPHEM_TYPE}&\
CENTER={COORD_CENTER}&\
START_TIME={START}&\
STOP_TIME={END}&\
STEP_SIZE={STEP}"
    return url


def get_horizons_data(
    OBJECT:int,
    COORD_CENTER:str, #"000@399",
    START:str = None,
    END:str = None,
    STEP:str = "1d",
    OBJ_DATA:str = "YES",
    MAKE_EPHEM:str = "YES",
    EPHEM_TYPE:str = "VECTORS",
    FORMAT:str = "text",
):
    if START is None:
        today = datetime.today()
        START = today.strftime("%Y-%b-%d")
    if END is None:
        END = today + timedelta(days=1)
        END = END.strftime("%Y-%b-%d")
    url_dict = {
        'OBJECT':OBJECT,
        'COORD_CENTER':COORD_CENTER,
        'START':START,
        'END':END,
        'STEP':STEP,
        'OBJ_DATA':OBJ_DATA,
        'MAKE_EPHEM':MAKE_EPHEM,
        'EPHEM_TYPE':EPHEM_TYPE,
        'FORMAT':FORMAT
    }
    url = make_url(**url_dict)
    print(url)
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def get_timedate(line):
    timedate_numeric = line.split(" ")[0]
    timedate_pattern = r'\d{4}-[A-Za-z]{3}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{4}'
    timedate_str = re.search(timedate_pattern, line)
    return timedate_numeric, timedate_str.group()


def get_key_values(line):
    pattern = r'(\w+)\s*=\s*(-?\d+\.?\d*+E[+-]?\d+)'
    kvs = re.findall(pattern, line)
    return kvs


def parse_line(line):
    result = None
    try:
        result = get_timedate(line)
    except AttributeError as e:
        if "NoneType" in e.args[0]:
            pass
        else:
            raise e
    if not result:
        result = get_key_values(line)
    return result


def parse_lines(lines):
    parsed_lines = [parse_line(line) for line in lines]
    records = []
    for i in range(0, len(parsed_lines), 4):
        single_record = parsed_lines[i: i+4]
        record = {}
        record['date_num'] = single_record[0][0]
        record['date_str'] = single_record[0][1]
        flattened_list = list(itertools.chain(*single_record[1:]))
        for k,v in flattened_list:
            record[k] = v
        records.append(record)
    return pd.DataFrame(records)


def load_ephemeris(filepath):
    """Load HORIZONS ephemeris data into pandas dataframe"""

    #Read in ephemeris file
    with open(filepath, "r") as ephemeris:
        lines = ephemeris.readlines()
    #Get line number with start and end of ephemeris symbol
    start = [i for i,line in enumerate(lines) if "$$SOE" in line][0]
    end = [i for i,line in enumerate(lines) if "$$EOE" in line][0]
    lines = lines[start+1:end]
    ephemeris = parse_lines(lines)
    return ephemeris


def index_multiplier(index):
    power = re.search(r"10\^(\d+)", index)
    if power:
        power = power.group(1)
        power = float(power)
    else:
        power = 0
    return 10**power


def load_physical_data(filepath):
    with open(filepath, "r") as ephemeris:
        lines = ephemeris.readlines()
    #Get line number with start and end of ephemeris symbol
    start = [i for i,line in enumerate(lines) if line.startswith((" PHYSICAL", " GEOPHYSICAL", " SATELLITE PHYSICAL PROPERTIES"))][0]
    end = [i for i,line in enumerate(lines) if re.search("[Aa]phelion|SATELLITE ORBIT|Sunspot", line)][0]
    lines = lines[start+1:end]
    lines = [line.replace("~","") for line in lines]
    pattern = r'(\w+[\w\s\(\)\^\/\-\[\]\.,]+\s*)+\s*=\s*(-?\d+\.?\d*)'
    KVs = [re.findall(pattern, line) for line in lines]
    flattened_list = list(itertools.chain(*KVs))
    physical_data = {}
    for k,v in flattened_list:
        multiplier = index_multiplier(k)
        physical_data[k] = float(v) * multiplier
    physical_data = pd.Series(physical_data)
    return physical_data


ephem = get_horizons_data(OBJECT=199, COORD_CENTER="000@399")
filepath = "eg_ephem.txt"
with open(filepath, "w") as f:
    f.write(ephem)
ephem = load_ephemeris(filepath)
physical_data = load_physical_data(filepath)
