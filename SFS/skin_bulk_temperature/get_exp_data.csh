#!/bin/csh -f

if ($#argv < 5 ) then
  echo " "
  echo " To gather data from HPSS "
  echo " "
  echo "Required module(s): hpss"
  echo " "
  echo "REQUIRED INPUTS: "
  echo " "
  echo "Data Path (on HPSS)" 
  echo "e.g., /ESRL/BMC/fim/5year/Shan.Sun/hr4hydro_20241024/"
  echo " "
  echo "Name of the experiment"
  echo "e.g., c96mx100_mem000"
  echo " "
  echo "Date (format: yyyymmdd)" 
  echo " e.g., 19940501"
  echo " "
  echo "Type of the file (e.g., surface atmosphere: _atm_raw_sfcf_)"
  echo " e.g., _atm_raw_sfcf_"
  echo " "
  echo "Output data path"
  echo " e.g., /collab1/data/Santha.Akella/skinSST_vs_NSST/data"
  echo " "
  exit 1
endif

set data_path_root = $1 
set exp_name = $2
set start_date = $3
set fType = $4
set output_data_path = $5

echo " "
echo "-- Gathering data from HPSS --"
echo " "

set fName_tmpl = ${exp_name}${fType}${start_date}".tar"

set fName = ${data_path_root}/${exp_name}/${start_date}/${fName_tmpl}
echo $fName

cd ${output_data_path}

echo " "
echo "Current path: "
pwd -P
echo " "

set output_dir = ${exp_name}_${start_date}
mkdir -p ${output_dir}
hsi get ${fName}
/usr/bin/mv *.tar ${output_dir}

echo " "
echo "All done."
