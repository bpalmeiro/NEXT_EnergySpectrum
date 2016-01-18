from array import array
import ROOT as rt


rt.gStyle.SetOptStat(1111);
rt.gStyle.SetOptFit(1111111);

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

esperado ={60: {0 : 0 ,
                1 : 36,
                2 : 203,
                3 : 1,
                4 : 77,
                5 : 346,
                6 : 27,
                7 : 0,
                8 : 1850,
                9 : 16,
                10 : 1313,
                11 : 6,
                12 : 2726,
                13 : 128,
                14 : 3,
                15 : 833,
                16 : 11336
                },
           40: {0 : 38 ,
                1 : 200,
                2 : 19,
                3 : 28,
                4 : 7740,
                5 : 800,
                6 : 3,
                7 : 4,
                8 : 172,
                9 : 0,
                10 : 0,
                11 : 45,
                12 : 510,
                13 : 0,
                14 : 0,
                15 : 51,
                16 : 0
                },
          214: {0 : 92 ,
                1 : 18,
                2 : 32,
                3 : 56,
                4 : 421,
                5 : 212,
                6 : 4,
                7 : 39,
                8 : 289,
                9 : 40,
                10 : 86,
                11 : 111,
                12 : 135,
                13 : 375,
                14 : 2115,
                15 : 89,
                16 : 675
                },
          208: {0 : 21,
                1 : 3,
                2 : 7,
                3 : 52,
                4 : 95,
                5 : 46,
                6 : 1,
                7 : 7,
                8 : 6,
                9 : 15,
                10 : 83,
                11 : 53,
                12 : 103,
                13 : 129,
                14 : 684,
                15 : 19,
                16 : 591
                }


	}







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

h_el_Co = rt.TH1F('ElCo','ElCo',17,0,17)
h_el_K = rt.TH1F('ElK','ElK',17,0,17)
h_el_Bi = rt.TH1F('ElBi','ElBi',17,0,17)
h_el_Tl = rt.TH1F('ElTl','ElTl',17,0,17)


h_pos_Co = rt.TH3F('PosCo','PosCo;z;x;y',100,-1500,1500,100,-1500,1500,100,-1500,1500)
h_pos_K = rt.TH3F('PosK','PosK;z;x;y',100,-1500,1500,100,-1500,1500,100,-1500,1500)
h_pos_Bi = rt.TH3F('PosBi','PosBi;z;x;y',100,-1500,1500,100,-1500,1500,100,-1500,1500)
h_pos_Tl = rt.TH3F('PosTl','PosTl;z;x;y',100,-1500,1500,100,-1500,1500,100,-1500,1500)

for i in range(int(t.GetEntries())):
    t.GetEntry(i)
    if element[0] == 40:
        h_el_K.Fill(part[0])
        h_pos_K.Fill(Zi[0],Xi[0],Yi[0])
    elif element[0] == 60:
        h_el_Co.Fill(part[0])
        h_pos_Co.Fill(Zi[0],Xi[0],Yi[0])
    elif element[0] == 214:
        h_el_Bi.Fill(part[0])
        h_pos_Bi.Fill(Zi[0],Xi[0],Yi[0])
    elif element[0] == 208:
        h_el_Tl.Fill(part[0])
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
