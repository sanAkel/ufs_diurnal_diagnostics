#!/usr/bin/env python3

# Load py
# - On Ursa
# -- Not the same as before for plotting locations (which was a custom env).
# -- But a generic one for anyone. 
# module purge

# module load eccodes/2.34.0
# module load python/3.11
# -- (if you want a nice pandas interface, only once.)
# pip install pdbufr
# -- (otherwise no pip install is needed.)
# 

import eccodes
import os
import sys
import argparse

def get_args():
    parser = argparse.ArgumentParser(description="Filter NCEP BUFR using subsetName to isolate 564s.")
    parser.add_argument("--date", required=True, help="Date to process (YYYYMMDD)")
    parser.add_argument("--code", type=int, default=564, help="The NCEP code (used for filename only)")
    parser.add_argument("--base_dir", default="/scratch5/NCEPDEV/rstprod/Santha.Akella/data/no_dbuoy", help="Root directory")
    return parser.parse_args()

def filter_and_append(input_path, target_out, master_out):
    t_sub, m_sub, o_sub = 0, 0, 0
    
    with open(input_path, 'rb') as f_in, \
         open(target_out, 'ab') as f_target, \
         open(master_out, 'ab') as f_master:
        
        while True:
            bid = eccodes.codes_bufr_new_from_file(f_in)
            if bid is None: break
            
            nsub = eccodes.codes_get(bid, "numberOfSubsets")
            o_sub += nsub
            
            try:
                cat = eccodes.codes_get(bid, "dataCategory")
                # subsetName is the NCEP mnemonic (NC001003 = 564)
                sname = eccodes.codes_get(bid, "subsetName")
                
                # NC001003 is the standard NCEP mnemonic for Drifting Buoys (Type 564)
                is_dbuoy = (sname == "NC001003")

                # 1. ALWAYS keep Table Messages (Category 11) in both
                if cat == 11:
                    eccodes.codes_write(bid, f_target)
                    eccodes.codes_write(bid, f_master)
                # 2. Route Drifting Buoys (564) to extracted file
                elif is_dbuoy:
                    eccodes.codes_write(bid, f_target)
                    t_sub += nsub
                # 3. Route everything else to master
                else:
                    eccodes.codes_write(bid, f_master)
                    m_sub += nsub
            except:
                eccodes.codes_write(bid, f_master)
                m_sub += nsub
            finally:
                eccodes.codes_release(bid)
                
    return t_sub, m_sub, o_sub

def main():
    args = get_args()
    cycles = ["00z", "06z", "12z", "18z"]
    categories = ["ADPSFC", "ADPUPA", "AIRCFT", "ASCATW", "RASSDA", "SATWND", "SFCSHP", "SYNDAT", "VADWND"]
    
    date_path = os.path.join(args.base_dir, args.date)
    if not os.path.exists(date_path):
        print(f"ERROR: Path {date_path} not found.")
        sys.exit(1)

    print(f"--- Starting Final Cull | Date: {args.date} | Target: 564 (NC001003) ---")

    for hr in cycles:
        cycle_dir = os.path.join(date_path, hr)
        if not os.path.exists(cycle_dir): continue

        out_ext = os.path.join(cycle_dir, f"extracted_cat_{args.code}_{hr}.bufr")
        out_mst = os.path.join(cycle_dir, f"gdas.t{hr}.prepbufr_no_cat_{args.code}.nr")

        for f in [out_ext, out_mst]:
            if os.path.exists(f): os.remove(f)

        print(f"\n[Cycle {hr}]")
        print(f"{'Category':<10} | {'Original':>10} | {'Kept':>10} | {'Extracted':>10}")
        print("-" * 52)

        for cat in categories:
            f_in = os.path.join(cycle_dir, cat)
            if os.path.exists(f_in):
                t, m, o = filter_and_append(f_in, out_ext, out_mst)
                print(f"{cat:10} | {o:10} | {m:10} | {t:10}")

    print("\nProcessing Complete.")

if __name__ == "__main__":
    main()
