#!/bin/csh -f

set input_path = "/ESRL/BMC/fim/5year/Shan.Sun/hr4hydro_20241024/"
set exp_name = "c96mx100_mem000"
set file_type = "_atm_raw_sfcf_"
set output_path = "/collab1/data/Santha.Akella/skinSST_vs_NSST/data"
set cmd_name = "./get_exp_data.csh "

set start_year = 1995
set end_year = 2023
set mon_ = 5
set dd_ = 1
# --

# month and day need to be 2 digit
set mon = `printf "%02d" ${mon_}`
set dd  = `printf "%02d" ${dd_}`

set yr = ${start_year}
while (${yr} <= ${end_year})
  set date = ${yr}${mon}${dd}
  echo ${date}
  ${cmd_name} ${input_path} ${exp_name} ${date} ${file_type} ${output_path}
  set yr = `expr ${yr} + 1`
end

