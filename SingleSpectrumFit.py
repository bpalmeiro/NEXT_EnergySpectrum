import ROOT as rt


rt.gStyle.SetOptStat(1111)
rt.gStyle.SetOptFit(1111111)

E = rt.RooRealVar("E","E",0.,3.0)#

Ea = rt.RooArgList(E)
Eap = rt.RooArgSet(E)

Ftrain = rt.TFile("TrainSet.root","READONLY")
Ftest  = rt.TFile("TestSet.root","READONLY")

h_pdf  = Ftrain.Get('K40_total_Gauss_rebin')
h_test = Ftest .Get('K40_total_Gauss_rebin')

N0 = h_test.GetEntries()

h_pdf  = rt.RooDataHist("h_pdf","h_pdf",Ea,h_pdf)
h_test = rt.RooDataHist("h_test","h_test",Ea,h_test)
pdf    = rt.RooHistPdf("pdf","pdf",rt.RooArgSet(E),h_pdf)

N = rt.RooRealVar("N","N",1e3,0,1000000)
model = rt.RooAddPdf('model','model',rt.RooArgList(pdf),rt.RooArgList(N))

fit = model.fitTo(h_test,rt.RooFit.Save())
fit.Print('v')

frame = E.frame(rt.RooFit.Title(""))

h_test.plotOn(frame)
model.plotOn(frame)

frame.Draw()
rt.gPad.SetLogy()

print N0
raw_input('ok')