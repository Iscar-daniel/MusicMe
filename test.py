import svm
import csv
from numpy import *

def loadData(thelist) :
    dataMat = list()
    labelMat = list()
    labels=checked() #audio features yang dipilih
    for i in thelist :
        dataMat.append({y : float(i[y]) for y in labels})
        if('label' in i) :
            labelMat.append(float(i['label']))
        else:
            labelMat.append(i['id']) #BUAT REKOMENDASI
    return dataMat,labelMat

def checked() :
    checked_list=list()
    checked_list.append('danceability')
    checked_list.append('acousticness')
    checked_list.append('energy')
    checked_list.append('instrumentalness')
    checked_list.append('speechiness')
    checked_list.append('valence')
    return checked_list



file="C:\\Users\\Daniel\\PycharmProjects\\Spotiwew\\Sandro Yusuf Sihaloho\\main.csv"
csvReader=csv.DictReader(open(file))
thelist=list()
for i in csvReader :
    thelist.append(i)
datas, labels = loadData(thelist) #dalam datas yang berbentuk list ada dict. disini memisahkan data dan label
#print(thelist)
list_temp=list()
for i in datas:
    sublist = list()
    for key in i:
        sublist.append(i[key])  # get value of the key
    list_temp.append(sublist)  # add to list
datas = mat(list_temp)
m, n = shape(datas)
kernel = mat(zeros((m, m)))
print("size=", m)
for i in range(m):
    kernel[:, i] = svm.kernelTrans(datas, datas[i, :],kTup={'type': "laplacian", 'gamma': 0.5})
    # print("kernel=",kernel)
b, alphas = svm.smoSimple(kernel, labels,C=10, toler=0.1, maxIter=2)
print(b)
print(alphas)





