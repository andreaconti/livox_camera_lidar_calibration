#! /usr/bin/env python

"""
Utility to launch pcd_viewer and collect coordinates
"""

import rospy
import subprocess
import re
import os
import sys
import argparse
from glob import glob

parser = argparse.ArgumentParser()
parser.add_argument("pcd_folder", type=str)
parser.add_argument("out_path", type=str)
parser.add_argument("ROS_ARGS", nargs="+")
args = parser.parse_args()

for pcd_path in sorted(list(glob(args.pcd_folder + "/*"))):
    print("viewing file " + pcd_path)
    proc = subprocess.Popen(
        ["pcl_viewer", "-use_point_picking", pcd_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    points = []
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        searched = re.search(
            "\[([+-]?[0-9]+\.[0-9]+), +([+-]?[0-9]+\.[0-9]+), +([+-]?[0-9]+\.[0-9]+)\]",
            line,
        )
        if searched:
            x, y, z = searched.groups()
            points.append((x, y, z))
            print("Picked " + " ".join(points[-1]))

    pcl_idx = os.path.basename(pcd_path).split(".")[0]
    with open(sys.argv[2], "at") as f:
        lines = ["test" + pcl_idx + "\n"]
        for idx, point in enumerate(points[-4:], start=1):
            lines.append(str(idx) + "\n")
            lines.append(" ".join(point) + "\n")
        f.writelines(lines)

print("points written in " + args.out_path)
