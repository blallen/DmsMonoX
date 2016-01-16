# Configuration for a simple monojet topology. Use this as a template for your own Run-2 mono-X analysis
# First provide ouput file name in out_file_name field 
out_file_name = 'mono-x.root'

#1;2c can define any thing useful here which may be common to several categories, eg binning in MET 
#bins = range(200,1100,800)
#bins = range(200,1100,50)

bins = [200.0, 250.0, 300.0, 350.0, 400.0, 500.0, 600.0, 1000.0]
#bins = [200.0, 250.0, 300.0, 350.0, 400.0, 500.0, 600.0, 900.0, 1500.0]


# Define each of the categories in a dictionary of the following form .. 
#	'name' : the category name 
#	'in_file_name' : input ntuple file for this category 
#	'cutstring': add simple cutrstring, applicable to ALL regions in this category (eg mvamet > 200)
#	'varstring': the main variable to be fit in this category (eg mvamet), must be named as the branch in the ntuples
#	'weightname': name of the weight variable 
#	'bins': binning given as a python list
#	'additionalvars': list additional variables to be histogrammed by the first stage, give as a list of lists, each list element 
#			  as ['variablename',nbins,min,max]
#	'pdfmodel': integer --> N/A  redudant for now unless we move back to parameteric fitting estimates
# 	'samples' : define tree->region/process map given as a dictionary with each entry as follows 
#	TreeName : ['region','process',isMC,isSignal] --> Note isSignal means DM/Higgs etc for signal region but Z-jets/W-jets for the di/single-muon regions !!!

#  OPTIONAL --> 'extra_cuts': additional cuts maybe specific to this control region (eg ptphoton cuts) if this key is missing, the code will not complain   
 
monojet_category = {
	    'name':"monojet"
           ,'in_file_name':"monojet_final.root"
           ,"cutstring":"met>200"
           ,"varstring":["met",200,1000]
           #,"varstring":["met",200,1500]
	   ,"weightname":"scaleMC_w"
	   ,"bins":bins[:]
           ,"additionalvars":[['met',100,200,1000]]
	   ,"pdfmodel":0
	   ,"samples":
	   	{  
		  # Signal Region
                   "Zvv_ht100_signal"              :['signal','zjets',1,0]
                  ,"Zvv_ht200_signal"              :['signal','zjets',1,0]
                  ,"Zvv_ht400_signal"              :['signal','zjets',1,0]
                  ,"Zvv_ht600_signal"              :['signal','zjets',1,0]
                  ,"Zll_ht100_signal"              :['signal','zll',1,0]
                  ,"Zll_ht200_signal"              :['signal','zll',1,0]
                  ,"Zll_ht400_signal"              :['signal','zll',1,0]
                  ,"Zll_ht600_signal"              :['signal','zll',1,0]                   
                  ,"Wlv_ht100_signal"              :['signal','wjets',1,0]
                  ,"Wlv_ht200_signal"              :['signal','wjets',1,0]
                  ,"Wlv_ht400_signal"              :['signal','wjets',1,0]
                  ,"Wlv_ht600_signal"              :['signal','wjets',1,0]
                  ,"others_signal"                 :['signal','top',1,0]
                  ,"antitop_signal"                :['signal','top',1,0]
                  ,"antitop_5f_signal"             :['signal','top',1,0]
                  ,"top_signal"                    :['signal','top',1,0]
                  ,"top_5f_signal"                 :['signal','top',1,0]
                  ,"QCD_200To300_signal"           :['signal','qcd',1,0]
                  ,"QCD_300To500_signal"           :['signal','qcd',1,0]
                  ,"QCD_500To700_signal"           :['signal','qcd',1,0]
                  ,"QCD_700To1000_signal"          :['signal','qcd',1,0]
                  ,"QCD_1000To1500_signal"         :['signal','qcd',1,0]
                  ,"QCD_200To300_signal"           :['signal','qcd',1,0]
                  ,"signal_dm_av_1_2_signal"       :['signal','axialvector_1_2',1,1]
                  ,"signal_dm_ps_300_100_signal"   :['signal','ps_300_100',1,1]
                  ,"signal_h_ggf_signal"           :['signal','higgs150',1,1]
                  ,"signal_h_vbf_signal"           :['signal','higgs150',1,1]
                  ,"signal_dm_ps_200_1_signal"     :['signal','ps_200_1',1,1]
                  ,"signal_dm_ps_200_10_signal"    :['signal','ps_10_1',1,1]
                  ,"signal_dm_ps_200_100_signal"   :['signal','ps_100_1',1,1]
                  ,"signal_dm_ps_200_150_signal"   :['signal','ps_150_1',1,1]
                  ,"signal_dm_ps_200_50_signal"    :['signal','ps_50_1',1,1]
                  ,"GJets_100To200_signal"         :['signal','gjets',1,0]
                  ,"GJets_200To400_signal"         :['signal','gjets',1,0]
                  ,"GJets_400To600_signal"         :['signal','gjets',1,0]
                  ,"GJets_600ToInf_signal"         :['signal','gjets',1,0]
                  ,"WW_signal"                     :['signal','diboson',1,0]
                  ,"WZ_signal"                     :['signal','diboson',1,0]
                  ,"ZZ_signal"                     :['signal','diboson',1,0]                  
                  ,"data_signal"                   :['signal','data',0,0]

                  # Dimuon Control Region
                  ,"Zll_ht100_Zmm"              :['Zmm','zll',1,1]
                  ,"Zll_ht200_Zmm"              :['Zmm','zll',1,1]
                  ,"Zll_ht400_Zmm"              :['Zmm','zll',1,1]
                  ,"Zll_ht600_Zmm"              :['Zmm','zll',1,1]
                  ,"others_Zmm"                 :['Zmm','top',1,0]
                  ,"WW_Zmm"                     :['Zmm','diboson',1,0]
                  ,"WZ_Zmm"                     :['Zmm','diboson',1,0]
                  ,"ZZ_Zmm"                     :['Zmm','diboson',1,0]
                  ,"data_Zmm"                   :['Zmm','data',0,0]

                  # Dielectron Control Region
                  ,"Zll_ht100_Zee"              :['Zee','zll',1,1]
                  ,"Zll_ht200_Zee"              :['Zee','zll',1,1]
                  ,"Zll_ht400_Zee"              :['Zee','zll',1,1]
                  ,"Zll_ht600_Zee"              :['Zee','zll',1,1]
                  ,"others_Zee"                 :['Zee','top',1,0]
                  ,"WW_Zee"                     :['Zee','diboson',1,0]
                  ,"WZ_Zee"                     :['Zee','diboson',1,0]
                  ,"ZZ_Zee"                     :['Zee','diboson',1,0]
                  ,"data_Zee"                   :['Zee','data',0,0]

                  # Single muon-Control
                  ,"Wlv_ht100_Wmn"              :['Wmn','wjets',1,1]
                  ,"Wlv_ht200_Wmn"              :['Wmn','wjets',1,1]
                  ,"Wlv_ht400_Wmn"              :['Wmn','wjets',1,1]
                  ,"Wlv_ht600_Wmn"              :['Wmn','wjets',1,1]
                  ,"Zll_ht100_Wmn"              :['Wmn','zll',1,0]
                  ,"Zll_ht200_Wmn"              :['Wmn','zll',1,0]
                  ,"Zll_ht400_Wmn"              :['Wmn','zll',1,0]
                  ,"Zll_ht600_Wmn"              :['Wmn','zll',1,0]                   
                  ,"others_Wmn"                 :['Wmn','top',1,0]
                  ,"antitop_Wmn"                :['Wmn','top',1,0]
                  ,"antitop_5f_Wmn"             :['Wmn','top',1,0]
                  ,"top_Wmn"                    :['Wmn','top',1,0]
                  ,"top_5f_Wmn"                 :['Wmn','top',1,0]
                  ,"QCD_200To300_Wmn"           :['Wmn','qcd',1,0]
                  ,"QCD_300To500_Wmn"           :['Wmn','qcd',1,0]
                  ,"QCD_500To700_Wmn"           :['Wmn','qcd',1,0]
                  ,"QCD_700To1000_Wmn"          :['Wmn','qcd',1,0]
                  ,"QCD_1000To1500_Wmn"         :['Wmn','qcd',1,0]
                  ,"QCD_200To300_Wmn"           :['Wmn','qcd',1,0]
                  ,"WW_Wmn"                     :['Wmn','diboson',1,0]
                  ,"WZ_Wmn"                     :['Wmn','diboson',1,0]
                  ,"ZZ_Wmn"                     :['Wmn','diboson',1,0]
                  ,"data_Wmn"                   :['Wmn','data',0,0]

                  # Single electron-Control
                  ,"Wlv_ht100_Wen"              :['Wen','wjets',1,1]
                  ,"Wlv_ht200_Wen"              :['Wen','wjets',1,1]
                  ,"Wlv_ht400_Wen"              :['Wen','wjets',1,1]
                  ,"Wlv_ht600_Wen"              :['Wen','wjets',1,1]
                  ,"Zll_ht100_Wen"              :['Wen','zll',1,0]
                  ,"Zll_ht200_Wen"              :['Wen','zll',1,0]
                  ,"Zll_ht400_Wen"              :['Wen','zll',1,0]
                  ,"Zll_ht600_Wen"              :['Wen','zll',1,0]
                  ,"others_Wen"                 :['Wen','top',1,0]
                  ,"antitop_Wen"                :['Wen','top',1,0]
                  ,"antitop_5f_Wen"             :['Wen','top',1,0]
                  ,"top_Wen"                    :['Wen','top',1,0]
                  ,"top_5f_Wen"                 :['Wen','top',1,0]
                  ,"QCD_200To300_Wen"           :['Wen','qcd',1,0]
                  ,"QCD_300To500_Wen"           :['Wen','qcd',1,0]
                  ,"QCD_500To700_Wen"           :['Wen','qcd',1,0]
                  ,"QCD_700To1000_Wen"          :['Wen','qcd',1,0]
                  ,"QCD_1000To1500_Wen"         :['Wen','qcd',1,0]
                  ,"QCD_200To300_Wen"           :['Wen','qcd',1,0]
                  ,"WW_Wen"                     :['Wen','diboson',1,0]
                  ,"WZ_Wen"                     :['Wen','diboson',1,0]
                  ,"ZZ_Wen"                     :['Wen','diboson',1,0]
                  ,"data_Wen"                   :['Wen','data',0,0]
                   
                  # photon control region
                  ,"QCD_200To300_gjets"           :['gjets','qcd',1,0]
                  ,"QCD_300To500_gjets"           :['gjets','qcd',1,0]
                  ,"QCD_500To700_gjets"           :['gjets','qcd',1,0]
                  ,"QCD_700To1000_gjets"          :['gjets','qcd',1,0]
                  ,"QCD_1000To1500_gjets"         :['gjets','qcd',1,0]
                  ,"QCD_200To300_gjets"           :['gjets','qcd',1,0]
                  ,"GJets_100To200_gjets"         :['gjets','gjets',1,1]
                  ,"GJets_200To400_gjets"         :['gjets','gjets',1,1]
                  ,"GJets_400To600_gjets"         :['gjets','gjets',1,1]
                  ,"GJets_600ToInf_gjets"         :['gjets','gjets',1,1]
                  ,"data_gjets"                   :['gjets','data',0,0]

	   	},
}
categories = [monojet_category]
