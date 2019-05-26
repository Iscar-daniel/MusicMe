import sys
import pickle
from _ast import Nonlocal

from PyQt5.uic.Compiler.qtproxies import QtGui
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
from PyQt5.QtWidgets import QApplication,QTableWidgetItem,QFileDialog,QWidget
from collections import OrderedDict, UserList
import userGui
import testData


def main() :
    iseng = testData.primary()
    iseng.__init__(userGui=userGui.userWindow(),userConnect=userConnect.connect())
    app =QApplication(sys.argv)
    iseng.show()
    sys.exit(app.exec_())

# win.b1.clicked.connect(lambda: c.paste_token())
# win.b_getData.clicked.connect(lambda: c.get_dataset())
# win.bFiles.clicked.connect(lambda: win.openFileNameDialog())
# win.b_train.clicked.connect(lambda: c.start_svm(win.filename))
# win.bRecomm.clicked.connect(lambda: c.recommend())
if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function