#!/usr/bin/env python3

import os
import pandas as pd

date_s, date_e = ['20241016', '20241031']

for d in pd.date_range(date_s, date_e):
  # print( d.strftime('%Y%m%d'))
  cmd = "./diff_surf_fields.py --date {}".format(d.strftime('%Y%m%d'))
  print(cmd)
  exit_code = os.system(cmd) # REPLACE WITH SHUTIL
