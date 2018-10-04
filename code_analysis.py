# -*- coding: utf-8 -*-
import re
import os
import sys

try:
    filename=sys.argv[1]

except Exception:
    print("Usage:python code_analysis.py filename")
    sys.exit()

names = []#函数名
group = []
functions = {}#函数名与函数体
strcpy_error={}
strncpy_error={}

pattern = re.compile(r'((?:const[ \t\*]+)?(?:void|int|char|long|double|float|unsigned|unsigned int|unsigned long|long long)[ \t\*]+(?:const[ \t*]+)?)(\w+)(\([^\;]*\))[^\;]*(\{([^{}]*(\{([^{}]*(\{([^{}]*(\{[^{}]*\})*[^\{\}]*?)*\})*[^\{\}]*?)*\})*[^\{\}]*?)*\})', re.S)

def get_functions(filepath):
    f = open(filepath, "r")
    str = f.read()
    f.close()
    group = pattern.findall(str)
    #print(group)
    for g in group:
        names.append(g[1])
        functions[g[1]] = g[3]
        #print(g[3]) #函数名
        #print(g[5]) #函数体

def strcpy_check(name,function,var,var_pointer,var_arrays):#参数为函数名，函数体，三种参数，属于栈溢出
	value_line=function.splitlines()#函数体分行
	strcpy_pattern=re.compile(r'strcpy\([ \t]*([\w_]+)[ \t]*[\,][ \t]*([\w_]+)[ \t]*[\)\;]+')
	for (i,element) in list(enumerate(value_line)):
		result=element.find("strcpy")
		if result!=-1: #确定strcpy所在行
			strcpy_para=strcpy_pattern.findall(element)#提取两个参数
			for para in strcpy_para:
				for(key,value) in var_pointer.items():
					result1=key.find(para[0])
					if result1!=-1:
						para1_size=var_pointer[key]
						break
				for(key,value) in var_pointer.items():
					result2=key.find(para[1])
					if result2!=-1:
						para2_size=var_pointer[key]
						break
				for(key,value) in var_arrays.items():
					result1=key.find(para[0])
					if result1!=-1:
						para1_size=var_arrays[key]
						break
				for(key,value) in var_arrays.items():
					result2=key.find(para[1])
					if result2!=-1:
						para2_size=var_arrays[key]
						break
						
			if para1_size < para2_size:
				if strcpy_error[name].has_key("strcpy")==0:
                                    strcpy_error[name].setdefault("strcpy",[]).append(i)
							
def strncpy_check(name,function,var,var_pointer,var_arrays):#参数为函数名，函数体，三种参数，属于栈溢出
	value_line=function.splitlines()#函数体分行
	strncpy_pattern=re.compile(r'strncpy\([ \t]*([\w_]+)[ \t]*[\,][ \t]*([\w_]+)[ \t]*\,[ \t]*([\d]+)[ \t]*[\)\;]+')
	for (i,element) in list(enumerate(value_line)):
		result=element.find("strncpy")
		if result!=-1: #确定strncpy所在行
			strncpy_para=strncpy_pattern.findall(element)#提取两个参数
			for para in strncpy_para:
				for(key,value) in var_pointer.items():
					result1=key.find(para[0])
					if result1!=-1:
						para1_size=var_pointer[key]
						break
				for(key,value) in var_pointer.items():
					result2=key.find(para[1])
					if result2!=-1:
						para2_size=var_pointer[key]
						break
				for(key,value) in var_arrays.items():
					result1=key.find(para[0])
					if result1!=-1:
						para1_size=var_arrays[key]
						break
				for(key,value) in var_arrays.items():
					result2=key.find(para[1])
					if result2!=-1:
						para2_size=var_arrays[key]
						break
			print(para1_size)
				print(para2_size)
				print(para[2])
						
				if (para1_size < para[2]) or (para2_size < para[2]):
					if strncpy_error[name].has_key("strncpy")==0:
						strncpy_error[name].setdefault("strncpy",[]).append(i)
			
'''
def memcpy_check(function):
def memncpy_check(function):
def strcat_check(function):
def strncat_check(function):
'''	

def var_search(name,function,var_type):
    declarations = []
    var={}
    var_pointer={}
    var_arrays = {}
    if var_type=="char":
	var_size=1
    if var_type=="int":
        var_size=4
    if var_type=="short":
	var_size=2
    if var_type=="long":
	var_size=8
    #获取char[]相关变量,+一次或无限次，*0次或无限次，？0次或1次
    filter_expression="("+var_type+"[ \t\*]+([\w_]+)(\[[\w_]*\])*[ \t]*(\={1}[^\;\,]*)*[ \t]*(\,[ \t\*]*([\w\_]+)(\[[\w\_]*\])*[ \t]*(\={1}[^\;\,]*)*[ \t]*)*\;)"
    var_pattern = re.compile(filter_expression, re.S)
    all_decl = var_pattern.findall(function)
    #print(all_decl)
    for decl in all_decl:
        declarations.append(decl[0])#将var型声明语句提取出来
	#print(decl[0])

    #过滤出数组类型，该数组类型为直接定义数组大小
    arrays_filter1=var_type+"[ \t]+([\w\_]+)(\[([\w\_]+)\])"
    arrays_filter2="\,[ \t]*([\w\_]+)(\[([\w\_]+)\])"
    para_pattern1 = re.compile(arrays_filter1)#得到数组声明的第一个
    para_pattern2 = re.compile(arrays_filter2)#得到数组声明第二个及之后
    for declaration in declarations:
        parameters1 = para_pattern1.findall(declaration)
        parameters2 = para_pattern2.findall(declaration)
	#print(parameters1)#声明行第一个声明的char数组
	#print(parameters2)
	for para in parameters1:
	    var_arrays[para[0]]=para[2]
	for para in parameters2:
	    var_arrays[para[0]]=para[2]
	
	#过滤出数组类型，该数组类型为根据字符串定义数组大小
	arrays__filter1=var_type+"[ \t]+([\w_]+)(\[[ \t]*\])[ \t]*\={1}[ \t]*\"{1}([\w]+)\"{1}"
	arrays__filter2="\,[ \t]*([\w_]+)(\[[ \t]*\])[ \t]*\={1}[ \t]*\"{1}([\w]+)\"{1}"
	para__pattern1 = re.compile(arrays__filter1)#得到数组声明的第一个
    para__pattern2 = re.compile(arrays__filter2)#得到数组声明第二个及之后
    for declaration in declarations:
        parameters_1 = para__pattern1.findall(declaration)
        parameters_2 = para__pattern2.findall(declaration)
	#print(parameters1)#声明行第一个声明的char数组
	#print(parameters2)
	for para in parameters_1:
	    var_arrays[para[0]]=len(para[2])
	for para in parameters_2:
	    var_arrays[para[0]]=len(para[2])
	
	#获取var类型变量
    var_filter1=var_type+"[ \t]+([\w_]+)(?!\[)(?=[ \t]*[\,\;]+)"
    var_filter2="\,[ \t]*([\w_]+)(?!\[)(?=[ \t]*[\,\;]+)"
    para_pattern3 = re.compile(var_filter1)
    para_pattern4 = re.compile(var_filter2)
    for declaration in declarations:
	print(declaration)
        parameters3 = para_pattern3.findall(declaration)
        parameters4 = para_pattern4.findall(declaration)
	
        for para in parameters3:
            var[para]=var_size
        for para in parameters4:
            var[para]=var_size
	#print(char)
	
	#获取var*型变量
    var_pointer_filter1=var_type+"[ \t]*[\*]+[ \t]*([\w\_]+)(?=[ \t]*[\,\;]+)"
    var_pointer_filter2="\,[\*]+[ \t]*([\w\_]+)(?=[ \t]*[\,\;]+)"
    para_pattern5 = re.compile(var_pointer_filter1)
    para_pattern6 = re.compile(var_pointer_filter2)
    for declaration in declarations:
        parameters5 = para_pattern5.findall(declaration)
        parameters6 = para_pattern6.findall(declaration)
	#print(parameters5)#声明行第一个声明的char数组
	#print(parameters6)
        for para in parameters5:
            var_pointer[para]=""
        for para in parameters6:
            var_pointer[para]=""
	
	#获取malloc分配空间
	malloc_space="([\w_]+)\={1}\({1}"+var_type+"[ \t]*\*[ \t]*\){1}[ \t]*malloc[ \t]*\({1}[ \t]*([\d]+)[ \t]*\*{1}[ \t]*sizeof\({1}"+var_type+"\){2}"
	para_pattern7 = re.compile(malloc_space)
	malloc=para_pattern7.findall(function)
	for pointer in malloc:
	    var_pointer[pointer[0]]=pointer[1]
	
	strcpy_check(name,function,var,var_pointer,var_arrays)
	strncpy_check(name,function,var,var_pointer,var_arrays)
    print(var_arrays)
    #print(" ")
    print(var)
    #print(" ")
    print(var_pointer)
    #print(" ")
    print(strcpy_error)

	
def assign(function):#获取所有直接赋值语句
	pattern=re.compile(r'([\w_]+)\={1}([\w_]+)')
	assign=pattern.findall(function)
	
def check_heap_overflow(function):
    pass


get_functions(filename)
#get_call_relationship(names, functions)

for (key, value) in functions.items():#遍历函数体
    #print(value)
    strcpy_error[key]={}
    strncpy_error[key]={}
    var_search(key,value,"char")
    if not strcpy_error[key]:#如果该函数体中没有错误则删除该键
        del strcpy_error[key]
    #char_search(value)
    print("")
print(strcpy_error)
