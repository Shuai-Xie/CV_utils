"""
找出没交的作业名单
- python 读取 csv: https://www.jianshu.com/p/4a3a6291af1b
- pandas 读写 xls 需要 xlrd, xlwt
- dataframe: https://www.cnblogs.com/timotong/p/9678490.html
- pandas Series: https://blog.csdn.net/Quincuntial/article/details/72886716
"""

import pandas as pd
import os

# 所有学生名单
stu_info = pd.read_excel(r'C:\Users\Shuai\Desktop\学生名单.xls',
                         header=3,  # 表头所在行，如果直接读数据不太好
                         usecols=[1, 3])  # 指定 id, name 列
stu_info = stu_info.iloc[0:-2, :]  # 按照行列 idx 来取；去掉末尾2个补考
# stu_info = stu_info.loc[0:-2, ['id', 'name']]  # loc 根据实际行列标签来取，所以 -2 不可
stu_info.columns = ['id', 'name']  # 为 unnamed 列，设置名称


def check_in(ck_list, *ck_keys):
    for item in ck_list:  # 每个被检索文件名
        for key in ck_keys:  # 每个检索 key
            if key in item:
                return True
    return False


def filter_no_submits(check_dir, out_file='no_submits.xls'):
    # 已上交
    submit_list = os.listdir(check_dir)
    no_handle = [(str(row['id']), row['name'])
                 for _, row in stu_info.iterrows()
                 if not check_in(submit_list, str(row['id']), row['name'])]

    stu_no_handle = pd.DataFrame(no_handle, columns=['学号', '姓名'])
    print(stu_no_handle)
    # stu_no_handle.to_excel(out_file, sheet_name='no_submits',  # excel 下面的表名
    #                        index=False)  # 不显示索引号


if __name__ == '__main__':
    root = r'C:\Users\Shuai\Desktop\IMG2019_res'

    for hw in os.listdir(root):
        print(hw)
        filter_no_submits(check_dir=os.path.join(root, hw))
