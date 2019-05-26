from numpy import *
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import chi2_kernel,laplacian_kernel,sigmoid_kernel,rbf_kernel

from coba import list_loudness


def selectJrand(i,m):
    j=i #make sure J not equal to i
    while (j==i):
        j = int(random.uniform(0,m))
    return j

def clipAlpha(aj,H,L):
    if aj > H: 
        aj = H
    if L > aj:
        aj = L
    return aj

def smoSimple(dataMatIn, classLabels, C, toler, maxIter):
    dataMatrix = mat(dataMatIn); labelMat = mat(classLabels).transpose()
    b = 0
    m,n = shape(dataMatrix)
    alphas = mat(zeros((m,1)))
    iter = 0
    while (iter < maxIter):
        alphaPairsChanged = 0
        for i in range(m):
            Ei = (float(multiply(alphas,labelMat).T*(dataMatrix*dataMatrix[i,:].T)) + b) - float(labelMat[i]) #the error. buat seminimal mungkin(<tolerance)
            if ((labelMat[i]*Ei < -toler) and (alphas[i] < C)) or ((labelMat[i]*Ei > toler) and (alphas[i] > 0)):
                j = selectJrand(i,m)
                Ej = (float(multiply(alphas,labelMat).T*(dataMatrix*dataMatrix[j,:].T)) + b) - float(labelMat[j]) #the error utk data ke j
                alphaIold = alphas[i].copy(); alphaJold = alphas[j].copy();
                if (labelMat[i] != labelMat[j]):
                    L = max(0, alphas[j] - alphas[i])
                    H = min(C, C + alphas[j] - alphas[i])
                else:
                    L = max(0, alphas[j] + alphas[i] - C)
                    H = min(C, alphas[j] + alphas[i])
                if L==H:
                    continue
                eta = 2.0 * dataMatrix[i,:]*dataMatrix[j,:].T - dataMatrix[i,:]*dataMatrix[i,:].T - dataMatrix[j,:]*dataMatrix[j,:].T
                if eta >= 0:
                    continue
                alphas[j] -= labelMat[j]*(Ei - Ej)/eta
                alphas[j] = clipAlpha(alphas[j],H,L)
                if (abs(alphas[j] - alphaJold) < 0.00001):
                    continue
                alphas[i] += labelMat[j]*labelMat[i]*(alphaJold - alphas[j])
                b1 = b - Ei- labelMat[i]*(alphas[i]-alphaIold)*dataMatrix[i,:]*dataMatrix[i,:].T - labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[i,:]*dataMatrix[j,:].T
                b2 = b - Ej- labelMat[i]*(alphas[i]-alphaIold)*dataMatrix[i,:]*dataMatrix[j,:].T - labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[j,:]*dataMatrix[j,:].T
                if (0 < alphas[i]) and (C > alphas[i]): b = b1
                elif (0 < alphas[j]) and (C > alphas[j]): b = b2
                else: b = (b1 + b2)/2.0
                alphaPairsChanged += 1
               # print("iter: %d i:%d, pairs changed %d" % (iter,i,alphaPairsChanged))
        if (alphaPairsChanged == 0): iter += 1
        else: iter = 0
       # print("iteration number: %d" % iter)
    return b,alphas

# def check_number(x,aTup) :#     if(aTup[0]=='min') :
#         if(x<aTup[1]) :
#             x=aTup[1]
#     else :
#         if (aTup[0] == 'max'):
#             if (x > aTup[1]):
#                 x = aTup[1]
#     return x

def normalize(theList,type) :
    #hanya fitur tempo dan loudness yang akan dinormalisasi
        list_tempo=list()
        list_loudness=list()
        print("masuk sini")
        if 'tempo' in theList[0] :
            for i in theList:
                list_tempo.append(i['tempo'])


        if 'loudness' in theList[0] :
            for i in theList:
                list_loudness.append(i['loudness'])


        if (len(list_tempo) > 0):
            meanTempo = sum(list_tempo) / len(list_tempo)
            maxTempo = 219.467
            minTempo = 49.621
        if (len(list_loudness) > 0):
            meanLoudness = sum(list_loudness) / len(list_loudness)
            maxLoudness = 3.639
            minLoudness = -20.535

        if (type == 'mean'):
            if (len(list_tempo) > 0):
                for i in range(len(list_tempo)):
                    list_tempo[i] = (list_tempo[i] - meanTempo) / (maxTempo - minTempo)
            print("masuk mean")
            if (len(list_loudness) > 0):
                for i in range(len(list_loudness)):
                    list_loudness[i] = (list_loudness[i] - meanLoudness) / (maxLoudness - minLoudness)
            print("masuk loudness")
        if (type == 'minmax'):
            if (len(list_tempo) > 0):
                for i in range(len(list_tempo)):
                    if (list_tempo[i] > maxTempo):
                        list_tempo[i] = maxTempo
                    if (list_tempo[i] < minTempo):
                        list_tempo[i] = minTempo
                    list_tempo[i] = (list_tempo[i] - minTempo) / (maxTempo - minTempo)
                print("temponya ada")
            if (len(list_loudness) > 0):
                for i in range(len(list_loudness)):
                   # check_number(list_loudness[i],)
                    if (list_loudness[i] > maxLoudness):
                        list_loudness[i] = maxLoudness
                    if (list_loudness[i] < minLoudness):
                        list_loudness[i] = minLoudness
                    list_loudness[i] = (list_loudness[i] - minLoudness) / (maxLoudness - minLoudness)
                print("loudness ada")
                # masukkan kembali ke theList
        if (len(list_tempo) > 0):
            for i in range(len(theList)):
                theList[i]['tempo'] = list_tempo[i]
        if (len(list_loudness) > 0):
            for i in range(len(theList)):
                theList[i]['loudness'] = list_loudness[i]
        print("sudah beres")
        return theList


def kernelTrans(X, A, kTup):
    m,n = shape(X)
    K = mat(zeros((m,1)))
    if kTup['type']=='linear':
        K = X * A.T   #linear kernel

    if kTup['type']=='RBF':
        for j in range(m):
            deltaRow = X[j,:] - A
            K[j] = deltaRow*deltaRow.T  #squared euclidean distance
        K = exp(K/(-2*kTup['gamma']**2))


    if kTup['type'] == 'laplacian':

        for j in range(m):
            K[j] = sum(fabs(X[j,:]-A)) #manhattan distance
        K = exp(K*(-1*1/kTup['gamma']))
    return K