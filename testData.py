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

import svm
from random import randrange
import userGui
import RevuserConnect as userConnect
import userGui
from PyQt5.QtWidgets import QApplication,QTableWidgetItem,QFileDialog,QMainWindow,QWidget
from PyQt5.QtGui import *
from collections import OrderedDict, UserList


class primary() :
    def __init__(self,win=None,connect=None):
    #isi untuk menjalankan program utama
        self.headers = ['id', 'danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'valence',
                   'tempo', 'label']
        self.listAlbum=list()#list untuk simpan album
        self.listPositive=list() # list lagu yang akan diberi label positif
        self.mypath=""
        self.b = float()
        self.alphas = list()
        self.training = list()
        self.csvFiles = ""
        self.win=win
        self.connect=connect

        self.win.b1.clicked.connect(lambda: self.paste_token())
        self.win.b_getData.clicked.connect(lambda: self.get_dataset())
        self.win.bFiles.clicked.connect(lambda: win.openFileNameDialog())
        self.win.b_train.clicked.connect(lambda: self.start_svm(win.filename))
        self.win.bRecomm.clicked.connect(lambda: self.recommend())
        print(win.kernelType.currentText())
        win.bFiles.clicked.connect(lambda: win.openFileNameDialog())

    def paste_token(self) :
        self.win.labelbox.clear()
        self.win.labelbox.setText(QApplication.clipboard().text())

    def create_csv(self,filename,mypath) :
        #initilaize folder

        if not os.path.exists(mypath):
            os.makedirs(mypath)
        # initialize header
        if not os.path.isfile(str(mypath+filename)) :
            spamwriter = csv.DictWriter(open(mypath +"/"+filename, "w"), fieldnames=self.headers, lineterminator='\n')
            spamwriter.writeheader()

    def write_to_csv(self,jsonfile,targetcsv,label=None) :

        f=json.loads(jsonfile)
        print(f)
        f=f['audio_features']
        print(targetcsv)
        spamwriter=csv.DictWriter(open(targetcsv,"a"),fieldnames=self.headers,lineterminator="\n")
        for i in f :
            if (i != None and label!=None) :
                spamwriter.writerow({'id': i['id'], 'danceability': i['danceability'], 'energy': i['energy'],
                                     'loudness': i['loudness'], 'speechiness': i['speechiness'],
                                     'acousticness': i['acousticness'],
                                     'instrumentalness': i['instrumentalness'], 'valence': i['valence'],
                                     'tempo': i['tempo'],'label': label })
            else :
                spamwriter.writerow({'id': i['id'], 'danceability': i['danceability'], 'energy': i['energy'],
                                     'loudness': i['loudness'], 'speechiness': i['speechiness'],
                                     'acousticness': i['acousticness'],
                                     'instrumentalness': i['instrumentalness'], 'valence': i['valence'],
                                     'tempo': i['tempo']})

    def get_audio_features(self,theList,mypath,label=None) : #mendapatkan audio features dari list
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
            temp_json=connect.get_several_audio_features(self.__list_to_str(newarray))
            if(label!=None) :
                self.write_to_csv(temp_json,str(mypath),label)
            else:
                self.write_to_csv(temp_json, str(mypath), label)

    def __list_to_str(self,list) :
        abc=""
        size=len(list)
        count=1
        for i in list :
            abc=abc+i
            if count<size :
                abc=abc+','
            count = count + 1
        return abc

    def start_svm(self,file) :
        csvReader=csv.DictReader(open(file))
        countRow=0
        csvList=list()
        for row in csvReader :
            countRow +=1
            csvList.append(row)
        print("countrow=",countRow)
        if(countRow>500) : #make limit to 500
            countRow=500
        batas=countRow*0.7
        batas = int(batas)
        training=list() #untuk training
        testing=list() #untuk yang diuji
        count=0
        while (len(training)+len(testing) != countRow ) and count<=countRow :
            temp = random.randint(-1, len(csvList) - 1)
            if(count < batas) :
                training.append(csvList[temp])
                csvList.pop(temp)
            else :
                testing.append(csvList[temp])
                csvList.pop(temp)
            count=count+1

        print("training=",len(training))
        print("testing=",len(testing))
        b,alphas= self.svm_process(training)

        #win.addAlphasItem(alphas)
        #win.label_alphas.setText("alphas size :"+str(len(alphas)))
        #win.label_bias.setText("Bias :"+str(b.item()))
        with open("resultSVM.txt", "wb") as fp:
            pickle.dump((alphas, b,training), fp)

        eval(alphas,b,testing,training)
        return b,alphas,training
        # recommend_time(alphas,b,recommendations,training)

    def _dictToList(self,theDict) :
        listTemp=list()
        for i in theDict:
            lista = list()
            for key in i:
                if key != 'id':
                    lista.append(i[key])
            listTemp.append(lista)
        return listTemp

    def eval(self,alphas,b,datas,training) :

        dataTrain,labelTrain = self.loadData(training)
        dataTrain = svm.normalize(dataTrain,win.normType.currentText())
        dataEval, labelEval = self.loadData(datas)
        dataEval = svm.normalize(dataEval,win.normType.currentText())
        dataTrain=mat(self._dictToList(dataTrain))
        dataEval=mat(self._dictToList(dataEval))
        #dataEval = mat(dataEval)
        m, n = shape(dataEval)
        labelTrain = mat(labelTrain).transpose()
        panjang = list() #simpan data buat f-score
        errorCount = 0
        for i in range (m) :
            kernelEval = svm.kernelTrans(dataTrain, dataEval[i, :], kTup={'type': win.kernelType.currentText(), 'gamma': win.paramGamma.value(),'degree': win.paramDegree.value()\
                                                                              ,'coef' :win.paramCoef.value()})
            predict = kernelEval.T * multiply(labelTrain, alphas) + b
            panjang.append(float(sign(predict)))
            #print("panjang=",predict)
            if sign(predict) != sign(labelEval[i]): errorCount += 1

        print("the error rate is: %f" % (float(+errorCount) / m))
        print("labelArr", labelEval)
        print("panjang", panjang)
        f1_positive = f1_score(labelEval, panjang,pos_label=1)
        f1_negative = f1_score(labelEval, panjang, pos_label=-1)
        print("the f1_score is :", (f1_positive + f1_negative) / 2)
        win.label_fscore.setText("f-score :"+str((f1_positive + f1_negative) / 2))



    def get_song_name(self,result) :
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

    def loadData(self,thelist) :
        dataMat = list()
        labelMat = list()
        labels=self.checked()
        print("loaddata")
        for i in thelist :
            dataMat.append({y : float(i[y]) for y in labels})
            if('label' in i) :
                labelMat.append(float(i['label']))
            else:
                labelMat.append(i['id'])
        return dataMat,labelMat



    def svm_process(self,theList) :
        # SVM process
        np.set_printoptions(threshold=np.NaN)
        datas, labels = self.loadData(theList) #dalam datas yang berbentuk list ada dict
        print("sebelum normalisasi")
        #win.textbox.insertPlainText("sebelum normalisasi")
        #win.add_table_data(datas)
        #desktop2.add_text(desktop.window,"jancokqq")
        datas = svm.normalize(datas,win.normType.currentText())
        print("setelah normalisasi")
        #win.add_table_data2(datas)
        list_temp=list()
        for i in datas:
            sublist=list()
            for key in i :
                sublist.append(i[key])
            list_temp.append(sublist)
        datas=mat(list_temp)
        m, n = shape(datas)
        kernel= mat(zeros((m,m)))
        print("size=",m)
        for i in range(m) :
            kernel[:,i] = svm.kernelTrans(datas, datas[i, :],kTup={'type': win.kernelType.currentText(), 'gamma': win.paramGamma.value(),'degree': win.paramDegree.value()\
                                                                              ,'coef' :win.paramCoef.value()})
            #print("kernel=",kernel)
        b, alphas = svm.smoSimple(kernel, labels, win.paramC.value(), win.paramTolerance.value(), win.paramIterate.value())
        # print('alphas')
        # print(alphas)
        # print('b')
        # print(b)
        return b, alphas

    def recommend(self) :
        with open("resultSVM.txt", "rb") as fp:
            alphas, b, training = pickle.load(fp)
        connect.set_headers(win.labelbox.text())
        song=list()
        with open("listPositive.txt", "rb") as fp:
            listPositive= pickle.load(fp)
        print("listPositive=",listPositive)
        listPositiveNew = list()
        if len(listPositive)>200 : #biar tidak tlalu banyak request]
            listPositive=self.random_del(listPositive,200)
        print("listnew=", len(listPositive))

        if connect.get_display_name() != None:
            mypath = str(connect.get_display_name())
        else:
            mypath = str(connect.get_current_user())
        for i in listPositive :
            tempJson=connect.recommendation_based_seeds(i)
            for j in tempJson['tracks'] :
                song.append(j['id'])
        if not os.path.exists(mypath+"/recommendations.csv"):
            print("cari rekomendasi")
            headers = ['id', 'danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'valence',
                   'tempo']
            self.create_csv("recommendations.csv",mypath,headers)
            mypath = mypath+"/recommendations.csv"
            print(mypath)
            self.get_audio_features(song,mypath) #skaligus write to csv
        else :
            mypath = mypath + "/recommendations.csv"
        recomTrain, labelTrain = self.loadData(training)
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
        dataReco, id_lagu = self.loadData(RecoCSV)  # simpan id lagu bukan label
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

        print('udah mo abis bgst')
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
        recom_song = self.__list_to_str(listRecomm)
        print(recom_song)
        result = connect.get_several_tracks(recom_song)
        self.get_song_name(result)

    def random_del(self,list_song,limit) :
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

    @property
    def get_user_playlist(self):
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
                    self.listPositive.append(j['track']['id'])
                    self.listAlbum.append(j['track']['album']['id'])
                    while (temp_data['total']-(offset+50)>0) :
                        offset=offset+50
                        print('masuk while euy')
                        temp_data = json.loads(connect.get_tracks_from_playlist(username, i, offset))
                        for k in temp_data['items'] :
                            self.listPositive.append(k['track']['id'])
                            self.listPositive.append(k['track']['id'])
                            self.listAlbum.append(k['track']['album']['id'])
                            print("bereseuy")
                        print("listalbum=",self.listAlbum)
            has_playlist=True
            return has_playlist

        except ValueError :
            print("tidak ada playlist")
            has_playlist=False
            return has_playlist


    def find_negative(self,mypath):
        list_tracks=list() #list track yg didapat dr album
        list_album = list(set(self.listAlbum))
        for i in list_album :
            temp_json=connect.get_tracks_from_album(str(i))
            temp_json=json.loads((temp_json))
            for j in temp_json['items'] :
                list_tracks.append(j['id'])
        list_negative=list(set(list_tracks)-set(self.listPositive))
        if(len(list_negative)>len(self.listPositive)) :
            while len(list_negative)>len(self.listPositive) :
                temp = random.random_integers(0, len(list_negative) - 1)
                list_negative.pop(temp)
                self.get_audio_features(list_negative,mypath+"/main.csv",label=-1)

    def get_saved_tracks(self) :
        offset = 0
        test = connect.get_saved_tracks(offset)
        x = json.loads(test)
        try :
            for i in x['items']:
                self.listPositive.append(i['track']['id'])
            while (x['total'] - (offset + 50) > 0):
                offset = offset + 50
                test = connect.get_saved_tracks(offset)
                x = json.loads(test)
                print("offset=",offset)
                for i in x['items']:
                    if i['track']['id'] not in self.listPositive :
                        self.listPositive.append(i['track']['id'])
                        self.listAlbum.append(i['track']['album']['id'])
            print("punya saved tracks")
        except ValueError :
            print("tidak ada saved tracks")



    def get_dataset(self) :
        self.connect.set_headers(win.labelbox.text())
        # connect.set_headers(
        #     "BQClTU4pL-DshgSs9S394waLTIWbjS0ljgN3ziES-ZJtcyYM5pe2j29JZYabjwg07dMZ2eypfjPCWu9w4mCg8OyFqVx64v7a1gV2N-7HVZr6OIOd1PCZPjWCnttdrAqk7b_I24DQgcbKBuJi9A76qE-JLl0GL5xdGOK27TFbLAGzU0jDTQ1OWIX0SAsBlV41BBmgzCBlhha2knLGOpmMR4Yeray_w6q4OIKuzUvr1DliJqciDRBznHUADGlbGpgj3B-gP0MTZOvlXS2cBEDIPio")
        if connect.get_display_name()!= None :
            mypath = str(connect.get_display_name())
        else :
            mypath = str(connect.get_current_user())
        print("mypath=", mypath)
        self.create_csv("main.csv", mypath,self.headers)
        print("hai")
        has_playlist = self.get_user_playlist()  # get from playlist
        has_saved_track = self.get_saved_tracks()  # mendapatkan lagu dari lagu yang di like user
        print("has_playlist=", has_playlist)
        print(self.listPositive)
        with open("listPositive.txt", "wb") as fp:
            pickle.dump((self.listPositive), fp)
        self.get_audio_features(self.listPositive,mypath+"/main.csv",label=1)
        self.find_negative(mypath)
        print("sudah beres")




    def checked(self) :
        checked_list=list()
        if(self.win.ckboxDanceability.isChecked()) :
            checked_list.append('danceability')
        if (self.win.ckboxAcousticness.isChecked()):
            checked_list.append('acousticness')
        if (self.win.ckboxEnergy.isChecked()):
            checked_list.append('energy')
        if (self.win.ckboxInstrumentalness.isChecked()):
            checked_list.append('instrumentalness')
        if (self.win.ckboxLoudness.isChecked()):
            checked_list.append('loudness')
        if (self.win.ckboxSpeechiness.isChecked()):
            checked_list.append('speechiness')
        if (self.win.ckboxTempo.isChecked()):
            checked_list.append('tempo')
        if (self.win.ckboxValence.isChecked()):
            checked_list.append('valence')
        return checked_list


    #win.b1.clicked.connect(lambda: recommend())

    #recommend()


    #bagian rekomendasi


    """yang diatas yang dipakai nanti"""