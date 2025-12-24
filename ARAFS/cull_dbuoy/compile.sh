#!/bin/bash

# Ensure gfortran is in your path
# -- on Ursa
# ml gcc/12.4.0

gfortran prepbufr_no_dbuoy.F90 -o /home/Santha.Akella/marine-scratch5/tmp/ufs_diurnal_diagnostics/ARAFS/cull_dbuoy/no_dbuoy.x \
    /home/Santha.Akella/marine-scratch5/ncep-bufr/install/lib64/libbufr_4.a

chmod +x /home/Santha.Akella/marine-scratch5/tmp/ufs_diurnal_diagnostics/ARAFS/cull_dbuoy/no_dbuoy.x


#gfortran mnemonic_discovery.F90 -o discovery.x \
#   /home/Santha.Akella/marine-scratch5/ncep-bufr/install/lib64/libbufr_4.a
