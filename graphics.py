#To help us perform math operations
import numpy as np
import pandas as pd
#to plot our data and model visually
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter
import csv
from matplotlib.font_manager import FontProperties

fontP = FontProperties()
fontP.set_size('large')

file="C:\\Users\\Daniel\\PycharmProjects\\Spotiwew\\Iqbal Lazuardy\\main.csv"

reader=csv.DictReader(open(file))
csvList=list()
danceabilities=list()
valences=list()
energies=list()
speechinesses=list()
for row in reader :
    csvList.append(row)

pandaMaster=pd.DataFrame(csvList)

#plt.bar(pandaDance,1.0)
#plt.plot(pandaVal,color='green')
#print(pandamaster)
x=np.arange(pandaMaster.size)
pandaTemp=pandaMaster.drop_duplicates(subset="id")
pandaTemp=pandaTemp.head(n=30)
# h=pandaMaster['danceability'].values
# for i in h :
#     plt.plot(1,i,"r+",label="danceability")
#
# h=pandaMaster['energy'].values
# for i in h :
#     plt.plot(2,i,"m>",label="energy")
#
# h=pandaMaster['acousticness'].values
# for i in h :
#     plt.plot(3,i,"bo",label="acousticness")
#
# h=pandaMaster['instrumentalness'].values
# for i in h :
#     plt.plot(4,i,"yx",label="instrumentalness")
#
# h=pandaMaster['speechiness'].values
# for i in h :
#     plt.plot(5,i,"g*",label="speechiness")
#
# h=pandaMaster['valence'].values
# for i in h :
#     plt.plot(6,i,"c>",label="valence")
#
# plt.show()


# plt.plot(pandaMaster['acousticness'].values, "bo", label="acousticness")
# plt.plot(pandaMaster['danceability'].values,"rx",label="danceability")

# plt.show()

#random number


#ax0.hist(pandamaster['danceability'].head())

# ax.bar(x,pandamaster['acousticness'].head())
# ax.bar(x,pandamaster['danceability'].head())

plt.plot(pandaTemp['danceability'],"b*",label="danceability")
plt.plot(pandaTemp['energy'],"m>",label="energy")
plt.plot(pandaTemp['acousticness'],'ro')
plt.plot(pandaTemp['instrumentalness'],"gx",label="instrumentalness")
plt.plot(pandaTemp['speechiness'],"y+",label="speechiness")
plt.plot(pandaTemp['valence'],"c<",label="valence")
#
plt.ylabel("nilai")
plt.xlabel("lagu")
plt.legend(loc='best',prop=fontP,bbox_to_anchor=(1.05,1.0))
plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False) # labels along the bottom edge are off
#
plt.savefig('graph3.png',papertype='A4')
plt.show()
