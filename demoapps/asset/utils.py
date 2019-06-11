import os


def traverse(f):
    '''
    :param f: 检索路径
    :return: list => [(ctime, path_name)]
    '''
    fs = os.listdir(f)
    search_file_list = []
    for f1 in fs:
        tmp_path = os.path.join(f,f1)
        if os.path.isdir(tmp_path):
            search_file_list += traverse(tmp_path)
        else:
            file_ctime = os.path.getctime(tmp_path)
            search_file_list.append((file_ctime, tmp_path))
    return search_file_list


def system_path_search(curpath):
    find_t =''
    if curpath[-1] != "/":
        *curpath_list, find_t = curpath.split('/')
        curpath = '/'.join(curpath_list) + '/'
    try:
        cur_list = [t for t in os.listdir(curpath)]
        if find_t:
            cur_list = [t for t in  cur_list if find_t in t]
        return cur_list
    except FileNotFoundError:
        return []
