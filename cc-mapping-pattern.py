def generate_pattern(start, end):
  for cc_num in range(start, end + 1):
    for i in range(22):
      print(f"\"CC{cc_num}.{key_value_pairs[i]}\": ({i + 1},{cc_num - 1}),")
    print()

# Define the key-value pairs
key_value_pairs = [
  "Conv1_ChuteJam",
  "Conv1_ChuteFull",
  "Conv2_ChuteJam",
  "Conv2_ChuteFull",
  "Conv12Jam",
  "Conv3_ChuteJam",
  "Conv3_ChuteFull",
  "Conv4_ChuteJam",
  "Conv4_ChuteFull",
  "Conv23Jam",
  "Conv5_ChuteJam",
  "Conv5_ChuteFull",
  "Conv6_ChuteJam",
  "Conv6_ChuteFull",
  "Conv34Jam",
  "Conv7_ChuteJam",
  "Conv7_ChuteFull",
  "Conv8_ChuteJam",
  "Conv8_ChuteFull",
  "OutputBJam",
  "Bin_BLeft_Full",
  "Bin_BRight_Full"
]

# Generate the pattern for CC1 to CC77
generate_pattern(1, 77)