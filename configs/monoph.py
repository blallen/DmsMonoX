# Configuration for a simple monojet topology. Use this as a template for your own Run-2 mono-X analysis
# First provide ouput file name in out_file_name field 

out_file_name = 'mono-x.root'

# bins = [175.0,190.0,250.0,400.0,700.0,1000.0]
# bins = [175.0, 200., 225., 250., 275., 300., 325., 350., 400., 450., 500., 600., 800., 1000.0] # maybe can do a bin at 800, improve limits, but tfactors and fits go weird
# bins = [175.0, 200., 250., 300., 400., 600., 800., 1000.0]
bins = [400.0, 1000.0]

monophoton_category = {
	    'name':"monophoton"
            ,'in_file_name':"monophTrees.root"
            ,"cutstring":"phoPtHighMet>175"
            ,"varstring":["phoPtHighMet",175,1000]
            ,"weightname":"weight"
            ,"bins":bins[:]
            ,"additionalvars":[] #[['phoPtHighMet',100,200,1250]]
            ,"pdfmodel":0
            ,"systematics":['lumi', 'gec', 'jec', 'photonSF', 'customIDSF', 'leptonVetoSF', 'muonSF', 'electronSF',
                            'haloNorm', 'haloShape', 'hfakeTfactor', 'purity', 'egFakerate', 
                            'minorPDF', 'minorQCDscale', 'vgPDF', 'vgQCDscale', 'wgEWK', 'zgEWK']
            ,"samples":
	   	{          
		  # Signal Region
                   "monoph-phoPtHighMet-minor"    :['signal','minor',1,0]
                  ,"monoph-phoPtHighMet-gjets"    :['signal','gjets',1,0]
                  ,"monoph-phoPtHighMet-vvg"      :['signal','vvg',1,0]
                  ,"monoph-phoPtHighMet-halo"     :['signal','halo',1,0]
                  ,"monoph-phoPtHighMet-hfake"    :['signal','hfake',1,0]
                  ,"monoph-phoPtHighMet-efake"    :['signal','efake',1,0]
                  ,"monoph-phoPtHighMet-wg"       :['signal','wg',1,0]
                  ,"monoph-phoPtHighMet-zg"       :['signal','zg',1,0]
                  ,"monoph-phoPtHighMet-data_obs" :['signal','data',0,0]

                  ,"monoph-phoPtHighMet-dmv-500-1":['signal','dmv-500-1',1,1]
                  ,"monoph-phoPtHighMet-dmv-1000-1":['signal','dmv-1000-1',1,1]
                  ,"monoph-phoPtHighMet-dmv-2000-1":['signal','dmv-2000-1',1,1]

                  # Dimuon Control Region
                  ,"dimu-phoPtHighMet-vvg"        :['dimu','vvg',1,0]
                  ,"dimu-phoPtHighMet-zjets"      :['dimu','zjets',1,0]
                  ,"dimu-phoPtHighMet-top"        :['dimu','top',1,0]
                  ,"dimu-phoPtHighMet-zg"         :['dimu','zg',1,0]
                  ,"dimu-phoPtHighMet-data_obs"   :['dimu','data',0,0]
                   
                  # Dielectron Control Region
                  ,"diel-phoPtHighMet-vvg"        :['diel','vvg',1,0]
                  ,"diel-phoPtHighMet-top"        :['diel','top',1,0]
                  ,"diel-phoPtHighMet-zjets"      :['diel','zjets',1,0]
                  ,"diel-phoPtHighMet-zg"         :['diel','zg',1,0]
                  ,"diel-phoPtHighMet-data_obs"   :['diel','data',0,0]

                  # Single muon Control Region
                  ,"monomu-phoPtHighMet-vvg"      :['monomu','vvg',1,0]
                  ,"monomu-phoPtHighMet-zgamm"    :['monomu','zgamm',1,0]
                  ,"monomu-phoPtHighMet-top"      :['monomu','top',1,0]
                  ,"monomu-phoPtHighMet-wg"       :['monomu','wg',1,0]
                  ,"monomu-phoPtHighMet-data_obs" :['monomu','data',0,0]

                   # Single Electron Control Region
                  ,"monoel-phoPtHighMet-vvg"       :['monoel','vvg',1,0]
                  ,"monoel-phoPtHighMet-zgamm"     :['monoel','zgamm',1,0]
                  ,"monoel-phoPtHighMet-top"       :['monoel','top',1,0]
                  ,"monoel-phoPtHighMet-wg"        :['monoel','wg',1,0]
                  ,"monoel-phoPtHighMet-data_obs"  :['monoel','data',0,0]

	   	},
}

categories = [monophoton_category]
