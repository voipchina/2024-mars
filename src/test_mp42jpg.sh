# write bash script
# convert all frames of mp4 files to jpg, 
# the input directory is under the "/root/autodl-tmp/2024_mars/train/mp4"
# the output directory is "/root/autodl-tmp/2024_mars/train/jpg"
# The output file name format is {source file basename}_{frame_id}.jpg
# Using 12 cores to convert the files in parallel.

#!/bin/bash
input_dir="/root/autodl-tmp/2024_mars/test/mp4"
output_dir="/root/autodl-tmp/2024_mars/coco/images/test2017"
mkdir -p "$output_dir"
num_cores=12
i=1
while [ $i -le 39 ]
do
  mp4_file=$input_dir/test_$i.mp4
  formatted_i=$(printf "%03d" $i)
  ffmpeg -i "$mp4_file" -threads "$num_cores" "$output_dir/test_$formatted_i"_%04d.jpg
  ((i++))
done
