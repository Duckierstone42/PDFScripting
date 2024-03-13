import os
import shutil
data_path = os.path.join(os.getcwd(), "language_struct_project_data")
safe = 0
total = 0
for file in os.listdir(data_path):
    file_path = os.path.join(data_path,file)
    total+=1
    if (len(os.listdir(file_path)) == 2):
        safe+=1
    else:
        shutil.rmtree(file_path)

print(safe/total)