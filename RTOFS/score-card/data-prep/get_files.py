#!/usr/bin/env python3

import os
import sys
import subprocess
import yaml
import argparse
import pandas as pd

import warnings
warnings.filterwarnings('ignore') 
# --

from utils import rtofs_hpss_path

# user inputs
get_inputs = argparse.ArgumentParser(prog='\nget_files.py',\
             description='To gather RTOFS nowcast and forecast files from HPSS', usage='%(prog)s [options]')

get_inputs.add_argument('--config_file', type=str,\
                        help='yaml file that sets configuration, see provided yaml file for an example',\
                        default=\
                        '/collab1/data/Santha.Akella/skinSST_vs_NSST/scripts/ufs_diurnal_diagnostics/RTOFS/score-card/data-prep/config-get_data.yaml')
args = get_inputs.parse_args()
# --

config_file = args.config_file

config = yaml.load( open( config_file, "r"), Loader=yaml.FullLoader)
exp_labels = config['exp_labels']

nEXP = len(exp_labels)

start_date, end_date = [pd.to_datetime(config['start_date']), pd.to_datetime(config['end_date'])]
data_dates=pd.date_range(start_date, end_date, freq='D')

print("\n\nMake sure you have loaded module: hpss\n\n")
cwd = os.getcwd()
print("Current path:\n{}".format(cwd))

# Gather data from experiment
for iexp in range(nEXP):
  exp_name  = config['%s'%(exp_labels[iexp])]['name']
  data_path = config['%s'%(exp_labels[iexp])]['path']
  print("\n\nGathering data from: ", exp_name)

  oPath = config['output_path'] + exp_name
  if os.path.exists( oPath):

      for data_date in data_dates:
         output_dir = oPath + "/"+ "{}".format(data_date.strftime('%Y%m%d'))
         subprocess.run( ["mkdir", "-p", "{}".format(output_dir)], check=True, capture_output=True)
         os.chdir( output_dir)
         #print(output_dir)

         cmd0 = rtofs_hpss_path( exp_name, config['%s'%(exp_labels[iexp])]['path'],\
                          data_date,\
                          config['%s'%(exp_labels[iexp])]['tar_file_pref'],\
                          config['%s'%(exp_labels[iexp])]['tar_file_suff'])
         #print(cmd0)

         cmd_n = cmd0 + config['nowcast_file_pref'] + '*' + config['nowcast_file_suff']
         cmd_f = cmd0 + config['fcstcast_file_pref']+ '*' + config['fcstcast_file_suff']

         stat1 = os.system("htar -xvf " + cmd_n)
         if stat1 == 0:
           print("Fetched nowcast files from {}".format(data_date.strftime('%Y%m%d')))

         stat2 = os.system("htar -xvf " + cmd_f)
         if stat2 == 0:
           print("Fetched forecast files from {}".format(data_date.strftime('%Y%m%d')))
