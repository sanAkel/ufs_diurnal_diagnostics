#!/usr/bin/env python3

import os
import argparse
import yaml
import pandas as pd

# user inputs
get_inputs = argparse.ArgumentParser(prog='\ndrive_fcst_err.py',\
             description='Calculate RTOFS forecast error over a daterange and variableS', usage='%(prog)s [options]')

get_inputs.add_argument('--config_file', type=str,\
             help='yaml file that sets configuration, see provided yaml file for an example',\
             default=\
             '/collab1/data/Santha.Akella/skinSST_vs_NSST/scripts/ufs_diurnal_diagnostics/RTOFS/score-card/compute/config-fcst_err.yaml')
args = get_inputs.parse_args()
# --

config_file = args.config_file
config = yaml.load( open( config_file, "r"), Loader=yaml.FullLoader)

start_date, end_date = [pd.to_datetime(config['start_date']), pd.to_datetime(config['end_date'])]
vars = config['variables']

for d in pd.date_range(start_date, end_date):
  for var in vars:
    cmd = "./forecast_error_day.py --proc_date {} --var_name {}".format(d.strftime('%Y%m%d'), var)
    #print(cmd)
    exit_code = os.system(cmd)
