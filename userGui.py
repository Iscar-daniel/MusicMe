import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui
import pathlib
import numpy as np
import os


class userWindow(QWidget):
   def __init__(self):
      #super(userWindow, self).__init__()
      #token = QLineEdit()

#      self.primarys.setWindow(self)

      self.tabs=QTabWidget()

      self.filename=" "
      self.path=" "
      self.lbelFilename = QLabel()
      self.initUI()
      super(userWindow,self).__init__()


   def abc(self):
      self.labelbox.setText(QApplication.clipboard().text())
   def addAlphasItem(self,alphas):
      for i in alphas:  # add items to QList
         self.alphas.addItem(str(i.item()))

   def add_text(self,text):
      self.textbox.insertPlainText(text)

   def add_table_dataRecom(self, array):  # setelah normalisasi
      array2=list()
      for i in array :
         array2.append(i)
      self.tableRecommendData.setRowCount(len(array2))
      self.tableRecommendData.setColumnCount(len(array2[0]))
      self.tableRecommendData.setHorizontalHeaderItem(0, QTableWidgetItem("Danceability"))
      self.tableRecommendData.setHorizontalHeaderItem(1, QTableWidgetItem("Energy"))
      self.tableRecommendData.setHorizontalHeaderItem(2, QTableWidgetItem("Loudness"))
      self.tableRecommendData.setHorizontalHeaderItem(3, QTableWidgetItem("Speechiness"))
      self.tableRecommendData.setHorizontalHeaderItem(4, QTableWidgetItem("Accousticness"))
      self.tableRecommendData.setHorizontalHeaderItem(5, QTableWidgetItem("Instrumentalness"))
      self.tableRecommendData.setHorizontalHeaderItem(6, QTableWidgetItem("Valence"))
      self.tableRecommendData.setHorizontalHeaderItem(7, QTableWidgetItem("Tempo"))

      for i, row in enumerate(array2):
         for j, val in enumerate(row):
            self.tableRecommendData.setItem(i, j, QTableWidgetItem(str(val)))

   def add_table_data2(self, array): #setelah normalisasi

      self.table2.setRowCount(len(array))
      self.table2.setColumnCount(len(array[0]))
      self.table2.setHorizontalHeaderItem(0, QTableWidgetItem("Danceability"))
      self.table2.setHorizontalHeaderItem(1, QTableWidgetItem("Energy"))
      self.table2.setHorizontalHeaderItem(2, QTableWidgetItem("Loudness"))
      self.table2.setHorizontalHeaderItem(3, QTableWidgetItem("Speechiness"))
      self.table2.setHorizontalHeaderItem(4, QTableWidgetItem("Accousticness"))
      self.table2.setHorizontalHeaderItem(5, QTableWidgetItem("Instrumentalness"))
      self.table2.setHorizontalHeaderItem(6, QTableWidgetItem("Valence"))
      self.table2.setHorizontalHeaderItem(7, QTableWidgetItem("Tempo"))

      for i, row in enumerate(array):
         for j, val in enumerate(row):
            self.table2.setItem(i, j, QTableWidgetItem(str(val)))



      for i, row in enumerate(array):
         for j, val in enumerate(row):
            self.table2.setItem(i, j, QTableWidgetItem(str(val)))

   def add_table_data(self,array): #buat table
      self.table.setRowCount(len(array))
      self.table.setColumnCount(len(array[0]))
      self.table.setHorizontalHeaderItem(0, QTableWidgetItem("Danceability"))
      self.table.setHorizontalHeaderItem(1, QTableWidgetItem("Energy"))
      self.table.setHorizontalHeaderItem(2, QTableWidgetItem("Loudness"))
      self.table.setHorizontalHeaderItem(3, QTableWidgetItem("Speechiness"))
      self.table.setHorizontalHeaderItem(4, QTableWidgetItem("Accousticness"))
      self.table.setHorizontalHeaderItem(5, QTableWidgetItem("Instrumentalness"))
      self.table.setHorizontalHeaderItem(6, QTableWidgetItem("Valence"))
      self.table.setHorizontalHeaderItem(7, QTableWidgetItem("Tempo"))
      self.table.setHorizontalHeaderItem(7, QTableWidgetItem("label"))

      for i, row in enumerate(array):
         for j, val in enumerate(row):
            self.table.setItem(i, j, QTableWidgetItem(str(val)))

   def openFileNameDialog(self):
      options = QFileDialog.Options()
      fileName, _ = QFileDialog.getOpenFileName(self, "Select FIle", "",
                                                "All Files (*);;csv Files (*.csv)", options=options)
      filepath=pathlib.Path(fileName)
      if fileName:
         print(fileName)

         self.filename=fileName
         self.path=os.path.dirname(fileName)
         print("path=",self.path)
         self.lbelFilename.setText(self.filename)
         self.tabs.setWindowTitle(str(filepath.parent))
      else :
         self.filename=fileName

   def initUI(self):
      self.ckboxDanceability=QCheckBox();self.ckboxDanceability.setText("danceability");self.ckboxDanceability.setChecked(True)
      self.ckboxEnergy=QCheckBox();self.ckboxEnergy.setText("energy");self.ckboxEnergy.setChecked(True)
      self.ckboxLoudness=QCheckBox();self.ckboxLoudness.setText("loudness");self.ckboxLoudness.setChecked(True)
      self.ckboxSpeechiness=QCheckBox();self.ckboxSpeechiness.setText("speechiness");self.ckboxSpeechiness.setChecked(True)
      self.ckboxAcousticness=QCheckBox();self.ckboxAcousticness.setText("accusticness");self.ckboxAcousticness.setChecked(True)
      self.ckboxInstrumentalness=QCheckBox();self.ckboxInstrumentalness.setText("instrumentalness");self.ckboxInstrumentalness.setChecked(True)
      self.ckboxValence=QCheckBox();self.ckboxValence.setText("valence");self.ckboxValence.setChecked(True)
      self.ckboxTempo=QCheckBox();self.ckboxTempo.setText("tempo");self.ckboxTempo.setChecked(True)
      self.slctFile=QFileDialog()

      self.kernelType=QComboBox();self.kernelType.addItems(['linear','RBF','laplacian']);self.kernelType.setCurrentText("laplacian")
      self.normType = QComboBox();self.normType.addItems(['minmax','mean'])

      self.myfont=QFont()
      self.myfont.setBold(True)

      self.labelParamC=QLabel();self.labelParamC.setText("C :");self.labelParamC.setAlignment(Qt.AlignTrailing);self.labelParamC.setFont(self.myfont)
      self.paramC=QDoubleSpinBox();self.paramC.setValue(10);self.paramC.setMinimum(0);self.paramC.setDecimals(7);self.paramC.setMaximum(1000)
      self.labelParamGamma=QLabel();self.labelParamGamma.setText("Gamma value (for RBF and Laplacian) :");self.labelParamGamma.setAlignment(Qt.AlignTrailing);self.labelParamGamma.setFont(self.myfont)
      self.paramGamma=QDoubleSpinBox();self.paramGamma.setValue(0.5);self.paramGamma.setMinimum(0);self.paramGamma.setDecimals(7)
      self.labelParamDegree = QLabel();self.labelParamDegree.setText("Degree value (for Polynomial) :");self.labelParamDegree.setAlignment(Qt.AlignTrailing);self.labelParamDegree.setFont(self.myfont)
      self.paramDegree = QSpinBox();self.paramDegree.setValue(2)
      self.labelParamCoef = QLabel();self.labelParamCoef.setText("Coef value (for Polynomial) :");self.labelParamCoef.setAlignment(Qt.AlignTrailing);self.labelParamCoef.setFont(self.myfont)
      self.paramCoef = QDoubleSpinBox();self.paramCoef.setValue(2);self.paramCoef.setMinimum(0);self.paramCoef.setDecimals(7)
      self.labelParamIterate=QLabel();self.labelParamIterate.setText("iterasi :");self.labelParamIterate.setAlignment(Qt.AlignTrailing);self.labelParamIterate.setFont(self.myfont)
      self.paramIterate=QSpinBox();self.paramIterate.setValue(2);self.paramIterate.setMaximum(100000)
      self.labelParamTolerance=QLabel();self.labelParamTolerance.setText("tolerance :");self.labelParamTolerance.setAlignment(Qt.AlignTrailing);self.labelParamTolerance.setFont(self.myfont)
      self.paramTolerance=QDoubleSpinBox();self.paramTolerance.setValue(0.1);self.paramTolerance.setMinimum(0);self.paramTolerance.setDecimals(7)


      self.dbleboxC=QLineEdit();self.dbleboxC.setText("2");lbelC=QLabel();lbelC.setText("C")
      self.dbleboxmaxIter=QLineEdit();self.dbleboxmaxIter.setText("5");lbelmaxIter=QLabel();lbelmaxIter.setText("Max Iteration")
      self.dbleboxToler=QLineEdit();self.dbleboxToler.setText("0.001");lbelToler=QLabel();lbelToler.setText("Tolerance")
      gbox3=QVBoxLayout()
      tab1=QWidget()
      tab2=QWidget()
      fbox = QGridLayout()
      gbox= QVBoxLayout()
      gbox2= QVBoxLayout()
      grid1=QGridLayout()
      #header=QTableWidgetItem("jancuk1","jancuk2","jancuk3")
      label_1 = QLabel()
      self.labelbox=QLineEdit()
      self.labelbox.setText("")
      label_training = QLabel()
      label_trainingNorm = QLabel()
      label_training.setText("Data Training")
      label_trainingNorm.setText("Data Training Setelah Normalisasi")
      self.label_bias=QLabel()
      self.label_fscore=QLabel()
      self.label_tableRecom=QLabel()
      self.label_tableRecom.setText("tabel rekomendasi")
      self.tableRecommendData=QTableWidget()


      self.label_recommend = QLabel()
      self.label_recommend.setText("rekomendasi lagu :")
      self.label_fscore.setText("f-score :")
      self.label_bias.setText("Bias :")
      self.label_alphas=QLabel()
      self.label_alphas.setText("alphas size :")
      label_1.setText("paste your Token here")
      self.string=QLineEdit()
      self.table=QTableWidget()
      self.table2=QTableWidget() #data training setelah dinormalisasi
      self.tableRecommend=QTableWidget() #buat rekomendasi
      self.tableRecommend.setRowCount(10)
      self.tableRecommend.setColumnCount(3)
      self.tableRecommend.setHorizontalHeaderItem(0, QTableWidgetItem("Artis"))
      self.tableRecommend.setHorizontalHeaderItem(1, QTableWidgetItem("Judul Lagu"))
      self.tableRecommend.setHorizontalHeaderItem(2, QTableWidgetItem("Album"))
      self.alphas=QListWidget()

      self.textbox = QTextEdit()
      print( self.string.text())
      self.b1 = QPushButton()
      self.bFiles=QPushButton()
      self.b_train=QPushButton()
      self.b_split=QPushButton()
      self.bRecomm = QPushButton()
      self.b_getData=QPushButton()
      self.b1.setText("Paste Token")
      self.bFiles.setText("select FIle")
      self.b_train.setText("Start Train")
      self.bRecomm.setText("Start Recommendations")
      self.b_split.setText("set Data train and test")
      self.b_getData.setText("get data")

      #self.b1.clicked.connect(lambda : self.start_svm())
      #fbox.addWidget(label_1)
      #fbox.addWidget(self.string)
      #fbox.addWidget(self.textbox)


      gbox2.addWidget(self.labelbox)
      gbox2.addWidget(self.b1)
      gbox2.addWidget(self.b_getData)

      gbox2.addWidget(label_training)
      gbox2.addWidget(self.table)
      gbox2.addWidget(label_trainingNorm)
      gbox2.addWidget(self.table2)
      gbox.addWidget(self.bRecomm)
      gbox.addWidget(self.label_alphas)
      gbox.addWidget(self.alphas)
      gbox.addWidget(self.label_bias)

      gbox.addWidget(self.label_tableRecom)
      gbox.addWidget(self.tableRecommendData)
      gbox.addWidget(self.label_recommend)
      gbox.addWidget(self.tableRecommend)

      grid1.addWidget(self.ckboxDanceability,0,0)
      grid1.addWidget(self.ckboxEnergy,0,1)
      grid1.addWidget(self.ckboxInstrumentalness,0,2)
      grid1.addWidget(self.ckboxSpeechiness,0,3)
      grid1.addWidget(self.ckboxAcousticness,1,0)
      grid1.addWidget(self.ckboxValence,1,1)
      grid1.addWidget(self.ckboxLoudness,1,2)
      grid1.addWidget(self.ckboxTempo,1,3)

      grid1.addWidget(self.labelParamC)
      grid1.addWidget(self.paramC)
      grid1.addWidget(self.labelParamTolerance)
      grid1.addWidget(self.paramTolerance)
      grid1.addWidget(self.labelParamIterate)
      grid1.addWidget(self.paramIterate)
      grid1.addWidget(self.labelParamGamma)
      grid1.addWidget(self.paramGamma)
      #grid1.addWidget(self.labelParamDegree)
      #grid1.addWidget(self.paramDegree)
      #grid1.addWidget(self.labelParamCoef)
      #grid1.addWidget(self.paramCoef)
      grid1.addWidget(self.normType)
      grid1.addWidget(self.kernelType)

      grid1.addWidget(self.bFiles)
      grid1.addWidget(self.b_train)
      grid1.addWidget(self.b_split)
      gbox3.addLayout(grid1)
      gbox3.addWidget(self.lbelFilename)
      gbox3.addWidget(self.label_fscore)
      #gbox3.addWidget(lbelC)
      #gbox3.addWidget(self.dbleboxC)
      #gbox3.addWidget(lbelmaxIter)
      #gbox3.addWidget(self.dbleboxmaxIter)
      #gbox3.addWidget(lbelToler)
      #gbox3.addWidget(self.dbleboxToler)
      # gbox3.addWidget(self.slctFile)
      # grid1.addIt(ckboxLoudness,0,2)
      fbox.addLayout(gbox,1,1)
      fbox.addLayout(gbox2,0,1)
      tab1.setLayout(gbox3)
      tab2.setLayout(fbox)
      self.tabs.addTab(tab1,"training")
      self.tabs.addTab(tab2,"recommend")
      self.tabs.setGeometry(100,100,800,600)
      print("sayang")
      self.tabs.setWindowTitle("hahahah")
      self.tabs.show()
      #print(self.paramTolerance.value())
      #temp=str(self.slctFile.getOpenFileNames())
# def openFileNameDialog(self):
#           options = QFileDialog.Options()
#           fileName, _ = QFileDialog.getOpenFileName(self, "Select FIle", "",
#                                                     "All Files (*);;csv Files (*.csv)", options=options)
#           if fileName:
#               print(fileName)

    #win.textbox.insertPlainText(win.string.text())
    #win.textbox.insertPlainText(text)
