from pathlib import Path
from os import getenv
from datetime import datetime, timedelta
import os

"""
Script for changing date in source data
"""

def update_file():
    start_point = datetime.fromisoformat(getenv("START_DATE").replace("Z", "+00:00"))
    path_files = [
                    getenv("FULL_PATH_SOURCE_TEST_DATA_TRAN"),
                    getenv("FULL_PATH_SOURCE_TRAIN_DATA_TRAN")
                ]
    header_time = getenv("HEADER_DATETIME")
    header_time_index  = -1
    save_dir = Path(getenv("SAVE_PATH"))
    for path_file in path_files:
        with open(path_file,"r",encoding="utf-8") as file_read:
            with open(os.path.join(save_dir,Path(path_file).name), "w", encoding="utf-8") as file_write:
                is_end = False
                for idx, line in enumerate(file_read):
                    if idx == 0:
                        header_time_index = line.split(",").index(header_time)
                        file_write.write(line)
                        continue
                    if "\n" not in line:
                        is_end = True
                    line = line.strip()
                    parts = line.split(",")
                    if header_time_index == -1:
                        raise IndexError("wrong index, index must be not -1")
                    else:
                        time_s = int(parts[header_time_index])

                    time_add = timedelta(seconds=time_s)
                    new_date = start_point+time_add
                    parts[header_time_index] = new_date.isoformat(timespec="milliseconds").replace("+00:00", "Z")
                    line = ",".join(parts)
                    if not is_end:
                        line += "\n"

                    file_write.write(line)
                
if __name__ == "__main__":
    update_file()