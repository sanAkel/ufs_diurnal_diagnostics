#!/usr/bin/env python3

import sys

def rtofs_hpss_path(exp_name, path, date, tar_file_pref, tar_file_suff):

  if exp_name == "v2.4":
    # If v2.4, form a string like:
    # /NCEPPROD/1year/hpssprod/runhistory/rh2024/202411/20241105/com_rtofs_v2.4_rtofs.20241105.nc.tar
    cmd = path +\
         'rh{}/'.format(date.strftime('%Y')) +\
         '{}/'.format(date.strftime('%Y%m')) +\
         '{}/'.format(date.strftime('%Y%m%d')) +\
         tar_file_pref + '{}'.format(date.strftime('%Y%m%d')) + tar_file_suff
    cmd = cmd +  ' ' + './'

  elif exp_name == "v2.5":
    # form a string like:
    # emc-ocean/5year/Dan.Iredell/rtofs.v2.5.test01/rtofs.20241225/rtofs.ncgrb.tar
    cmd = path +\
         'rtofs.{}/'.format(date.strftime('%Y%m%d')) +\
         tar_file_pref + tar_file_suff
    cmd = cmd +  ' '

  else:
    sys.exit("\n\nUnknown exp_name. Fix and try again\n\n")

  return cmd

