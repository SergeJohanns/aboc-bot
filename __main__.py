#!/usr/bin/env python3.8

import json
from Bot import Bot

PERS_CORE = "PersonalityCore.json"
print(f"Loading personality core '{PERS_CORE}'...", end='\r')
with open(PERS_CORE, 'r') as pcorefile:
    pcore = json.loads(pcorefile.read())
print(f"Successfully loaded personality core '{PERS_CORE}'")
print(f"Target functionality cores: {', '.join(pcore['fcores'])}")

Bot(pcore)