# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 17:22:40 2017

@author: Vio
"""
from sklearn import metrics
from sklearn.datasets import load_svmlight_file
from sklearn.svm import SVC 
'''
def dependencies_for_myprogram():
    from scipy.sparse.csgraph import _validation
'''
#svm
def svm(X_train,y_train,X_test,y_test):
    outfile = open('./result/result.txt','w')
    
    model = SVC(C=0.0001,kernel='linear')
    model.fit(X_train, y_train)
    print(model)
    # make predictions
    #expected = y_test
    predicted = model.predict(X_test)    
    count = 0    
    for i in predicted:
        count += 1
        if i==1:
            #print count
            print d.get(str(count))
            outfile.write(d.get(str(count)))
            outfile.write('\n')
    outfile.close()
       
#载入libsvm格式数据中行数与文档名的对应字典
f = open('./test/filedict_finish.txt')
d={} 
for line in f: 
    (a,b)=line.strip().split(',') 
    d[a]=b  
f.close()
    
#libsvm格式数据的导入
#X_train特征值，y_train训练集标注
X_train, y_train = load_svmlight_file("./train/train.txt")
X_train.todense()#将稀疏矩阵转化为完整特征矩阵
#X_test特征值，y_test测试集标注
X_test,y_test = load_svmlight_file("./test/test_finish.txt")
X_test.todense()

#c = input("please input the value of parameter c(such as 0.0001):" + '\n')
svm(X_train, y_train,X_test,y_test)