import ROOT
from counting_experiment import *
# Define how a control region(s) transfer is made by defining cmodel provide, the calling pattern must be unchanged!
# First define simple string which will be used for the datacard 
model = "wg"
def cmodel(cid,nam,_f,_fOut, out_ws, diag):
  
  # Some setup
  _fin    = _f.Get("category_%s"%cid)
  _wspace = _fin.Get("wspace_%s"%cid)


  # ############################ USER DEFINED ###########################################################
  # First define the nominal transfer factors (histograms of signal/control, usually MC 
  # note there are many tools available inside include/diagonalize.h for you to make 
  # special datasets/histograms representing these and systematic effects 
  # but for now this is just kept simple 
  processName  = "wg" # Give a name of the process being modelled
  metname      = "phoPtHighMet"    # Observable variable name 
  targetmc     = _fin.Get("signal_wg")      # define monimal (MC) of which process this config will model
  controlmc    = _fin.Get("monolep_wg")  # defines in / out acceptance

  controlmc_muonSFUp    = _fin.Get("monolep_wg_muonSFUp")  
  controlmc_muonSFDown  = _fin.Get("monolep_wg_muonSFDown")  

  controlmc_electronSFUp    = _fin.Get("monolep_wg_electronSFUp")  
  controlmc_electronSFDown  = _fin.Get("monolep_wg_electronSFDown")  

  # Create the transfer factors and save them (not here you can also create systematic variations of these 
  # transfer factors (named with extention _sysname_Up/Down
  WlnScales = targetmc.Clone(); WlnScales.SetName("monolep_weights_%s"%cid)
  WlnScales.Divide(controlmc);  _fOut.WriteTObject(WlnScales)  # always write out to the directory 

  ## Lepton Scale factors
  """
  WlnScalesSFUp = targetmc.Clone(); WlnScalesSFUp.SetName("monolep_weights_%s_muonSF_Up" %cid)
  WlnScalesSFUp.Divide(controlmc_SFUp);  _fOut.WriteTObject(WlnScalesSFUp)  # always write out to the directory 

  WlnScalesSFUp = targetmc.Clone(); WlnScalesSFUp.SetName("monolep_weights_%s_electronSF_Up" %cid)
  WlnScalesSFUp.Divide(controlmc_e_SFUp);  _fOut.WriteTObject(WlnScalesSFUp)  # always write out to the directory 

  WlnScalesSFDown = targetmc.Clone(); WlnScalesSFDown.SetName("monolep_weights_%s_muonSF_Down" %cid)
  WlnScalesSFDown.Divide(controlmc_SFDown);  _fOut.WriteTObject(WlnScalesSFDown)  # always write out to the directory 

  WlnScalesSFDown = targetmc.Clone(); WlnScalesSFDown.SetName("monolep_weights_%s_electronSF_Down" %cid)
  WlnScalesSFDown.Divide(controlmc_e_SFDown);  _fOut.WriteTObject(WlnScalesSFDown)  # always write out to the directory 
  """
  #######################################################################################################

  _bins = []  # take bins from some histogram, can choose anything but this is easy 
  for b in range(targetmc.GetNbinsX()+1):
    _bins.append(targetmc.GetBinLowEdge(b+1))

  # Here is the important bit which "Builds" the control region, make a list of control regions which 
  # are constraining this process, each "Channel" is created with ...
  # 	(name,_wspace,out_ws,cid+'_'+model,TRANSFERFACTORS) 
  # the second and third arguments can be left unchanged, the others instead must be set
  # TRANSFERFACTORS are what is created above, eg WlnScales

  CRs = [
   Channel("monolep",_wspace,out_ws,cid+'_'+model,WlnScales),
  ]


  # ############################ USER DEFINED ###########################################################
  # Add systematics in the following, for normalisations use name, relative size (0.01 --> 1%)
  # for shapes use add_nuisance_shape with (name,_fOut)
  # note, the code will LOOK for something called NOMINAL_name_Up and NOMINAL_name_Down, where NOMINAL=WlnScales.GetName()
  # these must be created and writted to the same dirctory as the nominal (fDir)

  # Statistical uncertainties too!, one per bin 
  for b in range(targetmc.GetNbinsX()):
    err = WlnScales.GetBinError(b+1)
    if not WlnScales.GetBinContent(b+1)>0: continue 
    relerr = err/WlnScales.GetBinContent(b+1)
    if relerr<0.001: continue
    byb_u = WlnScales.Clone(); byb_u.SetName("monolep_weights_%s_%s_stat_error_%s_bin%d_Up"%(cid,cid,"monolepCR",b))
    byb_u.SetBinContent(b+1,WlnScales.GetBinContent(b+1)+err)
    byb_d = WlnScales.Clone(); byb_d.SetName("monolep_weights_%s_%s_stat_error_%s_bin%d_Down"%(cid,cid,"monolepCR",b))
    byb_d.SetBinContent(b+1,WlnScales.GetBinContent(b+1)-err)
    _fOut.WriteTObject(byb_u)
    _fOut.WriteTObject(byb_d)
    print "Adding an error -- ", byb_u.GetName(),err
    CRs[0].add_nuisance_shape("%s_stat_error_%s_bin%d"%(cid,"monolepCR",b),_fOut)


  #######################################################################################################

  # CRs[0].add_nuisance_shape('muonSF', _fOut)
  # CRs[0].add_nuisance_shape('electronSF', _fOut)

  #######################################################################################################

  cat = Category(model,cid,nam,_fin,_fOut,_wspace,out_ws,_bins,metname,targetmc.GetName(),CRs,diag)

  # cat.setDependant("zg","wgsignal")  # Can use this to state that the "BASE" of this is already dependant on another process
  # EG if the W->lv in signal is dependant on the Z->vv and then the W->mv is depenant on W->lv, then 
  # give the arguments model,channel name from the config which defines the Z->vv => W->lv map! 
  # Return of course

  return cat

