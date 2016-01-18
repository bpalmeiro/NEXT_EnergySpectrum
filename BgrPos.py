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
trun = 197.3 #dias


Nbb2n = int(st.estimation(mass,purity,trun)*.695197)

texp = trun * 24 * 3600 #s

elementdic = {60: 'Co60',
            208: 'Tl208',
            214: 'Bi214',
            40: 'K40'}


filedic = {0 :'ANODE_QUARTZ ',
        1 :'CARRIER_PLATE ',
        2 :'DICE_BOARD ',
        3 :'ENCLOSURE_BODY ',
        4 :'ICS ',
        5 :'PEDESTAL ',
        6 :'PMT_BODY ',
        7 :'SHIELDING_STRUCT ',
        8 :'VESSEL ',
        9 :'BUFFER_TUBE ',
        10 :'DB_PLUG ',
        11 :'DRIFT_TUBE ',
        12 :'ENCLOSURE_WINDOW ',
        13 :'OPTICAL_PAD ',
        14 :'PMT_BASE ',
        15 :'SHIELDING_LEAD ',
        16 :'SUPPORT_PLATE '
	}

esperado ={60: {0 :  int(round(3.935333e-2 * 0       /1000.   *texp)),
                1 :  int(round(1.781900e-2 * 2.32e-1 /1000.   *texp)),
                2 :  int(round(2.663240e-3 * 8.82    /1000.   *texp)),
                3 :  int(round(6.060000e-5 * 8.4e-1  /1000.   *texp)),
                4 :  int(round(3.945800e-2 * 2.27e-1 /1000.   *texp)),
                5 :  int(round(4.147233e-2 * 9.66e-1 /1000.   *texp)),
                6 :  int(round(1.525725e-3 * 2.02    /1000.   *texp)),
                7 :  int(round(1.616075e-2 * 0       /1000.   *texp)),
                8 :  int(round(8.496444e-3 * 2.52e1  /1000.   *texp)),
                9 :  int(round(1.553625e-2 * 1.16e-1 /1000.   *texp)),
                10 : int(round(9.619500e-5 * 1.58e3  /1000.   *texp)),
                11 : int(round(3.361000e-3 * 2.03e-1 /1000.   *texp)),
                12 : int(round(6.919778e-3 * 4.56e1  /1000.   *texp)),
                13 : int(round(1.182263e-5 * 1.25e3  /1000.   *texp)),
                14 : int(round(3.444875e-6 * 1.00e2  /1000.   *texp)),
                15 : int(round(5.184667e-3 * 1.24e1  /1000.   *texp)),
                16 : int(round(4.619750e-4 * 2.84e3  /1000.   *texp))
                },
           40: {0 :  int(round(4.262175e-3 * 1.03    /1000.   *texp)),
                1 :  int(round(1.038175e-3 * 1.38e1   /1000.   *texp)),
                2 :  int(round(1.676425e-4 * 1.33e1  /1000.   *texp)),
                3 :  int(round(4.483846e-6 * 9.52e1  /1000.   *texp)),
                4 :  int(round(2.201075e-3 * 4.07e2  /1000.   *texp)),
                5 :  int(round(2.358350e-3 * 5.79e1  /1000.   *texp)),
                6 :  int(round(9.838308e-5 * 3.05    /1000.   *texp)),
                7 :  int(round(9.100154e-4 * 3.4e-1  /1000.   *texp)),
                8 :  int(round(5.244000e-4 * 3.81e1  /1000.   *texp)),
                9 :  int(round(8.711692e-4 * 4.44    /1000.   *texp)),
                10 : int(round(0           * 5.76e1  /1000.   *texp)),
                11 : int(round(2.022533e-4 * 2.55e1  /1000.   *texp)),
                12 : int(round(4.074067e-4 * 1.45e2  /1000.   *texp)),
                13 : int(round(0           * 1.87e3  /1000.   *texp)),
                14 : int(round(0           * 3.7e5   /1000.   *texp)),
                15 : int(round(3.162600e-4 * 1.88e1  /1000.   *texp)),
                16 : int(round(3.100538e-5 * 1.03e2  /1000.   *texp))
                },
          214: {0 :  int(round(3.188567e-2 * 3.34e-1 /1000.   *texp)),
                1 :  int(round(9.943231e-3 * 2.05e-1 /1000.   *texp)),
                2 :  int(round(1.409567e-3 * 2.58    /1000.   *texp)),
                3 :  int(round(3.629250e-5 * 1.79e2  /1000.   *texp)),
                4 :  int(round(2.299831e-2 * 2.12    /1000.   *texp)),
                5 :  int(round(2.362262e-2 * 1.04    /1000.   *texp)),
                6 :  int(round(8.227000e-4 * 5.9e-1  /1000.   *texp)),
                7 :  int(round(9.060444e-3 * 5.05e-1  /1000.   *texp)),
                8 :  int(round(4.535320e-3 * 7.38    /1000.   *texp)),
                9 :  int(round(8.353222e-3 * 5.65e-1 /1000.   *texp)),
                10 : int(round(6.012250e-5 * 1.66e2  /1000.   *texp)),
                11 : int(round(1.818040e-3 * 7.03    /1000.   *texp)),
                12 : int(round(3.713360e-3 * 4.2     /1000.   *texp)),
                13 : int(round(7.966818e-6 * 5.45e3  /1000.   *texp)),
                14 : int(round(2.331544e-6 * 1.05e5  /1000.   *texp)),
                15 : int(round(2.742629e-3 * 3.64    /1000.   *texp)),
                16 : int(round(2.630100e-4 * 2.97e2  /1000.   *texp))
                },
          208: {0 :  int(round(4.405350e-2 * 5.41e-2 /1000.   *texp)),
                1 :  int(round(1.300250e-2 * 2.52e-2 /1000.   *texp)),
                2 :  int(round(2.493200e-3 * 3.23e-1 /1000.   *texp)),
                3 :  int(round(1.078600e-4 * 5.6e1   /1000.   *texp)),
                4 :  int(round(3.341017e-2 * 3.3e-1  /1000.   *texp)),
                5 :  int(round(3.065883e-2 * 1.72e-1 /1000.   *texp)),
                6 :  int(round(1.416540e-3 * 7.13e-2 /1000.   *texp)),
                7 :  int(round(1.044113e-2 * 7.13e-2 /1000.   *texp)),
                9 :  int(round(7.782667e-4 * 9.23e-1 /1000.   *texp)),
                8 :  int(round(1.053888e-2 * 1.67e-1 /1000.   *texp)),
                10 : int(round(1.768800e-4 * 5.4e1   /1000.   *texp)),
                11 : int(round(2.669667e-3 * 2.3     /1000.   *texp)),
                12 : int(round(5.219333e-3 * 2.28    /1000.   *texp)),
                13 : int(round(2.816600e-5 * 5.30e2  /1000.   *texp)),
                14 : int(round(8.416333e-6 * 9.4e3   /1000.   *texp)),
                15 : int(round(4.837350e-3 * 4.55e-1 /1000.   *texp)),
                16 : int(round(7.067467e-4 * 9.68e1  /1000.   *texp))
                }


	}


computado ={	}

for i in esperado:
    computado[i] = {}
    for j in esperado[i]:
        computado[i][j] = 0



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



h_pos_Co = rt.TH3F('PosCo','PosCo;z;x;y',100,-1500,1500,100,-1500,1500,100,-1500,1500)
h_pos_K = rt.TH3F('PosK','PosK;z;x;y',100,-1500,1500,100,-1500,1500,100,-1500,1500)
h_pos_Bi = rt.TH3F('PosBi','PosBi;z;x;y',100,-1500,1500,100,-1500,1500,100,-1500,1500)
h_pos_Tl = rt.TH3F('PosTl','PosTl;z;x;y',100,-1500,1500,100,-1500,1500,100,-1500,1500)

for i in range(int(t.GetEntries())):
    t.GetEntry(i)
    if element[0] == 40:
        if not computado[element[0]][part[0]]>esperado[element[0]][part[0]]:
            h_pos_K.Fill(Zi[0],Xi[0],Yi[0])
            computado[element[0]][part[0]] += 1
    elif element[0] == 60:
        if not computado[element[0]][part[0]]>esperado[element[0]][part[0]]:
            computado[element[0]][part[0]] += 1
            h_pos_Co.Fill(Zi[0],Xi[0],Yi[0])
    elif element[0] == 214:
        if not computado[element[0]][part[0]]>esperado[element[0]][part[0]]:
            computado[element[0]][part[0]] += 1
            h_pos_Bi.Fill(Zi[0],Xi[0],Yi[0])
    elif element[0] == 208:
        if not computado[element[0]][part[0]]>esperado[element[0]][part[0]]:
            computado[element[0]][part[0]] += 1
            h_pos_Tl.Fill(Zi[0],Xi[0],Yi[0])


c1 = rt.TCanvas()
h_pos_Co.Draw()
c2 = rt.TCanvas()
h_pos_K.Draw()
c3 = rt.TCanvas()
h_pos_Bi.Draw()
c4 = rt.TCanvas()
h_pos_Tl.Draw()

raw_input('enter para salir')
