import ROOT
from counting_experiment import *
# Define how a control region(s) transfer is made by defining *cmodel*, the calling pattern must be unchanged!
# First define simple string which will be used for the datacard 
model = "zg"

def cmodel(cid,nam,_f,_fOut, out_ws, diag):
  
  # Some setup
  _fin = _f.Get("category_%s"%cid)
  _wspace = _fin.Get("wspace_%s"%cid)

  # ############################ USER DEFINED ###########################################################
  # First define the nominal transfer factors (histograms of signal/control, usually MC 
  # note there are many tools available inside include/diagonalize.h for you to make 
  # special datasets/histograms representing these and systematic effects 
  # example below for creating shape systematic for photon which is just every bin up/down 30% 

  metname    = "phoPtHighMet"          # Observable variable name 

  target             = _fin.Get("signal_zg")      # define monimal (MC) of which process this config will model
  controlmc          = _fin.Get("dimu_zg")        # defines Zmm MC of which process will be controlled by
  controlmc_e        = _fin.Get("diel_zg")        # defines Zee MC of which process will be controlled by

  # Create the transfer factors and save them (not here you can also create systematic variations of these 
  # transfer factors (named with extention _sysname_Up/Down
  ZmmScales = target.Clone(); ZmmScales.SetName("dimu_weights_%s" %cid)
  ZmmScales.Divide(controlmc);  
  # for iBin in range(1, ZmmScales.GetNbinsX()+1):
  #   ZmmScales.SetBinError(iBin, 0.)
  _fOut.WriteTObject(ZmmScales)  # always write out to the directory 

  ZeeScales = target.Clone(); ZeeScales.SetName("diel_weights_%s" %cid)
  ZeeScales.Divide(controlmc_e);  
  # for iBin in range(1, ZeeScales.GetNbinsX()+1):
  #   ZeeScales.SetBinError(iBin, 0.)
  _fOut.WriteTObject(ZeeScales)  # always write out to the directory 

  #######################################################################################################

  _bins = []  # take bins from some histogram, can choose anything but this is easy 
  for b in range(target.GetNbinsX()+1):
    _bins.append(target.GetBinLowEdge(b+1))

  # Here is the important bit which "Builds" the control region, make a list of control regions which 
  # are constraining this process, each "Channel" is created with ...
  # 	(name,_wspace,out_ws,cid+'_'+model,TRANSFERFACTORS) 
  # the second and third arguments can be left unchanged, the others instead must be set
  # TRANSFERFACTORS are what is created above, eg WScales

  CRs = [
  Channel("dimu",_wspace,out_ws,cid+'_'+model,ZmmScales)
  ,Channel("diel",_wspace,out_ws,cid+'_'+model,ZeeScales)
  ]

  # ############################ USER DEFINED ###########################################################
  # Add systematics in the following, for normalisations use name, relative size (0.01 --> 1%)
  # for shapes use add_nuisance_shape with (name,_fOut)
  # note, the code will LOOK for something called NOMINAL_name_Up and NOMINAL_name_Down, where NOMINAL=WScales.GetName()
  # these must be created and writted to the same dirctory as the nominal (fDir)

  CRs[0].addUncorrStatSysts(target, ZmmScales, "dimu", "dimu", cid, _fOut)
  CRs[1].addUncorrStatSysts(target, ZeeScales, "diel", "diel", cid, _fOut)

  # lepSFSystSetup(_wspace, _fin, _fOut, cid)

  #######################################################################################################

  # CRs[0].add_nuisance_shape('muonSF', _fOut)
  # CRs[1].add_nuisance_shape('electronSF', _fOut)

  #######################################################################################################
  
  cat = Category(model,cid,nam,_fin,_fOut,_wspace,out_ws,_bins,metname,target.GetName(),CRs,diag)
  # Return of course
  return cat

def lepSFSystSetup(_wspace, _fin, _fOut, nam):
  
  target             = _fin.Get("signal_zg")      # define monimal (MC) of which process this config will model

  controlmc_SFUp     = _fin.Get("dimu_zg_muonSFUp")
  controlmc_SFDown   = _fin.Get("dimu_zg_muonSFDown")

  controlmc_e_SFUp     = _fin.Get("diel_zg_electronSFUp")
  controlmc_e_SFDown   = _fin.Get("diel_zg_electronSFDown")

  ZmmScalesSFUp = target.Clone(); ZmmScalesSFUp.SetName("dimu_weights_%s_muonSF_Up" %cid)
  ZmmScalesSFUp.Divide(controlmc_SFUp);  _fOut.WriteTObject(ZmmScalesSFUp)  # always write out to the directory 

  ZeeScalesSFUp = target.Clone(); ZeeScalesSFUp.SetName("diel_weights_%s_electronSF_Up" %cid)
  ZeeScalesSFUp.Divide(controlmc_e_SFUp);  _fOut.WriteTObject(ZeeScalesSFUp)  # always write out to the directory 

  ZmmScalesSFDown = target.Clone(); ZmmScalesSFDown.SetName("dimu_weights_%s_muonSF_Down" %cid)
  ZmmScalesSFDown.Divide(controlmc_SFDown);  _fOut.WriteTObject(ZmmScalesSFDown)  # always write out to the directory 

  ZeeScalesSFDown = target.Clone(); ZeeScalesSFDown.SetName("diel_weights_%s_electronSF_Down" %cid)
  ZeeScalesSFDown.Divide(controlmc_e_SFDown);  _fOut.WriteTObject(ZeeScalesSFDown)  # always write out to the directory 
