# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 16:55:48 2017

@author: Vio
"""
import re
import chardet
import os

#导入正则表达式
f_regex = open('./wordlist/regex.txt')
regex_list = []
for i in f_regex:
    regex_list.append(i.strip())

#匹配邮箱
p_mail_edu = re.compile(regex_list[0]) #匹配教育邮箱
p_mail_ieee = re.compile(regex_list[1]) #匹配ieee的邮箱
p_mail_base = re.compile(regex_list[2]) #匹配普通邮箱
#匹配电话号
p_phone1 = re.compile(regex_list[3]) #8位固话
p_phone2 = re.compile(regex_list[4]) #11位手机号，1开头
p_phone3 = re.compile(regex_list[5]) #例如010 5880 5522格式
p_phone4 = re.compile(regex_list[6]) #例如010-68940964格式
p_phone5 = re.compile(regex_list[7]) #例如(010)58807927格式
p_phone6 = re.compile(regex_list[8]) #例如0086-10-66692008格式
p_phone7 = re.compile(regex_list[9]) #例如021-20231000-2221格式
#匹配个人主页、实验室网站等
p_url = re.compile(regex_list[10])
#匹配专利号
p_zl = re.compile(regex_list[11])#申请号或授权号
p_zl2 = re.compile(regex_list[12])#授权公告号
p_zl3 = re.compile(regex_list[13])

##匹配论文、专著##
#匹配书号（ISBN,ISSN）
p_isbn = re.compile(regex_list[14])
p_issn = re.compile(regex_list[15]) #末位校验位数字或X
#匹配论文中的文献类型
p_label = re.compile(regex_list[16]) #匹配文献标准格式中的文献类型[M][C][J]等
#匹配论文中的日期 页数
#1998，(3):167-173 或 1997，38(3),358-361 形式
p_page1 = re.compile(regex_list[17])
#1957:15-18形式
p_page2 = re.compile(regex_list[18])
# 10(8):1573-1581, 2012形式
p_page3 = re.compile(regex_list[19])
#735-746,2012形式
p_page4 = re.compile(regex_list[20])
#pp. 47-57
p_page5 = re.compile(regex_list[21])
##匹配论文、专著##

#匹配专著的书名号
p_book = re.compile(regex_list[22])

#匹配年份
p_year1 = re.compile(regex_list[23]) #2001年
p_year2 = re.compile(regex_list[24]) #2001.01

#匹配词表
organization_list = [] #学术组织列表
for word in open('./wordlist/organization.txt'):
    organization_list.append(word.strip('\n'))

direction_list = [] #研究方向列表
for word in open('./wordlist/directions.txt'):
    direction_list.append(word.strip('\n'))

title_list = [] #简历标题词列表
for word in open('./wordlist/title.txt'):
    title_list.append(word.strip('\n'))
    
position_list = [] #职务词条列表
for word in open('./wordlist/position.txt'):
    position_list.append(word.strip('\n'))

commonword_list = [] #高频词
for word in open('./wordlist/CommonWord.txt'):
    commonword_list.append(word.strip('\n'))
    
minzu_list = [] #民族词条列表
for word in open('./wordlist/minzu.txt'):
    minzu_list.append(word.strip('\n'))

resumeword_list = [] #简历同义词词条列表
for word in open('./wordlist/resume_word.txt'):
    resumeword_list.append(word.strip('\n'))

def classify_single(file_path,data,file_charset):
    f1 = 0 #每个文本的长度。
    f2 = 0 #邮箱数
    f3 = 0 #电话号码数
    f4 = 0 #网站数
    f5 = 0 #专利号数
    f6 = 0 #专著、论文数
    f7 = 0 #书名号数目
    f8 = 0 #年份词
    f9 = 0 #包含学术组织词条数
    f10 = 0 #包含研究方向词条数
    f11 = 0 #简历标题词数
    f12 = 0 #职务词条数
    f13 = 0 #简历中常出现词条的数目
    f14 = 0 #是否包含民族词条
    f15 = 0 #是否含有‘简历’或‘简历’的同义词

    
    for word in organization_list:
        if word in data.replace(' ','').decode(file_charset,'ignore').encode('utf-8'):
            f9 += 1
        
    for word in direction_list:
        if word in data.replace(' ','').decode(file_charset,'ignore').encode('utf-8'):
            f10 += 1
            
    for word in title_list:
        if word in data.replace(' ','').decode(file_charset,'ignore').encode('utf-8'):
            f11 += 1
    
    for word in position_list:
        if word in data.replace(' ','').decode(file_charset,'ignore').encode('utf-8'):
            f12 += 1
            
    for word in commonword_list:
        if word in data.replace(' ','').decode(file_charset,'ignore').encode('utf-8'):
            f13 += 1
    
    for word in minzu_list:
        if word in data.replace(' ','').decode(file_charset,'ignore').encode('utf-8'):
            f14 += 1
    
    for word in resumeword_list:
        if word in data.replace(' ','').decode(file_charset,'ignore').encode('utf-8'):
            f15 += 1
    
    
            
    for line in open(file_path):
        line_encode = line.replace('\n','').replace(' ','').decode(file_charset,'ignore').encode('utf-8')
        line_len = len(line_encode)
        f1 += line_len
        #匹配邮箱    
        match_mail_edu =  p_mail_edu.findall(line_encode)
        match_mail_ieee = p_mail_ieee.findall(line_encode)
        match_mail_base = p_mail_base.findall(line_encode)
        
        if match_mail_edu:
            for i in match_mail_edu:
                f2 += 1
        if match_mail_ieee: 
            for i in match_mail_ieee:
                f2 += 1
        if match_mail_base:
            for i in match_mail_base:
                f2 += 1
        #匹配电话号
        match_phone1 = p_phone1.findall(line_encode)
        match_phone2 = p_phone2.findall(line_encode)
        match_phone3 = p_phone3.findall(line_encode)
        match_phone4 = p_phone4.findall(line_encode)
        match_phone5 = p_phone5.findall(line_encode)
        match_phone6 = p_phone6.findall(line_encode)
        match_phone7 = p_phone7.findall(line_encode)
        
        if match_phone1:
            for i in match_phone1:
                f3 += 1
        if match_phone2:
            for i in match_phone2:
                f3 += 1
        if match_phone3:
            for i in match_phone3:
                f3 += 1
        if match_phone4:
            for i in match_phone4:
                f3 += 1
        if match_phone5:
            for i in match_phone5:
                f3 += 1
        if match_phone6:
            for i in match_phone6:
                f3 += 1
        if match_phone7:
            for i in match_phone7:
                f3 += 1
        #匹配个人主页、实验室网站等
        match_url = p_url.findall(line_encode)
        if match_url:
            for i in match_url:
                f4 += 1
        #匹配专利号
        match_zl = p_zl.findall(line_encode)
        match_zl2 = p_zl2.findall(line_encode)
        match_zl3 = p_zl3.findall(line_encode)
        if match_zl:
            for i in match_zl:
                f5 += 1
        if match_zl2:
            for i in match_zl2:
                f5 += 1
        if match_zl3:
            for i in match_zl3:
                f5 += 1
        #匹配论文、专著
        match_label = p_label.findall(line_encode)
        match_isbn= p_isbn.findall(line_encode)
        match_issn= p_issn.findall(line_encode)
        match_page1 = p_page1.findall(line_encode)
        match_page2 = p_page2.findall(line_encode)
        match_page3 = p_page3.findall(line_encode)
        match_page4 = p_page4.findall(line_encode)
        match_page5 = p_page5.findall(line_encode)
        
        if match_label:
            for i in match_label:
                f6 += 1
        if match_isbn:
            for i in match_isbn:
                f6 += 1
        if match_issn:
            for i in match_issn:
                f6 += 1
        if match_page1:
            for i in match_page1:
                f6 += 1
        if match_page2:
            for i in match_page2:
                f6 += 1
        if match_page3:
            for i in match_page3:
                f6 += 1
        if match_page4:
            for i in match_page4:
                f6 += 1
        if match_page5:
            for i in match_page5:
                f6 += 1
                
        match_book = p_book.findall(line_encode)
        if match_book:
            for n in match_book:
                f7 += 1
        
        #匹配年份词
        match_year1 = p_year1.findall(line_encode)
        match_year2 = p_year2.findall(line_encode)
        if match_year1:
            for i in match_year1:
                f8 += 1
        if match_year2:
            for i in match_year2:
                f8 += 1
            
    return f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15

def GetFileList(dir, fileList):#遍历文件夹下所有文件
    newDir = dir
    if os.path.isfile(dir):
        fileList.append(dir.decode('gbk'))
    elif os.path.isdir(dir):  
        for s in os.listdir(dir):
            #如果需要忽略某些文件夹，使用以下代码
            #if s == "xxx":
                #continue
            newDir=os.path.join(dir,s)
            GetFileList(newDir, fileList)  
    return fileList

#处理预测集
filefolder = '.\\webtext' #从网上抓取的文本文档
#filefolder = 'C:\\Users\\Vio\\Desktop\\project\\0109corpus\\test_corpus_folder\\test4'
outfile = open('./test/test.txt','w') #抽取特征后的libsvm格式预测集
dict_outfile = open('./test/filedict.txt','w') #记录libsvm文本中，行数与txt文件名的对应关系

filter_list = [] #过滤词条列表
for word in open('./wordlist/filter_words.txt'):
    filter_list.append(word.strip('\n'))
    
count = 0 #libsvm格式数据中行数
list_predict = GetFileList(filefolder, [])    
for file_path in list_predict:    
    f = open(file_path)
    data = f.read()
    label = 0 #若label值为0，指不含过滤词； 若值为1，指包含过滤词
    file_charset = chardet.detect(data)['encoding'] 
    if file_charset == None:
        file_charset = 'utf8'
    
    for word in filter_list:
        if word in data.replace(' ','').decode(file_charset,'ignore').encode('utf-8'):
            print word
            label = 1
            break
    
    if label==1: 
        print file_path
        continue
    else: 
        print file_path
        f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15 = classify_single(file_path,data,file_charset)
        count += 1     
        dict_outfile.write(str(count))
        dict_outfile.write(',')
        dict_outfile.write(file_path)
        dict_outfile.write('\n')
        outfile.write('0 1:%s 2:%s 3:%s 4:%s 5:%s 6:%s 7:%s 8:%s 9:%s 10:%s 11:%s 12:%s 13:%s 14:%s 15:%s'%(f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15))
        outfile.write('\n')

dict_outfile.close()
outfile.close()
os.rename('./test/filedict.txt','./test/filedict_finish.txt') #dict_outfile
os.rename('./test/test.txt','./test/test_finish.txt') #outfile



    
    