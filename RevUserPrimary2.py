import sys
import pickle
from _ast import Nonlocal
from numpy import *
from sklearn.metrics import f1_score,precision_recall_fscore_support
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import os
import csv
import json
from operator import itemgetter

import svmBackup as svm
from random import randrange
import userGui
import RevuserConnect as userConnect
from PyQt5.QtWidgets import QApplication,QTableWidgetItem,QFileDialog
from collections import OrderedDict, UserList



#isi untuk menjalankan fprogram utama
headers = ['id', 'danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'valence',
               'tempo', 'label']
listAlbum=list()#list untuk simpan album
listPositive=list() # list lagu yang akan diberi label positif
mypath=""

def paste_token(win) :
    win.labelbox.clear()
    win.labelbox.setText(QApplication.clipboard().text())

def create_csv(filename,mypath,headers) :
    #initilaize folder

    if not os.path.exists(mypath):
        os.makedirs(mypath)
    # initialize header
    if not os.path.isfile(str(mypath+filename)) :
        spamwriter = csv.DictWriter(open(mypath +"/"+filename, "w"), fieldnames=headers, lineterminator='\n')
        spamwriter.writeheader()

def write_to_csv(jsonfile,targetcsv,label=None) :

    f=json.loads(jsonfile)
    print(f)
    f=f['audio_features']
    print(targetcsv)
    spamwriter=csv.DictWriter(open(targetcsv,"a"),fieldnames=headers,lineterminator="\n")
    for i in f :
        if (i != None and label!=None) :
            spamwriter.writerow({'id': i['id'], 'danceability': i['danceability'], 'energy': i['energy'],
                                 'loudness': i['loudness'], 'speechiness': i['speechiness'],
                                 'acousticness': i['acousticness'],
                                 'instrumentalness': i['instrumentalness'], 'valence': i['valence'],
                                 'tempo': i['tempo'],'label': label })
        else :
            try:
             spamwriter.writerow({'id': i['id'], 'danceability': i['danceability'], 'energy': i['energy'],
                                 'loudness': i['loudness'], 'speechiness': i['speechiness'],
                                 'acousticness': i['acousticness'],
                                 'instrumentalness': i['instrumentalness'], 'valence': i['valence'],
                                 'tempo': i['tempo']})
            except Exception as e:
                continue
            
            

def get_audio_features(theList,mypath,label=None) : #mendapatkan audio features dari list
    offset = 0
    total = len(theList)
    newarray = list()
    while total > 0:
        newarray.clear()
        for i in range(100):
            newarray.append(theList[offset])
            total = total - 1
            offset = offset + 1

            if (total == 0):
                break
        temp_json=connect.get_several_audio_features(__list_to_str(newarray))
        if(label!=None) :
            write_to_csv(temp_json,str(mypath),label)
        else:
            write_to_csv(temp_json, str(mypath), label)

def __list_to_str(list) :
    print("===the list=====")
    print(list)
    abc=""
    size=len(list)
    count=1
    for i in list :
        if(i!=None) :
            abc=abc+i
            if count<size :
             abc=abc+','
            count = count + 1
        
        
    return abc

def start_svm(file) :
    csvReader=csv.DictReader(open(file))
    countRow=0
    csvList=list()
    for row in csvReader : #menentukan jumlah row dalam file CSV
        countRow +=1
        csvList.append(row) #gambar 4.2 menjadi gambar 4.3
    print("countrow=",countRow)
    if(countRow>500) : #make limit to 500
        countRow=500
    batas=countRow*0.7
    batas = int(batas)
    training=list() #untuk training
    testing=list() #untuk yang diuji
    count=0
    while (len(training)+len(testing) != countRow ) and count<=countRow : 
        temp = random.randint(-1, len(csvList) - 1) #random int
        if(count < batas) : 
            training.append(csvList[temp]) #list untuk data train ditambah
            csvList.pop(temp) #list yang sudah dikirim ke list training dihilangkan dari csvList
        else :
            testing.append(csvList[temp]) #Untuk data testing
            csvList.pop(temp)
        count=count+1

    print("training=",len(training))
    print("testing=",len(testing))
    #"""we give 3 svm process to get the best f-measure"""
    mypath=win.path
    with open(mypath+"/traintest.txt", "wb") as fp:
        pickle.dump((training,testing), fp)


def _dictToList(theDict) :
    listTemp=list()
    for i in theDict:
        lista = list()
        for key in i:
            if key != 'id':
                lista.append(i[key])
        listTemp.append(lista)
    return listTemp

def eval(alphas,b,datas,training) :

    dataTrain,labelTrain = loadData(training)
    dataTrain = svm.normalize(dataTrain,win.normType.currentText())
    dataEval, labelEval = loadData(datas)
    dataEval = svm.normalize(dataEval,win.normType.currentText())
    dataTrain=mat(_dictToList(dataTrain))
    dataEval=mat(_dictToList(dataEval))
    #dataEval = mat(dataEval)
    m, n = shape(dataEval)
    labelTrain = mat(labelTrain).transpose()
    panjang = list() #simpan data buat f-score
    errorCount = 0
    for i in range (m) :
        kernelEval = svm.kernelTrans(dataTrain, dataEval[i, :], kTup={'type': win.kernelType.currentText(), 'gamma': win.paramGamma.value(),'degree': win.paramDegree.value()\
                                                                          ,'coef' :win.paramCoef.value()})
        predict = kernelEval.T * multiply(labelTrain, alphas) + b
        panjang.append(float(sign(predict))) #menampung hasil data eval yang sudah diberi label positif/negatif
        #print("panjang=",predict)
        if sign(predict) != sign(labelEval[i]): errorCount += 1

    #print("the error rate is: %f" % (float(+errorCount) / m))
    print("labelArr", labelEval)
    print("panjang", panjang)
    f1_positive = f1_score(labelEval, panjang,pos_label=1)
    f1_negative = f1_score(labelEval, panjang, pos_label=-1)
    print("the f1_score is :", (f1_positive + f1_negative) / 2)
    win.label_fscore.setText("f-score :"+str((f1_positive + f1_negative) / 2))
#    return ((f1_positive + f1_negative) / 2)



def get_song_name(result) :
    json_str = json.loads(result)
    json_2=json_str['tracks']
    count=0
    uri = list()
    for i in json_2 :
        #        win.tableRecommend.setItem(i,0,i['artists']['name'])
        artist=i['album']['artists'][0]['name']#;artist=artist.encode("UTF-8")
        judul_lagu=i['name']#;judul_lagu=judul_lagu.encode("UTF-8")
        album=i['album']['name']#;album=album.encode("UTF-8")
        print("artist="+artist+" judul lagu=",judul_lagu+" album="+album)
        #win.tableRecommend.setItem(count, 0, QTableWidgetItem(str(artist)))
        #win.tableRecommend.setItem(count, 1, QTableWidgetItem(str(judul_lagu)))
        #win.tableRecommend.setItem(count, 2, QTableWidgetItem(str(album)))
        uri.append(i['uri'])
        count = count +1
    playlist_id=connect.create_playlist() #yg ini buat bikin playlist
    connect.add_track_to_playlist(playlist_id,(uri))
    print("udah jadi")
    #print i['album']['artists'][0]['name']
    #print i['album']

    #print list_id
    # text=__list_to_str(list_id)
    # print text

def loadData(thelist) :
    dataMat = list()
    labelMat = list()
    labels=checked() #audio features yang dipilih
    print("loaddata")
    for i in thelist :
        dataMat.append({y : float(i[y]) for y in labels})
        if('label' in i) :
            labelMat.append(float(i['label']))
        else:
            labelMat.append(i['id']) #BUAT REKOMENDASI
    return dataMat,labelMat



def svm_process() :
    mypath=win.path
    if findFile("traintest.txt",mypath) :
            print("ada")
            with open(mypath+"/traintest.txt", "rb") as fp:
                training,testing=pickle.load(fp)
            theList=training
            # SVM process
            np.set_printoptions(threshold=np.NaN)
            datas, labels = loadData(
                theList)  # dalam datas yang berbentuk list ada dict. disini memisahkan data dan label
            print("sebelum normalisasi")
            # win.textbox.insertPlainText("sebelum normalisasi")
            # win.add_table_data(datas)
            datas = svm.normalize(datas, win.normType.currentText())
            print("setelah normalisasi")
            # win.add_table_data2(datas)
            list_temp = list()
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
                kernel[:, i] = svm.kernelTrans(datas, datas[i, :], kTup={'type': win.kernelType.currentText(),
                                                                         'gamma': win.paramGamma.value()})
                # print("kernel=",kernel)
            b, alphas = svm.smoSimple(kernel, labels, win.paramC.value(), win.paramTolerance.value(),
                                      win.paramIterate.value())
            eval(alphas, b, testing, training)
            # print('alphas')
            # print(alphas)
            # print('b')
            # print(b)
            return b, alphas
    else :
        start_svm(win.filename)


def recommend() :
    with open("resultSVM.txt", "rb") as fp:
        alphas, b, training = pickle.load(fp)
    connect.set_headers(win.labelbox.text())
    song=list()
    with open("listPositive.txt", "rb") as fp:
        listPositive= pickle.load(fp)
    print("listPositive=",listPositive)
    listPositiveNew = list()
    if len(listPositive)>200 : #biar tidak tlalu banyak request]
        listPositive=random_del(listPositive,200)
    print("listnew=", len(listPositive))

    if connect.get_display_name() != None:
        mypath = str(connect.get_display_name())
    else:
        mypath = str(connect.get_current_user())
    for i in listPositive :
        if(i!=None) :
            tempJson=connect.recommendation_based_seeds(i)
            for j in tempJson['tracks'] :
                song.append(j['id'])
    if not os.path.exists(mypath+"/recommendations.csv"):
        print("cari rekomendasi")
        headers = ['id', 'danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'valence',
               'tempo']
        create_csv("recommendations.csv",mypath,headers)
        mypath = mypath+"/recommendations.csv"
        print(mypath)
        get_audio_features(song,mypath) #skaligus write to csv
    else :
        mypath = mypath + "/recommendations.csv"
    recomTrain, labelTrain = loadData(training)
    # win.add_table_data(dataTrain)
    recomTrain = svm.normalize(recomTrain, win.normType.currentText())
    templist=list()
    for i in recomTrain :
        sublist=list()
        for key in i :
            sublist.append(i[key])
        templist.append(sublist)
    recomTrain=templist
    print("dataTrain=", shape(mat(recomTrain)))
    print(recomTrain)
    # win.add_table_data2(dataTrain)
    # win.addAlphasItem(alphas)
    # win.label_alphas.setText("alphas size :" + str(len(alphas)))
    # win.label_bias.setText("Bias :"+str(b))

    csvReader = csv.DictReader(open(mypath))
    RecoCSV=list()
    print(csvReader)
    for i in csvReader :
        RecoCSV.append(i)
    dataReco, id_lagu = loadData(RecoCSV)  # simpan id lagu bukan label
    print("datareco=",dataReco)
    dataReco = svm.normalize(dataReco, win.normType.currentText())
    print("datareconorm=", dataReco)
    templist2=list()
    for j in dataReco :
        sublist2=list()
        for key2 in j :
            sublist2.append(j[key2])
        #print("sublist2=",sublist2)
        templist2.append(sublist2)
    dataReco=templist2
    print(dataReco)
    recomTrain = mat(recomTrain)
    print(recomTrain)
    #win.add_table_dataRecom(dataReco)
    dataReco = mat(dataReco)
    m, n = shape(dataReco)
    labelTrain = mat(labelTrain).transpose()

    print(id_lagu)
    listPredict=list()
    print("komall", shape(recomTrain))
    print(shape(dataReco))
    print(shape(labelTrain))
    print(shape(alphas))
    print("datareco=",dataReco)
    print("dataTrain=", recomTrain)

    for i in range(m):
        if (id_lagu[i] in listPredict)==False:
            kernelEval = svm.kernelTrans(recomTrain, dataReco[i, :],
                                         kTup={'type': win.kernelType.currentText(), 'gamma': win.paramGamma.value(),
                                               'degree': win.paramDegree.value(), 'coef': win.paramCoef.value()})

            predict = kernelEval.T * multiply(labelTrain, alphas) + b
            temp = {'id' : id_lagu[i],"value":predict }
            if temp not in listPredict :
                listPredict.append(temp)
    print("list predict=",listPredict)
    print("list predict=", type(listPredict))
    seen=set()
    newListPredict=list()
    # for d in list(listPredict) : #in here we delete the dict with same
    #     t=tuple(d.items())
    #     if t not in seen :
    #         seen.add(t)
    #         newListPredict.append(t)
    # listPredict=newListPredict
    listPredict.sort(key=itemgetter('value'),reverse=True)
    print("listPredict=",listPredict)
    # listRecomm = list()
    # count=0
    # while len(listRecomm) < 10:
    #     temp_l.append(listPredict[count])
    #     count+=1
    listTemp=listPredict[:10]
    listRecomm=list()
    for i in listTemp :
        listRecomm.append(i['id'])
    recom_song = __list_to_str(listRecomm)
    print(recom_song)
    result = connect.get_several_tracks(recom_song)
    get_song_name(result)

def random_del(list_song,limit) :
    while len(list_song) >limit :
        r= randrange(0,len(list_song))
        list_song.pop(r)
    return list_song

def isEmpty(file) :
    file = open(str(file), "r+").read()
    temp = json.loads(file)
    if(len(temp)==0) :
        return False
    else : return True

def findFile(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return True


def get_user_playlist():
    # mendapatkan track dari playlist yang dibuat oleh user
    json_data=connect.get_current_user_playlist()
    username=connect.get_current_user()
    try :
        pList = json.loads(json_data)
        listPlaylist = list()
        for i in pList['items']:
            if (i['owner']['id'] ==username):
                listPlaylist.append(i['id'])
                print("ada")
        print(listPlaylist)
        for i in listPlaylist :
            #get tracks from playlist
            offset = 0
            temp_data=json.loads(connect.get_tracks_from_playlist(username,i,offset))
            for j in temp_data['items'] :
                listPositive.append(j['track']['id'])
                listAlbum.append(j['track']['album']['id'])
                while (temp_data['total']-(offset+50)>0) :
                    offset=offset+50
                    print('masuk while euy')
                    temp_data = json.loads(connect.get_tracks_from_playlist(username, i, offset))
                    for k in temp_data['items'] :
                        listPositive.append(k['track']['id'])
                        listPositive.append(k['track']['id'])
                        listAlbum.append(k['track']['album']['id'])
                        print("bereseuy")
                    print("listalbum=",listAlbum)
        has_playlist=True
        return has_playlist

    except ValueError :
        print("tidak ada playlist")
        has_playlist=False
        return has_playlist


def find_negative(mypath):
    list_tracks=list() #list track yg didapat dr album
    list_album = list(set(listAlbum))
    for i in list_album :
        temp_json=connect.get_tracks_from_album(str(i))
        temp_json=json.loads((temp_json))
        print("====temp_json=====")
        print(temp_json)
        try:
            for j in temp_json['items'] :
                if(j['id']!=None) :
                    list_tracks.append(j['id'])
        except Exception as e:
            continue
        
    list_negative=list(set(list_tracks)-set(listPositive))
    if(len(list_negative)>len(listPositive)) :
        while len(list_negative)>len(listPositive) :
            temp = random.random_integers(0, len(list_negative) - 1)
            list_negative.pop(temp)
    get_audio_features(list_negative,mypath+"/main.csv",label=-1)

def get_saved_tracks() :
    offset = 0
    test = connect.get_saved_tracks(offset)
    x = json.loads(test)
    try :
        for i in x['items']:
            listPositive.append(i['track']['id'])
        while (x['total'] - (offset + 50) > 0):
            offset = offset + 50
            test = connect.get_saved_tracks(offset)
            x = json.loads(test)
            print("offset=",offset)
            for i in x['items']:
                if i['track']['id'] not in listPositive :
                    listPositive.append(i['track']['id'])
                    listAlbum.append(i['track']['album']['id'])
        print("punya saved tracks")
    except ValueError :
        print("tidak ada saved tracks")



def get_dataset() :
    connect.set_headers(win.labelbox.text())
    # connect.set_headers(
    #     "BQClTU4pL-DshgSs9S394waLTIWbjS0ljgN3ziES-ZJtcyYM5pe2j29JZYabjwg07dMZ2eypfjPCWu9w4mCg8OyFqVx64v7a1gV2N-7HVZr6OIOd1PCZPjWCnttdrAqk7b_I24DQgcbKBuJi9A76qE-JLl0GL5xdGOK27TFbLAGzU0jDTQ1OWIX0SAsBlV41BBmgzCBlhha2knLGOpmMR4Yeray_w6q4OIKuzUvr1DliJqciDRBznHUADGlbGpgj3B-gP0MTZOvlXS2cBEDIPio")
    if connect.get_display_name()!= None :
        mypath = str(connect.get_display_name())
    else :
        mypath = str(connect.get_current_user())
    print("mypath=", mypath)
    create_csv("main.csv", mypath,headers)
    print("hai")
    has_playlist = get_user_playlist()  # get from playlist
    has_saved_track = get_saved_tracks()  # mendapatkan lagu dari lagu yang di like user
    print("has_playlist=", has_playlist)
    print(listPositive)
    with open("listPositive.txt", "wb") as fp:
        pickle.dump((listPositive), fp)
    get_audio_features(listPositive,mypath+"/main.csv",label=1)
    find_negative(mypath)
    print("sudah beres")




def checked() :
    checked_list=list()
    if(win.ckboxDanceability.isChecked()) :
        checked_list.append('danceability')
    if (win.ckboxAcousticness.isChecked()):
        checked_list.append('acousticness')
    if (win.ckboxEnergy.isChecked()):
        checked_list.append('energy')
    if (win.ckboxInstrumentalness.isChecked()):
        checked_list.append('instrumentalness')
    if (win.ckboxLoudness.isChecked()):
        checked_list.append('loudness')
    if (win.ckboxSpeechiness.isChecked()):
        checked_list.append('speechiness')
    if (win.ckboxTempo.isChecked()):
        checked_list.append('tempo')
    if (win.ckboxValence.isChecked()):
        checked_list.append('valence')
    return checked_list



app = QApplication(sys.argv)
win = userGui.userWindow()
connect = userConnect.connect()
csvFiles=""
b=float()
alphas=list()
training=list()

print(shape(training))
#win.b1.clicked.connect(lambda: recommend())
win.b1.clicked.connect(lambda: paste_token(win))
win.b_getData.clicked.connect(lambda: get_dataset())
win.bFiles.clicked.connect(lambda: win.openFileNameDialog())
win.b_train.clicked.connect(lambda : svm_process())
win.b_split.clicked.connect(lambda : start_svm(win.filename))
win.bRecomm.clicked.connect(lambda : recommend())

# win.bFiles.clicked.connect(lambda  : win.openFileNameDialog())
#recommend()
sys.exit(app.exec_())

#bagian rekomendasi


"""yang diatas yang dipakai nanti"""
