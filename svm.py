from numpy import *
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import chi2_kernel,laplacian_kernel,sigmoid_kernel,rbf_kernel

from coba import list_loudness


class strukDatSVM :
    def __init__(self,dataMatrix,labelMat,toler,C,b,maxIter,alphas,fcache):
        self.dataMatrix=dataMatrix
        m, n = shape(self.dataMatrix)
        self.labelMat=labelMat
        self.toler=toler
        self.C=C
        self.maxIter=maxIter
        self.alphas=alphas
        self.fcache=fcache
        self.b=b

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

def findbestJ(i,theDatas,Ei) :
    """ try to find J rather than do the rand things 
        in this method we calculate the Error, then find the best (lowest as possible)
    """
    m,n=shape(theDatas.dataMatrix)
    bestj=-1
    bestEj=0
    bestScore=0
    validEcacheList = nonzero(theDatas.fcache[:, 0].A)[0]
    if(len(validEcacheList)> 1 ) :
        for j in validEcacheList:
            if(j==i) :
                continue
            Ej=hitungError(theDatas,j)
            if(abs(Ei-Ej) > bestScore) : #hitung selisih sama Ei
                bestEj=Ej
                bestj=j
        return  bestj,bestEj
    else:
        #for first case
        #soalnya masih pada 0 smua gitu
        j = selectJrand(i,m)
        Ej= hitungError(theDatas,j)
        return j,Ej

def hitungError(theDatas,indeks) :
    return (float(multiply(theDatas.alphas,theDatas.labelMat).T*(theDatas.dataMatrix*theDatas.dataMatrix[indeks,:].T))+theDatas.b)\
           - float(theDatas.labelMat[indeks]) #the error. buat seminimal mungkin(<tolerance)

def flagCache(theDatas,x) : #kasih tanda kalo sudah dihitung Erornya. minimize proses perhitungan
    return [1,hitungError(theDatas,x)]


def examineExample(i,theDatas) :
    Ei = hitungError(theDatas,i)
    if ((theDatas.labelMat[i] * Ei < -theDatas.toler) and (theDatas.alphas[i] < theDatas.C)) or \
            ((theDatas.labelMat[i] * Ei > theDatas.toler) and (theDatas.alphas[i] > 0)):
        # j = selectJrand(i,m)
        # Ej = (float(multiply(alphas,labelMat).T*(dataMatrix*dataMatrix[j,:].T)) + b) - float(labelMat[j]) #the error utk data ke j
        j, Ej = findbestJ(i,theDatas,Ei)
        alphaIold = theDatas.alphas[i].copy();
        alphaJold = theDatas.alphas[j].copy();
        if (theDatas.labelMat[i] != theDatas.labelMat[j]):
            L = max(0, theDatas.alphas[j] - theDatas.alphas[i])
            H = min(theDatas.C, theDatas.C + theDatas.alphas[j] - theDatas.alphas[i])
        else:
            L = max(0, theDatas.alphas[j] + theDatas.alphas[i] - theDatas.C)
            H = min(theDatas.C, theDatas.alphas[j] + theDatas.alphas[i])
        if L == H:
            return 0
        eta = 2.0 * theDatas.dataMatrix[i, :] * theDatas.dataMatrix[j, :].T - \
              theDatas.dataMatrix[i, :] * theDatas.dataMatrix[i, :].T - theDatas.dataMatrix[j, :] * theDatas.dataMatrix[j, :].T
        if eta >= 0:
            return 0
        theDatas.alphas[j] -= theDatas.labelMat[j] * (Ei - Ej) / eta
        theDatas.alphas[j] = clipAlpha(theDatas.alphas[j], H, L)
        theDatas.fcache[j]= flagCache(theDatas, j)
        if (abs(theDatas.alphas[j] - alphaJold) < 0.00001):
            return 0
        theDatas.alphas[i] += theDatas.labelMat[j] * theDatas.labelMat[i] * (alphaJold - theDatas.alphas[j])
        theDatas.fcache[i] = flagCache(theDatas, i)
        b1 = theDatas.b - Ei - theDatas.labelMat[i] * (theDatas.alphas[i] - alphaIold) * theDatas.dataMatrix[i,
                                                                                         :] * theDatas.dataMatrix[i,
                                                                                              :].T - \
             theDatas.labelMat[j] * (theDatas.alphas[j] - alphaJold) * theDatas.dataMatrix[i, :] * theDatas.dataMatrix[
                                                                                                   j, :].T
        b2 = theDatas.b - Ej - theDatas.labelMat[i] * (theDatas.alphas[i] - alphaIold) * theDatas.dataMatrix[i,
                                                                                         :] * theDatas.dataMatrix[j,
                                                                                              :].T - \
             theDatas.labelMat[j] * (theDatas.alphas[j] - alphaJold) * theDatas.dataMatrix[j, :] * theDatas.dataMatrix[
                                                                                                   j, :].T
        if (0 < theDatas.alphas[i]) and (theDatas.C > theDatas.alphas[i]):
            theDatas.b = b1
        elif (0 < theDatas.alphas[j]) and (theDatas.C > theDatas.alphas[j]):
            theDatas.b = b2
        else:
            theDatas.b = (b1 + b2) / 2.0
        return 1
    else:
        return 0 #alphapairschanged


def smoSimple(dataMatIn, classLabels, C, toler, maxIter):
    dataMatrix = mat(dataMatIn); labelMat = mat(classLabels).transpose()
    b = 0
    m,n = shape(dataMatrix)
    alphas = mat(zeros((m,1)))
    iter = 0
    fcache=mat(zeros((m,2))) #yang satu buat kasih tanda kalau sudah diitung
    theDatas=strukDatSVM(dataMatrix,labelMat,toler,C,b,maxIter,alphas,fcache) #biar tidak banyak lempar parameter nanti
    examineAll=True
    alphaPairsChanged = 0
    while (iter < maxIter) and ((alphaPairsChanged > 0) or (examineAll)):
        alphaPairsChanged = 0
        if examineAll :
            for i in range(m):
                examineExample(i,theDatas)
            iter=iter+1
        else :
            nonBoundIs = nonzero((theDatas.alphas.A > 0) * (theDatas.alphas.A < C))[0]
            for i in nonBoundIs:
                alphaPairsChanged =alphaPairsChanged+ examineExample(i, theDatas)
            iter = iter+1
        if examineAll:
            examineAll = False  # toggle entire set loop
        elif (alphaPairsChanged == 0):
            examineAll = True
       # print("iteration number: %d" % iter)
    return theDatas.b,theDatas.alphas

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