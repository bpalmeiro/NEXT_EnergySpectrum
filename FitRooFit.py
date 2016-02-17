from array import array
import ROOT as rt


rt.gStyle.SetOptStat(1111)
rt.gStyle.SetOptFit(1111111)

E = rt.RooRealVar("E","E",0.5,3.)#

Ea = rt.RooArgList(E)
Eap = rt.RooArgSet(E)

ff = rt.TFile("Train_800.root","READONLY")

h_CoL    = ff.Get('Co_total_Gaussrebin')
h_KL     = ff.Get('K_total_Gaussrebin')
h_TlL    = ff.Get('Tl_total_Gaussrebin')
h_BiL    = ff.Get('Bi_total_Gaussrebin')
h_bb2nL  = ff.Get('bb2nu_Gaussrebin')
#ff.Close()



ffp = rt.TFile("Poissonizado_100.root","READONLY")
h_totalL = ffp.Get('total_Gaussrebin')
h_testnnL = ffp.Get('bb2nu_Gaussrebin')
tree = ffp.Get('t')


data = rt.RooDataSet("RealData","RealData",tree,rt.RooArgSet(E))
#ffp.Close()

h_Co    = rt.RooDataHist("h_Co","h_Co Gauss",Ea,h_CoL)
h_K     = rt.RooDataHist("h_K","h_K Gauss",Ea,h_KL)
h_Tl    = rt.RooDataHist("h_Tl","h_Tl Gauss",Ea,h_TlL)
h_Bi    = rt.RooDataHist("h_Bi","h_Bi Gauss",Ea,h_BiL)
h_bb2n  = rt.RooDataHist("h_bb2n","h_bb2n Gauss",Ea,h_bb2nL)
h_total = rt.RooDataHist("h_total","h_total Gauss",Ea,h_totalL)
h_testnn = rt.RooDataHist("h_bb","h_total bb",Ea,h_testnnL)

pdf_Co   = rt.RooHistPdf("pdf_Co","pdf_Co Gauss",rt.RooArgSet(E),h_Co)
pdf_K    = rt.RooHistPdf("pdf_K","pdf_K Gauss",rt.RooArgSet(E),h_K)
pdf_Tl   = rt.RooHistPdf("pdf_Tl","pdf_Tl Gauss",rt.RooArgSet(E),h_Tl)
pdf_Bi   = rt.RooHistPdf("pdf_Bi","pdf_Bi Gauss",rt.RooArgSet(E),h_Bi)
pdf_bb2n = rt.RooHistPdf("pdf_bb2nu","pdf_bb2n Gauss",rt.RooArgSet(E),h_bb2n)


n_Co   = rt.RooRealVar("n_Co","n_Co",0,0,1000000)
n_K    = rt.RooRealVar("n_K","n_K",0,0,1000000)
n_Tl   = rt.RooRealVar("n_Tl","n_Tl",0,0,1000000)
n_Bi   = rt.RooRealVar("n_Bi","n_Bi",0,0,1000000)
n_bb2n = rt.RooRealVar("n_bb2nu","n_bb2ny",1000000,0,1000000)


model = rt.RooAddPdf('model','model',rt.RooArgList(pdf_Co,pdf_K,pdf_Tl,pdf_Bi,pdf_bb2n),rt.RooArgList(n_Co,n_K,n_Tl,n_Bi,n_bb2n))




mean = rt.RooRealVar('mean','mean',-20,20)
#model = rt.RooExponential('asdas','asdasd',E,mean)
fit = model.fitTo(h_total,rt.RooFit.Save(),rt.RooFit.Extended())

frame = E.frame(rt.RooFit.Title(""))

h_total.plotOn(frame)

model.plotOn(frame)

model.plotOn(frame,rt.RooFit.Components("pdf_Co"),rt.RooFit.FillStyle(1001),rt.RooFit.FillColor(rt.kCyan-8),rt.RooFit.DrawOption("F"))
model.plotOn(frame,rt.RooFit.Components("pdf_K"),rt.RooFit.FillStyle(1001),rt.RooFit.FillColor(rt.kOrange-9),rt.RooFit.DrawOption("F"))
model.plotOn(frame,rt.RooFit.Components("pdf_Bi"),rt.RooFit.FillStyle(1001),rt.RooFit.FillColor(rt.kMagenta-10),rt.RooFit.DrawOption("F"))
model.plotOn(frame,rt.RooFit.Components("pdf_Tl"),rt.RooFit.FillStyle(3001),rt.RooFit.FillColor(rt.kOrange+1),rt.RooFit.DrawOption("F"))
model.plotOn(frame,rt.RooFit.Components("pdf_bb2nu"),rt.RooFit.LineColor(12),rt.RooFit.LineStyle(1))

#frame.SetLogy
frame.Draw()
'''
h_Co.plotOn(frame)
h_K.plotOn(frame)
h_Bi.plotOn(frame)
h_Tl.plotOn(frame)
h_bb2n.plotOn(frame)
'''

h_testnn.plotOn(frame)
frame.Draw()
