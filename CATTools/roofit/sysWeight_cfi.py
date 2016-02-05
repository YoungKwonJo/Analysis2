
baseWeight = "weight*puweight*lepweight"
mceventweight=[
{"name":"NOM",                 "var": "("+baseWeight+")"},
{"name":"woLep",               "var": "(weight*puweight)"},
{"name":"csvweight",           "var": "("+baseWeight+"*csvweight)"},
{"name":"PuWeightUp",          "var": "(weight*puweightUp*lepweight*csvweight)"},
{"name":"PUWeightDN",          "var": "(weight*puweightDown*lepweight*csvweight)"},
{"name":"JER_Up",              "var": "("+baseWeight+"*csvweight)"},
{"name":"JER_Down",            "var": "("+baseWeight+"*csvweight)"},
{"name":"csvweight_JES_Up",    "var": "("+baseWeight+"*csvweight_JES_Up)"},        
{"name":"csvweight_JES_Down",  "var": "("+baseWeight+"*csvweight_JES_Down)"},      
{"name":"csvweight_LF_Up",     "var": "("+baseWeight+"*csvweight_LF_Up)"},         
{"name":"csvweight_LF_Down",   "var": "("+baseWeight+"*csvweight_LF_Down)"},       
#]
#ddddd=[
{"name":"csvweight_HF_Up",           "var": "("+baseWeight+"*csvweight_HF_Up)"},           
{"name":"csvweight_HF_Down",         "var": "("+baseWeight+"*csvweight_HF_Down)"},         
{"name":"csvweight_HF_Stats1_Up",    "var": "("+baseWeight+"*csvweight_HF_Stats1_Up)"},    
{"name":"csvweight_HF_Stats1_Down",  "var": "("+baseWeight+"*csvweight_HF_Stats1_Down)"},  
{"name":"csvweight_HF_Stats2_Up",    "var": "("+baseWeight+"*csvweight_HF_Stats2_Up)"},    
{"name":"csvweight_HF_Stats2_Down",  "var": "("+baseWeight+"*csvweight_HF_Stats2_Down)"},  
{"name":"csvweight_LF_Stats1_Up",    "var": "("+baseWeight+"*csvweight_LF_Stats1_Up)"},    
{"name":"csvweight_LF_Stats1_Down",  "var": "("+baseWeight+"*csvweight_LF_Stats1_Down)"},  
{"name":"csvweight_LF_Stats2_Up",    "var": "("+baseWeight+"*csvweight_LF_Stats2_Up)"},    
{"name":"csvweight_LF_Stats2_Down",  "var": "("+baseWeight+"*csvweight_LF_Stats2_Down)"},  
{"name":"csvweight_Charm_Err1_Up",   "var": "("+baseWeight+"*csvweight_Charm_Err1_Up)"},   
{"name":"csvweight_Charm_Err1_Down", "var": "("+baseWeight+"*csvweight_Charm_Err1_Down)"}, 
{"name":"csvweight_Charm_Err2_Up",   "var": "("+baseWeight+"*csvweight_Charm_Err2_Up)"},   
{"name":"csvweight_Charm_Err2_Down", "var": "("+baseWeight+"*csvweight_Charm_Err2_Down)"} 
#"csvt_sf","csvm_sf","csvl_sf","csvt_sfup","csvt_sfdw","csvm_sfup","csvm_sfdw","csvl_sfup","csvl_sfdw"
]


