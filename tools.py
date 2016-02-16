from ROOT import *
from array import array
import numpy as np
import random as rd


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


def CreateGraph(x,y):
    return TGraph(len(x),array('f',x),array('f',y))

def Plot4D( x, y, z, t, markerstyle = 20, markersize = 1 ):
    '''
        Plot a 3D dataset (x,y,z) with an extra color coordinate (t).
    '''
    data = array( 'd', [0.] * 4 )
    tree = TTree('DummyTree','DummyTree')
    tree.Branch('xyzt', data, 'x/D:y:z:t')

    for datai in zip(x,y,z,t):
        data[0], data[1], data[2], data[3] = datai
        tree.Fill()
    tree.SetMarkerStyle( markerstyle )
    tree.SetMarkerSize( markersize )
    c = TCanvas()
    tree.Draw('x:y:z:t','','zcol')
    return c, tree

def ReadData( prefijo ):
    Ef = open(prefijo+'E.dat', 'r')
    Xf = open(prefijo+'x.dat','r')
    Yf = open(prefijo+'y.dat','r')
    Zf = open(prefijo+'z.dat','r')
    ChiRf = open(prefijo+'chi2R.dat','r')
    ChiNf = open(prefijo+'chi2N.dat','r')

    for E,x,y,z,chiR,chiN in zip(Ef,Xf,Yf,Zf,ChiRf,ChiNf):
        x = np.array(map(float,x.split()))
        y = np.array(map(float,y.split()))
        z = np.array(map(float,z.split()))
        E = np.array(map(float,E.split()))
        dE = np.array([E[i]-E[i+1] for i in range(len(E)-1)] + [E[-1]])
        chiR = np.array(map(float,chiR.split()))
        chiN = np.array(map(float,chiN.split()))
        yield x,y,z,E,dE,chiR,chiN
    Ef.close()
    Xf.close()
    Yf.close()
    Zf.close()
    ChiRf.close()
    ChiNf.close()

def rval(x,y,nhits=None):
    if nhits==None:
        nhits = min(len(x),len(y))
    x = np.array(x[:nhits])
    y = np.array(y[:nhits])
    xm = np.mean(x)
    ym = np.mean(y)
    dx = x - xm
    dy = y - ym
    r = np.dot(dx,dy)/( sum(dx**2) * sum(dy**2) )**0.5
    return r

rand = TRandom3(0);
def Gaussianizator(E,sigma = -1):

    if sigma<0:
        sigma = SigmaEstimator(E)
    return rand.Gaus(E,sigma)

def SigmaEstimator(E):
    rlim = 0.01     #res en Q_bb
    qbb = 2.458     #MeV

    return rlim*(qbb*E)**0.5/2.35482

def CloneHist(hist,name = 'clone',nbin = None):
    if nbin == None:
        nbin = hist.GetNbinsX()
    #if (hist == NULL) return NULL;
    return TH1F(hist.GetName()+"_"+name,hist.GetTitle()+"_"+name, nbin ,hist.GetXaxis().GetXmin(),hist.GetXaxis().GetXmax())





def h_Gauss(hist,sigma = -1):
    nbin = hist.GetNbinsX()

    hnew = CloneHist(hist,'Gauss')

    for i in range(1,nbin+1):
        Caux = hist.GetXaxis().GetBinCenter(i)
        naux = hist.GetBinContent(i)
        for j in range(int(naux)):
            hnew.Fill(Gaussianizator(Caux,sigma))
    return hnew





def GetFitHist(Epos,E2nu,esperado,Nbb2n,minE = 0.,maxE = 3.,bin = 500):
    rand = TRandom(0)
    h_Etot = TH1F('h_Etot','h_Etot',500,minE,maxE)
    h_bb2n = TH1F('h_bb2n','h_bb2n',500,minE,maxE)
    n = {}
    for i in Epos:
        n[i] = {}
        n[i]['real'] = 0
        n[i]['pois'] = 0

    nn = 1
    for tt in range(nn):

        for i in Epos:
            for j in filedic:
                rd.shuffle(Epos[i][j])
                n[i]['real'] += esperado[i][j]

                for k in Epos[i][j][:(esperado[i][j])]: #rand.Poisson
                    #if k >1.5 and k<2.7:
                        n[i]['pois'] += 1
                        h_Etot.Fill(k)

                #print j, ' : ', esperado[i][j], '  ', len(Epos[i][j])
                #print n[i]

        rd.shuffle(E2nu)
        n['bb'] = {}
        n['bb']['real'] = Nbb2n
        n['bb']['pois'] = 0
        for i in E2nu[:rand.Poisson(Nbb2n)]:
            n['bb']['pois'] += 1
            h_Etot.Fill(i)
            h_bb2n.Fill(i)
        #print tt

    #h_Etot.Scale(1./nn)
    #h_bb2n.Scale(1./nn)

    return h_Gauss(h_Etot).Rebin(4),h_Gauss(h_bb2n).Rebin(4),n



def FitFit(Epos,E2nu,trainfile,esperado,Nbb2n,minE = 0.,maxE = 3.,bin = 100):

    E = RooRealVar("E","E",0.5,3.)#
    Ea = RooArgList(E)
    Eap = RooArgSet(E)

    ff = TFile(trainfile,"READONLY")

    h_CoL    = ff.Get('Co_total_Gaussrebin')
    h_KL     = ff.Get('K_total_Gaussrebin')
    h_TlL    = ff.Get('Tl_total_Gaussrebin')
    h_BiL    = ff.Get('Bi_total_Gaussrebin')
    h_bb2nL  = ff.Get('bb2nu_Gaussrebin')

    h_totalL,h_testnnL,n = GetFitHist(Epos,E2nu,esperado,Nbb2n,minE,maxE,bin)

    ntotr = 0
    ntot = 0

    for i in n:
        ntotr += n[i]['real']
        ntot += n[i]['pois']
    n['tot'] = {}
    n['tot']['real'] = ntotr
    n['tot']['pois'] = ntot

    h_Co    = RooDataHist("h_Co","h_Co Gauss",Ea,h_CoL)
    h_K     = RooDataHist("h_K","h_K Gauss",Ea,h_KL)
    h_Tl    = RooDataHist("h_Tl","h_Tl Gauss",Ea,h_TlL)
    h_Bi    = RooDataHist("h_Bi","h_Bi Gauss",Ea,h_BiL)
    h_bb2n  = RooDataHist("h_bb2n","h_bb2n Gauss",Ea,h_bb2nL)
    h_total = RooDataHist("h_total","h_total Gauss",Ea,h_totalL)
    h_testnn = RooDataHist("h_bb","h_total bb",Ea,h_testnnL)

    pdf_Co   = RooHistPdf("pdf_Co","pdf_Co Gauss",Eap,h_Co)
    pdf_K    = RooHistPdf("pdf_K","pdf_K Gauss",Eap,h_K)
    pdf_Tl   = RooHistPdf("pdf_Tl","pdf_Tl Gauss",Eap,h_Tl)
    pdf_Bi   = RooHistPdf("pdf_Bi","pdf_Bi Gauss",Eap,h_Bi)
    pdf_bb2n = RooHistPdf("pdf_bb2nu","pdf_bb2n Gauss",Eap,h_bb2n)


    n_Co   = RooRealVar("n_Co","n_Co",0.0001,0.,ntot)
    n_K    = RooRealVar("n_K","n_K",0.0001,0.,ntot)
    n_Tl   = RooRealVar("n_Tl","n_Tl",0.0001,0.,ntot)
    n_Bi   = RooRealVar("n_Bi","n_Bi",0.0001,0.,ntot)
    n_bb2n = RooRealVar("n_bb2nu","n_bb2ny",n['bb']['real'],0,1000000)


    model = RooAddPdf('model','model',RooArgList(pdf_Co,pdf_K,pdf_Tl,pdf_Bi,pdf_bb2n),RooArgList(n_Co,n_K,n_Tl,n_Bi,n_bb2n))
    #model = RooAddPdf('model','model',RooArgList(pdf_K,pdf_Tl,pdf_Bi,pdf_bb2n),RooArgList(n_K,n_Tl,n_Bi,n_bb2n))

    fit = model.fitTo(h_total,RooFit.Extended()) #l,RooFit.Extended()

    frame = E.frame(RooFit.Title(""))
    h_total.plotOn(frame)
    model.plotOn(frame)

    model.plotOn(frame,RooFit.Components("pdf_Co"),RooFit.FillStyle(1001),RooFit.FillColor(kCyan-8),RooFit.DrawOption("F"))
    model.plotOn(frame,RooFit.Components("pdf_K"),RooFit.FillStyle(1001),RooFit.FillColor(kOrange-9),RooFit.DrawOption("F"))
    model.plotOn(frame,RooFit.Components("pdf_Bi"),RooFit.FillStyle(1001),RooFit.FillColor(kMagenta-10),RooFit.DrawOption("F"))
    model.plotOn(frame,RooFit.Components("pdf_Tl"),RooFit.FillStyle(3001),RooFit.FillColor(kOrange+1),RooFit.DrawOption("F"))
    model.plotOn(frame,RooFit.Components("pdf_bb2nu"),RooFit.LineColor(12),RooFit.LineStyle(1))

    #frame.SetLogy
    #frame.Draw()

    '''
    h_Co.plotOn(frame)
    h_K.plotOn(frame)
    h_Bi.plotOn(frame)
    h_Tl.plotOn(frame)
    h_bb2n.plotOn(frame)
    '''

    h_testnn.plotOn(frame)
    frame.Draw()
    #print esperado
    #print n
    raw_input()
    nfit = {}
    nfit[40]  = {'val':n_K.getVal(),'err': n_K.getError() }
    nfit[60]  = {'val':n_Co.getVal(),'err': n_Co.getError() }
    nfit[208] = {'val':n_Tl.getVal(),'err': n_Tl.getError() }
    nfit[214] = {'val':n_Bi.getVal(),'err': n_Bi.getError() }
    nfit['bb'] = {'val':n_bb2n.getVal(), 'err': n_bb2n.getError()}
    #raw_input('cac')
    return n,nfit

def GetPullVars(n,nfit):
    pulldata = {}

    #error = {}
    for i in nfit:
        pulldata[i] = {}
        pulldata[i]['pull'] = (n[i]['pois']-nfit[i]['val'])/nfit[i]['err']
        pulldata[i]['val'] = nfit[i]['val']
        pulldata[i]['err'] = nfit[i]['err']
        #error[i] =

    return pulldata#,error
