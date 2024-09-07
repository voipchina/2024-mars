# write bash script
# convert all frames of mp4 files to jpg, 
# the input directory is under the "/root/autodl-tmp/2024_mars/train/mp4"
# the output directory is "/root/autodl-tmp/2024_mars/train/jpg"
# The output file name format is {source file basename}_{frame_id}.jpg
# Using 12 cores to convert the files in parallel.

#!/bin/bash

input_dir="/root/autodl-tmp/2024_mars/train/mp4"
output_dir="/root/autodl-tmp/2024_mars/coco/images/train2017"
mkdir -p "$output_dir"
num_cores=12
for mp4_file in "$input_dir"/*.mp4; do
    base_name=$(basename "$mp4_file" .mp4)
    echo $base_name
    formatted_base_name=$(printf "%03d" $base_name)
    ffmpeg -i "$mp4_file" -threads "$num_cores" "$output_dir/$formatted_base_name"_%04d.jpg
done
