import os
from tqdm import tqdm
import zipfile
import rarfile
import py7zr

"""
支持格式：zip, rar, 7z
- rarfile FAQ: https://rarfile.readthedocs.io/en/latest/faq.html
- py7zr: https://py7zr.readthedocs.io/en/latest/py7zr.html
- 7zfile: https://www.jianshu.com/p/270bbe25bce7
"""

# 指定 winrar 路径
rarfile.UNRAR_TOOL = r'C:\Program Files\WinRAR\UnRAR.exe'
ALLOW_EXTS = ['rar', 'zip', '7z']

zip_dir = r'C:\Users\Shuai\Desktop\IMG_add'
ext_dir = r'C:\Users\Shuai\Desktop\IMG_add_res'

# for dir in os.listdir(zip_dir):
for dir in os.listdir(zip_dir):
    print(dir)
    sub_dir = os.path.join(zip_dir, dir)
    sub_ext_dir = os.path.join(ext_dir, dir)
    os.makedirs(sub_ext_dir, exist_ok=True)

    process_bar = tqdm(os.listdir(sub_dir))
    for zip_file in process_bar:
        # process_bar.set_description(zip_file)  # 设置 bar 头
        process_bar.set_postfix_str(zip_file)  # 设置 bar 尾，在 [] 里

        ext = zip_file.rsplit('.', maxsplit=1)[-1]

        if ext in ALLOW_EXTS:
            zip_path = os.path.join(sub_dir, zip_file)
            out_path = os.path.join(sub_ext_dir, zip_file.replace('.zip', '').replace('.rar', '').replace('.7z', ''))
            os.makedirs(out_path, exist_ok=True)

            if ext == 'zip':
                try:
                    zfile = zipfile.ZipFile(zip_path, 'r')
                    zfile.extractall(out_path)
                except zipfile.BadZipFile:
                    print(zip_file, 'is a bad zip file')

            elif ext == 'rar':
                try:
                    rfile = rarfile.RarFile(zip_path, 'r')
                    rfile.extractall(out_path)
                except rarfile.BadRarFile:
                    print(zip_file, 'is a bad rar file')
                except rarfile.RarCRCError:
                    print(zip_file, 'har CRC error')

            elif ext == '7z':
                try:
                    zfile = py7zr.SevenZipFile(zip_path, 'r')
                    zfile.extractall(out_path)
                except py7zr.Bad7zFile:
                    print(zip_file, 'is a bad 7z file')

        else:
            print('skip:', zip_file)
