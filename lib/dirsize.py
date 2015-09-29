
import os

__author__ = 'Matthias Lohr <matthias@lohr.me>'


def dirsize(cur_dir):
    total_size = os.path.getsize(cur_dir)
    for item in os.listdir(cur_dir):
        itempath = os.path.join(cur_dir, item)
        if os.path.isfile(itempath):
            total_size += os.path.getsize(itempath)
        elif os.path.isdir(itempath):
            total_size += dirsize(itempath)
    return total_size
