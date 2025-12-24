#!/bin/sh

bufr_code="564"
DATE_DIR="20251222"
data_path="/scratch5/NCEPDEV/rstprod/Santha.Akella/data/no_dbuoy/${DATE_DIR}"

for HR in 00z 06z 12z 18z; do
    INPUT_FILE="${data_path}/${HR}/drifting_buoys_raw.txt"
    OUTPUT_FILE="drifting_buoys_${DATE_DIR}_${HR}.csv"

    if [ -f "$INPUT_FILE" ]; then
        echo "Processing cycle: $HR -> Creating $OUTPUT_FILE ..."

        # Write header to the hourly file
        echo "StationID,Longitude,Latitude,TimeOffset,ReportType" > "$OUTPUT_FILE"

        # Pass the shell variable bufr_code to awk using -v target_code
        awk -v target_code="$bufr_code" '
            BEGIN { 
                sid="N/A"; xob="N/A"; yob="N/A"; dhr="N/A"; t29="N/A" 
            }

            # When we hit SID, process the previous block before resetting
            /SID/ {
                if (t29 == target_code && sid != "MASKSTID" && sid != "N/A") {
                    print sid "," xob "," yob "," dhr "," t29
                }
                
                # Capture new SID and reset others
                sid=$3; xob="N/A"; yob="N/A"; dhr="N/A"; t29="N/A"
            }

            /XOB/ { xob=$3 }
            /YOB/ { yob=$3 }
            /DHR/ { dhr=$3 }
            /T29/ { t29=$3 }

            # Handle the very last block in the file
            END {
                if (t29 == target_code && sid != "MASKSTID" && sid != "N/A") {
                    print sid "," xob "," yob "," dhr "," t29
                }
            }
        ' "$INPUT_FILE" >> "$OUTPUT_FILE"
        
        echo "Done $HR."
    else
        echo "File not found: $INPUT_FILE"
    fi
done
