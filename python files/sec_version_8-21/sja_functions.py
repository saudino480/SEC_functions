from IPython.display import display, HTML
import pandas as pd
import numpy as np
import re

'''
Basic Functions, helper functions
'''

def columnCleaner(dataFrame, key_words, stop_words, verbose = False, key_override = False, \
               condense = False, cleaner_label = "default"):

    dataFrame = dataFrame.rename(str.lower, axis = 'columns')

    if key_words is None:
        raise ValueError("Please remember to at least pass key_words an empty list if you are not going to use keywords.")

    i = 0
    transformation_dict = {}

    for colName in dataFrame.columns:
        key_bool = False

        for unit in key_words:
            temporary_unit = re.sub('[,\s]+', '', unit)
            temp_column = re.sub('[,\s]+', '', colName)
            stop_words = [re.sub('[,\s]+', '', x) for x in stop_words]
            if (temporary_unit in temp_column) & (stopWords(temp_column, stop_words)):
                key_bool = True
                unit_placeholder = unit

        if key_bool:

            i += 1
            new_name = cleaner_label + str(i)

            idx = dataFrame.columns.get_loc(colName)

            transformation_dict.update({colName : new_name})

            dataFrame = dataFrame.rename(columns = {colName : new_name})


            length = dataFrame.shape[0]
            if key_override:
                new_vals = np.array([unit_placeholder]*length)
            else:
                new_vals = np.array([colName]*length)
            dataFrame.insert(idx+1, new_name+"_type", new_vals)

    if condense:
        cols = [col for col in dataFrame.columns if (re.search(cleaner_label+ "_\d+", col) != None \
                                                     and re.search('_type$', col) == None)]
        idx = df[cols[0]].values == ""
        for col in cols[~0]:
            merge_idx = idx & (df[col].values != "")
            df[cols[0]].iloc[merge_idx] = df[col].values[merge_idx]


    if verbose:
        print(cleaner_label, " finished, processed " + str(i) + " columns.")
        print("-"*50)
        for item in transformation_dict.items():
            print("Old column: ", item[0], "  ----->  ", "New column: ", item[1])

        print("-"*50)

    return dataFrame

def replacerLogic(str1, str2, placeholder_str = ""):

    if ((str1 in str2) or (str1 == placeholder_str)):
        return str2
    elif str2 in str1:
        return str1
    else:
        return(str1 + " " + str2)


def trimDictonary(dictonary, value):
    new_dict = {}
    listOfItems = dictonary.items()
    for item in listOfItems:
        if item[1] != value:
            new_dict.update({item[0] : item[1]})
    return new_dict


def filterBusiness(dictonary, businessTicker):
    new_dict = {}
    listOfItems = dictonary.items()
    for item in listOfItems:
        if businessTicker in item[0]:
            new_dict.update({item[0] : item[1]})
    return new_dict


def stopWords(string, stopword_list):

    for stopword in stopword_list:
        if stopword in string:
            return False

    return True


def columnSorter(dataFrame, date_special = False):

    colNames = list(dataFrame.columns)

    unprocessed_columns = []
    for colName in colNames:
        if date_special:
            if re.search("vol_\d+", colName):
                continue
            elif re.search("price_\d+", colName):
                continue
            elif re.search("datetime_\d+", colName):
                continue
            # elif re.search('product_\D+', colName):
            #     continue
            # elif re.search('instrument_\D+', colName):
            #     continue
            # elif re.search('additional', colName):
            #     continue
            elif re.search('unit_type', colName):
                continue
            else:
                unprocessed_columns.append(colName)
        else:
            if re.search("vol_\d+", colName):
                continue
            elif re.search("price_\d+", colName):
                continue
            # elif re.search("datetime_\d+", colName):
            elif re.search("maturity", colName):
                continue
            elif re.search('product_\D+', colName):
                continue
            elif re.search('instrument_\D+', colName):
                continue
            elif re.search('additional', colName):
                continue
            elif re.search('unit_type', colName):
                continue
            else:
                unprocessed_columns.append(colName)

    return unprocessed_columns


def imputer(df, colID, replacement_string):
    old_values = df[colID].values

    new_values = []
    imputor = ""
    for val in old_values:
        if val != replacement_string:
            imputor = val
            new_values.append(imputor)
        else:
            new_values.append(imputor)

    df[colID] = new_values

    return df


def colCondensor(df, col_type):
    col_types_helper = {'volume' : 'vol_\d',
                        'date' : 'datetime_\d',
                        'price' : 'price_\d'}
    try:
        col_regex = col_types_helper[col_type]
    except:
        print('Invalid key. Please select either, \"volume\", \"date\" or \"price\"')
        return df

    colIDX_dict = {}
    col_list = [col for col in df.columns if (re.search(col_regex, col) != None)]

    for col in col_list:
        temp_df = df[col].replace('', np.nan)
        temp_df.dropna(inplace = True)
        idx = temp_df.index.values
        if len(idx) != 0:
            colIDX_dict.update({col : idx})


'''
Advanced functions, functions incoporate some of the above functions in order
to work.
'''

def verticalSplit(df_list, dictonary, verbose = False):
    split_dfs = []

    for df in df_list:
        df.columns = df.columns.str.lower()
        split_dict = {}

        for key in dictonary.keys():
            other_keys = [k for k in dictonary.keys() if k != key]
            exclusion_list = []
            for exclude in other_keys:
              exclusion_list += dictonary[exclude]

            split_columns = [col for col in df.columns if (any(name in col for name in dictonary[key]) \
                                                         or not any(name in col for name in exclusion_list))]
            pure_split_columns = [col for col in df.columns if (any(name in col for name in dictonary[key]) \
                                                              and not any(name in col for name in exclusion_list))]

            split_dict.update({key : [split_columns, pure_split_columns]})

        if sum([1 if val[1] != [] else 0 for val in split_dict.values()]) >= 2:
            i = 0
            for item in split_dict.items():
                if verbose:
                    print("Splitting on ", item[0])
                    print("Split ", i, "columns:\n", item[1][0])
                    print("Split ", i, "pure columns:\n", item[1][1])
                i += 1
                if item[1][1] == []:
                    continue

                if verbose:
                    split_df = df.loc[:, item[1][0]]
                    split_df.replace('', np.nan, inplace = True)
                    display(HTML(split_df.to_html()))
                    split_df.dropna(how = 'all', subset = item[1][1], inplace = True)
                    split_df.replace(np.nan, '', inplace = True)
                    display(HTML(split_df.to_html()))
                else:
                    split_df = df.loc[:, item[1][0]]
                    split_df.replace('', np.nan, inplace = True)
                    split_df.dropna(how = 'all', subset = item[1][1], inplace = True)
                    split_df.replace(np.nan, '', inplace = True)

                if split_df.shape[0] != 0:
                    split_dfs.append(split_df)
        else:
            if verbose:
                print("There was nothing to split!")
            split_dfs.append(df)

    return split_dfs


def anyCleaner(dataFrame, key_words, stop_words, units_column_helper, verbose = False, key_override = False, \
               condense = False, cleaner_label = "default"):

    dataFrame = dataFrame.rename(str.lower, axis = 'columns')
    if key_words is None: raise ValueError("Please remember to at least pass key_words an empty list if you are not going to use keywords.")
    if stop_words is None: stop_words = []
    if units_column_helper is None: units_column_helper = ['btu', 'bbl', 'gj']

    i = 0
    transformation_dict = {}
    df_col_names = list(dataFrame.columns)

    for colName in df_col_names:
        key_bool = False

        for unit in key_words:
            temporary_unit = re.sub('[,\s]+', '', unit)
            temp_column = re.sub('[,\s]+', '', colName)
            stop_words = [re.sub('[,\s]+', '', x) for x in stop_words]
            if (temporary_unit in temp_column) & (stopWords(temp_column, stop_words)):
                key_bool = True
                unit_placeholder = unit

        if key_bool:

            i += 1
            new_name = cleaner_label + "_" + str(i)

            idx = dataFrame.columns.get_loc(colName)

            transformation_dict.update({colName : new_name})

            dataFrame = dataFrame.rename(columns = {colName : new_name})


            length = dataFrame.shape[0]
            if key_override:
                new_vals = np.array([unit_placeholder]*length)
            else:
                new_vals = np.array([colName]*length)
            dataFrame.insert(idx+1, new_name+"_type", new_vals)

            if (idx+2) < len(dataFrame.columns):
                for unit in units_column_helper:
                    if np.any(dataFrame.iloc[:,idx+2].astype(str).str.contains(unit, regex = False, case = False)):
                        dataFrame[new_name+"_type"] = dataFrame.iloc[:,idx+2]
                        df_col_names = [col for col in df_col_names if col != dataFrame.columns[idx+2]]
                        dataFrame = dataFrame.drop(columns = dataFrame.columns[idx+2])
                        break

    if condense:
        cols = [col for col in dataFrame.columns if (re.search(cleaner_label+ "_\d+", col) != None \
                                                     and re.search('_type$', col) == None)]
        if verbose:
            print("These are the columns we are trying to condense: ", cols)
            print("And these are the columns of our dataframe: ", dataFrame.columns)
            display(HTML(dataFrame.to_html()))

        idx = (dataFrame[cols[0]].values == "")
        if (len(cols) == 2):
            merge_idx = idx & (dataFrame[cols[~0]].values != "")
            dataFrame[cols[0]].iloc[merge_idx, ] = dataFrame[cols[~0]].values[merge_idx]
            dataFrame[cols[~0]].iloc[merge_idx, ] = ""
            dataFrame[cols[0]+"_type"].iloc[merge_idx, ] = dataFrame[cols[~0]+"_type"].values[merge_idx]
            if all(dataFrame[cols[~0]].values == ""):
                dataFrame.drop(cols[~0], axis = 1, inplace = True)
                dataFrame.drop(cols[~0]+"_type", axis = 1, inplace = True)

        elif (len(cols) > 2):
            for col in cols[~0]:
                merge_idx = (idx & (dataFrame[col].values != ""))
                dataFrame[cols[0]].iloc[merge_idx, ] = dataFrame[col].values[merge_idx]
                dataFrame[col].iloc[merge_idx, ] = ""
                dataFrame[cols[0]+"_type"].iloc[merge_idx, ] = dataFrame[col+"_type"].values[merge_idx]
                idx = dataFrame[cols[0]].values == ""

                if all(dataFrame[col].values == ""):
                    dataFrame.drop(col, axis = 1, inplace = True)
                    dataFrame.drop(col+"_type", axis = 1, inplace = True)

        else:
            print("last part of condense")

    if verbose:
        print(cleaner_label, " finished, processed " + str(i) + " columns.")
        print("-"*50)
        for item in transformation_dict.items():
            print("Old column: ", item[0], "  ----->  ", "New column: ", item[1])

        print("-"*50)

    return dataFrame



def volumeCleaner(dataFrame, key_words, stop_words, verbose = False, key_override = False, \
                  condense = False, cleaner_label = "default", unit_search = False):
    dataFrame = dataFrame.rename(str.lower, axis = 'columns')
    #dataFrame = dataFrame.loc[:,~dataFrame.columns.duplicated()]
    if key_words == "":
        key_words = ['mmbbls', 'mbbls', 'bbl',
                  'mmcfe', 'mmcf', 'mcfe',
                  'mcf', 'bcfe', 'bcf',
                  'mmbtu', 'mbtu', 'btu',
                  'gj', 'dekatherm', 'volume',
                  'barrel', 'barrle', 'production',
                  'total outstanding notional']
    if stop_words == "":
        stop_words = ['sold price', 'purchased price', 'sales']

    units_column_helper = ['bbl', 'btu', 'gj']

    i = 0

    transformation_dict = {}

    for colName in dataFrame.columns:
        key_bool = False
        if colName not in dataFrame.columns:
            continue

        for unit in key_words:
            temporary_unit = re.sub('[,\s]+', '', unit)
            temp_column = re.sub('[,\s]+', '', colName)
            stop_words = [re.sub('[,\s]+', '', x) for x in stop_words]
            if (temporary_unit in temp_column) & (stopWords(temp_column, stop_words)):
                key_bool = True
                unit_placeholder = unit
                break

        if key_bool:
            if (np.any(dataFrame[colName].str.contains('$', regex = False))):
                continue
            i += 1
            new_name = 'vol_' + str(i)
            idx = dataFrame.columns.get_loc(colName)
            transformation_dict.update({colName : new_name})
            dataFrame = dataFrame.rename(columns = {colName : new_name})

            length = dataFrame.shape[0]
            if key_override:
                new_vals = np.array([unit_placeholder]*length)
            else:
                new_vals = np.array([colName]*length)

            dataFrame.insert(idx+1, new_name+"_type", new_vals)

            if unit_search:
                if (idx+2) < len(dataFrame.columns):
                    for unit in units_column_helper:
                        if np.any(dataFrame.iloc[:,idx+2].astype(str).str.contains(unit, regex = False, case = False)):
                            dataFrame[new_name+"_type"] = dataFrame.iloc[:,idx+2]
                            dataFrame = dataFrame.drop(columns = dataFrame.columns[idx+2])
                            break
    if verbose:
        print("volumeCleaner finished, processed " + str(i) + " columns.")
        print("-"*50)

        for item in transformation_dict.items():
            print("Old column: ", item[0], "  ----->  ", "New column: ", item[1])

        print("-"*50)

    return dataFrame


def dateCleaner(dataFrame, value_ids = ["placeholder"], ad_column = "additional", impute = False, duplicate = False):
    dataFrame = dataFrame.rename(str.lower, axis = 'columns')

    unprocessed_cols = columnSorter(dataFrame, date_special = True)
    # print(unprocessed_cols)
    for col in unprocessed_cols:
        for value_id in value_ids:
            if any(dataFrame[col].str.contains(value_id)):
                # print("I am true!", col)
                try:
                    dataFrame[col] = [dataFrame[ad_column].values[j] if re.search(value_id,x)==None else x for j,x in enumerate(dataFrame[col])]
                except:
                    print("We're gonna go but choose a better ad_column next time!", "\n\n")

                if duplicate:
                    dataFrame['old_maturity'] = dataFrame[col]
                dataFrame[col] = dataFrame[col].str.extract('(' + value_id + ')')
                dataFrame.rename(columns = {col : "maturity"}, inplace = True)


                if impute:
                    dataFrame = imputer(dataFrame, 'maturity', "")

                return dataFrame

    return dataFrame

def priceCleaner(dataFrame, key_words = "", stop_words = "", verbose = False, key_override = False):

    dataFrame = dataFrame.rename(str.lower, axis = 'columns')

    if key_words == "":
        key_words = ['fair value', 'weighted', 'price',
                     'ceiling', 'floor', 'sale', 'sold',
                     '$']

    if stop_words == "":
        stop_words = ['(in thousands,', 'united states', 'priceindex',
                      'price index', 'volume', 'mmbtu/d', 'mbbls/d',
                      'except price']

    i = 0

    transformation_dict = {}

    for colName in dataFrame.columns:
        key_bool = False

        for unit in key_words:
            temporary_unit = re.sub('[,\s]+', '', unit)
            temp_column = re.sub('[,\s]+', '', colName)
            stop_words = [re.sub('[,\s]+', '', x) for x in stop_words]
            if (temporary_unit in temp_column) & (stopWords(temp_column, stop_words)):
                key_bool = True
                unit_placeholder = unit

        if key_bool:

            i += 1
            new_name = 'price_' + str(i)

            idx = dataFrame.columns.get_loc(colName)

            transformation_dict.update({colName : new_name})

            dataFrame = dataFrame.rename(columns = {colName : new_name})


            length = dataFrame.shape[0]
            if key_override:
                new_vals = np.array([unit_placeholder]*length)
            else:
                new_vals = np.array([colName]*length)
            dataFrame.insert(idx+1, new_name+"_type", new_vals)

    if verbose:
        print("priceCleaner finished, processed " + str(i) + " columns.")
        print("-"*50)
        for item in transformation_dict.items():
            print("Old column: ", item[0], "  ----->  ", "New column: ", item[1])

        print("-"*50)

    return dataFrame


def productCleaner(dataFrame, key_words = "", stop_words = "", impute = False, verbose = False):
    dataFrame = dataFrame.rename(str.lower, axis = "columns")
    #dataFrame = dataFrame.loc[:, ~dataFrame.columns.duplicated()]

    if key_words == "":
        key_words = ['oil', 'natural gas liquid', 'liquid natural gas', 'natural gas', 'gas',
                     'barrel', 'btu', 'bbl', 'ngl', 'mcf']
        units_helper = {'barrel' : 'oil', 'btu' : 'natural gas', 'bbl' : 'oil', 'gas': 'natural gas',
                        'ngl': 'natural gas liquid', 'mcf' : 'natural gas'}
    if stop_words == "":
        stop_words = []

    i = 0

    transformation_dict = {}
    product_types = []

    # checks to see if product_type already exists as a column name
    if "product_type" not in list(dataFrame.columns):
        condition = 1
    elif any(dataFrame['product_type'] == ''):
        condition = 2
    else:
        condition = 3

    if (condition == 1) or (condition == 2):
        if condition == 1:
            idx = len(list(dataFrame.columns))
            length = dataFrame.shape[0]
            new_vals = np.array(["@"]*length)
            dataFrame.insert(idx, "product_type", new_vals)
        if condition == 2:
            dataFrame['product_type'] = dataFrame['product_type'].replace('', '@')


        # look through the keywords
        for key in key_words:
            data_rows = dataFrame[dataFrame.apply(lambda row: row.astype(str).str.contains(key, case = False).any(), axis = 1)]

            if key in units_helper.keys():
                prod_type = units_helper[key]
            else:
                prod_type = key

            # if we have any results, continue
            if data_rows.shape[0] != 0:
                # same logic as instrumentCleaner, looks to see if it needs updating or replacing of the value.
                updated_values = dataFrame.product_type.loc[data_rows.index, ].apply(lambda existing_val: replacerLogic(existing_val, prod_type, '@'))
                dataFrame.loc[data_rows.index, "product_type"] = updated_values
                transformation_dict.update({", ".join(data_rows.index.values.astype(str)) : key + " " + prod_type})

        # if there is still a "@" (aka placeholder) in the product_type, continue
        if "@" in dataFrame.product_type.values:

            # filter rows that still need information
            rows_to_update = dataFrame[dataFrame.product_type == "@"]
            # placeholder value so we can do string comparison later
            # without it throwing an error
            product_types = {}

            for colName in dataFrame.columns:

                for key in key_words:
                    if ((key in colName) & stopWords(colName, stop_words)):
                        idx = (dataFrame[colName] != '')
                        product_types.update({key : idx})

            for dict_key in product_types.keys():
                idx = product_types[dict_key]

                if dict_key in units_helper.keys():
                    key = units_helper[dict_key]
                else:
                    key = dict_key

                transformation_dict.update({'added these products' : product_types})

                dataFrame.loc[idx, 'product_type'] = dataFrame.loc[idx, 'product_type'].apply(lambda existing_val: key if (existing_val == '@') else existing_val)

        if impute:
            dataFrame = imputer(dataFrame, 'product_type', "@")

        if verbose:
            print("productCleaner finished, processed " + str(i) + " columns.")
            print("-"*50)

            for item in transformation_dict.items():
                print("Old column: ", item[0], "  ----->  ", "The product_type entry is: ", item[1])

            print("-"*50)
    else:
        if verbose:
            print("Column product_type already exists")

        if impute:
            dataFrame = imputer(dataFrame, 'product_type', "")

    return dataFrame

# make it accept unit helper as well
def instrumentCleaner(dataFrame, key_words = "", stop_words = "", impute = False, verbose = False):
    '''
    instrumentCleaner attempts to isolate option, whether it be swaps, collars, put,
    etc. It first looks through the column names, and then through the table itself
    in order to impute what kind of option it is.
    '''
    dataFrame = dataFrame.rename(str.lower, axis = "columns")
    #dataFrame = dataFrame.loc[:, ~dataFrame.columns.duplicated()]
    if key_words == "":
        key_words = ['cap-swaps','swap option', 'fixed-price swap', 'basis swap',
                     'two-way collar', 'three-way collar', 'two way collar',
                     'three way collar', 'put option', 'fixed price swap',
                     'floor', 'ceiling', 'fixed price',
                     'swaption', 'swap', 'collar', 'put', 'call']
        units_helper = {'floor' : 'collar', 'ceiling' : 'collar', 'fixed-price swap' : 'swap',
                        'fixed price swap' : 'swap'}
    if stop_words == "":
        stop_words = []

    i = 0
    transformation_dict = {}
    # need to store instrument_types in case there are multiple in the table.
    instrument_types = []

    # make sure you don't already have this column in your DF.

    if "instrument_type" not in list(dataFrame.columns):
        condition = 1
    elif any(dataFrame['instrument_type'] == ''):
        condition = 2
    else:
        condition = 3

    if (condition == 1) or (condition == 2):
        if condition == 1:
            idx = len(list(dataFrame.columns))
            length = dataFrame.shape[0]
            new_vals = np.array(["@"]*length)
            dataFrame.insert(idx, "instrument_type", new_vals)
        if condition == 2:
            dataFrame['instrument_type'] = dataFrame['instrument_type'].replace('', '@')


        for key in key_words:
            # isolate the rows in the dataFrame that contain the key.
            data_rows = dataFrame[dataFrame.apply(lambda row: row.astype(str).str.contains(key, case = False).any(), axis = 1)]

            if key in units_helper:
                key = units_helper[key]
            # if any rows are found, continue
            if data_rows.shape[0] != 0:
                # FIRST: get a subset of the dataFrame column we made above 'instrument_type' using the data_rows that are flagged (also above)
                # SECOND: use .apply to decide whether to UPDATE, or REPLACE the existing_val in the dataFrame.
                # THIRD: update the dataFrame with the new values.
                # FOURTH: update the transformation dictionary to store changes.
                updated_values = dataFrame.instrument_type.loc[data_rows.index, ].apply(lambda existing_val: replacerLogic(existing_val, key, '@'))
                dataFrame.instrument_type.loc[data_rows.index, ] = updated_values
                transformation_dict.update({", ".join(data_rows.index.values.astype(str)) : key})

    if "@" in dataFrame.instrument_type.values:
        rows_to_update = dataFrame[dataFrame.instrument_type == "@"]
        instrument_types = {}
        for colName in dataFrame.columns:

            for key in key_words:
                if ((key in colName) & stopWords(colName, stop_words)):
                    idx = (dataFrame[colName] != '')
                    instrument_types.update({key : idx})

        # if any of the keywords showed up. continue through to here
        for dict_key in instrument_types.keys():
            idx = instrument_types[dict_key]

            if dict_key in units_helper.keys():
                key = units_helper[dict_key]
            else:
                key = dict_key

            transformation_dict.update({'added these products' : instrument_types})

            # get index for rows that need to still be updated
            # update them with the list collapsed to a single string
            dataFrame.loc[idx, "instrument_type"] = dataFrame.loc[idx, 'instrument_type'].apply(lambda existing_val: key if (existing_val == '@') else existing_val)

        if impute:
            dataFrame = imputer(dataFrame, 'instrument_type', "@")

    else:
        print("instrument_type column already exists")

        if impute:
            dataFrame = imputer(dataFrame, 'instrument_type', "")



    if verbose:
        print("instrumentCleaner finished, processed " + str(i) + " columns.")
        print("-"*50)

        for item in transformation_dict.items():
            print("Old column: ", item[0], "  ----->  ", "The instrument_type entry is: ", item[1])

        print("-"*50)

    return dataFrame


# PHASING OUT, TO BE REMOVED SOON
def dateCleaner_legacy(dataFrame, key_words = "", stop_words = "", impute = False, verbose = False):

    dataFrame = dataFrame.rename(str.lower, axis = 'columns')
    #dataFrame = dataFrame.loc[:,~dataFrame.columns.duplicated()]
    if key_words == "":
        key_words = ['date', 'period', 'term',
                     'commodity/operating area/index', 'month',
                     'maturity', 'expiration', 'duration']
    if stop_words == "":
        stop_words = ['price', 'location', 'volume',
                      'type of', ',,period,']

    if (re.search("\d{4}", dataFrame.index.values.astype(str)[0]) is not None) or \
       (re.search("quarter", dataFrame.index.values.astype(str)[0]) is not None):
        # store old_name to use for values later
        old_name = dataFrame.columns.name
        #print(old_name)
        # reset the index to pop the date information into a column
        dataFrame = dataFrame.reset_index().rename(columns={dataFrame.columns.name : None})

        # make new column name
        i += 1
        new_name = 'datetime_' + str(i)

        # keep track of transformations
        transformation_dict.update({'index' : new_name})

        # rename the now-reset index.
        dataFrame = dataFrame.rename(columns = {'index' : new_name})

        # get index so we can add the type column after our newly renamed column
        idx = dataFrame.columns.get_loc(new_name)
        # insert new type column
        length = dataFrame.shape[0]
        new_vals = np.array(['index']*length)
        dataFrame.insert(idx+1, new_name+"_type", new_vals)

        if impute:
            dataFrame = imputer(dataFrame, new_name, "")


    for colName in dataFrame.columns:

        key_bool = False

        if 'datetime_' in colName:
            continue

        if colName == "":
            if (re.search("\d{4}", dataFrame[colName].values.astype(str)[0]) is not None):
                key_bool = True
            else:
                continue

        for unit in key_words:
            temporary_unit = re.sub('[,\s]+', '', unit)
            temp_column = re.sub('[,\s]+', '', colName)
            stop_words = [re.sub('[,\s]+', '', x) for x in stop_words]
            if (temporary_unit in temp_column) & (stopWords(temp_column, stop_words)):
                key_bool = True
                unit_placeholder = unit

        if key_bool:
            i += 1
            new_name = 'datetime_' + str(i)
            idx = dataFrame.columns.get_loc(colName)
            # print('The index of the changed date column is : ', idx, '\n',
            #       'The column name is: ', colName)
            transformation_dict.update({colName : new_name})
            dataFrame = dataFrame.rename(columns = {colName : new_name})

            length = dataFrame.shape[0]
            if key_override:
                new_vals = np.array([key_impute]*length)
            else:
                new_vals = np.array([colName]*length)
            dataFrame.insert(idx+1, new_name+"_type", new_vals)

            if impute:
                dataFrame = imputer(dataFrame, new_name, "")

    if verbose:
        print("dateCleaner finished, processed " + str(i) + " columns.")
        print("-"*50)

        for item in transformation_dict.items():
            print("Old column: ", item[0], "  ----->  ", "New column: ", item[1])

        print("-"*50)

    return dataFrame



'''
THE FUNCTION GRAVEYARD (VERY SPOOKY KEEP OUT)
def theConcatenator(dictonary, output="df"):

    big_df = pd.DataFrame()
    listOfItems = dictonary.items()
    processed_dict = {}

    for item in listOfItems:
        print("*"*50)
        print(item[0])
        print("Processing ", len(item[1]), " tables")
        doc_id = item[0]
        processed_tables = tableProcessor(item[1])

        if output == "df":
            for table in processed_tables:
                length = table.shape[0]
                doc_id_col = np.array([doc_id]*length)
                table.insert(0, "doc_id", doc_id_col)
                table = table.drop_duplicates(  )
                big_df = pd.concat([big_df, table], axis = 0, join = 'outer', sort = False)

        elif output == 'pickle':
            for table in processed_tables:
                length = table.shape[0]
                doc_id_col = np.array([doc_id]*length)
                table.insert(0, "doc_id", doc_id_col)
                table = table.drop_duplicates()
            processed_dict.update({item[0] : processed_tables})

        else:
            print('not recognized output')
            return ""

    if output == 'df':
        big_df = big_df.drop_duplicates()
        return big_df
    elif output == 'pickle':
        return processed_dict
    else:
        return ""


def tableProcessor(table_list):
    new_list = []
    i = 0
    for table in table_list:
        i += 1
        print("@"*50, "\n", "Processing table: " + str(i))
        display(HTML(table.to_html()))
        table = dateCleaner(table)
        table = volumeCleaner(table)
        table = priceCleaner(table)
        table.columns = table.columns.str.lower()
        unprocessed = columnSorter(table)
        print("Unprocessed columns: ", "\n", unprocessed)
        display(HTML(table.to_html()))
        new_list.append(table)

    return new_list

def productCleaner(dataFrame, key_words = "", stop_words = "", impute = False, verbose = False):
    dataFrame = dataFrame.rename(str.lower, axis = "columns")
    #dataFrame = dataFrame.loc[:, ~dataFrame.columns.duplicated()]

    if key_words == "":
        key_words = ['oil', 'natural gas liquid', 'liquid natural gas', 'natural gas', 'gas',
                     'barrel', 'btu', 'bbl', 'ngl', 'mcf']
        units_helper = {'barrel' : 'oil', 'btu' : 'natural gas', 'bbl' : 'oil', 'gas': 'natural gas',
                        'ngl': 'natural gas liquid', 'mcf' : 'natural gas'}
    if stop_words == "":
        stop_words = []

    i = 0

    transformation_dict = {}
    product_types = []

    # checks to see if product_type already exists as a column name
    if "product_type" not in dataFrame.columns:
        # if not, it creates a column with '@' as a temporary placeholder for easy searching.
        idx = len(list(dataFrame.columns))

        # inserts column at the end of the dataFrame.
        length = dataFrame.shape[0]
        new_vals = np.array(["@"]*length)
        dataFrame.insert(idx, "product_type", new_vals)

        # look through the keywords
        for key in key_words:
            if key in units_helper.keys():
                prod_type = units_helper[key]
            else:
                prod_type = key
            # filter data rows that contain any product information ('oil', 'gas', etc)
            data_rows = dataFrame[dataFrame.apply(lambda row: row.astype(str).str.contains(key, case = False).any(), axis = 1)]

            # if we have any results, continue
            if data_rows.shape[0] != 0:
                # same logic as instrumentCleaner, looks to see if it needs updating or replacing of the value.
                updated_values = dataFrame.product_type.loc[data_rows.index, ].apply(lambda existing_val: replacerLogic(existing_val, prod_type, '@'))
                dataFrame.loc[data_rows.index, "product_type"] = updated_values
                transformation_dict.update({", ".join(data_rows.index.values.astype(str)) : key + " " + prod_type})

        # if there is still a "@" (aka placeholder) in the product_type, continue
        if "@" in dataFrame.product_type.values:

            # filter rows that still need information
            rows_to_update = dataFrame[dataFrame.product_type == "@"]
            # placeholder value so we can do string comparison later
            # without it throwing an error
            product_types = [""]

            for colName in dataFrame.columns:

                for key in key_words:
                    if (key in colName):
                        if key in units_helper.keys():
                            key = units_helper[key]
                        # so we want to make sure we don't add the same thing
                        # (ie, 'gas', 'natural gas') so we do a little boolean logic
                        # to check if the key we are about to add is already a substring.
                        for product in product_types:
                            # this is our base case and will evaluate the first time a keyword shows up.
                            if product == "":
                                # we want to remove it, since it's just a placeholder, and replace it with
                                # the key that is in the colName.
                                product_types.remove(product)
                                product_types.append(key)
                            # if the key is not in product_types, it's ok to add it
                            if key not in product:
                                product_types.append(key)
                            # otherwise we want to remove the key that's a substring, and replace it with
                            # the new key.
                            else:
                                product_types.remove(product)
                                product_types.append(key)

            # if any keys are added in the last step, continue
            if len(product_types) != 0:

                # remove duplicates
                product_types = list(dict.fromkeys(product_types))
                transformation_dict.update({'added these products' : product_types})

                # get index for rows that need to still be updated
                update_idx = dataFrame.product_type[dataFrame.product_type == "@"].index

                # update them with the list collapsed to a single string
                dataFrame.loc[update_idx, "product_type"] = ", ".join(product_types)

        if impute:
            dataFrame = imputer(dataFrame, 'product_type', "@")

        if verbose:
            print("productCleaner finished, processed " + str(i) + " columns.")
            print("-"*50)

            for item in transformation_dict.items():
                print("Old column: ", item[0], "  ----->  ", "The product_type entry is: ", item[1])

            print("-"*50)
    else:
        if verbose:
            print("Column product_type already exists")

        if impute:
            dataFrame = imputer(dataFrame, 'product_type', "")

    return dataFrame


def volumeCleaner_specialSauce(dataFrame, key_words = "", stop_words = "", verbose = False):
    dataFrame = dataFrame.rename(str.lower, axis = 'columns')
    #dataFrame = dataFrame.loc[:,~dataFrame.columns.duplicated()]
    if key_words == "":
        key_words = ['mmbbls', 'mbbls', 'bbl',
                  'mmcfe', 'mmcf', 'mcfe',
                  'mcf', 'bcfe', 'bcf',
                  'mmbtu', 'mbtu', 'btu',
                  'gj', 'dekatherm', 'volume',
                  'barrel', 'barrle', 'production',
                  'total outstanding notional']
    if stop_words == "":
        stop_words = ['sold price', 'purchased price', 'sales']

    units_column_helper = ['bbl', 'btu', 'gj']

    i = 0

    transformation_dict = {}

    for colName in dataFrame.columns:
        volume_bool = False
        if colName not in dataFrame.columns:
            continue

        for key in key_words:
            if (key in colName) & (stopWords(colName, stop_words)):
                volume_bool = True
                break

        if volume_bool:
            if (np.any(dataFrame[colName].str.contains('$', regex = False))):
                continue
            i += 1
            new_name = 'vol_' + str(i)
            idx = dataFrame.columns.get_loc(colName)
            transformation_dict.update({colName : new_name})
            dataFrame = dataFrame.rename(columns = {colName : new_name})

            length = dataFrame.shape[0]
            new_vals = np.array([colName]*length)
            dataFrame.insert(idx+1, new_name+"_type", new_vals)

            # if (idx+2) < len(dataFrame.columns):
            #     for unit in units_column_helper:
            #         if np.any(dataFrame.iloc[:,idx+2].astype(str).str.contains(unit, regex = False, case = False)):
            #             dataFrame[new_name+"_type"] += ", " + dataFrame.iloc[:,idx+2]
            #             dataFrame = dataFrame.drop(columns = dataFrame.columns[idx+2])
            #             break
    if verbose:
        print("volumeCleaner finished, processed " + str(i) + " columns.")
        print("-"*50)

        for item in transformation_dict.items():
            print("Old column: ", item[0], "  ----->  ", "New column: ", item[1])

        print("-"*50)

    return dataFrame

def labelCleaner(colString, keys, split_on = ""):
    units_helper = {'mm': 1e7, 'm': 1e4, 'day': 365, 'month': 12}
    match_list = []
    if isinstance(split_on, str):
        string_list = colString.split(split_on)
    else:
        print("Wrong type for split_on, please enter a different value.")
        return colString
    for string in string_list:
        for key in keys:
            if key in string:
                match_list.append(string)

    clean_string = "".join(match_list)

    return clean_string

def verticalSplit(table_list, verbose = False):
    Takes a list of tables and attempts to split them.
    Returns a new table_list that has the original tables split, if needed.
    split_dfs = []
    transformation_dict = {}

    i = 0
    #print(len(table_list))
    for table in table_list:
        table = table.rename(str.lower, axis = "columns")
        table_columns = table.columns
        # we want the columns that have either the word 'oil' or 'bbl' in the column, but we want to omit columns that
        # have information purely about gas, ie, either 'gas' or 'btu'. We then add these two queries together, and remove
        # the columns that are duplicates between oil_cols and oil_cols2.
        # We then create a pure_oil_cols, which we make sure does not have ANY gas information in it.
        oil_helper = ['oil', 'bbl']
        gas_helper = ['gas', 'ngl', 'btu']

        oil_cols = [col for col in table_columns if (not any(gas in col for gas in gas_helper) \
                                                             or any(oil in col for oil in oil_helper))]
        pure_oil_cols = [col for col in oil_cols if (not any(gas in col for gas in gas_helper) \
                                                     and any(oil in col for oil in oil_helper))]


        gas_cols = [col for col in table_columns if (any(gas in col for gas in gas_helper) \
                                                     or not any(oil in col for oil in oil_helper))]
        pure_gas_cols = [col for col in gas_cols if (any(gas in col for gas in gas_helper) \
                                                     and not any(oil in col for oil in oil_helper))]

        # output to console
        if verbose:
            print("oil_cols: ", oil_cols)
            print("pure_oil_cols: ", pure_oil_cols)
            print("gas_cols: ", gas_cols)
            print("pure_gas_cols: ", pure_gas_cols)

        # if we have BOTH columns that ONLY HAVE oil information and gas information, we continue.
        if ((pure_oil_cols != []) & (pure_gas_cols != [])):
            # this is the noisy version of the below function
            if verbose:
                print("Oil Split")
                print("*"*50)
                oil_df = table.loc[:, oil_cols]
                oil_df.replace('', np.nan, inplace = True)
                display(HTML(oil_df.to_html()))
                oil_df = oil_df.dropna(how = 'all', subset = pure_oil_cols)
                display(HTML(oil_df.to_html()))

                print("Gas Split")
                print("*"*50)
                gas_df = table.loc[:, gas_cols]
                gas_df.replace('', np.nan, inplace = True)
                display(HTML(gas_df.to_html()))
                gas_df = gas_df.dropna(how = 'all', subset = pure_gas_cols)
                display(HTML(gas_df.to_html()))
            else:
                # grab columns that we've sorted using oil_cols
                oil_df = table.loc[:, oil_cols]
                # replace all empty strings with np.nan so we can drop NA
                oil_df.replace('', np.nan, inplace = True)
                # if the PURELY OIL columns have NAs for all values, that means that they can be dropped without loss of information.
                oil_df = oil_df.dropna(how = 'all', subset = pure_oil_cols)

                # this is the same process as the oil.
                gas_df = table.loc[:, gas_cols]
                gas_df.replace('', np.nan, inplace = True)
                gas_df = gas_df.dropna(how = 'all', subset = pure_gas_cols)

            # return the NANs to empty strings so you don't break anyone elses' function.
            oil_df.replace(np.nan, '', inplace = True)
            gas_df.replace(np.nan, '', inplace = True)
            # add the newly split dfs to a new list, that we will eventually return.
            split_dfs.append(oil_df)
            split_dfs.append(gas_df)

            # keep track of updates
            transformation_dict.update({"table" : "attempted to split horizontally"})
            i += 1

        else:
            # if we did not have both pure_gas_cols and pure_oil_cols, we don't need to split,
            # so we just add the table and move on.
            if verbose:
                print("Nothing to split here! Moving on...")
                print("^"*50)
            split_dfs.append(table)

    # return new table_list with the newly split dataFrames.
    return split_dfs


'''
