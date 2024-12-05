#!/usr/bin/env python3

import os
import pandas as pd

#date_s, date_e = ['20240705', '20241009'] # parallel (v2.5) forecasts did not go out to 8-days.
date_s, date_e = ['20241010', '20241031']
#date_s, date_e = ['20241101', '20241130']

year='2024'
output_root_path = "/home/Santha.Akella/marineda-scratch2/data/rtofs-v2.5/"

cmd_str = "htar -xvf "
prod_path_root = "/NCEPPROD/1year/hpssprod/runhistory/rh{}/".format(year)
para_path_root = "emc-ocean/5year/Dan.Iredell/rtofs.v2.5.test01/"

# Use of os.system() SHOULD BE CLEANED UP!
for d in pd.date_range(date_s, date_e):

  VER_NUM = "2.4" # default, but changes if below happens
  mm = "{}".format(d.strftime('%m'))
  dd = "{}".format(d.strftime('%d'))
  if (mm=="07") or (mm=="08"):
    VER_NUM = "2.3"
  if (mm=="09") and (dd<"13"):
    VER_NUM = "2.3"

  # create output (sub)dir(s)
  output_prod_path = output_root_path + "v2.4/{}".format(d.strftime('%Y%m%d'))
  output_para_path = output_root_path + "v2.5/{}".format(d.strftime('%Y%m%d'))
  cmd1 = "mkdir -p {}".format(output_prod_path)
  cmd2 = "mkdir -p {}".format(output_para_path)

  #print(cmd1)
  #print(cmd2)
  exit_code1 = os.system(cmd1)
  exit_code2 = os.system(cmd2)

  # get files from hpss
  prod_cmd = cmd_str + prod_path_root+\
                 "{}/".format(d.strftime('%Y%m'))+\
                 "{}/".format(d.strftime('%Y%m%d'))+\
                 "com_rtofs_v{}_rtofs.{}.nc.tar".format(VER_NUM, d.strftime('%Y%m%d')) +\
                 "  " + "./rtofs_glo_2ds_f*_prog.nc"
  #print(prod_cmd)
  exit_code3 = os.system(prod_cmd)
  cmd_x1 = "mv *.nc {}".format(output_prod_path)
  #print(cmd_x1)
  exit_code4 = os.system(cmd_x1)

  para_cmd = cmd_str + para_path_root+\
                 "rtofs.{}/".format(d.strftime('%Y%m%d'))+\
                 "rtofs.ncgrb.tar" +\
                 "  " + "rtofs_glo_2ds_f*_prog.nc"

  #print(para_cmd)
  exit_code5 = os.system(para_cmd)
  cmd_x2 = "mv *.nc {}".format(output_para_path)
  #print(cmd_x2)
  exit_code6 = os.system(cmd_x2)
