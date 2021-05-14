# -*- coding: utf-8 -*-
'''
@Author billie
@Date 2020/5/7 14:33
@Describe 

'''
import os,filecmp,re,shutil
import time

def is_common(file1,file2):
    print(file1,file2)
    return filecmp.cmp(file1,file2)#返回bool值
def compare_two_dirs(dir1,dir2):
    if not dir1.endswith('\\'): dir1=dir1+'\\'  # 加上/
    if not dir2.endswith('\\'): dir2=dir2+'\\'  # 加上/
    mycomp=filecmp.dircmp(dir1,dir2)
    #备份模式1、若dir1中有dir2中没有的文件，则继续执行
    if len(mycomp.left_list) > 0:#dir1中的文件
        for file in mycomp.left_list:#dir1中的所有文件
            if not os.path.exists(dir2+file):#如dir2中不存在此文件，则
                shutil.copy(dir1+file,dir2+file)#复制dir1中的文件
                print('已备份|', dir2 + file)
    #备份模式2、若dir1中的文件与dir2中的文件存在差异，则继续执行
    for file in mycomp.common:#dir1、dir2中的相同文件
        about_update_files=[]
        if is_common(dir1+file,dir2+file) == False:
            about_update_files.append(file)
            print('待更新|',dir2+file)
            shutil.copy(dir1 + file, dir2 + file)  # 复制dir1中的文件
            print('已更新|', dir2 + file)
        else:print('无需更新|',dir2+file)

def back_up_two_dirs(dir1,back_up_path):
    if not os.path.exists(back_up_path+dir1): os.mkdir(back_up_path+dir1)
    compare_two_dirs(dir1,dir2=back_up_path+dir1)
    time.sleep(10)
def back_up_two_files(file1,back_up_path):
    if not os.path.exists(back_up_path+file1):open(back_up_path+file1,'w',encoding='utf-8')#创建写入文件
    file2 = back_up_path+file1
    if is_common(file1, file2) == False:#判断文件异同
        print('待更新|', file2)
        shutil.copy(file1, file2)  # 复制dir1中的文件
        print('已更新|', file2)
    else:
        print('无需更新|', file2)
if __name__=='__main__':
    base_back_up_path='D:\\back_up_file\\'
    #如备份目录下未存在此文件夹，则创建
    if not os.path.exists(base_back_up_path+os.path.basename(os.getcwd())):
        os.mkdir(base_back_up_path+os.path.basename(os.getcwd()))
    back_up_path=base_back_up_path+os.path.basename(os.getcwd())+'\\'
    print(back_up_path)
    #获取目录下所有的文件和文件夹
    all=os.listdir(os.getcwd())
    for one in all:
        if os.path.isfile(one):#如果是文件
            back_up_two_files(one,back_up_path)
        elif os.path.isdir(one):#如果是目录
            back_up_two_dirs(one,back_up_path)
