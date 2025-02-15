import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import table
import matplotlib.colors as mcolors
import sys

if len(sys.argv) != 2:
    print("Usage: python3 script.py [filename.xlsx]")
    sys.exit(1)

file_path = sys.argv[1]

df = pd.read_excel(file_path)

df['timestamp'] = pd.to_datetime(df['timestamp'])
df['point_val'] = df['point_val'].fillna(0).astype(int)

df = df.sort_values(by='timestamp')

# init dict for 2 features
total_time_differences = {}
trigger_counts = {}

# iter thru rows of data table
for _, row in df.iterrows():
    alarm_id = row['alarm_id']
    point_val = row['point_val']
    timestamp = row['timestamp']

    # init trigger time if it's the first time seeing this alarm_id
    if alarm_id not in trigger_counts:
        trigger_counts[alarm_id] = 0
        total_time_differences[alarm_id] = pd.Timedelta(0)

    # when a trigger is encountered (point_val = 1)
    if point_val == 1:
        trigger_counts[alarm_id] += 1
        trigger_time = timestamp

    # when a resolution is encountered (point_val = 0)
    elif point_val == 0 and alarm_id in trigger_counts:
        # only process if there was a trigger before this resolution
        if trigger_counts[alarm_id] > 0:
            time_diff = timestamp - trigger_time  # calc time difference
            total_time_differences[alarm_id] += time_diff  # add to total time

# map row/col of our MaRS system
row_col_mapping = {
    # SHOESORTER1
    "SHOESORTER1.ConvA_PE1_Jam": (0,0),
    "SHOESORTER1.ConvB_PE1_Jam": (0,1),

    "SHOESORTER1.PE1_Jam": (0,2),
    "SHOESORTER1.PE2_Jam": (0,3),
    "SHOESORTER1.PE3_Jam": (0,4),
    "SHOESORTER1.PE4_Jam": (0,5),
    "SHOESORTER1.PE5_Jam": (0,6),
    "SHOESORTER1.PE6_Jam": (0,7),
    "SHOESORTER1.PE7_Jam": (0,8),
    "SHOESORTER1.PE8_Jam": (0,9),
    "SHOESORTER1.PE9_Jam": (0,10),
    "SHOESORTER1.PE10_Jam": (0,11),
    "SHOESORTER1.PE11_Jam": (0,12),
    "SHOESORTER1.PE12_Jam": (0,13),
    "SHOESORTER1.PE13_Jam": (0,14),
    "SHOESORTER1.PE14_Jam": (0,15),
    "SHOESORTER1.PE15_Jam": (0,16),
    "SHOESORTER1.PE16_Jam": (0,17),
    "SHOESORTER1.PE17_Jam": (0,18),
    "SHOESORTER1.PE18_Jam": (0,19),
    "SHOESORTER1.PE19_Jam": (0,20),
    "SHOESORTER1.PE20_Jam": (0,21),
    "SHOESORTER1.PE21_Jam": (0,22),
    "SHOESORTER1.PE22_Jam": (0,23),
    "SHOESORTER1.PE23_Jam": (0,24),
    "SHOESORTER1.PE24_Jam": (0,25),
    "SHOESORTER1.PE25_Jam": (0,26),
    "SHOESORTER1.PE26_Jam": (0,27),
    "SHOESORTER1.PE27_Jam": (0,28),
    "SHOESORTER1.PE28_Jam": (0,29),
    "SHOESORTER1.PE29_Jam": (0,30),
    "SHOESORTER1.PE30_Jam": (0,31),
    "SHOESORTER1.PE31_Jam": (0,32),
    "SHOESORTER1.PE32_Jam": (0,33),
    "SHOESORTER1.PE33_Jam": (0,34),
    "SHOESORTER1.PE34_Jam": (0,35),
    "SHOESORTER1.PE35_Jam": (0,36),
    "SHOESORTER1.PE36_Jam": (0,37),
    "SHOESORTER1.PE37_Jam": (0,38),
    "SHOESORTER1.PE38_Jam": (0,39),
    "SHOESORTER1.PE39_Jam": (0,40),
    "SHOESORTER1.PE40_Jam": (0,41),
    "SHOESORTER1.PE41_Jam": (0,42),
    "SHOESORTER1.PE42_Jam": (0,43),
    "SHOESORTER1.PE43_Jam": (0,44),
    "SHOESORTER1.PE44_Jam": (0,45),
    "SHOESORTER1.PE45_Jam": (0,46),
    "SHOESORTER1.PE46_Jam": (0,47),
    "SHOESORTER1.PE47_Jam": (0,48),
    "SHOESORTER1.PE48_Jam": (0,49),
    "SHOESORTER1.PE49_Jam": (0,50),
    "SHOESORTER1.PE50_Jam": (0,51),
    "SHOESORTER1.PE51_Jam": (0,52),
    "SHOESORTER1.PE52_Jam": (0,53),
    "SHOESORTER1.PE53_Jam": (0,54),
    "SHOESORTER1.PE54_Jam": (0,55),
    "SHOESORTER1.PE55_Jam": (0,56),
    "SHOESORTER1.PE56_Jam": (0,57),
    "SHOESORTER1.PE57_Jam": (0,58),
    "SHOESORTER1.PE58_Jam": (0,59),
    "SHOESORTER1.PE59_Jam": (0,60),
    "SHOESORTER1.PE60_Jam": (0,61),
    "SHOESORTER1.PE61_Jam": (0,62),
    "SHOESORTER1.PE62_Jam": (0,63),
    "SHOESORTER1.PE63_Jam": (0,64),
    "SHOESORTER1.PE64_Jam": (0,65),
    "SHOESORTER1.PE65_Jam": (0,66),
    "SHOESORTER1.PE66_Jam": (0,67),
    "SHOESORTER1.PE67_Jam": (0,68),
    "SHOESORTER1.PE68_Jam": (0,69),
    "SHOESORTER1.PE69_Jam": (0,70),
    "SHOESORTER1.PE70_Jam": (0,71),
    "SHOESORTER1.PE71_Jam": (0,72),
    "SHOESORTER1.PE72_Jam": (0,73),
    "SHOESORTER1.PE73_Jam": (0,74),
    "SHOESORTER1.PE74_Jam": (0,75),
    "SHOESORTER1.PE75_Jam": (0,76),
    "SHOESORTER1.PE76_Jam": (0,77),
    "SHOESORTER1.PE77_Jam": (0,78),

    "SHOESORTER1.Sorter_Chain_Stretch": (0,79),
    "SHOESORTER1.Sorter_Shoe_Check": (0,80),
    "SHOESORTER1.ConvB_PE4_Jam": (0,81),

    # SHOESORTER2
    "SHOESORTER2.ConvA_PE1_Jam": (1,0),
    "SHOESORTER2.ConvB_PE1_Jam": (1,1),

    "SHOESORTER2.PE1_Jam": (1,2),
    "SHOESORTER2.PE2_Jam": (1,3),
    "SHOESORTER2.PE3_Jam": (1,4),
    "SHOESORTER2.PE4_Jam": (1,5),
    "SHOESORTER2.PE5_Jam": (1,6),
    "SHOESORTER2.PE6_Jam": (1,7),
    "SHOESORTER2.PE7_Jam": (1,8),
    "SHOESORTER2.PE8_Jam": (1,9),
    "SHOESORTER2.PE9_Jam": (1,10),
    "SHOESORTER2.PE10_Jam": (1,11),
    "SHOESORTER2.PE11_Jam": (1,12),
    "SHOESORTER2.PE12_Jam": (1,13),
    "SHOESORTER2.PE13_Jam": (1,14),
    "SHOESORTER2.PE14_Jam": (1,15),
    "SHOESORTER2.PE15_Jam": (1,16),
    "SHOESORTER2.PE16_Jam": (1,17),
    "SHOESORTER2.PE17_Jam": (1,18),
    "SHOESORTER2.PE18_Jam": (1,19),
    "SHOESORTER2.PE19_Jam": (1,20),
    "SHOESORTER2.PE20_Jam": (1,21),
    "SHOESORTER2.PE21_Jam": (1,22),
    "SHOESORTER2.PE22_Jam": (1,23),
    "SHOESORTER2.PE23_Jam": (1,24),
    "SHOESORTER2.PE24_Jam": (1,25),
    "SHOESORTER2.PE25_Jam": (1,26),
    "SHOESORTER2.PE26_Jam": (1,27),
    "SHOESORTER2.PE27_Jam": (1,28),
    "SHOESORTER2.PE28_Jam": (1,29),
    "SHOESORTER2.PE29_Jam": (1,30),
    "SHOESORTER2.PE30_Jam": (1,31),
    "SHOESORTER2.PE31_Jam": (1,32),
    "SHOESORTER2.PE32_Jam": (1,33),
    "SHOESORTER2.PE33_Jam": (1,34),
    "SHOESORTER2.PE34_Jam": (1,35),
    "SHOESORTER2.PE35_Jam": (1,36),
    "SHOESORTER2.PE36_Jam": (1,37),
    "SHOESORTER2.PE37_Jam": (1,38),
    "SHOESORTER2.PE38_Jam": (1,39),
    "SHOESORTER2.PE39_Jam": (1,40),
    "SHOESORTER2.PE40_Jam": (1,41),
    "SHOESORTER2.PE41_Jam": (1,42),
    "SHOESORTER2.PE42_Jam": (1,43),
    "SHOESORTER2.PE43_Jam": (1,44),
    "SHOESORTER2.PE44_Jam": (1,45),
    "SHOESORTER2.PE45_Jam": (1,46),
    "SHOESORTER2.PE46_Jam": (1,47),
    "SHOESORTER2.PE47_Jam": (1,48),
    "SHOESORTER2.PE48_Jam": (1,49),
    "SHOESORTER2.PE49_Jam": (1,50),
    "SHOESORTER2.PE50_Jam": (1,51),
    "SHOESORTER2.PE51_Jam": (1,52),
    "SHOESORTER2.PE52_Jam": (1,53),
    "SHOESORTER2.PE53_Jam": (1,54),
    "SHOESORTER2.PE54_Jam": (1,55),
    "SHOESORTER2.PE55_Jam": (1,56),
    "SHOESORTER2.PE56_Jam": (1,57),
    "SHOESORTER2.PE57_Jam": (1,58),
    "SHOESORTER2.PE58_Jam": (1,59),
    "SHOESORTER2.PE59_Jam": (1,60),
    "SHOESORTER2.PE60_Jam": (1,61),
    "SHOESORTER2.PE61_Jam": (1,62),
    "SHOESORTER2.PE62_Jam": (1,63),
    "SHOESORTER2.PE63_Jam": (1,64),
    "SHOESORTER2.PE64_Jam": (1,65),
    "SHOESORTER2.PE65_Jam": (1,66),
    "SHOESORTER2.PE66_Jam": (1,67),
    "SHOESORTER2.PE67_Jam": (1,68),
    "SHOESORTER2.PE68_Jam": (1,69),
    "SHOESORTER2.PE69_Jam": (1,70),
    "SHOESORTER2.PE70_Jam": (1,71),
    "SHOESORTER2.PE71_Jam": (1,72),
    "SHOESORTER2.PE72_Jam": (1,73),
    "SHOESORTER2.PE73_Jam": (1,74),
    "SHOESORTER2.PE74_Jam": (1,75),
    "SHOESORTER2.PE75_Jam": (1,76),
    "SHOESORTER2.PE76_Jam": (1,77),
    "SHOESORTER2.PE77_Jam": (1,78),

    "SHOESORTER2.Sorter_Chain_Stretch": (1,79),
    "SHOESORTER2.Sorter_Shoe_Check": (1,80),
    "SHOESORTER2.ConvB_PE4_Jam": (1,81),

    # SHOESORTER3
    "SHOESORTER3.ConvA_PE1_Jam": (2,0),
    "SHOESORTER3.ConvB_PE1_Jam": (2,1),

    "SHOESORTER3.PE1_Jam": (2,2),
    "SHOESORTER3.PE2_Jam": (2,3),
    "SHOESORTER3.PE3_Jam": (2,4),
    "SHOESORTER3.PE4_Jam": (2,5),
    "SHOESORTER3.PE5_Jam": (2,6),
    "SHOESORTER3.PE6_Jam": (2,7),
    "SHOESORTER3.PE7_Jam": (2,8),
    "SHOESORTER3.PE8_Jam": (2,9),
    "SHOESORTER3.PE9_Jam": (2,10),
    "SHOESORTER3.PE10_Jam": (2,11),
    "SHOESORTER3.PE11_Jam": (2,12),
    "SHOESORTER3.PE12_Jam": (2,13),
    "SHOESORTER3.PE13_Jam": (2,14),
    "SHOESORTER3.PE14_Jam": (2,15),
    "SHOESORTER3.PE15_Jam": (2,16),
    "SHOESORTER3.PE16_Jam": (2,17),
    "SHOESORTER3.PE17_Jam": (2,18),
    "SHOESORTER3.PE18_Jam": (2,19),
    "SHOESORTER3.PE19_Jam": (2,20),
    "SHOESORTER3.PE20_Jam": (2,21),
    "SHOESORTER3.PE21_Jam": (2,22),
    "SHOESORTER3.PE22_Jam": (2,23),
    "SHOESORTER3.PE23_Jam": (2,24),
    "SHOESORTER3.PE24_Jam": (2,25),
    "SHOESORTER3.PE25_Jam": (2,26),
    "SHOESORTER3.PE26_Jam": (2,27),
    "SHOESORTER3.PE27_Jam": (2,28),
    "SHOESORTER3.PE28_Jam": (2,29),
    "SHOESORTER3.PE29_Jam": (2,30),
    "SHOESORTER3.PE30_Jam": (2,31),
    "SHOESORTER3.PE31_Jam": (2,32),
    "SHOESORTER3.PE32_Jam": (2,33),
    "SHOESORTER3.PE33_Jam": (2,34),
    "SHOESORTER3.PE34_Jam": (2,35),
    "SHOESORTER3.PE35_Jam": (2,36),
    "SHOESORTER3.PE36_Jam": (2,37),
    "SHOESORTER3.PE37_Jam": (2,38),
    "SHOESORTER3.PE38_Jam": (2,39),
    "SHOESORTER3.PE39_Jam": (2,40),
    "SHOESORTER3.PE40_Jam": (2,41),
    "SHOESORTER3.PE41_Jam": (2,42),
    "SHOESORTER3.PE42_Jam": (2,43),
    "SHOESORTER3.PE43_Jam": (2,44),
    "SHOESORTER3.PE44_Jam": (2,45),
    "SHOESORTER3.PE45_Jam": (2,46),
    "SHOESORTER3.PE46_Jam": (2,47),
    "SHOESORTER3.PE47_Jam": (2,48),
    "SHOESORTER3.PE48_Jam": (2,49),
    "SHOESORTER3.PE49_Jam": (2,50),
    "SHOESORTER3.PE50_Jam": (2,51),
    "SHOESORTER3.PE51_Jam": (2,52),
    "SHOESORTER3.PE52_Jam": (2,53),
    "SHOESORTER3.PE53_Jam": (2,54),
    "SHOESORTER3.PE54_Jam": (2,55),
    "SHOESORTER3.PE55_Jam": (2,56),
    "SHOESORTER3.PE56_Jam": (2,57),
    "SHOESORTER3.PE57_Jam": (2,58),
    "SHOESORTER3.PE58_Jam": (2,59),
    "SHOESORTER3.PE59_Jam": (2,60),
    "SHOESORTER3.PE60_Jam": (2,61),
    "SHOESORTER3.PE61_Jam": (2,62),
    "SHOESORTER3.PE62_Jam": (2,63),
    "SHOESORTER3.PE63_Jam": (2,64),
    "SHOESORTER3.PE64_Jam": (2,65),
    "SHOESORTER3.PE65_Jam": (2,66),
    "SHOESORTER3.PE66_Jam": (2,67),
    "SHOESORTER3.PE67_Jam": (2,68),
    "SHOESORTER3.PE68_Jam": (2,69),
    "SHOESORTER3.PE69_Jam": (2,70),
    "SHOESORTER3.PE70_Jam": (2,71),
    "SHOESORTER3.PE71_Jam": (2,72),
    "SHOESORTER3.PE72_Jam": (2,73),
    "SHOESORTER3.PE73_Jam": (2,74),
    "SHOESORTER3.PE74_Jam": (2,75),
    "SHOESORTER3.PE75_Jam": (2,76),
    "SHOESORTER3.PE76_Jam": (2,77),
    "SHOESORTER3.PE77_Jam": (2,78),

    "SHOESORTER3.Sorter_Chain_Stretch": (2,79),
    "SHOESORTER3.Sorter_Shoe_Check": (2,80),
    "SHOESORTER3.ConvB_PE4_Jam": (2,81),

    # SHOESORTER4
    "SHOESORTER4.ConvA_PE1_Jam": (3,0),
    "SHOESORTER4.ConvB_PE1_Jam": (3,1),

    "SHOESORTER4.PE1_Jam": (3,2),
    "SHOESORTER4.PE2_Jam": (3,3),
    "SHOESORTER4.PE3_Jam": (3,4),
    "SHOESORTER4.PE4_Jam": (3,5),
    "SHOESORTER4.PE5_Jam": (3,6),
    "SHOESORTER4.PE6_Jam": (3,7),
    "SHOESORTER4.PE7_Jam": (3,8),
    "SHOESORTER4.PE8_Jam": (3,9),
    "SHOESORTER4.PE9_Jam": (3,10),
    "SHOESORTER4.PE10_Jam": (3,11),
    "SHOESORTER4.PE11_Jam": (3,12),
    "SHOESORTER4.PE12_Jam": (3,13),
    "SHOESORTER4.PE13_Jam": (3,14),
    "SHOESORTER4.PE14_Jam": (3,15),
    "SHOESORTER4.PE15_Jam": (3,16),
    "SHOESORTER4.PE16_Jam": (3,17),
    "SHOESORTER4.PE17_Jam": (3,18),
    "SHOESORTER4.PE18_Jam": (3,19),
    "SHOESORTER4.PE19_Jam": (3,20),
    "SHOESORTER4.PE20_Jam": (3,21),
    "SHOESORTER4.PE21_Jam": (3,22),
    "SHOESORTER4.PE22_Jam": (3,23),
    "SHOESORTER4.PE23_Jam": (3,24),
    "SHOESORTER4.PE24_Jam": (3,25),
    "SHOESORTER4.PE25_Jam": (3,26),
    "SHOESORTER4.PE26_Jam": (3,27),
    "SHOESORTER4.PE27_Jam": (3,28),
    "SHOESORTER4.PE28_Jam": (3,29),
    "SHOESORTER4.PE29_Jam": (3,30),
    "SHOESORTER4.PE30_Jam": (3,31),
    "SHOESORTER4.PE31_Jam": (3,32),
    "SHOESORTER4.PE32_Jam": (3,33),
    "SHOESORTER4.PE33_Jam": (3,34),
    "SHOESORTER4.PE34_Jam": (3,35),
    "SHOESORTER4.PE35_Jam": (3,36),
    "SHOESORTER4.PE36_Jam": (3,37),
    "SHOESORTER4.PE37_Jam": (3,38),
    "SHOESORTER4.PE38_Jam": (3,39),
    "SHOESORTER4.PE39_Jam": (3,40),
    "SHOESORTER4.PE40_Jam": (3,41),
    "SHOESORTER4.PE41_Jam": (3,42),
    "SHOESORTER4.PE42_Jam": (3,43),
    "SHOESORTER4.PE43_Jam": (3,44),
    "SHOESORTER4.PE44_Jam": (3,45),
    "SHOESORTER4.PE45_Jam": (3,46),
    "SHOESORTER4.PE46_Jam": (3,47),
    "SHOESORTER4.PE47_Jam": (3,48),
    "SHOESORTER4.PE48_Jam": (3,49),
    "SHOESORTER4.PE49_Jam": (3,50),
    "SHOESORTER4.PE50_Jam": (3,51),
    "SHOESORTER4.PE51_Jam": (3,52),
    "SHOESORTER4.PE52_Jam": (3,53),
    "SHOESORTER4.PE53_Jam": (3,54),
    "SHOESORTER4.PE54_Jam": (3,55),
    "SHOESORTER4.PE55_Jam": (3,56),
    "SHOESORTER4.PE56_Jam": (3,57),
    "SHOESORTER4.PE57_Jam": (3,58),
    "SHOESORTER4.PE58_Jam": (3,59),
    "SHOESORTER4.PE59_Jam": (3,60),
    "SHOESORTER4.PE60_Jam": (3,61),
    "SHOESORTER4.PE61_Jam": (3,62),
    "SHOESORTER4.PE62_Jam": (3,63),
    "SHOESORTER4.PE63_Jam": (3,64),
    "SHOESORTER4.PE64_Jam": (3,65),
    "SHOESORTER4.PE65_Jam": (3,66),
    "SHOESORTER4.PE66_Jam": (3,67),
    "SHOESORTER4.PE67_Jam": (3,68),
    "SHOESORTER4.PE68_Jam": (3,69),
    "SHOESORTER4.PE69_Jam": (3,70),
    "SHOESORTER4.PE70_Jam": (3,71),
    "SHOESORTER4.PE71_Jam": (3,72),
    "SHOESORTER4.PE72_Jam": (3,73),
    "SHOESORTER4.PE73_Jam": (3,74),
    "SHOESORTER4.PE74_Jam": (3,75),
    "SHOESORTER4.PE75_Jam": (3,76),
    "SHOESORTER4.PE76_Jam": (3,77),
    "SHOESORTER4.PE77_Jam": (3,78),

    "SHOESORTER4.Sorter_Chain_Stretch": (3,79),
    "SHOESORTER4.Sorter_Shoe_Check": (3,80),
    "SHOESORTER4.ConvB_PE4_Jam": (3,81),

    # SHOESORTER5
    "SHOESORTER5.ConvA_PE1_Jam": (4,0),
    "SHOESORTER5.ConvB_PE1_Jam": (4,1),

    "SHOESORTER5.PE1_Jam": (4,2),
    "SHOESORTER5.PE2_Jam": (4,3),
    "SHOESORTER5.PE3_Jam": (4,4),
    "SHOESORTER5.PE4_Jam": (4,5),
    "SHOESORTER5.PE5_Jam": (4,6),
    "SHOESORTER5.PE6_Jam": (4,7),
    "SHOESORTER5.PE7_Jam": (4,8),
    "SHOESORTER5.PE8_Jam": (4,9),
    "SHOESORTER5.PE9_Jam": (4,10),
    "SHOESORTER5.PE10_Jam": (4,11),
    "SHOESORTER5.PE11_Jam": (4,12),
    "SHOESORTER5.PE12_Jam": (4,13),
    "SHOESORTER5.PE13_Jam": (4,14),
    "SHOESORTER5.PE14_Jam": (4,15),
    "SHOESORTER5.PE15_Jam": (4,16),
    "SHOESORTER5.PE16_Jam": (4,17),
    "SHOESORTER5.PE17_Jam": (4,18),
    "SHOESORTER5.PE18_Jam": (4,19),
    "SHOESORTER5.PE19_Jam": (4,20),
    "SHOESORTER5.PE20_Jam": (4,21),
    "SHOESORTER5.PE21_Jam": (4,22),
    "SHOESORTER5.PE22_Jam": (4,23),
    "SHOESORTER5.PE23_Jam": (4,24),
    "SHOESORTER5.PE24_Jam": (4,25),
    "SHOESORTER5.PE25_Jam": (4,26),
    "SHOESORTER5.PE26_Jam": (4,27),
    "SHOESORTER5.PE27_Jam": (4,28),
    "SHOESORTER5.PE28_Jam": (4,29),
    "SHOESORTER5.PE29_Jam": (4,30),
    "SHOESORTER5.PE30_Jam": (4,31),
    "SHOESORTER5.PE31_Jam": (4,32),
    "SHOESORTER5.PE32_Jam": (4,33),
    "SHOESORTER5.PE33_Jam": (4,34),
    "SHOESORTER5.PE34_Jam": (4,35),
    "SHOESORTER5.PE35_Jam": (4,36),
    "SHOESORTER5.PE36_Jam": (4,37),
    "SHOESORTER5.PE37_Jam": (4,38),
    "SHOESORTER5.PE38_Jam": (4,39),
    "SHOESORTER5.PE39_Jam": (4,40),
    "SHOESORTER5.PE40_Jam": (4,41),
    "SHOESORTER5.PE41_Jam": (4,42),
    "SHOESORTER5.PE42_Jam": (4,43),
    "SHOESORTER5.PE43_Jam": (4,44),
    "SHOESORTER5.PE44_Jam": (4,45),
    "SHOESORTER5.PE45_Jam": (4,46),
    "SHOESORTER5.PE46_Jam": (4,47),
    "SHOESORTER5.PE47_Jam": (4,48),
    "SHOESORTER5.PE48_Jam": (4,49),
    "SHOESORTER5.PE49_Jam": (4,50),
    "SHOESORTER5.PE50_Jam": (4,51),
    "SHOESORTER5.PE51_Jam": (4,52),
    "SHOESORTER5.PE52_Jam": (4,53),
    "SHOESORTER5.PE53_Jam": (4,54),
    "SHOESORTER5.PE54_Jam": (4,55),
    "SHOESORTER5.PE55_Jam": (4,56),
    "SHOESORTER5.PE56_Jam": (4,57),
    "SHOESORTER5.PE57_Jam": (4,58),
    "SHOESORTER5.PE58_Jam": (4,59),
    "SHOESORTER5.PE59_Jam": (4,60),
    "SHOESORTER5.PE60_Jam": (4,61),
    "SHOESORTER5.PE61_Jam": (4,62),
    "SHOESORTER5.PE62_Jam": (4,63),
    "SHOESORTER5.PE63_Jam": (4,64),
    "SHOESORTER5.PE64_Jam": (4,65),
    "SHOESORTER5.PE65_Jam": (4,66),
    "SHOESORTER5.PE66_Jam": (4,67),
    "SHOESORTER5.PE67_Jam": (4,68),
    "SHOESORTER5.PE68_Jam": (4,69),
    "SHOESORTER5.PE69_Jam": (4,70),
    "SHOESORTER5.PE70_Jam": (4,71),
    "SHOESORTER5.PE71_Jam": (4,72),
    "SHOESORTER5.PE72_Jam": (4,73),
    "SHOESORTER5.PE73_Jam": (4,74),
    "SHOESORTER5.PE74_Jam": (4,75),
    "SHOESORTER5.PE75_Jam": (4,76),
    "SHOESORTER5.PE76_Jam": (4,77),
    "SHOESORTER5.PE77_Jam": (4,78),

    "SHOESORTER5.Sorter_Chain_Stretch": (4,79),
    "SHOESORTER5.Sorter_Shoe_Check": (4,80),
    "SHOESORTER5.ConvB_PE4_Jam": (4,81),

    # SHOESORTER6
    "SHOESORTER6.ConvA_PE1_Jam": (5,0),
    "SHOESORTER6.ConvB_PE1_Jam": (5,1),

    "SHOESORTER6.PE1_Jam": (5,2),
    "SHOESORTER6.PE2_Jam": (5,3),
    "SHOESORTER6.PE3_Jam": (5,4),
    "SHOESORTER6.PE4_Jam": (5,5),
    "SHOESORTER6.PE5_Jam": (5,6),
    "SHOESORTER6.PE6_Jam": (5,7),
    "SHOESORTER6.PE7_Jam": (5,8),
    "SHOESORTER6.PE8_Jam": (5,9),
    "SHOESORTER6.PE9_Jam": (5,10),
    "SHOESORTER6.PE10_Jam": (5,11),
    "SHOESORTER6.PE11_Jam": (5,12),
    "SHOESORTER6.PE12_Jam": (5,13),
    "SHOESORTER6.PE13_Jam": (5,14),
    "SHOESORTER6.PE14_Jam": (5,15),
    "SHOESORTER6.PE15_Jam": (5,16),
    "SHOESORTER6.PE16_Jam": (5,17),
    "SHOESORTER6.PE17_Jam": (5,18),
    "SHOESORTER6.PE18_Jam": (5,19),
    "SHOESORTER6.PE19_Jam": (5,20),
    "SHOESORTER6.PE20_Jam": (5,21),
    "SHOESORTER6.PE21_Jam": (5,22),
    "SHOESORTER6.PE22_Jam": (5,23),
    "SHOESORTER6.PE23_Jam": (5,24),
    "SHOESORTER6.PE24_Jam": (5,25),
    "SHOESORTER6.PE25_Jam": (5,26),
    "SHOESORTER6.PE26_Jam": (5,27),
    "SHOESORTER6.PE27_Jam": (5,28),
    "SHOESORTER6.PE28_Jam": (5,29),
    "SHOESORTER6.PE29_Jam": (5,30),
    "SHOESORTER6.PE30_Jam": (5,31),
    "SHOESORTER6.PE31_Jam": (5,32),
    "SHOESORTER6.PE32_Jam": (5,33),
    "SHOESORTER6.PE33_Jam": (5,34),
    "SHOESORTER6.PE34_Jam": (5,35),
    "SHOESORTER6.PE35_Jam": (5,36),
    "SHOESORTER6.PE36_Jam": (5,37),
    "SHOESORTER6.PE37_Jam": (5,38),
    "SHOESORTER6.PE38_Jam": (5,39),
    "SHOESORTER6.PE39_Jam": (5,40),
    "SHOESORTER6.PE40_Jam": (5,41),
    "SHOESORTER6.PE41_Jam": (5,42),
    "SHOESORTER6.PE42_Jam": (5,43),
    "SHOESORTER6.PE43_Jam": (5,44),
    "SHOESORTER6.PE44_Jam": (5,45),
    "SHOESORTER6.PE45_Jam": (5,46),
    "SHOESORTER6.PE46_Jam": (5,47),
    "SHOESORTER6.PE47_Jam": (5,48),
    "SHOESORTER6.PE48_Jam": (5,49),
    "SHOESORTER6.PE49_Jam": (5,50),
    "SHOESORTER6.PE50_Jam": (5,51),
    "SHOESORTER6.PE51_Jam": (5,52),
    "SHOESORTER6.PE52_Jam": (5,53),
    "SHOESORTER6.PE53_Jam": (5,54),
    "SHOESORTER6.PE54_Jam": (5,55),
    "SHOESORTER6.PE55_Jam": (5,56),
    "SHOESORTER6.PE56_Jam": (5,57),
    "SHOESORTER6.PE57_Jam": (5,58),
    "SHOESORTER6.PE58_Jam": (5,59),
    "SHOESORTER6.PE59_Jam": (5,60),
    "SHOESORTER6.PE60_Jam": (5,61),
    "SHOESORTER6.PE61_Jam": (5,62),
    "SHOESORTER6.PE62_Jam": (5,63),
    "SHOESORTER6.PE63_Jam": (5,64),
    "SHOESORTER6.PE64_Jam": (5,65),
    "SHOESORTER6.PE65_Jam": (5,66),
    "SHOESORTER6.PE66_Jam": (5,67),
    "SHOESORTER6.PE67_Jam": (5,68),
    "SHOESORTER6.PE68_Jam": (5,69),
    "SHOESORTER6.PE69_Jam": (5,70),
    "SHOESORTER6.PE70_Jam": (5,71),
    "SHOESORTER6.PE71_Jam": (5,72),
    "SHOESORTER6.PE72_Jam": (5,73),
    "SHOESORTER6.PE73_Jam": (5,74),
    "SHOESORTER6.PE74_Jam": (5,75),
    "SHOESORTER6.PE75_Jam": (5,76),
    "SHOESORTER6.PE76_Jam": (5,77),
    "SHOESORTER6.PE77_Jam": (5,78),

    "SHOESORTER6.Sorter_Chain_Stretch": (5,79),
    "SHOESORTER6.Sorter_Shoe_Check": (5,80),
    "SHOESORTER6.ConvB_PE4_Jam": (5,81),

    # SHOESORTER7
    "SHOESORTER7.ConvA_PE1_Jam": (6,0),
    "SHOESORTER7.ConvB_PE1_Jam": (6,1),

    "SHOESORTER7.PE1_Jam": (6,2),
    "SHOESORTER7.PE2_Jam": (6,3),
    "SHOESORTER7.PE3_Jam": (6,4),
    "SHOESORTER7.PE4_Jam": (6,5),
    "SHOESORTER7.PE5_Jam": (6,6),
    "SHOESORTER7.PE6_Jam": (6,7),
    "SHOESORTER7.PE7_Jam": (6,8),
    "SHOESORTER7.PE8_Jam": (6,9),
    "SHOESORTER7.PE9_Jam": (6,10),
    "SHOESORTER7.PE10_Jam": (6,11),
    "SHOESORTER7.PE11_Jam": (6,12),
    "SHOESORTER7.PE12_Jam": (6,13),
    "SHOESORTER7.PE13_Jam": (6,14),
    "SHOESORTER7.PE14_Jam": (6,15),
    "SHOESORTER7.PE15_Jam": (6,16),
    "SHOESORTER7.PE16_Jam": (6,17),
    "SHOESORTER7.PE17_Jam": (6,18),
    "SHOESORTER7.PE18_Jam": (6,19),
    "SHOESORTER7.PE19_Jam": (6,20),
    "SHOESORTER7.PE20_Jam": (6,21),
    "SHOESORTER7.PE21_Jam": (6,22),
    "SHOESORTER7.PE22_Jam": (6,23),
    "SHOESORTER7.PE23_Jam": (6,24),
    "SHOESORTER7.PE24_Jam": (6,25),
    "SHOESORTER7.PE25_Jam": (6,26),
    "SHOESORTER7.PE26_Jam": (6,27),
    "SHOESORTER7.PE27_Jam": (6,28),
    "SHOESORTER7.PE28_Jam": (6,29),
    "SHOESORTER7.PE29_Jam": (6,30),
    "SHOESORTER7.PE30_Jam": (6,31),
    "SHOESORTER7.PE31_Jam": (6,32),
    "SHOESORTER7.PE32_Jam": (6,33),
    "SHOESORTER7.PE33_Jam": (6,34),
    "SHOESORTER7.PE34_Jam": (6,35),
    "SHOESORTER7.PE35_Jam": (6,36),
    "SHOESORTER7.PE36_Jam": (6,37),
    "SHOESORTER7.PE37_Jam": (6,38),
    "SHOESORTER7.PE38_Jam": (6,39),
    "SHOESORTER7.PE39_Jam": (6,40),
    "SHOESORTER7.PE40_Jam": (6,41),
    "SHOESORTER7.PE41_Jam": (6,42),
    "SHOESORTER7.PE42_Jam": (6,43),
    "SHOESORTER7.PE43_Jam": (6,44),
    "SHOESORTER7.PE44_Jam": (6,45),
    "SHOESORTER7.PE45_Jam": (6,46),
    "SHOESORTER7.PE46_Jam": (6,47),
    "SHOESORTER7.PE47_Jam": (6,48),
    "SHOESORTER7.PE48_Jam": (6,49),
    "SHOESORTER7.PE49_Jam": (6,50),
    "SHOESORTER7.PE50_Jam": (6,51),
    "SHOESORTER7.PE51_Jam": (6,52),
    "SHOESORTER7.PE52_Jam": (6,53),
    "SHOESORTER7.PE53_Jam": (6,54),
    "SHOESORTER7.PE54_Jam": (6,55),
    "SHOESORTER7.PE55_Jam": (6,56),
    "SHOESORTER7.PE56_Jam": (6,57),
    "SHOESORTER7.PE57_Jam": (6,58),
    "SHOESORTER7.PE58_Jam": (6,59),
    "SHOESORTER7.PE59_Jam": (6,60),
    "SHOESORTER7.PE60_Jam": (6,61),
    "SHOESORTER7.PE61_Jam": (6,62),
    "SHOESORTER7.PE62_Jam": (6,63),
    "SHOESORTER7.PE63_Jam": (6,64),
    "SHOESORTER7.PE64_Jam": (6,65),
    "SHOESORTER7.PE65_Jam": (6,66),
    "SHOESORTER7.PE66_Jam": (6,67),
    "SHOESORTER7.PE67_Jam": (6,68),
    "SHOESORTER7.PE68_Jam": (6,69),
    "SHOESORTER7.PE69_Jam": (6,70),
    "SHOESORTER7.PE70_Jam": (6,71),
    "SHOESORTER7.PE71_Jam": (6,72),
    "SHOESORTER7.PE72_Jam": (6,73),
    "SHOESORTER7.PE73_Jam": (6,74),
    "SHOESORTER7.PE74_Jam": (6,75),
    "SHOESORTER7.PE75_Jam": (6,76),
    "SHOESORTER7.PE76_Jam": (6,77),
    "SHOESORTER7.PE77_Jam": (6,78),

    "SHOESORTER7.Sorter_Chain_Stretch": (6,79),
    "SHOESORTER7.Sorter_Shoe_Check": (6,80),
    "SHOESORTER7.ConvB_PE4_Jam": (6,81),

    # SHOESORTER8
    "SHOESORTER8.ConvA_PE1_Jam": (7,0),
    "SHOESORTER8.ConvB_PE1_Jam": (7,1),

    "SHOESORTER8.PE1_Jam": (7,2),
    "SHOESORTER8.PE2_Jam": (7,3),
    "SHOESORTER8.PE3_Jam": (7,4),
    "SHOESORTER8.PE4_Jam": (7,5),
    "SHOESORTER8.PE5_Jam": (7,6),
    "SHOESORTER8.PE6_Jam": (7,7),
    "SHOESORTER8.PE7_Jam": (7,8),
    "SHOESORTER8.PE8_Jam": (7,9),
    "SHOESORTER8.PE9_Jam": (7,10),
    "SHOESORTER8.PE10_Jam": (7,11),
    "SHOESORTER8.PE11_Jam": (7,12),
    "SHOESORTER8.PE12_Jam": (7,13),
    "SHOESORTER8.PE13_Jam": (7,14),
    "SHOESORTER8.PE14_Jam": (7,15),
    "SHOESORTER8.PE15_Jam": (7,16),
    "SHOESORTER8.PE16_Jam": (7,17),
    "SHOESORTER8.PE17_Jam": (7,18),
    "SHOESORTER8.PE18_Jam": (7,19),
    "SHOESORTER8.PE19_Jam": (7,20),
    "SHOESORTER8.PE20_Jam": (7,21),
    "SHOESORTER8.PE21_Jam": (7,22),
    "SHOESORTER8.PE22_Jam": (7,23),
    "SHOESORTER8.PE23_Jam": (7,24),
    "SHOESORTER8.PE24_Jam": (7,25),
    "SHOESORTER8.PE25_Jam": (7,26),
    "SHOESORTER8.PE26_Jam": (7,27),
    "SHOESORTER8.PE27_Jam": (7,28),
    "SHOESORTER8.PE28_Jam": (7,29),
    "SHOESORTER8.PE29_Jam": (7,30),
    "SHOESORTER8.PE30_Jam": (7,31),
    "SHOESORTER8.PE31_Jam": (7,32),
    "SHOESORTER8.PE32_Jam": (7,33),
    "SHOESORTER8.PE33_Jam": (7,34),
    "SHOESORTER8.PE34_Jam": (7,35),
    "SHOESORTER8.PE35_Jam": (7,36),
    "SHOESORTER8.PE36_Jam": (7,37),
    "SHOESORTER8.PE37_Jam": (7,38),
    "SHOESORTER8.PE38_Jam": (7,39),
    "SHOESORTER8.PE39_Jam": (7,40),
    "SHOESORTER8.PE40_Jam": (7,41),
    "SHOESORTER8.PE41_Jam": (7,42),
    "SHOESORTER8.PE42_Jam": (7,43),
    "SHOESORTER8.PE43_Jam": (7,44),
    "SHOESORTER8.PE44_Jam": (7,45),
    "SHOESORTER8.PE45_Jam": (7,46),
    "SHOESORTER8.PE46_Jam": (7,47),
    "SHOESORTER8.PE47_Jam": (7,48),
    "SHOESORTER8.PE48_Jam": (7,49),
    "SHOESORTER8.PE49_Jam": (7,50),
    "SHOESORTER8.PE50_Jam": (7,51),
    "SHOESORTER8.PE51_Jam": (7,52),
    "SHOESORTER8.PE52_Jam": (7,53),
    "SHOESORTER8.PE53_Jam": (7,54),
    "SHOESORTER8.PE54_Jam": (7,55),
    "SHOESORTER8.PE55_Jam": (7,56),
    "SHOESORTER8.PE56_Jam": (7,57),
    "SHOESORTER8.PE57_Jam": (7,58),
    "SHOESORTER8.PE58_Jam": (7,59),
    "SHOESORTER8.PE59_Jam": (7,60),
    "SHOESORTER8.PE60_Jam": (7,61),
    "SHOESORTER8.PE61_Jam": (7,62),
    "SHOESORTER8.PE62_Jam": (7,63),
    "SHOESORTER8.PE63_Jam": (7,64),
    "SHOESORTER8.PE64_Jam": (7,65),
    "SHOESORTER8.PE65_Jam": (7,66),
    "SHOESORTER8.PE66_Jam": (7,67),
    "SHOESORTER8.PE67_Jam": (7,68),
    "SHOESORTER8.PE68_Jam": (7,69),
    "SHOESORTER8.PE69_Jam": (7,70),
    "SHOESORTER8.PE70_Jam": (7,71),
    "SHOESORTER8.PE71_Jam": (7,72),
    "SHOESORTER8.PE72_Jam": (7,73),
    "SHOESORTER8.PE73_Jam": (7,74),
    "SHOESORTER8.PE74_Jam": (7,75),
    "SHOESORTER8.PE75_Jam": (7,76),
    "SHOESORTER8.PE76_Jam": (7,77),
    "SHOESORTER8.PE77_Jam": (7,78),

    "SHOESORTER8.Sorter_Chain_Stretch": (7,79),
    "SHOESORTER8.Sorter_Shoe_Check": (7,80),
    "SHOESORTER8.ConvB_PE4_Jam": (7,81),
}

# create dataframe with appropriate size (chicago 8 strands, 80 sorter columns) for heatmap generation
rows = 8
cols = 82
table_df = pd.DataFrame("", index=range(rows), columns=range(cols), dtype=object)

trigger_values = {}
for alarm_id, trigger in trigger_counts.items():
    if alarm_id in row_col_mapping:
        row, col = row_col_mapping[alarm_id]
        # table_df.loc[row, col] = trigger
        # table_df.loc[row, col] = ""
        trigger_values[(row, col)] = trigger

# row and col titles
table_df.index = ['Strand 1', 'Strand 2', 'Strand 3', 'Strand 4', 'Strand 5', 'Strand 6', 'Strand 7', 'Strand 8']
table_df.columns = ['A_PE1', 'B_PE1', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', 'Chain', 'Shoe', 'B_PE4']

# absolute count range for color mapping (in seconds)
min_count = 0  # min trigger count
max_count = max(trigger_values.values())  # max trigger count
# max_count = 20  # or custom max val
norm = mcolors.Normalize(vmin=min_count, vmax=max_count)
cmap = plt.colormaps.get_cmap("gnuplot2_r")  # different coloring on cmap() documentation

# # create cell colours based on trigger counts
# cell_colours = np.full((rows, cols), '#FFFFFF')  # init color grid
# for alarm_id, trigger in trigger_counts.items():
#     if alarm_id in row_col_mapping:
#         row, col = row_col_mapping[alarm_id]
#         color = cmap(norm(trigger))  # get color for the current trigger count
#         cell_colours[row, col] = mcolors.to_hex(color)  # convert to hex

# for alarm_id, (row, col) in row_col_mapping.items():
#     if alarm_id in trigger_counts:
#         count = trigger_counts[alarm_id]
#         color = cmap(norm(count))
#         cell_colours[row, col] = mcolors.to_hex(color)

cell_colours = np.full((rows, cols), '#FFFFFF')  # init color grid
for (row, col), count in trigger_values.items():
    color = cmap(norm(count))  # get color for the current trigger count
    cell_colours[row, col] = mcolors.to_hex(color)  # convert to hex



# cell_colours = np.full((rows, cols), '#FFFFFF')  # init color grid
# for alarm_id, trigger_count in trigger_counts.items():
#     if alarm_id in row_col_mapping:
#         row, col = row_col_mapping[alarm_id]
#         color = cmap(norm(trigger_count))        # get color for the trigger count
#         cell_colours[row, col] = mcolors.to_hex(color)  # convert to hex


# figure size
fig, ax = plt.subplots(figsize=(10, 6))
ax.axis('tight')
ax.axis('off')

# fig.suptitle("Alarm Events Heatmap", fontsize=16)  # title for the entire figure
# ax.set_title("Total Trigger Counts by Photo-Eye Jams", fontsize=14)  # title for the subplot


# heatmap's col widths
# tbl = table(ax, table_df, loc='center', colWidths=[0.1] * cols, cellColours=cell_colours)
tbl = table(ax, table_df, loc='center', colWidths=[0.04, 0.04, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.04, 0.04, 0.04], cellColours=cell_colours)


tbl.auto_set_font_size(False)
tbl.set_fontsize(7)
tbl.scale(0.7, 0.7)

# add colorbar on the right to indicate the feature (time range) from lo to hi
cbar_ax = fig.add_axes([0.1, 0.1, 0.8, 0.02])  # Position the colorbar on the right
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])  # empty array for scalarmappable
cbar = fig.colorbar(sm, cax=cbar_ax, label='Trigger Counts', orientation='horizontal')

# set ticks on the colorbar
# cbar.set_ticks([min_count, (max_count/3), (2*max_count/3), max_count])  # set ticks for min, mid, and max trigger counts
# cbar.set_ticklabels([int(min_count), int(max_count/3), int(2*max_count/3), int(max_count)])  # format ticks as integers
cbar.set_ticks([min_count, (max_count/10), (2*max_count/10), (3*max_count/10), (4*max_count/10), (5*max_count/10), (6*max_count/10), (7*max_count/10), (8*max_count/10), (9*max_count/10), max_count])  # set ticks for min, mid, and max trigger counts
cbar.set_ticklabels([min_count, float(max_count/10), 2*max_count/10, 3*max_count/10, 4*max_count/10, 5*max_count/10, 6*max_count/10, 7*max_count/10, 8*max_count/10, 9*max_count/10, max_count])  # format ticks as integers

# show figure
plt.show()
