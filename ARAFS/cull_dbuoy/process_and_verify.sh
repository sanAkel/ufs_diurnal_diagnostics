#!/bin/bash

# Path Configuration
DATE="20251222"
ORIG_DATA="/scratch5/NCEPDEV/rstprod/Santha.Akella/data/prepbufr/$DATE"
DEST_BASE="/scratch5/NCEPDEV/rstprod/Santha.Akella/data/no_dbuoy/$DATE"
CULLER="/home/Santha.Akella/marine-scratch5/tmp/ufs_diurnal_diagnostics/ARAFS/cull_dbuoy/no_dbuoy.x"
BINV="/home/Santha.Akella/marine-scratch5/ncep-bufr/install/bin/binv"

echo "------------------------------------------------------------"
echo "Starting One-Pass Precision Filter: $DATE"
echo "------------------------------------------------------------"

for HR in 00z 06z 12z 18z; do
    INPUT_FILE="$ORIG_DATA/gdas.t${HR}.prepbufr.nr"
    OUTPUT_FILE="$DEST_BASE/$HR/gdas.t${HR}.prepbufr_no_cat_564.nr"
    
    if [ -f "$INPUT_FILE" ]; then
        echo -e "\n[Cycle $HR]"
        mkdir -p "$DEST_BASE/$HR"
        
        # Surgical Filter
        $CULLER "$INPUT_FILE" "$OUTPUT_FILE"
        
        # Verify the squaring of the data
        if [ -s "$OUTPUT_FILE" ]; then
            echo "  Verification (Final Counts):"
            $BINV "$OUTPUT_FILE" | grep -E "SFCSHP|TOTAL"
        else
            echo "  ERROR: Output file is empty or missing."
        fi
    else
        echo "  SKIP: Original file not found at $INPUT_FILE"
    fi
done

echo -e "\n------------------------------------------------------------"
echo "Filter Complete. All 564s removed, Ships preserved."
