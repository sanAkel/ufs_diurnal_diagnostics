#!/bin/bash

exec_path="/scratch5/NCEPDEV/rstprod/Santha.Akella/ncep-bufr/install/bin/"

DATE_DIR="20251222"
data_path_in="/scratch5/NCEPDEV/rstprod/Santha.Akella/data/prepbufr/${DATE_DIR}/"
data_path_out="/scratch5/NCEPDEV/rstprod/Santha.Akella/data/no_dbuoy/${DATE_DIR}/"
#
# what to extract from SFCSHP ("surface marine" part of the prepbufr)
bufr_code=564

cwd=$(pwd)

# 1. Split prepbufr by type
for hdir in 00z 06z 12z 18z; do
  mkdir -p $data_path_out/$hdir/
  cd $data_path_out/$hdir/
  #echo $PWD
  infile="$data_path_in/gdas.t${hdir}.prepbufr.nr"
  if [[ -f "$infile" ]]; then
    echo "Splitting [$infile] "
    $exec_path/split_by_subset $infile
  fi
done

echo "Done splitting."
cd $cwd
echo $PWD

# 2. Extract: (564) Drifting buoy arriving in WMO BUFR format
for hdir in 00z 06z 12z 18z; do
  cd $data_path_out/$hdir/
  infile="$data_path_out/$hdir/SFCSHP"
  outfile="$data_path_out/$hdir/drifting_buoys_raw.txt"
  echo $infile, $outfile
  if [[ -f "$infile" ]]; then
    echo "Extracting from $infile..."
    yes "" | $exec_path/readbp -d -r $bufr_code "$infile" > "$outfile"
  fi
done
echo "Done extracting: " $bufr_code
cd $cwd
echo $PWD
