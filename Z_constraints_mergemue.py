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
  controlmc          = _fin.Get("dilep_zg")        # defines Zmm MC of which process will be controlled by

  controlmc_muonSFUp     = _fin.Get("dilep_zg_muonSFUp")
  controlmc_muonSFDown   = _fin.Get("dilep_zg_muonSFDown")

  controlmc_electronSFUp     = _fin.Get("dilep_zg_electronSFUp")
  controlmc_electronSFDown   = _fin.Get("dilep_zg_electronSFDown")

  # Create the transfer factors and save them (not here you can also create systematic variations of these 
  # transfer factors (named with extention _sysname_Up/Down
  ZllScales = target.Clone(); ZllScales.SetName("dilep_weights_%s" %cid)
  ZllScales.Divide(controlmc);  _fOut.WriteTObject(ZllScales)  # always write out to the directory 

  ## Lepton Scale factors

  """
  ZllScalesSFUp = target.Clone(); ZllScalesSFUp.SetName("dilep_weights_%s_muonSF_Up" %cid)
  ZllScalesSFUp.Divide(controlmc_SFUp);  _fOut.WriteTObject(ZllScalesSFUp)  # always write out to the directory 

  ZllScalesSFUp = target.Clone(); ZllScalesSFUp.SetName("dilep_weights_%s_electronSF_Up" %cid)
  ZllScalesSFUp.Divide(controlmc_e_SFUp);  _fOut.WriteTObject(ZllScalesSFUp)  # always write out to the directory 

  ZllScalesSFDown = target.Clone(); ZllScalesSFDown.SetName("dilep_weights_%s_muonSF_Down" %cid)
  ZllScalesSFDown.Divide(controlmc_SFDown);  _fOut.WriteTObject(ZllScalesSFDown)  # always write out to the directory 

  ZllScalesSFDown = target.Clone(); ZllScalesSFDown.SetName("dilep_weights_%s_electronSF_Down" %cid)
  ZllScalesSFDown.Divide(controlmc_e_SFDown);  _fOut.WriteTObject(ZllScalesSFDown)  # always write out to the directory 
  """

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
    Channel("dilep",_wspace,out_ws,cid+'_'+model,ZllScales)
    ]

  # ############################ USER DEFINED ###########################################################
  # Add systematics in the following, for normalisations use name, relative size (0.01 --> 1%)
  # for shapes use add_nuisance_shape with (name,_fOut)
  # note, the code will LOOK for something called NOMINAL_name_Up and NOMINAL_name_Down, where NOMINAL=WScales.GetName()
  # these must be created and writted to the same dirctory as the nominal (fDir)

  for b in range(target.GetNbinsX()):
    err = ZllScales.GetBinError(b+1)
    if not ZllScales.GetBinContent(b+1)>0: continue 
    relerr = err/ZllScales.GetBinContent(b+1)
    if relerr<0.01: continue
    byb_u = ZllScales.Clone(); byb_u.SetName("dilep_weights_%s_%s_stat_error_%s_bin%d_Up"%(cid,cid,"dilepCR",b))
    byb_u.SetBinContent(b+1,ZllScales.GetBinContent(b+1)+err)
    byb_d = ZllScales.Clone(); byb_d.SetName("dilep_weights_%s_%s_stat_error_%s_bin%d_Down"%(cid,cid,"dilepCR",b))
    if (ZllScales.GetBinContent(b+1)-err > 0):
      byb_d.SetBinContent(b+1,ZllScales.GetBinContent(b+1)-err)
    else:
      byb_d.SetBinContent(b+1,1)
    _fOut.WriteTObject(byb_u)
    _fOut.WriteTObject(byb_d)
    print "Adding an error -- ", byb_u.GetName(),err
    CRs[0].add_nuisance_shape("%s_stat_error_%s_bin%d"%(cid,"dilepCR",b),_fOut)

  #######################################################################################################

  # CRs[0].add_nuisance_shape('muonSF', _fOut)
  # CRs[0].add_nuisance_shape('electronSF', _fOut)

  #######################################################################################################
  
  cat = Category(model,cid,nam,_fin,_fOut,_wspace,out_ws,_bins,metname,target.GetName(),CRs,diag)
  # Return of course
  return cat

