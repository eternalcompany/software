# -*- coding: utf-8 -*-  
import re
import os
import sys
import difflib
from graphviz import Digraph
dot = Digraph(comment='CFG')
try:
    filename=sys.argv[1]
    filename2=sys.argv[2]
except Exception:
    print("Usage:python get_cfg.py filename")
    sys.exit()

names = []#储存函数名的列表
functions = {}#dict字典数据类型
names2 = []
functions2={}
cfg_in={}
cfg_out={}
cfg_in2={}
cfg_out2={}
In_sum=0
Out_sum=0
In_sum2=0
Out_sum2=0
pattern = re.compile(r'((const[ \t\*]+)?(void|int|char|long|double|float|unsigned|unsigned int|unsigned long|long long|struct))[ \t\*]+(\w+[ \t]+)?(\w+)(\([^\;]*\))[^\;]*(\{([^{}]*(\{([^{}]*(\{([^{}]*(\{[^{}]*\})*[^\{\}]*?)*\})*[^\{\}]*?)*\})*[^\{\}]*?)*\})', re.S)

def get_functions(filepath):#获取函数名和函数体
    f = open(filepath, "r")
    str = f.read()
    f.close()
    group = pattern.findall(str)#分段获取截获的字符串
    #print(group)
    for g in group:
        names.append(g[4])#向列表末端添加一个元素，多个则用extend,储存函数名
        functions[g[4]] = g[6]#函数名为
        #print(g[4]) #函数名
        #print(g[6]) #函数体

def get_call_relationship(names, functions):#参数为列表和字典
    for (key, value) in functions.items():#以列表返回键值
        print("function #" + key + "#  calls following functions:")
        flag = False
        for name in names:#遍历函数名
            result = value.find(name)#在键值中查找是否有函数名字符串
            if  result!=-1:
                flag = True
                dot.edge(key, name)
                print("    " + name)
        if flag == False:#函数没有调用其它函数时
            print("    none")
        print(" ")
    #dot.render('test-output/round-table.gv', view=True)#在该文件夹中生成图片并自动打开

def cfg_analysis(names,functions):#根据cfg图的结点进行分析
	cfg_in=functions.copy()
	cfg_out=cfg_in.copy()
	global In_sum;
	global Out_sum;
	for (key, value) in cfg_in.items():#以列表返回键值
		cfg_in[key]= 0
		cfg_out[key]= 0
	#print(functions)
	for (key, value) in functions.items():#以列表返回键值
		for name in names:
			result = value.find(name)#在键值中查找是否有函数名字符串
			if  result!=-1:
				cfg_out[key]=cfg_out[key]+1
				cfg_in[name]=cfg_in[name]+1
	for (key, value) in cfg_in.items():
		print("name: %25s    In degree: %10d     Out degree: %10d" % (key,cfg_in[key],cfg_out[key]))
		In_sum=In_sum+cfg_in[key]
		Out_sum=Out_sum+cfg_out[key]


def get_functions2(filepath):#获取函数名和函数体
    f = open(filepath, "r")
    str = f.read()
    f.close()
    group = pattern.findall(str)#分段获取截获的字符串
    #print(group)
    for g in group:
        names2.append(g[4])#向列表末端添加一个元素，多个则用extend,储存函数名
        functions2[g[4]] = g[6]#函数名为
        #print(g[4]) #函数名
        #print(g[6]) #函数体

def get_call_relationship2(names2, functions2):#参数为列表和字典
    for (key, value) in functions2.items():#以列表返回键值
        print("function #" + key + "#  calls following functions:")
        flag = False
        for name in names2:#遍历函数名
            result = value.find(name)#在键值中查找是否有函数名字符串
            if  result!=-1:
                flag = True
                dot.edge(key, name)
                print("    " + name)
        if flag == False:#函数没有调用其它函数时
            print("    none")
        print(" ")
    #dot.render('test-output/round-table.gv', view=True)#在该文件夹中生成图片并自动打开

def cfg_analysis2(names2,functions2):#根据cfg图的结点进行分析
	cfg_in2=functions2.copy()
	cfg_out2=cfg_in.copy()
	global In_sum2;
	global Out_sum2;
	for (key, value) in cfg_in2.items():#以列表返回键值
		cfg_in2[key]= 0
		cfg_out2[key]= 0
	#print(functions)
	for (key, value) in functions2.items():#以列表返回键值
		for name in names2:
			result = value.find(name)#在键值中查找是否有函数名字符串
			if  result!=-1:
				cfg_out2[key]=cfg_out2[key]+1
				cfg_in2[name]=cfg_in2[name]+1
	for (key, value) in cfg_in2.items():
		print("name: %25s    In degree: %10d     Out degree: %10d" % (key,cfg_in2[key],cfg_out2[key]))
		In_sum2=In_sum2+cfg_in2[key]
		Out_sum2=Out_sum2+cfg_out2[key]
		

get_functions(filename)
get_call_relationship(names, functions)
get_functions2(filename2)
get_call_relationship2(names2, functions2)
print("                                     In first file:")
cfg_analysis(names,functions)
print("                                     In second file:")
cfg_analysis2(names2,functions2)
In_difference=(In_sum+1)/(In_sum2+1)
if In_difference > 1:
	In_difference=(In_sum2+1)/(In_sum+1)
print(In_difference)
'''
Out_difference=(Out_sum+1)/(Out_sum2+1)
if Out_difference > 1:
	Out_difference=(Out_sum2+1)/(Out_sum+1)
print(Out_difference)
'''