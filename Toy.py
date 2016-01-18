from tools import *
#from TrackPlotter import *
import ROOT as rt

Fermi = rt.TF1('Fermi','[0]*sqrt(x^2+2*x*[1])*([2]-x)^2*(x+[1])*1',0,2.5)

Fermi.SetParameter(0,1)
Fermi.SetParameter(1,0.511)
Fermi.SetParameter(2,2.5)



bb2nfile = rt.TFile('bb2nu.root')
bb0nfile = rt.TFile('bb0nu.root')

h2nusin = bb2nfile.Get('MCE')
h0nusin = bb0nfile.Get('MCE')

nbins2 = h2nusin.GetNbinsX()
nbins0 = h0nusin.GetNbinsX()

h2nu = rt.TH1D("bb2#nu","bb2#nu",1000,0,2.5)
h0nu = rt.TH1D("bb0#nu","bb0#nu",1000,0,2.5)

for i in range(1,nbins2+1):
    Eaux2 = h2nusin.GetXaxis().GetBinCenter(i)
    naux2 = h2nusin.GetBinContent(i)
    for j in range(int(naux2)):
        h2nu.Fill(Gaussianizator(Eaux2))

    Eaux0 = h0nusin.GetXaxis().GetBinCenter(i)
    naux0 = h0nusin.GetBinContent(i)
    for j in range(int(naux0)):
        h0nu.Fill(Gaussianizator(Eaux0))
c = rt.TCanvas()
c.Divide(1,2)
c.cd(1)
h0nusin.Draw()
h0nu.SetLineColor(2)
h0nu.Draw('same')
h2nusin.SetLineColor(3)
h2nusin.Draw('same')
h2nu.SetLineColor(4)
h2nu.Draw('same')

h_E = rt.TH1D("Energy_spectrum","Energy_spectrum",1000,0,2.5)
h_E.Add(h2nu,h0nu,1,1)
c.cd(2)
h_E.Draw()
