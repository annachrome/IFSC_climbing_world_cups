import pandas as pd
import json
import logging
from datetime import datetime
import re

dir = '/Users/apple/Documents/PROGRAMMING/IFSC_climbing_world_cups/Data Analysis/ifsc_data/'
category = "Wcombined"

data = pd.read_csv(dir + category + ".csv")

print(data["stage_rank"])

