from array import array
import ROOT as rt
import random as rd
import numpy as np
from operator import concat
from tools import *
from estimation import estimation

#################################
### Job parameters
#################################
poissonize = False
DataInfoFilename = 'DataInfo.dat'
BBFile = 'bb2nu.root'
BkgFile = 'BgrClass.root'
outputfile = 'Poisson_100_80_80.root'

rt.gStyle.SetOptStat(1111);
rt.gStyle.SetOptFit(1111111);

# Histograms parameters
nBin = 500
Emin = 0.
Emax = 3.

mass = 5.81   # Xe mass in kg
purity = 0.91 # Ratio of 136Xe
trun = 100.   # Data taking time in days

BgrRej = 0.2 # Background rejection factor
SigEff = 0.8 # Signal efficiency factor

rand = rt.TRandom3(0)

# Double beta efficiency and expected number of events
BBeff = 0.695197
Nbb2n = int( round( estimation(mass,purity,trun) * BBeff * SigEff ) )
if poissonize:
    Nbb2n = rand.Poisson(Nbb2n)

texp = trun * 24 * 3600 # Exposition time in s

# "element" branch map
elementdic = { 60 : 'Co60',
              208 : 'Tl208',
              214 : 'Bi214',
               40 : 'K40'}

# "part" branch map
partdic = { 0 :'ANODE_QUARTZ ',
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

partdic = { 0 :'ANODE_QUARTZ ',
            1 :'BUFFER_TUBE ',
            2 :'CARRIER_PLATE ',
            3 :'DB_PLUG ',
            4 :'DICE_BOARD ',
            5 :'DRIFT_TUBE ',
            6 :'ENCLOSURE_BODY ',
            7 :'ENCLOSURE_WINDOW ',
            8 :'ICS ',
            9 :'OPTICAL_PAD ',
           10 :'PEDESTAL ',
           11 :'PMT_BASE ',
           12 :'PMT_BODY ',
           13 :'SHIELDING_LEAD ',
           14 :'SHIELDING_STRUCT ',
           15 :'SUPPORT_PLATE ',
           16 :'VESSEL '
    
    }

# Expected number of events
expected = { element : { part : {} for part in partdic } for element in elementdic }
for element, part, ratio, activity in np.loadtxt(DataInfoFilename):
    expected[element][part] = int( round( ratio * activity * 0.001 * texp * BgrRej ) )

# Deposited energy per part and element
Epos = { element : { part : [] for part in partdic } for element in elementdic }


######## Tree reading
ff = rt.TFile(BkgFile,'READONLY')
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


### Histogram booking
histos = { i : { j : rt.TH1F( '_'.join(( el, pt )), '_'.join(( el, pt )), nBin, Emin, Emax ) for j,pt in partdic.items() } for i,el in elementdic.items() }
h_part = { j : rt.TH1F( 'total_'+pt, 'total_'+pt, nBin, Emin, Emax ) for j,pt in partdic.items() }
h_elem = { i : rt.TH1F( el + '_total', el + '_total', nBin, Emin, Emax ) for i,el in elementdic.items() }

h_bkg   = rt.TH1F( 'total_bkg', 'total_bkg', nBin, Emin, Emax )
h_total = rt.TH1F( 'total'    , 'total'    , nBin, Emin, Emax )


### Get data from trees and arrange them in the dictionary
for i in range(int(t.GetEntries())):
    t.GetEntry(i)
    Epos[element[0]][part[0]].append(E[0])


### Get double beta data
bb2nfile = rt.TFile( BBFile, 'readonly' )
bt = bb2nfile.Get('t')
E2nur = array('f',[0.])
bt.SetBranchAddress('E',E2nur)
E2nu = []

h_bb2n = rt.TH1F( 'bb2nu', 'bb2nu', nBin, Emin, Emax )
for i in range(int(bt.GetEntries())):
    bt.GetEntry(i)
    E2nu.append(E2nur[0])


# Shuffle BB events and choose Nbb2n events (randomly).
# Fill the histogram with them.
rd.shuffle(E2nu)
E2nu = E2nu[:Nbb2n]
map( h_bb2n.Fill, E2nu )


# Fill histograms with data
for i,el in Epos.items():
    for j,events in el.items():
        rd.shuffle(events)
        el[j] = events[:expected[i][j]]
        map( histos[i][j].Fill, el[j] )

# Compute cumulative histograms
for j,h in h_part.items():
    for i in elementdic:
        h.Add( histos[i][j] )

for i,h in h_elem.items():
    map( h.Add, histos[i].values() )

map( h_bkg.Add, h_elem.values() )
h_total.Add( h_bkg )
h_total.Add( h_bb2n )

# Bunch of original histograms
h0 = [ h_total, h_bkg, h_bb2n ] + h_elem.values() + h_part.values() + reduce( concat, map( dict.values, histos.values() ) )

# Create gaussianly smeared histograms
h_gaus = map( h_Gauss, h0 )

# Same histograms rebined
h_rebin = map( lambda h: h.Clone( h.GetName() + '_rebin' ).Rebin(4), h_gaus )

of = rt.TFile(outputfile,'recreate')
t = rt.TTree('t','tree')
E = array('f',[0.])
t.Branch('E',E,'E')

for i,el in Epos.items():
    for j,events in el.items():
        for En in events:
            E[0] = En
            t.Fill()

### Save to file
map( lambda h: h.SetDirectory(of), h0 + h_gaus + h_rebin )

of.Write()
of.Close()
ff.Close()
bb2nfile.Close()


for i in elementdic:
    for j in partdic:
        print i,j,partdic[j],len(Epos[i][j]),expected[i][j]
