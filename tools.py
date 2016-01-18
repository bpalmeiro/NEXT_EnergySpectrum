from ROOT import *
from array import array
import numpy as np

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





def h_Gauss(hist):
    nbin = hist.GetNbinsX()

    hnew = CloneHist(hist,'Gauss')

    for i in range(1,nbin+1):
        Caux = hist.GetXaxis().GetBinCenter(i)
        naux = hist.GetBinContent(i)
        for j in range(int(naux)):
            hnew.Fill(Gaussianizator(Caux))
    return hnew
