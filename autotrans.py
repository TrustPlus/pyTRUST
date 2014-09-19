import sys
import getopt
import time

#Define Default Values
Ntries = 100 
Naddrs = 4 
ExpectedCoinsToSend = 1.
minCoinsMultiplier = .00000001
coinBinResolution = 1

#Take command line arguments
opts, args = getopt.getopt(sys.argv[1:], 'o:v', ['addr=','tries=','coins=','multiplier=','resolution='])
for opt,arg in opts:
  if opt in ('-a', '--addr'):
    Naddrs = int(arg)
  elif opt in ('-t','--tries'):
    Ntries = int(arg)
  elif opt in ('-c','--coins'):
    ExpectedCoinsToSend = float(arg)
  elif opt in ('-m','--multiplier'):
    minCoinsMultiplier = float(arg)
  elif opt in ('-r','--resolution'):
    coinBinResolution = int(arg)

import random as rnd
import numpy as np

maxCoinsToSendPerAttempt = ExpectedCoinsToSend*10.*minCoinsMultiplier
minCoinsToSendPerAttempt = ExpectedCoinsToSend*minCoinsMultiplier

while minCoinsToSendPerAttempt < .00000001:
  print 'Correcting:',
  minCoinsToSendPerAttempt = minCoinsToSendPerAttempt*10. 
  maxCoinsToSendPerAttempt = maxCoinsToSendPerAttempt*10. 
  minCoinsMultplier = 10.*minCoinsMultiplier

print
print 'Max Coins to send per Attempt: ',maxCoinsToSendPerAttempt
print 'Min Coins to send per Attempt: ',minCoinsToSendPerAttempt

Ntries = Ntries + 1
countAddr = [0.]*Ntries
countTime = [0.]*Ntries
countCoins = [0.]*Ntries

coinBins = Ntries*coinBinResolution
coinDist=[0.]*Ntries
addrDist=[0.]*Ntries
for i in range(Ntries):
  coinDist[i]=[0.]*(coinBins)
  addrDist[i]=[0.]*(Ntries)

sentCoins = 0.
numTransactions = 0
numBlocks = 0
maxSentCoins = 0
maxCoinsPerBlock = maxCoinsToSendPerAttempt*float(Ntries)
while sentCoins < ExpectedCoinsToSend:
  print 'Current block:', numBlocks,'Sent Coins:',sentCoins,'\r',
  #print
  numBlocks = numBlocks + 1
  countAddr1 = 0
  countTime1 = 0
  countSentCoins = 0.
  sqCountSentCoins = 0.
  for i in range(Ntries-1):
    randTime = rnd.randint(0,1)
    if randTime == 0:
      countTime1 = countTime1 + 1
      randAddr = rnd.randint(0,Naddrs-1)
      if randAddr == 0: 
        countAddr1 = countAddr1 + 1
        coinsToSendPerAttempt = rnd.uniform(minCoinsToSendPerAttempt,maxCoinsToSendPerAttempt)
        testSentCoins = countSentCoins + coinsToSendPerAttempt
        if testSentCoins <= ExpectedCoinsToSend:
          numTransactions = numTransactions + 1
          countSentCoins = testSentCoins
          sqCountSentCoins = testSentCoins*testSentCoins
          #print countSentCoins,sqCountSentCoins
        else:
          break
  #Count Total Coins Sent
  sentCoins = sentCoins + countSentCoins
  #print sentCoins
  #print countSentCoins,maxSentCoins

  #Count Total Times Transaction Occurred in Block
  #print countTime1,countAddr1
  addrDist[countTime1][countAddr1] = addrDist[countTime1][countAddr1] + 1

  #Count Total Coins Sent in Block
  if maxSentCoins <= countSentCoins:
    maxSentCoins = countSentCoins  
  #if countAddr1 > 0:
  ratioToMaxCoinsPerBlock = countSentCoins/maxCoinsPerBlock
  coinBin = int(ratioToMaxCoinsPerBlock*float(coinBins)) #/minCoinsMultiplier)
    #print 'Ratio to Max: ',ratioToMaxCoinsPerBlock
    #print 'coinBin:',coinBin
    #coinDist[countTime1][countAddr1] = coinDist[countTime1][countAddr1] + 1
  coinDist[countTime1][coinBin] = coinDist[countTime1][coinBin] + 1
  
print 'Current block:', numBlocks,'Sent Coins:',sentCoins,'\r',
print '\n\nExpected Coins:',ExpectedCoinsToSend
print 'Sent Coins:',sentCoins
percentDiff = 100.*(abs(ExpectedCoinsToSend-sentCoins)/ExpectedCoinsToSend)
print "%%diff: %.8f" % percentDiff
print
print 'Total Transactions: ',numTransactions
print 'Total Blocks: ',numBlocks

#BEGIN ANALYSIS

#dist = np.array(addrDist)
dist = np.array(coinDist)
#print dist

sumDist=0.
for i in range(Ntries-1):
  #for j in range(Ntries-1):
  for j in range(coinBins-1):
    sumDist = sumDist+.25*(dist[i+1][j+1]+dist[i+1][j]+dist[i][j+1]+dist[i][j])
maxDist = np.amax(dist)
dist = dist/sumDist
print
print "Max. Dist, Sum. Dist: %.8f, %.8f" % (maxDist,sumDist)

normSumDist=0.
for i in range(Ntries-1):
  #for j in range(Ntries-1):
  for j in range(coinBins-1):
    normSumDist = normSumDist+.25*(dist[i+1][j+1]+dist[i+1][j]+dist[i][j+1]+dist[i][j])
normMaxDist = np.amax(dist)
print "Norm. Max. Dist., Norm. Sum. Dist.: %.8f, %.8f" % (normMaxDist,normSumDist)

#MLAB plot commands
#from mayavi.mlab import *
#x, y = np.mgrid[0:Ntries-1, 0:Ntries-1]
#fg_color = (0.06666, 0.06666, 0.1804)
#bg_color = (1, 1, 0.94118)
#figure(fgcolor=fg_color, bgcolor=bg_color)
#s = surf(x,y,dist, warp_scale='auto')
#outline(s, color=(.7, .7, .7))
#ax = axes(s, nb_labels=5,line_width=0.5,color=(.7, .7, .7),xlabel="Trans.", ylabel="Coins.",zlabel="Prob.",ranges=(0,Ntries-1,0,coinsToSendPerAttempt*(Ntries-1),0,normMaxDist))
#ax.axes.font_factor=1
#colorbar(title='Norm. Prob.', orientation='vertical',nb_labels=5)
#show()

#Pyplot commands
import matplotlib.pyplot as plt

fig,ax = plt.subplots()

max_x = float(Ntries)*maxCoinsToSendPerAttempt
#max_x = float(Ntries)
cax = ax.imshow(dist, cmap=plt.cm.jet, interpolation='none',extent=[0,max_x,0,Ntries-1],aspect="auto")
ax.set_title('Prob. of TRUST for %d TAddys.' % Naddrs)
#cax = ax.imshow(dist, cmap=plt.cm.jet, interpolation='none',extent=[0,Ntries-1,0,Ntries-1],aspect="auto")
#ax.set_title('Prob. of Trans. for 1 of %d Addrs.' % Naddrs)

xticks_loc = np.arange(0.,max_x,max_x/(6.*float(Naddrs)))
#xticks_loc = np.arange(0.,max_x,max_x/(6.*float(Naddrs)))
plt.xticks(xticks_loc)
ax.set_xlim(0,1.5*max_x/float(2*Naddrs))
#ax.set_xlim(0,1.5*max_x/float(Naddrs))
ax.ticklabel_format(style='sci', scilimits=(0,0), axis='x') 
plt.xlabel('Coins per Block (TRUST)')
#plt.xlabel('Times Address Chosen per Block')

#yticks_loc = np.arange(0.,float(Ntries),float(Ntries)/6.)
#plt.yticks(yticks_loc)
ax.set_ylim(0.25*float(Ntries),0.75*float(Ntries-1))
plt.ylabel('Transactions per Block')

cbar_ticks = [-1,0,1]
cbar = fig.colorbar(cax)
#cbar.ax.set_yticklabels(['0', normMaxDist*0.25, normMaxDist*0.5, normMaxDist])
plt.subplots_adjust(left=0.085,right=1.02,top=.945,bottom=0.1)
plt.show()

