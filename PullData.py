from array import array
import ROOT as rt
import random as rd
from tools import *
import estimation as st
import numpy as np





f = open('DatosPull_Pois.txt', 'r')

Co_Pull = rt.TH1F('Co_Pull','Co_Pull',100,-5,5)
K_Pull = rt.TH1F('K_Pull','K_Pull',100,-5,5)
Tl_Pull = rt.TH1F('Tl_Pull','Tl_Pull',100,-5,5)
Bi_Pull = rt.TH1F('Bi_Pull','Bi_Pull',100,-5,5)
bb_Pull = rt.TH1F('bb_Pull','bb_Pull',100,-5,5)

h_list = {60: Co_Pull,40: K_Pull, 214: Bi_Pull, 208: Tl_Pull, 'bb': bb_Pull}
data = np.array([[ 0., 0., 0., 0., 0.],]*1000)
l,m = [0,0]
for i in range(1000):
    exec('pulldata ='+ f.readline()[:-1])

    l=0
    for j in pulldata:
        print m,l,pulldata[j]['pull']
        data[m,l]= pulldata[j]['val']
        l +=1
        h_list[j].Fill(pulldata[j]['pull'])

    m += 1

of = rt.TFile("Pulls_Pois.root","RECREATE")
map(lambda h: h.Fit('gaus'),h_list.values())
map(lambda h: h.SetDirectory(of),h_list.values())
rt.gStyle.SetOptStat(1111);
rt.gStyle.SetOptFit(1111111);
of.Write()
of.Close()



n,m = data.shape
mean = []
sigma = []
cov = np.zeros([m,m])
cor = np.zeros([m,m])
for i in range(m):
    xd = data[:,i]
    xmean = np.mean(xd)
    mean.append(xmean)
    sigma.append((sum((xd-xmean)**2)/n)**0.5)

    for j in range(m):
        yd = data[:,j]
        ymean = np.mean(yd)
        cov[i,j] = np.mean((yd-ymean)*(xd-xmean))
for i in range(m):
    for j in range(m):
        cor[i,j] = cov[i,j]/(sigma[i]*sigma[j])
print 'cor \n',cor
