import pandas as pd
import stem
from stem.descriptor import DocumentHandler, parse_file
from .utils import fingerprint_default, name_default, bandwidth_default

'''
Returns given consensus path as DataFrame with nicknames and bandwidths of relays
Inputs: *path       : path to consensus file
        fp_column   : (default: 'fingerprint') name of df column containing the fingerprint of relay
        name        : (default: 'name') name of df column containing the nickname of relay
        bandwidth   : (default: 'bw') name of df columns containing the bandwidth of relay
Returns: df         : DataFrame object containing 3 columns
'''
def getConsensusDataFrame(path, fp_column=fingerprint_default, name=name_default, bandwidth=bandwidth_default):
    consensus = next(parse_file(path, descriptor_type = 'network-status-consensus-3 1.0',\
                                document_handler = DocumentHandler.DOCUMENT,))
    # Get list of relays
    routers = consensus.routers.items()
    relays = []
    for fingerprint, relay in routers:
        relays.append(relay)

    # Return DF containing name and bandwidth
    df = pd.DataFrame()
    df[fp_column] = [r.nickname + ' ' + r.fingerprint for r in relays]
    df[name] = [r.nickname for r in relays]
    df[bandwidth] = [r.bandwidth for r in relays]
    return df

'''
Returns a list of the values that are present in every dataframe in the input list
Inputs:  *dfs        : list object containing all dataframes of interest
         column_name : (default: 'name') string of the name of the column of interest
Returns: values_present, values_all      : List object cotaining the values found present in all input dataframes
'''
def getPresentValueList(dfs, column_name=fingerprint_default):
    # Get list of unique values for nicknames in all dataframes
    df_all = pd.concat(dfs)
    values_all = df_all[column_name].unique()
    values_present = []
    
    # For each value check that it exists in every df and add it to the present value list
    for v in values_all:
        for i,df in enumerate(dfs):
            if df[column_name].isin([v]).any():
                if i==len(dfs)-1:
                    values_present.append(v)
            else:
                break
    return values_present, values_all


'''
Returns a dataframe using the selected column as the key and the 2nd selected column as the values.
IMPORTANT all input dataframes must be same length and names must be unique and equal in all dataframes
Inputs   *dfs        : list of dataframes
         key_name    : (default:'name') String name of column to be used for key. (Must be consistent through all dfs)
         values_name : (default:'bw') String name of columnt to be used as values
Returns: df          : Dataframe
'''
def rearrangeDataFrames(dfs, key_name=fingerprint_default, values_name=bandwidth_default, name_name=name_default):
    df = pd.DataFrame()
    n = len(dfs)
    
    # Check conditions are met
    lengths = [df.shape[0] for df in dfs]
    if len(set(lengths)) != 1:
        print('ERROR: Not all datframes have same length!')
        print('Returning empty dataframe ...')
        return df
    
    # Concat all dfs in a big dataframe and rearrange
    df_all = pd.concat(dfs)
    df_temp = df_all.groupby(key_name)[values_name].apply(list).reset_index(name='list')
    
    df_answer = pd.DataFrame(df_temp['list'].tolist(), columns=[str(i) for i in range(n)])
    df_answer[fingerprint_default] = df_temp[fingerprint_default]
    df_answer = df_answer.set_index(fingerprint_default)
    
    
    return df_answer