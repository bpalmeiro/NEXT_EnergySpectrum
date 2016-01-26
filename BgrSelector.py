from array import array
import ROOT as rt
import random as rd
from tools import *
import estimation as st


rt.gStyle.SetOptStat(1111);
rt.gStyle.SetOptFit(1111111);

nBin = 500
Emin = 0.
Emax = 3.

mass = 5.81 #masa de Xe
purity = 0.91 #pureza
trun = 100. #dias

BgrRej = 1.
SigEff = 1.


rand = rt.TRandom3(0)

Nbb2n = int(round(st.estimation(mass,purity,trun)*.695197*SigEff)) #rand.Poisson

texp = trun * 24 * 3600 #s

elementdic = {60: 'Co60',
            208: 'Tl208',
            214: 'Bi214',
            40: 'K40'}


filedic = {0 :'ANODE_QUARTZ ',
        1  :'BUFFER_TUBE ',
        2  :'CARRIER_PLATE ',
        3  :'DB_PLUG ',
        4  :'DICE_BOARD ',
        5  :'DRIFT_TUBE ',
        6  :'ENCLOSURE_BODY ',
        7  :'ENCLOSURE_WINDOW ',
        8  :'ICS ',
        9  :'OPTICAL_PAD ',
        10 :'PEDESTAL ',
        11 :'PMT_BASE ',
        12 :'PMT_BODY ',
        13 :'SHIELDING_LEAD ',
        14 :'SHIELDING_STRUCT ',
        15 :'SUPPORT_PLATE ',
        16 :'VESSEL '

	}
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

h_Co = [rt.TH1F('Co_'+filedic[i],'Co_'+filedic[i],nBin,Emin,Emax) for i in filedic]
h_K =  [rt.TH1F('K_'+filedic[i],'K_'+filedic[i],nBin,Emin,Emax) for i in filedic]
h_Bi = [rt.TH1F('Bi_'+filedic[i],'Bi_'+filedic[i],nBin,Emin,Emax) for i in filedic]
h_Tl = [rt.TH1F('Tl_'+filedic[i],'Tl_'+filedic[i],nBin,Emin,Emax) for i in filedic]
h_part = [rt.TH1F('total_'+filedic[i],'total_'+filedic[i],nBin,Emin,Emax) for i in filedic]

h_Co_total = rt.TH1F('Co_total','Co_total',nBin,Emin,Emax)
h_K_total = rt.TH1F('K_total','K_total',nBin,Emin,Emax)
h_Bi_total = rt.TH1F('Bi_total','Bi_total',nBin,Emin,Emax)
h_Tl_total = rt.TH1F('Tl_total','Tl_total',nBin,Emin,Emax)
h_total_Bgr = rt.TH1F('total_Brg','total_Bgr',nBin,Emin,Emax)
h_total = rt.TH1F('total','total',nBin,Emin,Emax)


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

rd.shuffle(E2nu)
E2nu = E2nu[:Nbb2n]

for i in E2nu:
    h_bb2n.Fill(i)






for i in Epos:
    for j in filedic:
        rd.shuffle(Epos[i][j])
        Epos[i][j] = Epos[i][j][:esperado[i][j]]
        for k in range(len(Epos[i][j])):
            if i == 40:
                h_K[j].Fill(Epos[i][j][k])
            if i == 60:
                h_Co[j].Fill(Epos[i][j][k])
            if i == 214:
                h_Bi[j].Fill(Epos[i][j][k])
            if i == 208:
                h_Tl[j].Fill(Epos[i][j][k])

for j in filedic:
    h_part[j].Add(h_K[j])
    h_part[j].Add(h_Co[j])
    h_part[j].Add(h_Bi[j])
    h_part[j].Add(h_Tl[j])

map(lambda h: h_Co_total.Add(h),h_Co)
map(lambda h: h_K_total.Add(h),h_K)
map(lambda h: h_Bi_total.Add(h),h_Bi)
map(lambda h: h_Tl_total.Add(h),h_Tl)
h_Co += [h_Co_total]
h_K += [h_K_total]
h_Bi += [h_Bi_total]
h_Tl += [h_Tl_total]
map(lambda h: h_total_Bgr.Add(h),h_part)
h_total.Add(h_total_Bgr)
h_total.Add(h_bb2n)



hlist = h_Co+h_K+h_Bi+h_Tl+h_part+[h_total,h_bb2n, h_total_Bgr]

a = []

hlist_G = map(h_Gauss,hlist)

for h in hlist_G:
    a += [h.Clone(h.GetName()+'rebin').Rebin(4)]
hlist += a


of = rt.TFile("Poissonizado_100.root","RECREATE")
t = rt.TTree('t','tree')
E = array('f',[0.])
t.Branch('E',E,'E')

for i in Epos:
    for j in filedic:
        for En in Epos[i][j]:
            E[0] = En
            t.Fill()

map(lambda h: h.SetDirectory(of),hlist+hlist_G)
of.Write()
of.Close()
ff.Close()
bb2nfile.Close()
