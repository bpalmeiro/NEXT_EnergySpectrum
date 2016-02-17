from array import array
import ROOT as rt
import random as rd
from tools import *
import estimation as st
import numpy as np

rt.gStyle.SetOptStat(1111);
rt.gStyle.SetOptFit(1111111);

nBin = 500
Emin = 0.
Emax = 3.

mass = 5.81 #masa de Xe
purity = 0.91 #pureza
trunlist = [300.]#10.,50.,100.,150.,200.,300.] #dias

BgrRej = 1.
SigEff = 1.


rand = rt.TRandom3(0)

graph = rt.TGraphErrors()
lup = 0;
hlist =[]
for trun in trunlist:

    hlist.append(rt.TH1F(str(trun),str(trun),100,0,10))

    Nbb2n = (int(round(st.estimation(mass,purity,trun)*.695197*SigEff))) #rand.Poisson

    texp = trun * 24 * 3600 #s


    #                               Ratio       act (mBq)
    esperado ={60: {0 :  int(round(3.935333e-2 * 0       /1000.   *texp * BgrRej)),
                    1 :  int(round(1.781900e-2 * 2.32e-1 /1000.   *texp * BgrRej)),
                    2 :  int(round(2.663240e-3 * 8.82    /1000.   *texp * BgrRej)),
                    3 :  int(round(6.060000e-5 * 8.4e-1  /1000.   *texp * BgrRej)),
                    4 :  int(round(3.945800e-2 * 2.27e-1 /1000.   *texp * BgrRej)),
                    5 :  int(round(4.147233e-2 * 9.66e-1 /1000.   *texp * BgrRej)),
                    6 :  int(round(1.525725e-3 * 2.02    /1000.   *texp * BgrRej)),
                    7 :  int(round(1.616075e-2 * 0       /1000.   *texp * BgrRej)),
                    8 :  int(round(8.496444e-3 * 2.52e1  /1000.   *texp * BgrRej)),
                    9 :  int(round(1.553625e-2 * 1.16e-1 /1000.   *texp * BgrRej)),
                    10 : int(round(9.619500e-5 * 1.58e3  /1000.   *texp * BgrRej)),
                    11 : int(round(3.361000e-3 * 2.03e-1 /1000.   *texp * BgrRej)),
                    12 : int(round(6.919778e-3 * 4.56e1  /1000.   *texp * BgrRej)),
                    13 : int(round(1.182263e-5 * 1.25e3  /1000.   *texp * BgrRej)),
                    14 : int(round(3.444875e-6 * 1.00e2  /1000.   *texp * BgrRej)),
                    15 : int(round(5.184667e-3 * 1.24e1  /1000.   *texp * BgrRej)),
                    16 : int(round(4.619750e-4 * 2.84e3  /1000.   *texp * BgrRej))
                    },
               40: {0 :  int(round(4.262175e-3 * 1.03    /1000.   *texp * BgrRej)),
                    1 :  int(round(1.038175e-3 * 1.38e1  /1000.   *texp * BgrRej)),
                    2 :  int(round(1.676425e-4 * 1.33e1  /1000.   *texp * BgrRej)),
                    3 :  int(round(4.483846e-6 * 9.52e1  /1000.   *texp * BgrRej)),
                    4 :  int(round(2.201075e-3 * 4.07e2  /1000.   *texp * BgrRej)),
                    5 :  int(round(2.358350e-3 * 5.79e1  /1000.   *texp * BgrRej)),
                    6 :  int(round(9.838308e-5 * 3.05    /1000.   *texp * BgrRej)),
                    7 :  int(round(9.100154e-4 * 3.4e-1  /1000.   *texp * BgrRej)),
                    8 :  int(round(5.244000e-4 * 3.81e1  /1000.   *texp * BgrRej)),
                    10 : int(round(0           * 5.76e1  /1000.   *texp * BgrRej)),
                    9 :  int(round(8.711692e-4 * 4.44    /1000.   *texp * BgrRej)),
                    11 : int(round(2.022533e-4 * 2.55e1  /1000.   *texp * BgrRej)),
                    12 : int(round(4.074067e-4 * 1.45e2  /1000.   *texp * BgrRej)),
                    13 : int(round(0           * 1.87e3  /1000.   *texp * BgrRej)),
                    14 : int(round(0           * 3.7e5   /1000.   *texp * BgrRej)),
                    15 : int(round(3.162600e-4 * 1.88e1  /1000.   *texp * BgrRej)),
                    16 : int(round(3.100538e-5 * 1.03e2  /1000.   *texp * BgrRej))
                    },
              214: {0 :  int(round(3.188567e-2 * 3.34e-1 /1000.   *texp * BgrRej)),
                    1 :  int(round(9.943231e-3 * 2.05e-1 /1000.   *texp * BgrRej)),
                    2 :  int(round(1.409567e-3 * 2.58    /1000.   *texp * BgrRej)),
                    3 :  int(round(3.629250e-5 * 1.79e2  /1000.   *texp * BgrRej)),
                    4 :  int(round(2.299831e-2 * 2.12    /1000.   *texp * BgrRej)),
                    5 :  int(round(2.362262e-2 * 1.04    /1000.   *texp * BgrRej)),
                    6 :  int(round(8.227000e-4 * 5.9e-1  /1000.   *texp * BgrRej)),
                    7 :  int(round(9.060444e-3 * 5.05e-1 /1000.   *texp * BgrRej)),
                    8 :  int(round(4.535320e-3 * 7.38    /1000.   *texp * BgrRej)),
                    9 :  int(round(8.353222e-3 * 5.65e-1 /1000.   *texp * BgrRej)),
                    10 : int(round(6.012250e-5 * 1.66e2  /1000.   *texp * BgrRej)),
                    11 : int(round(1.818040e-3 * 7.03    /1000.   *texp * BgrRej)),
                    12 : int(round(3.713360e-3 * 4.2     /1000.   *texp * BgrRej)),
                    13 : int(round(7.966818e-6 * 5.45e3  /1000.   *texp * BgrRej)),
                    14 : int(round(2.331544e-6 * 1.05e5  /1000.   *texp * BgrRej)),
                    15 : int(round(2.742629e-3 * 3.64    /1000.   *texp * BgrRej)),
                    16 : int(round(2.630100e-4 * 2.97e2  /1000.   *texp * BgrRej))
                    },
              208: {0 :  int(round(4.405350e-2 * 5.41e-2 /1000.   *texp * BgrRej)),
                    1 :  int(round(1.300250e-2 * 2.52e-2 /1000.   *texp * BgrRej)),
                    2 :  int(round(2.493200e-3 * 3.23e-1 /1000.   *texp * BgrRej)),
                    3 :  int(round(1.078600e-4 * 5.6e1   /1000.   *texp * BgrRej)),
                    4 :  int(round(3.341017e-2 * 3.3e-1  /1000.   *texp * BgrRej)),
                    5 :  int(round(3.065883e-2 * 1.72e-1 /1000.   *texp * BgrRej)),
                    6 :  int(round(1.416540e-3 * 7.13e-2 /1000.   *texp * BgrRej)),
                    7 :  int(round(1.044113e-2 * 7.13e-2 /1000.   *texp * BgrRej)),
                    9 :  int(round(7.782667e-4 * 9.23e-1 /1000.   *texp * BgrRej)),
                    8 :  int(round(1.053888e-2 * 1.67e-1 /1000.   *texp * BgrRej)),
                    10 : int(round(1.768800e-4 * 5.4e1   /1000.   *texp * BgrRej)),
                    11 : int(round(2.669667e-3 * 2.3     /1000.   *texp * BgrRej)),
                    12 : int(round(5.219333e-3 * 2.28    /1000.   *texp * BgrRej)),
                    13 : int(round(2.816600e-5 * 5.30e2  /1000.   *texp * BgrRej)),
                    14 : int(round(8.416333e-6 * 9.4e3   /1000.   *texp * BgrRej)),
                    15 : int(round(4.837350e-3 * 4.55e-1 /1000.   *texp * BgrRej)),
                    16 : int(round(7.067467e-4 * 9.68e1  /1000.   *texp * BgrRej))
                    }


    	}



    Epos = {60 : {}, 40 : {} , 214 : {} , 208: {} }
    for i in Epos:
        for j in filedic:
            Epos[i][j] = []
            #esperado[i][j] = rand.Poisson(esperado[i][j])



    ff = rt.TFile("BgrClass.root","READONLY")
    t = ff.Get('t')



    E,Xi,Yi,Zi,Xf,Yf,Zf = [array('f',[0.]) for i in range(7)]
    element,part,Process = [array('i',[0]) for i in range(3)]
    Epart = array('d',[0.])

    t.SetBranchAddress('E',E)
    t.SetBranchAddress('Element',element)
    t.SetBranchAddress('Part',part)
    t.SetBranchAddress('EPart',Epart)
    t.SetBranchAddress('Process',Process)
    t.SetBranchAddress('Xi',Xi)
    t.SetBranchAddress('Yi',Yi)
    t.SetBranchAddress('Zi',Zi)
    t.SetBranchAddress('Xf',Xf)
    t.SetBranchAddress('Yf',Yf)
    t.SetBranchAddress('Zf',Zf)



    for i in range(int(t.GetEntries())):
        t.GetEntry(i)
        Epos[element[0]][part[0]].append(E[0])



    bb2nfile = rt.TFile('bb2nu.root')
    bt = bb2nfile.Get('t')
    E2nur = array('f',[0.])
    bt.SetBranchAddress('E',E2nur)
    E2nu = []

    h_bb2n = rt.TH1F('bb2nu','bb2nu',nBin,Emin,Emax)
    for i in range(int(bt.GetEntries())):
        bt.GetEntry(i)
        E2nu.append(E2nur[0])

    Co_Pull = rt.TH1F('Co_Pull','Co_Pull',100,-5,5)
    K_Pull = rt.TH1F('K_Pull','K_Pull',100,-5,5)
    Tl_Pull = rt.TH1F('Tl_Pull','Tl_Pull',100,-5,5)
    Bi_Pull = rt.TH1F('Bi_Pull','Bi_Pull',100,-5,5)
    bb_Pull = rt.TH1F('bb_Pull','bb_Pull',100,-5,5)

    Co_Sigma = rt.TH1F('Co_Sigma','Co_Sigma',100,0,100)
    K_Sigma = rt.TH1F('K_Sigma','K_Sigma',100,0,100)
    Tl_Sigma = rt.TH1F('Tl_Sigma','Tl_Sigma',100,0,100)
    Bi_Sigma = rt.TH1F('Bi_Sigma','Bi_Sigma',100,0,100)
    bb_Sigma = rt.TH1F('bb_Sigma','bb_Sigma',100,0,100)


    h_list_Pull = {40: K_Pull, 214: Bi_Pull, 208: Tl_Pull, 'bb': bb_Pull} #60: Co_Pull,
    h_list_Sigma = {40: K_Sigma, 214: Bi_Sigma, 208: Tl_Sigma, 'bb': bb_Sigma} #60: Co_Sigma,

    dat = []
    nnn = []
    sss = []
    for i in range(50):
        n,nfit = FitFit(Epos,E2nu,"Train_800.root",esperado,Nbb2n,bin=125)
        dat.append(nfit['bb']['val']/nfit['bb']['err'])
        nnn.append(nfit['bb']['val'])
        sss.append(nfit['bb']['err'])
        graph.SetPoint(lup,trun,nfit['bb']['val']/nfit['bb']['err'])
        lup+=1
        hlist[-1].Fill(nfit['bb']['val']/nfit['bb']['err'])
    dat = np.array(dat)
    mean = np.mean(dat)
    err = np.sum((dat-mean)**2)**0.5/20.
    graph.SetPoint(lup,trun,mean)
    graph.SetPointError(lup,0,err)
    lup+=1
