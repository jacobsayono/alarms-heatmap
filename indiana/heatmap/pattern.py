def generate_cc_lines(start=6, end=75, output_file="pattern.txt"):
    """
    Generates the conveyor-chute pattern from CC[start] up to CC[end],
    appending them to 'pattern.txt' (or whatever filename you prefer).
    """
    
    # Master list of lines in order, using (index, tag) style.
    # We'll prefix each with CC{zone}. except for the "SHOESORTER" lines,
    # and we fill in {zone} for the zone number.
    # 
    # Note: The first and last entries (indices 0, 32) are the "left bin" lines
    # that we skip for odd zones.
    cc_line_map = {
        0:  "Bin_ALeft_Full",
        1:  "Bin_ARight_Full",
        2:  "OutputAJam",
        3:  "Conv1_ChuteJam",
        4:  "Conv1_ChuteFull",
        5:  "SHOESORTER1.PE",   # We'll append zone + "_Jam"
        6:  "SHOESORTER2.PE",
        7:  "Conv2_ChuteFull",
        8:  "Conv2_ChuteJam",
        9:  "Conv12Jam",
        10: "Conv3_ChuteJam",
        11: "Conv3_ChuteFull",
        12: "SHOESORTER3.PE",
        13: "SHOESORTER4.PE",
        14: "Conv4_ChuteFull",
        15: "Conv4_ChuteJam",
        16: "Conv23Jam",
        17: "Conv5_ChuteJam",
        18: "Conv5_ChuteFull",
        19: "SHOESORTER5.PE",
        20: "SHOESORTER6.PE",
        21: "Conv6_ChuteFull",
        22: "Conv6_ChuteJam",
        23: "Conv34Jam",
        24: "Conv7_ChuteJam",
        25: "Conv7_ChuteFull",
        26: "SHOESORTER7.PE",
        27: "SHOESORTER8.PE",
        28: "Conv8_ChuteFull",
        29: "Conv8_ChuteJam",
        30: "OutputBJam",
        31: "Bin_BRight_Full",
        32: "Bin_BLeft_Full"
    }

    with open(output_file, "w") as f:
        for zone in range(start, end + 1):

            # The y-value for CC(n) is n + 36
            y_val = zone + 36

            # Figure out which indices to include:
            # - Even CC => indices 0..32 (33 total)
            # - Odd CC  => indices 1..31 (31 total)
            if zone % 2 == 0:
                indices = range(0, 33)  # includes 0 and 32
            else:
                indices = range(1, 32)  # skip 0 and 32

            for i in indices:
                base_name = cc_line_map[i]
                
                # For the "SHOESORTER" lines, e.g. "SHOESORTER1.PE",
                # we need to append the zone and "_Jam". 
                if base_name.startswith("SHOESORTER"):
                    # e.g. "SHOESORTER1.PE" -> "SHOESORTER1.PE{zone}_Jam"
                    full_name = f"{base_name}{zone}_Jam"
                else:
                    # For everything else, it's "CC{zone}.{base_name}"
                    full_name = f"CC{zone}.{base_name}"

                # However, watch out for indices 0 and 32 for the even zones:
                # those lines already read "CC{zone}.Bin_ALeft_Full" or "CC{zone}.Bin_BLeft_Full"
                # (and that is correct for even zones)
                
                line_text = f"\"{full_name}\":\t({i},{y_val}),"
                f.write(line_text + "\n")  # Write each line as in your snippet.

# ------------------------------------------------------------------------
# USAGE:
# Just call this function. The default start=6, end=75 writes into 'pattern.txt'.
# Uncomment the line below to run directly:

generate_cc_lines()
