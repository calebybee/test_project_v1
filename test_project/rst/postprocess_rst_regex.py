import os
import re

work_dir = os.path.dirname(os.path.realpath(__file__))

for file_name in os.listdir(work_dir):
    # if the file name ends with htm, can change to xml or other extension
    if file_name.endswith((".rst")):
        absolute_path = os.path.join(work_dir, file_name)

        with open(absolute_path, 'r+') as f:

            a_tag = f.read()
            a_tag = re.sub('\*', r'\n', a_tag)
            a_tag = re.sub('defines', r'xxxxxxxxxxxxxxxxxxxxxxxx', a_tag)
            
            f.seek(0)
            f.write(a_tag)
            f.truncate()
