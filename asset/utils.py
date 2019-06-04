import os


def traverse(f):
    fs = os.listdir(f)
    search_file_list = []
    for f1 in fs:
        tmp_path = os.path.join(f,f1)
        if os.path.isdir(tmp_path):
            search_file_list += traverse(tmp_path)
        else:
            search_file_list.append(tmp_path)
    return search_file_list

