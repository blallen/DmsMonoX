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
  controlmc    = _fin.Get("monomu_wg")  # defines in / out acceptance
  controlmc_e  = _fin.Get("monoel_wg")  # defines in / out acceptance

  controlmc_SFUp    = _fin.Get("monomu_wg_muonSFUp")  
  controlmc_SFDown  = _fin.Get("monomu_wg_muonSFDown")  

  controlmc_e_SFUp    = _fin.Get("monoel_wg_electronSFUp")  
  controlmc_e_SFDown  = _fin.Get("monoel_wg_electronSFDown")  

  # Create the transfer factors and save them (not here you can also create systematic variations of these 
  # transfer factors (named with extention _sysname_Up/Down
  WmnScales = targetmc.Clone(); WmnScales.SetName("monomu_weights_%s"%cid)
  WmnScales.Divide(controlmc);  _fOut.WriteTObject(WmnScales)  # always write out to the directory 

  WenScales = targetmc.Clone(); WenScales.SetName("monoel_weights_%s"%cid)
  WenScales.Divide(controlmc_e);  _fOut.WriteTObject(WenScales)  # always write out to the directory 

  ## Lepton Scale factors

  WmnScalesSFUp = targetmc.Clone(); WmnScalesSFUp.SetName("monomu_weights_%s_muonSF_Up" %cid)
  WmnScalesSFUp.Divide(controlmc_SFUp);  _fOut.WriteTObject(WmnScalesSFUp)  # always write out to the directory 

  WenScalesSFUp = targetmc.Clone(); WenScalesSFUp.SetName("monoel_weights_%s_electronSF_Up" %cid)
  WenScalesSFUp.Divide(controlmc_e_SFUp);  _fOut.WriteTObject(WenScalesSFUp)  # always write out to the directory 

  WmnScalesSFDown = targetmc.Clone(); WmnScalesSFDown.SetName("monomu_weights_%s_muonSF_Down" %cid)
  WmnScalesSFDown.Divide(controlmc_SFDown);  _fOut.WriteTObject(WmnScalesSFDown)  # always write out to the directory 

  WenScalesSFDown = targetmc.Clone(); WenScalesSFDown.SetName("monoel_weights_%s_electronSF_Down" %cid)
  WenScalesSFDown.Divide(controlmc_e_SFDown);  _fOut.WriteTObject(WenScalesSFDown)  # always write out to the directory 

  #######################################################################################################

  _bins = []  # take bins from some histogram, can choose anything but this is easy 
  for b in range(targetmc.GetNbinsX()+1):
    _bins.append(targetmc.GetBinLowEdge(b+1))

  # Here is the important bit which "Builds" the control region, make a list of control regions which 
  # are constraining this process, each "Channel" is created with ...
  # 	(name,_wspace,out_ws,cid+'_'+model,TRANSFERFACTORS) 
  # the second and third arguments can be left unchanged, the others instead must be set
  # TRANSFERFACTORS are what is created above, eg WmnScales

  CRs = [
   Channel("monomu",_wspace,out_ws,cid+'_'+model,WmnScales),
   Channel("monoel",_wspace,out_ws,cid+'_'+model,WenScales)
  ]


  # ############################ USER DEFINED ###########################################################
  # Add systematics in the following, for normalisations use name, relative size (0.01 --> 1%)
  # for shapes use add_nuisance_shape with (name,_fOut)
  # note, the code will LOOK for something called NOMINAL_name_Up and NOMINAL_name_Down, where NOMINAL=WmnScales.GetName()
  # these must be created and writted to the same dirctory as the nominal (fDir)

  # Statistical uncertainties too!, one per bin 
  for b in range(targetmc.GetNbinsX()):
    err = WmnScales.GetBinError(b+1)
    if not WmnScales.GetBinContent(b+1)>0: continue 
    relerr = err/WmnScales.GetBinContent(b+1)
    if relerr<0.001: continue
    byb_u = WmnScales.Clone(); byb_u.SetName("monomu_weights_%s_%s_stat_error_%s_bin%d_Up"%(cid,cid,"monomuCR",b))
    byb_u.SetBinContent(b+1,WmnScales.GetBinContent(b+1)+err)
    byb_d = WmnScales.Clone(); byb_d.SetName("monomu_weights_%s_%s_stat_error_%s_bin%d_Down"%(cid,cid,"monomuCR",b))
    byb_d.SetBinContent(b+1,WmnScales.GetBinContent(b+1)-err)
    _fOut.WriteTObject(byb_u)
    _fOut.WriteTObject(byb_d)
    print "Adding an error -- ", byb_u.GetName(),err
    CRs[0].add_nuisance_shape("%s_stat_error_%s_bin%d"%(cid,"monomuCR",b),_fOut)

  # Statistical uncertainties too!, one per bin 
  for b in range(targetmc.GetNbinsX()):
    err_e = WenScales.GetBinError(b+1)
    if not WenScales.GetBinContent(b+1)>0: continue 
    relerr_e = err_e/WenScales.GetBinContent(b+1)
    if relerr_e<0.001: continue
    byb_u_e = WenScales.Clone(); byb_u_e.SetName("monoel_weights_%s_%s_stat_error_%s_bin%d_Up"%(cid,cid,"monoelCR",b))
    byb_u_e.SetBinContent(b+1,WenScales.GetBinContent(b+1)+err_e)
    byb_d_e = WenScales.Clone(); byb_d_e.SetName("monoel_weights_%s_%s_stat_error_%s_bin%d_Down"%(cid,cid,"monoelCR",b))
    byb_d_e.SetBinContent(b+1,WenScales.GetBinContent(b+1)-err_e)
    _fOut.WriteTObject(byb_u_e)
    _fOut.WriteTObject(byb_d_e)
    print "Adding an error -- ", byb_u_e.GetName(),err_e
    CRs[1].add_nuisance_shape("%s_stat_error_%s_bin%d"%(cid,"monoelCR",b),_fOut)

  #######################################################################################################

  CRs[0].add_nuisance_shape('muonSF', _fOut)
  CRs[1].add_nuisance_shape('electronSF', _fOut)

  #######################################################################################################

  cat = Category(model,cid,nam,_fin,_fOut,_wspace,out_ws,_bins,metname,targetmc.GetName(),CRs,diag)

  #cat.setDependant("zjets","wjetssignal")  # Can use this to state that the "BASE" of this is already dependant on another process
  # EG if the W->lv in signal is dependant on the Z->vv and then the W->mv is depenant on W->lv, then 
  # give the arguments model,channel name from the config which defines the Z->vv => W->lv map! 
  # Return of course

  return cat

