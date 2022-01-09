import os
import re

work_dir = os.path.dirname(os.path.realpath(__file__))

for file_name in os.listdir(work_dir):
    # if the file name ends with htm, can change to xml or other extension
    if file_name.endswith(".htm"):
        absolute_path = os.path.join(work_dir, file_name)

        with open(absolute_path, 'r+', encoding="utf-8") as f:

        
            f.seek(0)
            f.write(a_tag)
            f.truncate()
