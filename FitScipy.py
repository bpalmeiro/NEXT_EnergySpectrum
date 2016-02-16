from array import array
import ROOT as rt
import scipy
import scipy.optimize

def Normalize( h ):
    h.Scale( 1.0/ h.Integral() )
    return h

E   = rt.RooRealVar("E","E",0.5,3.0)
Ea  = rt.RooArgList(E)
Eap = rt.RooArgSet(E)

Ftrain   = rt.TFile("TrainSet_800days.root","READONLY")
#print Ftrain.ls()
Cotrain  = Normalize( Ftrain.Get('Co60_total_Gauss_rebin') )
Ktrain   = Normalize( Ftrain.Get('K40_total_Gauss_rebin') )
Tltrain  = Normalize( Ftrain.Get('Tl208_total_Gauss_rebin') )
Bitrain  = Normalize( Ftrain.Get('Bi214_total_Gauss_rebin') )
BBtrain  = Normalize( Ftrain.Get('bb2nu_Gauss_rebin') )

Ftest  = rt.TFile("TestSet_100days.root","READONLY")
Htest  = Ftest.Get('total_Gauss_rebin')
BBtest = Ftest.Get('bb2nu_Gauss_rebin')



h_Co     = rt.RooDataHist("h_Co","h_Co Gauss",Ea,Cotrain)
h_K      = rt.RooDataHist("h_K","h_K Gauss",Ea,Ktrain)
h_Tl     = rt.RooDataHist("h_Tl","h_Tl Gauss",Ea,Tltrain)
h_Bi     = rt.RooDataHist("h_Bi","h_Bi Gauss",Ea,Bitrain)
h_bb2n   = rt.RooDataHist("h_bb2n","h_bb2n Gauss",Ea,BBtrain)
data     = rt.RooDataSet("RealData","RealData",Ftest.Get('t'),rt.RooArgSet(E))


pdf_Co   = rt.RooHistPdf("pdf_Co","pdf_Co Gauss",rt.RooArgSet(E),h_Co)
pdf_K    = rt.RooHistPdf("pdf_K","pdf_K Gauss",rt.RooArgSet(E),h_K)
pdf_Tl   = rt.RooHistPdf("pdf_Tl","pdf_Tl Gauss",rt.RooArgSet(E),h_Tl)
pdf_Bi   = rt.RooHistPdf("pdf_Bi","pdf_Bi Gauss",rt.RooArgSet(E),h_Bi)
pdf_bb2n = rt.RooHistPdf("pdf_bb2nu","pdf_bb2n Gauss",rt.RooArgSet(E),h_bb2n)

xbins = range(1,Htest.GetNbinsX()+1)
def LLH(ns):
    nCo, nK, nTl, nBi, nBB = ns
    llh = 0.
    for i in xbins:
        x  = nCo * Cotrain.GetBinContent(i)
        x += nK  * Ktrain .GetBinContent(i)
        x += nTl * Tltrain.GetBinContent(i)
        x += nBi * Bitrain.GetBinContent(i)
        x += nBB * BBtrain.GetBinContent(i)
        if not x: continue
        llh -= Htest.GetBinContent(i) * scipy.log(x)
    return llh

#initial_guess = scipy.array( [3e3,2e3,3e2,1e3,1e3] )
initial_guess = scipy.array( [3e5,2e5,3e5,1e5,1e3] )
# initial_guess = scipy.array( [3e0,2e0,3e0,1e0,1e4] )
minimize_output = scipy.optimize.minimize( LLH, initial_guess, tol = 1e-8 )
result = minimize_output.x
success = minimize_output.success
message = minimize_output.message
print 'RESULT',result, success, message

n_Co   = rt.RooRealVar("n_Co","n_Co",result[0],0,1000000)
n_K    = rt.RooRealVar("n_K","n_K",result[1],0,1000000)
n_Tl   = rt.RooRealVar("n_Tl","n_Tl",result[2],0,1000000)
n_Bi   = rt.RooRealVar("n_Bi","n_Bi",result[3],0,1000000)
n_bb2n = rt.RooRealVar("n_bb2nu","n_bb2ny",result[4],0,1000000)

# n_Co   = rt.RooRealVar("n_Co","n_Co",3724,0,1000000)
# n_K    = rt.RooRealVar("n_K","n_K",1746,0,1000000)
# n_Tl   = rt.RooRealVar("n_Tl","n_Tl",383,0,1000000)
# n_Bi   = rt.RooRealVar("n_Bi","n_Bi",956,0,1000000)
# n_bb2n = rt.RooRealVar("n_bb2nu","n_bb2ny",1142,0,1000000)


model = rt.RooAddPdf('model','model',rt.RooArgList(pdf_Co,pdf_K,pdf_Tl,pdf_Bi,pdf_bb2n),rt.RooArgList(n_Co,n_K,n_Tl,n_Bi,n_bb2n))

Htest0  = rt.RooDataHist("Htest0","Htest0",Ea,Htest)
Htest1  = rt.RooHistPdf ("Htest1","Htest1",rt.RooArgSet(E),Htest0)
BBtest0 = rt.RooDataHist("BBtest0","BBtest0",Ea,BBtest)
BBtest1 = rt.RooHistPdf ("BBtest1","BBtest1",rt.RooArgSet(E),BBtest0)

frame = E.frame(rt.RooFit.Title(""))
# Htest1.plotOn(frame)
# BBtest1.plotOn(frame)
data.plotOn(frame,rt.RooFit.Binning(125))
model.plotOn(frame)
model.plotOn(frame,rt.RooFit.Components("pdf_Co"),rt.RooFit.FillStyle(1001),rt.RooFit.FillColor(rt.kCyan-8),rt.RooFit.DrawOption("F"))
model.plotOn(frame,rt.RooFit.Components("pdf_K"),rt.RooFit.FillStyle(1001),rt.RooFit.FillColor(rt.kOrange-9),rt.RooFit.DrawOption("F"))
model.plotOn(frame,rt.RooFit.Components("pdf_Bi"),rt.RooFit.FillStyle(1001),rt.RooFit.FillColor(rt.kMagenta-10),rt.RooFit.DrawOption("F"))
model.plotOn(frame,rt.RooFit.Components("pdf_Tl"),rt.RooFit.FillStyle(3001),rt.RooFit.FillColor(rt.kOrange+1),rt.RooFit.DrawOption("F"))
model.plotOn(frame,rt.RooFit.Components("pdf_bb2nu"),rt.RooFit.LineColor(12),rt.RooFit.LineStyle(1))


frame.Draw()

raw_input('done')
