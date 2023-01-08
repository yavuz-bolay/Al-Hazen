import sys

import AlHazen


def main(*args):
    od_dir = args[0]
    ds_dir = args[1]
    try:
        thresh = int(args[2])
    except ValueError:
        thresh = "auto"
    try:
        detect_val = float(args[4])
    except ValueError:
        detect_val = 0.85
    try:
        thresh_ratio = float(args[3])
    except ValueError:
        thresh_ratio = 0.85
    print("START PROCESS:")
    print("#"*150)
    print(f"Original Data Directory: {od_dir}")
    print(f"Dataset Directory: {ds_dir}")
    print(f"Thresh Type/Value: {thresh}")
    print(f"Thresh Ratio: {thresh_ratio}")
    print(f"Detect Ratio: {detect_val}")
    sure = input("STARTING, ARE YOU SURE? (y/n)")
    while sure in "nN":
        od_dir = input("Original Data Directory: ")
        ds_dir = input("Dataset Directory: ")
        thresh = input("Thresh Value: ")
        detect_val = input("Detect Ratio: ")
        sure = input("STARTING, ARE YOU SURE? (y/n)")
    print("="*150)
    AlHazen.Run(od_dir, ds_dir, thresh, thresh_ratio, detect_val).run()


if __name__ == '__main__':
    args = sys.argv[1:]
    main(*args)
