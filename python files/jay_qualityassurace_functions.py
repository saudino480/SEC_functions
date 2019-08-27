# Pipeline to spot errors

colNvalue_dict = {}
def key_ColFHtableNum_with_Vals(processdict):
    for k in processdict.keys():    # File Headers
        for i in range(0, len(processdict[k])):  # Tables lengths in one File Header
            for d in range(0, len(processdict[k][i].columns)):  # Column length in one table
                
                colNvalue_dict[ processdict[k][i].columns.to_list()[d].lower() + str('_') + str(k) + str('_') + str(i) ] = list( processdict[k][i][ processdict[k][i].columns[d] ] )
                
key_ColFHtableNum_with_Vals(df_dic)
colNvalue_dict

# Doc_id Checker

def doc_id_chekcer(colvaldict): 
    ## doc_id 
    for i in range(0, len( list(colvaldict.keys())) ):  # keys, (ex) price1_FST20030321_0
        if 'doc_id' in list(colvaldict.keys())[i] :
            for j in range(0, len(list(colvaldict.values())[i])): # values in the above keys, (ex) '$4.10','$4.07' ,'$4.16' ..
                if ( list(colvaldict.values())[i][j] in list(processed_dict.keys()) ):
                    print('"doc_id" column and value matches') 
                else: 
                    print(list(colvaldict.keys())[i])  # returns mismatching doc_id_fileheader_tableNo.
doc_id_chekcer(colNvalue_dict)



# Prob1

# Volume Checker #########################################################################################

matching= []
emptystr = []
notmathcing = []
dollarsign = []

# -
def vol_checker(colvaldict):
     
    for i in range(0, len( list(colvaldict.keys())) ):
        if 'vol' in list(colvaldict.keys())[i] and 'type' not in  list(colvaldict.keys())[i] : 
        
            for j in range(0, len(list(colvaldict.values())[i])):
                
                if list(colvaldict.values())[i][j].replace('.','',1).isdigit() == True: # and (  not in list(colvaldict.values())[i][j]) ) :
                    matching.append(list(colvaldict.keys())[i])
                elif list(colvaldict.values())[i][j].replace('-','', 2) == '':
                    emptystr.append(list(colvaldict.keys())[i])
                elif '$' in list(colvaldict.values())[i][j]:
                    dollarsign.append(list(colvaldict.keys())[i])
                    #print( (list(colvaldict.keys())[i]), 'contains an empty string value')
                else:
                     notmathcing.append(list(colvaldict.keys())[i])
                    #print( ( list(colvaldict.keys())[i]) , 'vol column contains a value that Does Not match')
    print('Mismatching of column and values in:', set(notmathcing))
    print('\n\n')                                                       # there are tables that can contain all notmatching, empty strings, matching, so focus on the non-matchings  
    print('Empty string is contained in:', set(emptystr))
    print('\n\n')
    print('Dollar sign is contained, so likely be values for price:', set(dollarsign))        
                
            
            
            
               # elif list(colvaldict.values())[i][j].replace('.','',1).isdigit() == False:
               #     print( list(colvaldict.keys())[i], 'check problem' )
    
vol_checker(colNvalue_dict)
   
#########################################################################################33333333333333333333

# Prob 1

# Price Checker
# To Do 

# Figure out the Fair Value
# Others are sufficient 


check_single_dict = {}
check_doubtrip_dict  = {}



emptystring = {}
singlevalue = {}

doubletriple = {}

single_character = {}
single_less150 = {}
single_over150 = {}
single_over150_fair = {}


def price_checker(colvaldict):
    
    for i in range(0, len(list(colvaldict.keys()))):
        if ('price' in list(colvaldict.keys())[i] or 'Price' in list(colvaldict.keys())[i])\
        and 'prices' not in list(colvaldict.keys())[i] and 'type' not in list(colvaldict.keys())[i] :
            
            for j in range(0, len(list(colvaldict.values())[i])):
                
                    if ("/" not in list(colvaldict.values())[i][j]) and ("|" not in list(colvaldict.values())[i][j]):
                        check_single_dict[str(list(colvaldict.keys())[i])] = list(colvaldict.values())[i][j] 
                                               
                        
                    elif ("/" in list(colvaldict.values())[i][j]) or ("|" in list(colvaldict.values())[i][j]): 
                        check_doubtrip_dict[str(list(colvaldict.keys())[i])] = list(colvaldict.values())[i][j]
                        
                                               
                    for m in range(0, len(list(check_single_dict.values()))):
                        
                        if list(check_single_dict.values())[m] == '':
                                    emptystring[list(colvaldict.keys())[i]] = list(check_single_dict.values())[m]
                                
                        elif (list(check_single_dict.values())[m].replace('.','',1).isdigit() == True) and (float(list(check_single_dict.values())[m]) > 150):
                                    single_over150[list(colvaldict.keys())[i]] = list(check_single_dict.values())[m]        # Fair value 못하겠음
                                
                        elif (  list(check_single_dict.values())[m].replace('.','',1).isdigit() == True) and (float(list(check_single_dict.values())[m]) < 150) :
                                    single_less150[list(colvaldict.keys())[i]] = list(check_single_dict.values())[m]
                                
                        elif (  list(check_single_dict.values())[m].replace('Neg', '', 2).replace('neg', '', 2)\
                                                                   .replace('$', '', 2)\
                                                                   .replace('(', '', 2)\
                                                                   .replace('.','',2)\
                                                                   .replace(' ','',1)\
                                                                   .replace(',','',2).isdigit() == False):
                                    single_character[list(colvaldict.keys())[i]] = list(check_single_dict.values())[m]
                                
price_checker(colNvalue_dict) 

#check
check_doubtrip_dict 
single_over150
single_less150
single_character




# Fair value checker (from single price over 150 )

ls = []
dic = {}

fair_single_over150 = {}
notfair_single = {}

def fair_value_checker(colvaldict, singleover150):

    for p in list(singleover150.keys()):
        for i in range(0, len(list(colvaldict.keys()))):
            if (p == list(colvaldict.keys())[i]) and ('fair' in list(colvaldict.values())[i+1][0]):     
                fair_single_over150[p] = str(colvaldict[p]) + str("   ") + str(list(colvaldict.values())[i+1]) 
            elif (p == list(colvaldict.keys())[i]) and ('fair' not in list(colvaldict.values())[i+1][0]):   
                notfair_single[p] = str(colvaldict[p]) + str("   ") + str(list(colvaldict.values())[i+1][0])
            
fair_value_checker(colNvalue_dict, single_over150)

fair_single_over150
notfair_single