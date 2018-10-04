# -*- coding: UTF-8 -*-
import difflib
import sys
import time
import os
import re

define_rules = re.compile(r'\#define[ \t]+(([^ \t])+)[ \t]+([^\n]+)\n')
commet_rules = re.compile(r'((?<=\n)|^)[ \t]*\/\*.*?\*\/\n?|\/\*.*?\*\/|((?<=\n)|^)[ \t]*\/\/[^\n]*\n|\/\/[^\n]*', re.S)
def main():
    """主函数"""
    try:
        f1 = sys.argv[1]#获取文件名
        f2 = sys.argv[2]
    except  Exception as e:
        print("Error: "+ str(e))
        print("Usage : python compareFile.py filename1 filename2")
        sys.exit()

    if f1 == "" or f2 == "":#参数不够
        print("Usage : python compareFile.py filename1 filename2")
        sys.exit()

    tf1 = readFile(f1)
    tf2 = readFile(f2)

    d = difflib.Differ()
    diff = d.compare(tf1,tf2)
    #print(list(diff))
    differ=list(diff)
    print('\n'.join(differ))
    matcher = difflib.SequenceMatcher(None,tf1,tf2).ratio()
    print(matcher)
    a=open('test.txt',"w")
    a.write('\n'.join(differ))
    a.close()

def readFile(filename):
    """读取文件，并处理"""
    try:
        fileHandle = open(filename, "r")
        str = fileHandle.read()
	fileHandle.close()
	#去注释
	str = re.sub(commet_rules, "", str)
	#define宏定义替换，并去除宏定义语句
	group1 = define_rules.findall(str)
	str = re.sub(define_rules, "", str)
	for g in group1:
		str = str.replace(g[0], g[2])
        text = str.splitlines()
        return text
    except IOError as e:
        print("Read file error: "+ str(e))
        sys.exit()
        
main()
