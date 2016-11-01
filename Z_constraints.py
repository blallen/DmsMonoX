import ROOT
import math
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

  target             = _fin.Get("signal_zg")      # define nomimal (MC) of process this config models
  controlmc          = _fin.Get("dimu_zg")        # defines Zmm MC which will control process
  controlmc_e        = _fin.Get("diel_zg")        # defines Zee MC which will control process
  controlmc_w        = _fin.Get("signal_wg")      # defines Wln MC which will control process

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
  
  WZScales = target.Clone(); WZScales.SetName("wz_weights_%s" %cid)
  WZScales.Divide(controlmc_w);  _fOut.WriteTObject(WZScales)  # always write out to the directory 

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
  ,Channel("wgsignal",_wspace,out_ws,cid+'_'+model,WZScales)
  ]

  # ############################ USER DEFINED ###########################################################
  # Add systematics in the following, for normalisations use name, relative size (0.01 --> 1%)
  # for shapes use add_nuisance_shape with (name,_fOut)
  # note, the code will LOOK for something called NOMINAL_name_Up and NOMINAL_name_Down, where NOMINAL=WScales.GetName()
  # these must be created and writted to the same dirctory as the nominal (fDir)

  CRs[0].addUncorrStatSysts(target, ZmmScales, "dimu", "dimu", cid, _fOut)
  CRs[1].addUncorrStatSysts(target, ZeeScales, "diel", "diel", cid, _fOut)
  CRs[2].addUncorrStatSysts(target, WZScales, "wz", "wz", cid, _fOut)
  
  # lepSFSystSetup(_wspace, _fin, _fOut, cid)
  WZ_systSetup(_wspace, _fin, _fOut, cid)

  #######################################################################################################

  # CRs[0].add_nuisance_shape('muonSF', _fOut)
  # CRs[1].add_nuisance_shape('electronSF', _fOut)

  CRs[2].add_nuisance_shape("vgPDF", _fOut)
  CRs[2].add_nuisance_shape("vgQCDscale", _fOut)

  for b in range(target.GetNbinsX()):
    CRs[2].add_nuisance_shape("wz_ewk_%s_bin%d" % (cid,b), _fOut)

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

def WZ_systSetup(_wspace, _fin, _fOut, nam):
  
  target             = _fin.Get("signal_zg")      # define monimal (MC) of which process this config will model
  controlmc_w          = _fin.Get("signal_wg")

  WZScales = target.Clone(); WZScales.SetName("wz_weights_%s" %nam)
  WZScales.Divide(controlmc_w);  # not writing since already did in main part

  WSpectrum = controlmc_w.Clone(); WSpectrum.SetName("w_spectrum_%s_"%nam)
  ZvvSpectrum  = target.Clone(); ZvvSpectrum.SetName("zvv_spectrum_%s_"%nam)

  _fOut.WriteTObject( WSpectrum )

  ### PDF Uncertainty

  target_PDFUp = _fin.Get("signal_zg_vgPDFUp")
  target_PDFDown = _fin.Get("signal_zg_vgPDFDown")
  controlmc_w_PDFUp = _fin.Get("signal_wg_vgPDFUp")
  controlmc_w_PDFDown = _fin.Get("signal_wg_vgPDFDown")
  
  WZScalesPDFUp = target_PDFUp.Clone(); WZScalesPDFUp.SetName("wz_weights_%s_vgPDF_Up" %nam)
  WZScalesPDFUp.Divide(controlmc_w_PDFUp);  _fOut.WriteTObject(WZScalesPDFUp)  # always write out to the directory

  WZScalesPDFDown = target_PDFDown.Clone(); WZScalesPDFDown.SetName("wz_weights_%s_vgPDF_Down" %nam)
  WZScalesPDFDown.Divide(controlmc_w_PDFDown);  _fOut.WriteTObject(WZScalesPDFDown)  # always write out to the directory

  ### QCD Scale Uncertainty

  target_QCDUp = _fin.Get("signal_zg_vgQCDscaleUp")
  target_QCDDown = _fin.Get("signal_zg_vgQCDscaleDown")
  controlmc_w_QCDUp = _fin.Get("signal_wg_vgQCDscaleUp")
  controlmc_w_QCDDown = _fin.Get("signal_wg_vgQCDscaleDown")

  corr = 0.80

  WZScalesQCDUp = WZScales.Clone(); WZScalesQCDUp.SetName("wz_weights_%s_vgQCDscale_Up" % nam)
  for b in range(1, WZScalesQCDUp.GetNbinsX()+1):
    rNom = WZScales.GetBinContent(b)
    upup = target_QCDUp.GetBinContent(b) / controlmc_w_QCDUp.GetBinContent(b) - rNom
    updown = target_QCDUp.GetBinContent(b) / controlmc_w_QCDDown.GetBinContent(b) -rNom

    dRatio = math.sqrt( (1 + corr)/2 * upup**2 + (1 - corr)/2 * updown**2 )
    rUp = rNom + dRatio
    WZScalesQCDUp.SetBinContent(b, rUp)

  _fOut.WriteTObject(WZScalesQCDUp)

  WZScalesQCDDown = WZScales.Clone(); WZScalesQCDDown.SetName("wz_weights_%s_vgQCDscale_Down" % nam)
  for b in range(1, WZScalesQCDDown.GetNbinsX()+1):
    rNom = WZScales.GetBinContent(b)
    downdown = target_QCDDown.GetBinContent(b) / controlmc_w_QCDDown.GetBinContent(b) - rNom
    downup = target_QCDDown.GetBinContent(b) / controlmc_w_QCDUp.GetBinContent(b) - rNom

    dRatio = math.sqrt( (1 + corr)/2 * downdown**2 + (1 - corr)/2 * downup**2 )
    rDown = rNom - dRatio
    WZScalesQCDDown.SetBinContent(b, rDown)

  _fOut.WriteTObject(WZScalesQCDDown)

  ### EWK Uncertainty

  target_EWKUp = _fin.Get("signal_zg_zgEWKUp")
  target_EWKDown = _fin.Get("signal_zg_zgEWKDown")
  controlmc_w_EWKUp = _fin.Get("signal_wg_wgEWKUp")
  controlmc_w_EWKDown = _fin.Get("signal_wg_wgEWKDown")
  
  WZScalesEWKUp = target_EWKUp.Clone(); WZScalesEWKUp.SetName("wz_weights_%s_vgEWK_Up" %nam)
  WZScalesEWKUp.Divide(controlmc_w_EWKUp);  # _fOut.WriteTObject(WZScalesEWKUp)  # always write out to the directory

  WZScalesEWKDown = target_EWKDown.Clone(); WZScalesEWKDown.SetName("wz_weights_%s_vgEWK_Down" %nam)
  WZScalesEWKDown.Divide(controlmc_w_EWKDown);  # _fOut.WriteTObject(WZScalesEWKDown)  # always write out to the directory

  #Now lets uncorrelate the bins:
  for b in range(target.GetNbinsX()):
    ewk_up_w = WZScales.Clone(); ewk_up_w.SetName("wz_weights_%s_wz_ewk_%s_bin%d_Up"%(nam,nam,b))
    ewk_down_w = WZScales.Clone(); ewk_down_w.SetName("wz_weights_%s_wz_ewk_%s_bin%d_Down"%(nam,nam,b))
    for i in range(target.GetNbinsX()):
      if i==b:
        ewk_up_w.SetBinContent(i+1, WZScalesEWKUp.GetBinContent(i+1))
        ewk_down_w.SetBinContent(i+1, WZScalesEWKDown.GetBinContent(i+1))
        break

    _fOut.WriteTObject(ewk_up_w)
    _fOut.WriteTObject(ewk_down_w)
