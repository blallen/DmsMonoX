import ROOT
from counting_experiment import *
# Define how a control region(s) transfer is made by defining *cmodel*, the calling pattern must be unchanged!
# First define simple string which will be used for the datacard 
model = "zjets"


# My Function. Just to put all of the complicated part into one function
def my_function(_wspace,_fin,_fOut,nam,diag):

  metname    = "met"    # Observable variable name 
  gvptname   = "genBos_pt"    # Weights are in generator pT
  wvarname   = "scaleMC_w"
  target     = _fin.Get("signal_zjets")      # define monimal (MC) of which process this config will model
  controlmc  = _fin.Get("Zmm_zll")  # defines in / out acceptance

  controlmc_photon   = _fin.Get("gjets_gjets")  # defines in / out acceptance

  _gjet_mcname 	= "gjets_gjets"
  GJet          = _fin.Get("gjets_gjets")

  fkFactor = r.TFile.Open("files/Photon_Z_NLO_kfactors_w80pcorr.root")
  nlo_pho = fkFactor.Get("pho_NLO_LO")
  nlo_zjt = fkFactor.Get("Z_NLO_LO")

  Pho = target.Clone(); Pho.SetName("photon_weights_denom_%s"%nam)
  for b in range(Pho.GetNbinsX()): Pho.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Pho,nlo_pho,gvptname,metname,_wspace.data(_gjet_mcname))

  Zvv = target.Clone(); Zvv.SetName("photon_weights_nom_%s"%nam)
  for b in range(Zvv.GetNbinsX()): Zvv.SetBinContent(b+1,0)
  diag.generateWeightedTemplate(Zvv,nlo_zjt,gvptname,metname,_wspace.data("signal_zjets"))

  PhotonOverZ = Pho.Clone(); PhotonOverZ.SetName("PhotonOverZNLO")
  PhotonOverZ.Divide(Zvv)
  PhotonOverZ.Multiply(target)
  PhotonOverZ.Divide(GJet)
  diag.generateWeightedDataset("photon_gjet_nlo",PhotonOverZ,wvarname,metname,_wspace,"gjets_gjets")

  PhotonSpectrum = Pho.Clone(); PhotonSpectrum.SetName("photon_spectrum_%s_"%nam)
  ZvvSpectrum 	 = Zvv.Clone(); ZvvSpectrum.SetName("zvv_spectrum_%s_"%nam)
  _fOut.WriteTObject( PhotonSpectrum )
  _fOut.WriteTObject( ZvvSpectrum )

  #################################################################################################################

  # Have to also add one per systematic variation :(, 
  Zvv.Divide(Pho); 		 Zvv.SetName("photon_weights_%s"%nam)

  PhotonScales = Zvv.Clone()
  _fOut.WriteTObject(PhotonScales)

def cmodel(cid,nam,_f,_fOut, out_ws, diag):
  
  # Some setup
  _fin = _f.Get("category_%s"%cid)
  _wspace = _fin.Get("wspace_%s"%cid)


  # ############################ USER DEFINED ###########################################################
  # First define the nominal transfer factors (histograms of signal/control, usually MC 
  # note there are many tools available inside include/diagonalize.h for you to make 
  # special datasets/histograms representing these and systematic effects 
  # example below for creating shape systematic for photon which is just every bin up/down 30% 

  metname = "met"    # Observable variable name 
  targetmc     = _fin.Get("signal_zjets")      # define monimal (MC) of which process this config will model
  controlmc    = _fin.Get("Zmm_zll")  # defines in / out acceptance

  controlmc_photon   = _fin.Get("gjets_gjets")  # defines in / out acceptance 

  # Create the transfer factors and save them (not here you can also create systematic variations of these 
  # transfer factors (named with extention _sysname_Up/Down
  ZmmScales = targetmc.Clone(); ZmmScales.SetName("zmm_weights_%s"%cid)
  ZmmScales.Divide(controlmc)
  _fOut.WriteTObject(ZmmScales)  # always write out to the directory 

  my_function(_wspace,_fin,_fOut,cid,diag)
  PhotonScales = _fOut.Get("photon_weights_%s"%cid)
  #######################################################################################################

  _bins = []  # take bins from some histogram, can choose anything but this is easy 
  for b in range(targetmc.GetNbinsX()+1):
    _bins.append(targetmc.GetBinLowEdge(b+1))

  # Here is the important bit which "Builds" the control region, make a list of control regions which 
  # are constraining this process, each "Channel" is created with ...
  # 	(name,_wspace,out_ws,cid+'_'+model,TRANSFERFACTORS) 
  # the second and third arguments can be left unchanged, the others instead must be set
  # TRANSFERFACTORS are what is created above, eg WScales

  CRs = [
   Channel("photon",_wspace,out_ws,cid+'_'+model,PhotonScales) 
  ,Channel("dimuon",_wspace,out_ws,cid+'_'+model,ZmmScales)
  #,Channel("wjetssignal",_wspace,out_ws,cid+'_'+model,WZScales)
  ]


  # ############################ USER DEFINED ###########################################################
  # Add systematics in the following, for normalisations use name, relative size (0.01 --> 1%)
  # for shapes use add_nuisance_shape with (name,_fOut)
  # note, the code will LOOK for something called NOMINAL_name_Up and NOMINAL_name_Down, where NOMINAL=WScales.GetName()
  # these must be created and writted to the same dirctory as the nominal (fDir)

  # Bin by bin nuisances to cover statistical uncertainties ...
#  for b in range(targetmc.GetNbinsX()):
#    err = PhotonScales.GetBinError(b+1)
#    if not PhotonScales.GetBinContent(b+1)>0: continue 
#    relerr = err/PhotonScales.GetBinContent(b+1)
#    if relerr<0.01: continue
#    byb_u = PhotonScales.Clone(); byb_u.SetName("photon_weights_%s_%s_stat_error_%s_bin%d_Up"%(cid,cid,"photonCR",b))
#    byb_u.SetBinContent(b+1,PhotonScales.GetBinContent(b+1)+err)
#    byb_d = PhotonScales.Clone(); byb_d.SetName("photon_weights_%s_%s_stat_error_%s_bin%d_Down"%(cid,cid,"photonCR",b))
#    byb_d.SetBinContent(b+1,PhotonScales.GetBinContent(b+1)-err)
#    _fOut.WriteTObject(byb_u)
#    _fOut.WriteTObject(byb_d)
#    print "Adding an error -- ", byb_u.GetName(),err
#    CRs[0].add_nuisance_shape("%s_stat_error_%s_bin%d"%(cid,"photonCR",b),_fOut)

#  for b in range(targetmc.GetNbinsX()):
#    err = ZmmScales.GetBinError(b+1)
#    if not ZmmScales.GetBinContent(b+1)>0: continue 
#    relerr = err/ZmmScales.GetBinContent(b+1)
#    if relerr<0.01: continue
#    byb_u = ZmmScales.Clone(); byb_u.SetName("zmm_weights_%s_%s_stat_error_%s_bin%d_Up"%(cid,cid,"dimuonCR",b))
#    byb_u.SetBinContent(b+1,ZmmScales.GetBinContent(b+1)+err)
#    byb_d = ZmmScales.Clone(); byb_d.SetName("zmm_weights_%s_%s_stat_error_%s_bin%d_Down"%(cid,cid,"dimuonCR",b))
#    byb_d.SetBinContent(b+1,ZmmScales.GetBinContent(b+1)-err)
#    _fOut.WriteTObject(byb_u)
#    _fOut.WriteTObject(byb_d)
#    print "Adding an error -- ", byb_u.GetName(),err
#    CRs[1].add_nuisance_shape("%s_stat_error_%s_bin%d"%(cid,"dimuonCR",b),_fOut)
  #######################################################################################################


  cat = Category(model,cid,nam,_fin,_fOut,_wspace,out_ws,_bins,metname,targetmc.GetName(),CRs,diag)
  # Return of course
  return cat

