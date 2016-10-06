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

  target             = _fin.Get("signal_zg")      # define monimal (MC) of which process this config will model
  controlmc          = _fin.Get("dilep_zg")        # defines Zmm MC of which process will be controlled by
  controlmc_w        = _fin.Get("signal_wg")

  # Create the transfer factors and save them (not here you can also create systematic variations of these 
  # transfer factors (named with extention _sysname_Up/Down
  ZllScales = target.Clone(); ZllScales.SetName("dilep_weights_%s" %cid)
  ZllScales.Divide(controlmc);  _fOut.WriteTObject(ZllScales)  # always write out to the directory 
  
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
      Channel("dilep",_wspace,out_ws,cid+'_'+model,ZllScales)
      ,Channel("wgsignal",_wspace,out_ws,cid+'_'+model,WZScales)
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

  addUncorrStatSysts(target, WZScales, "wz", "wz", CRs[1], cid, _fOut)

  WZ_systSetup(_wspace, _fin, _fOut, cid)

  #######################################################################################################

  # CRs[0].add_nuisance_shape('muonSF', _fOut)
  # CRs[0].add_nuisance_shape('electronSF', _fOut)
  
  # CRs[1].add_nuisance_shape("wrenscale",_fOut)
  # CRs[1].add_nuisance_shape("wfacscale",_fOut)
  # CRs[1].add_nuisance_shape("wpdf",_fOut) 

  CRs[1].add_nuisance_shape("vgPDF", _fOut)
  CRs[1].add_nuisance_shape("vgQCDscale", _fOut)

  #CRs[0].add_nuisance_shape("ewk",_fOut) 
  for b in range(target.GetNbinsX()):
    # CRs[0].add_nuisance_shape("ewk_%s_bin%d"%(cid,b),_fOut) ## ???????
    # CRs[1].add_nuisance_shape("w_ewk_%s_bin%d"%(cid,b),_fOut)
    CRs[1].add_nuisance_shape("wz_ewk_%s_bin%d" % (cid,b), _fOut)

  #######################################################################################################
  
  cat = Category(model,cid,nam,_fin,_fOut,_wspace,out_ws,_bins,metname,target.GetName(),CRs,diag)
  # Return of course
  return cat

def WZ_systSetup(_wspace, _fin, _fOut, nam):
  
  target             = _fin.Get("signal_zg")      # define monimal (MC) of which process this config will model
  controlmc_w          = _fin.Get("signal_wg")

  WZScales = target.Clone(); WZScales.SetName("wz_weights_%s" %nam)
  WZScales.Divide(controlmc_w);  # _fOut.WriteTObject(WZScales)  # always write out to the directory 

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


def WZ_systSetup_NickStyle(_wspace, _fin, _fOut, nam, diag):
  metname    = "phoPtHighMet"          # Observable variable name 
  gvptname   = "genBos_pt"    # Weights are in generator pT

  target             = _fin.Get("signal_zg")      # define monimal (MC) of which process this config will model
  controlmc_w          = _fin.Get("signal_wg")

  fztow = r.TFile.Open("files/new/wtoz_unc.root") 
  
  ztow_renscale_up   = fztow.Get("znlo1_over_wnlo1_renScaleUp")
  ztow_renscale_down = fztow.Get("znlo1_over_wnlo1_renScaleDown")

  ztow_facscale_up   = fztow.Get("znlo1_over_wnlo1_facScaleUp")
  ztow_facscale_down = fztow.Get("znlo1_over_wnlo1_facScaleDown")

  ztow_pdf_up   = fztow.Get("znlo1_over_wnlo1_pdfUp")
  ztow_pdf_down = fztow.Get("znlo1_over_wnlo1_pdfDown")

  WSpectrum = controlmc_w.Clone(); WSpectrum.SetName("w_spectrum_%s_"%nam)
  ZvvSpectrum  = target.Clone(); ZvvSpectrum.SetName("zvv_spectrum_%s_"%nam)

  _fOut.WriteTObject( WSpectrum )

  #################################################################################################################

  Wsig = controlmc_w.Clone(); Wsig.SetName("wz_weights_denom_%s"%nam)
  Zvv_w = target.Clone(); Zvv_w.SetName("wz_weights_nom_%s"%nam)

  wratio_ren_scale_up = Zvv_w.Clone();  wratio_ren_scale_up.SetName("wz_weights_%s_wrenscale_Up"%nam);
  for b in range(wratio_ren_scale_up.GetNbinsX()): wratio_ren_scale_up.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(wratio_ren_scale_up,ztow_renscale_up,gvptname,metname,_wspace.data("signal_zjets"))
  wratio_ren_scale_up.Divide(Wsig)
  _fOut.WriteTObject(wratio_ren_scale_up)
  
  wratio_ren_scale_down = Zvv_w.Clone();  wratio_ren_scale_down.SetName("wz_weights_%s_wrenscale_Down"%nam);
  for b in range(wratio_ren_scale_down.GetNbinsX()): wratio_ren_scale_down.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(wratio_ren_scale_down,ztow_renscale_down,gvptname,metname,_wspace.data("signal_zjets"))
  wratio_ren_scale_down.Divide(Wsig)
  _fOut.WriteTObject(wratio_ren_scale_down)

  wratio_fac_scale_up = Zvv_w.Clone(); wratio_fac_scale_up.SetName("wz_weights_%s_wfacscale_Up"%nam);
  for b in range(wratio_fac_scale_up.GetNbinsX()): wratio_fac_scale_up.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(wratio_fac_scale_up,ztow_facscale_up,gvptname,metname,_wspace.data("signal_zjets"))
  wratio_fac_scale_up.Divide(Wsig)
  _fOut.WriteTObject(wratio_fac_scale_up)
  
  wratio_fac_scale_down = Zvv_w.Clone();  wratio_fac_scale_down.SetName("wz_weights_%s_wfacscale_Down"%nam);
  for b in range(wratio_fac_scale_down.GetNbinsX()): wratio_fac_scale_down.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(wratio_fac_scale_down,ztow_facscale_down,gvptname,metname,_wspace.data("signal_zjets"))
  wratio_fac_scale_down.Divide(Wsig)
  _fOut.WriteTObject(wratio_fac_scale_down)

  wratio_pdf_up = Zvv_w.Clone();  wratio_pdf_up.SetName("wz_weights_%s_wpdf_Up"%nam);
  for b in range(wratio_pdf_up.GetNbinsX()): wratio_pdf_up.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(wratio_pdf_up,ztow_pdf_up,gvptname,metname,_wspace.data("signal_zjets"))
  wratio_pdf_up.Divide(Wsig)
  _fOut.WriteTObject(wratio_pdf_up)
  
  wratio_pdf_down = Zvv_w.Clone();  wratio_pdf_down.SetName("wz_weights_%s_wpdf_Down"%nam);
  for b in range(ratio_pdf_down.GetNbinsX()): wratio_pdf_down.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(wratio_pdf_down,ztow_pdf_down,gvptname,metname,_wspace.data("signal_zjets"))
  wratio_pdf_down.Divide(Wsig)
  _fOut.WriteTObject(wratio_pdf_down)

  #fztowewk = r.TFile.Open("files/wtoz_ewkunc.root")
  fztowewk = r.TFile.Open("files/new/wtoz_unc.root")
  ztow_ewk_up   = fztowewk.Get("w_ewkcorr_overz_Upcommon")
  ztow_ewk_down = fztowewk.Get("w_ewkcorr_overz_Downcommon")

  wratio_ewk_up = Zvv_w.Clone();  wratio_ewk_up.SetName("wz_weights_%s_ewk_Up"%nam);
  for b in range(wratio_ewk_up.GetNbinsX()): wratio_ewk_up.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(wratio_ewk_up,ztow_ewk_up,gvptname,metname,_wspace.data("signal_zjets"))
  wratio_ewk_up.Divide(Wsig)
  # We are now going to uncorrelate the bins
  #_fOut.WriteTObject(ratio_ewk_up)
  
  wratio_ewk_down = Zvv_w.Clone();  wratio_ewk_down.SetName("wz_weights_%s_ewk_Down"%nam);
  for b in range(wratio_ewk_down.GetNbinsX()): wratio_ewk_down.SetBinContent(b+1,0)  
  diag.generateWeightedTemplate(wratio_ewk_down,ztow_ewk_down,gvptname,metname,_wspace.data("signal_zjets"))
  wratio_ewk_down.Divide(Wsig)
  # We are now going to uncorrelate the bins
  #_fOut.WriteTObject(ratio_ewk_down)

  Zvv_w.Divide(Wsig)

  #Now lets uncorrelate the bins:
  for b in range(target.GetNbinsX()):
    ewk_up_w = Zvv_w.Clone(); ewk_up_w.SetName("wz_weights_%s_w_ewk_%s_bin%d_Up"%(nam,nam,b))
    ewk_down_w = Zvv_w.Clone(); ewk_down_w.SetName("wz_weights_%s_w_ewk_%s_bin%d_Down"%(nam,nam,b))
    for i in range(target.GetNbinsX()):
      if i==b:
        ewk_up_w.SetBinContent(i+1,wratio_ewk_up.GetBinContent(i+1))
        ewk_down_w.SetBinContent(i+1,wratio_ewk_down.GetBinContent(i+1))
        break

    _fOut.WriteTObject(ewk_up_w)
    _fOut.WriteTObject(ewk_down_w)
