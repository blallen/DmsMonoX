# Configuration for a simple monojet topology. Use this as a template for your own Run-2 mono-X analysis
# First provide ouput file name in out_file_name field 
out_file_name = 'mono-x.root'

# can define any thing useful here which may be common to several categories, eg binning in MET 
bins = range(200,1000,100)

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
	   ,"weightname":"scale_w"
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
                  ,"Zll_signal"                    :['signal','zll',1,0]
                  ,"Wlv_signal"                    :['signal','wjets',1,0]
                  ,"others_signal"                 :['signal','top',1,0]
                  ,"QCD_200To300_signal"           :['signal','qcd',1,0]
                  ,"QCD_300To500_signal"           :['signal','qcd',1,0]
                  ,"QCD_500To700_signal"           :['signal','qcd',1,0]
                  ,"QCD_700To1000_signal"          :['signal','qcd',1,0]
                  ,"QCD_1000To1500_signal"         :['signal','qcd',1,0]
                  ,"QCD_200To300_signal"           :['signal','qcd',1,0]
                  ,"signal_dm_signal"              :['signal','pseudoscalar',1,1]
                  ,"GJets_100To200_signal"         :['signal','gjets',1,0]
                  ,"GJets_200To400_signal"         :['signal','gjets',1,0]
                  ,"GJets_400To600_signal"         :['signal','gjets',1,0]
                  ,"GJets_600ToInf_signal"         :['signal','gjets',1,0]
                  ,"WW_signal"                     :['signal','diboson',1,0]
                  ,"WZ_signal"                     :['signal','diboson',1,0]
                  ,"ZZ_signal"                     :['signal','diboson',1,0]
                  ,"data_signal"                   :['signal','data',0,0]

                  # Dimuon Control Region
                  ,"Zll_Zmm"                    :['Zmm','zll',1,1]
                  ,"Zvv_ht100_Zmm"              :['Zmm','zjets',1,0]
                  ,"Zvv_ht200_Zmm"              :['Zmm','zjets',1,0]
                  ,"Zvv_ht400_Zmm"              :['Zmm','zjets',1,0]
                  ,"Zvv_ht600_Zmm"              :['Zmm','zjets',1,0]
                  ,"Wlv_Zmm"                    :['Zmm','wjets',1,0]
                  ,"others_Zmm"                 :['Zmm','top',1,0]
                  ,"QCD_200To300_Zmm"           :['Zmm','qcd',1,0]
                  ,"QCD_300To500_Zmm"           :['Zmm','qcd',1,0]
                  ,"QCD_500To700_Zmm"           :['Zmm','qcd',1,0]
                  ,"QCD_700To1000_Zmm"          :['Zmm','qcd',1,0]
                  ,"QCD_1000To1500_Zmm"         :['Zmm','qcd',1,0]
                  ,"QCD_200To300_Zmm"           :['Zmm','qcd',1,0]
                  ,"signal_dm_Zmm"              :['Zmm','pseudoscalar',1,0]
                  ,"GJets_100To200_Zmm"         :['Zmm','gjets',1,0]
                  ,"GJets_200To400_Zmm"         :['Zmm','gjets',1,0]
                  ,"GJets_400To600_Zmm"         :['Zmm','gjets',1,0]
                  ,"GJets_600ToInf_Zmm"         :['Zmm','gjets',1,0]
                  ,"WW_Zmm"                     :['Zmm','diboson',1,0]
                  ,"WZ_Zmm"                     :['Zmm','diboson',1,0]
                  ,"ZZ_Zmm"                     :['Zmm','diboson',1,0]
                  ,"data_Zmm"                   :['Zmm','data',0,0]


                  # Dielectron Control Region
                  ,"Zll_Zee"                    :['Zee','zll',1,1]
                  ,"Zvv_ht100_Zee"              :['Zee','zjets',1,0]
                  ,"Zvv_ht200_Zee"              :['Zee','zjets',1,0]
                  ,"Zvv_ht400_Zee"              :['Zee','zjets',1,0]
                  ,"Zvv_ht600_Zee"              :['Zee','zjets',1,0]
                  ,"Wlv_Zee"                    :['Zee','wjets',1,0]
                  ,"others_Zee"                 :['Zee','top',1,0]
                  ,"QCD_200To300_Zee"           :['Zee','qcd',1,0]
                  ,"QCD_300To500_Zee"           :['Zee','qcd',1,0]
                  ,"QCD_500To700_Zee"           :['Zee','qcd',1,0]
                  ,"QCD_700To1000_Zee"          :['Zee','qcd',1,0]
                  ,"QCD_1000To1500_Zee"         :['Zee','qcd',1,0]
                  ,"QCD_200To300_Zee"           :['Zee','qcd',1,0]
                  ,"signal_dm_Zee"              :['Zee','pseudoscalar',1,0]
                  ,"GJets_100To200_Zee"         :['Zee','gjets',1,0]
                  ,"GJets_200To400_Zee"         :['Zee','gjets',1,0]
                  ,"GJets_400To600_Zee"         :['Zee','gjets',1,0]
                  ,"GJets_600ToInf_Zee"         :['Zee','gjets',1,0]
                  ,"WW_Zee"                     :['Zee','diboson',1,0]
                  ,"WZ_Zee"                     :['Zee','diboson',1,0]
                  ,"ZZ_Zee"                     :['Zee','diboson',1,0]
                  ,"data_Zee"                   :['Zee','data',0,0]

                  # Single muon-Control
                  ,"Wlv_Wen"                    :['Wen','wjets',1,1]
                  ,"Zvv_ht100_Wen"              :['Wen','zjets',1,0]
                  ,"Zvv_ht200_Wen"              :['Wen','zjets',1,0]
                  ,"Zvv_ht400_Wen"              :['Wen','zjets',1,0]
                  ,"Zvv_ht600_Wen"              :['Wen','zjets',1,0]
                  ,"Zll_Wen"                    :['Wen','zll',1,0]
                  ,"others_Wen"                 :['Wen','top',1,0]
                  ,"QCD_200To300_Wen"           :['Wen','qcd',1,0]
                  ,"QCD_300To500_Wen"           :['Wen','qcd',1,0]
                  ,"QCD_500To700_Wen"           :['Wen','qcd',1,0]
                  ,"QCD_700To1000_Wen"          :['Wen','qcd',1,0]
                  ,"QCD_1000To1500_Wen"         :['Wen','qcd',1,0]
                  ,"QCD_200To300_Wen"           :['Wen','qcd',1,0]
                  ,"signal_dm_Wen"              :['Wen','pseudoscalar',1,0]
                  ,"GJets_100To200_Wen"         :['Wen','gjets',1,0]
                  ,"GJets_200To400_Wen"         :['Wen','gjets',1,0]
                  ,"GJets_400To600_Wen"         :['Wen','gjets',1,0]
                  ,"GJets_600ToInf_Wen"         :['Wen','gjets',1,0]
                  ,"WW_Wen"                     :['Wen','diboson',1,0]
                  ,"WZ_Wen"                     :['Wen','diboson',1,0]
                  ,"ZZ_Wen"                     :['Wen','diboson',1,0]
                  ,"data_Wen"                   :['Wen','data',0,0]

                  # Single muon-Control
                  ,"Wlv_Wen"                    :['Wen','wjets',1,1]
                  ,"Zvv_ht100_Wen"              :['Wen','zjets',1,0]
                  ,"Zvv_ht200_Wen"              :['Wen','zjets',1,0]
                  ,"Zvv_ht400_Wen"              :['Wen','zjets',1,0]
                  ,"Zvv_ht600_Wen"              :['Wen','zjets',1,0]
                  ,"Zll_Wen"                    :['Wen','zll',1,0]
                  ,"others_Wen"                 :['Wen','top',1,0]
                  ,"QCD_200To300_Wen"           :['Wen','qcd',1,0]
                  ,"QCD_300To500_Wen"           :['Wen','qcd',1,0]
                  ,"QCD_500To700_Wen"           :['Wen','qcd',1,0]
                  ,"QCD_700To1000_Wen"          :['Wen','qcd',1,0]
                  ,"QCD_1000To1500_Wen"         :['Wen','qcd',1,0]
                  ,"QCD_200To300_Wen"           :['Wen','qcd',1,0]
                  ,"signal_dm_Wen"              :['Wen','pseudoscalar',1,0]
                  ,"GJets_100To200_Wen"         :['Wen','gjets',1,0]
                  ,"GJets_200To400_Wen"         :['Wen','gjets',1,0]
                  ,"GJets_400To600_Wen"         :['Wen','gjets',1,0]
                  ,"GJets_600ToInf_Wen"         :['Wen','gjets',1,0]
                  ,"WW_Wen"                     :['Wen','diboson',1,0]
                  ,"WZ_Wen"                     :['Wen','diboson',1,0]
                  ,"ZZ_Wen"                     :['Wen','diboson',1,0]
                  ,"data_Wen"                   :['Wen','data',0,0]
                   
                  # photon control region
                  ,"Wlv_gjets"                    :['gjets','wjets',1,0]
                  ,"Zvv_ht100_gjets"              :['gjets','zjets',1,0]
                  ,"Zvv_ht200_gjets"              :['gjets','zjets',1,0]
                  ,"Zvv_ht400_gjets"              :['gjets','zjets',1,0]
                  ,"Zvv_ht600_gjets"              :['gjets','zjets',1,0]
                  ,"Zll_gjets"                    :['gjets','zll',1,0]
                  ,"others_gjets"                 :['gjets','top',1,0]
                  ,"QCD_200To300_gjets"           :['gjets','qcd',1,0]
                  ,"QCD_300To500_gjets"           :['gjets','qcd',1,0]
                  ,"QCD_500To700_gjets"           :['gjets','qcd',1,0]
                  ,"QCD_700To1000_gjets"          :['gjets','qcd',1,0]
                  ,"QCD_1000To1500_gjets"         :['gjets','qcd',1,0]
                  ,"QCD_200To300_gjets"           :['gjets','qcd',1,0]
                  ,"signal_dm_gjets"              :['gjets','pseudoscalar',1,0]
                  ,"GJets_100To200_gjets"         :['gjets','gjets',1,1]
                  ,"GJets_200To400_gjets"         :['gjets','gjets',1,1]
                  ,"GJets_400To600_gjets"         :['gjets','gjets',1,1]
                  ,"GJets_600ToInf_gjets"         :['gjets','gjets',1,1]
                  ,"WW_gjets"                     :['gjets','diboson',1,0]
                  ,"WZ_gjets"                     :['gjets','diboson',1,0]
                  ,"ZZ_gjets"                     :['gjets','diboson',1,0]
                  ,"data_gjets"                   :['gjets','data',0,0]

	   	},
}
categories = [monojet_category]
