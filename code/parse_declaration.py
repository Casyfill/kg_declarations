import pandas as pd
idx = pd.IndexSlice

def get_meta(df, bp):
    '''getting the general info from the declaration'''

    meta_names = df.iloc[1:bp, 0]
    meta_part = df.iloc[1:bp, 7]
    mask = meta_names.notnull()
    r = meta_part[mask]
    r.index = meta_names[mask]
    r.index.name = None
    meta = r.to_dict()
    meta['date'] = df.iloc[0,0].split(' ')[-1]
    return meta


def _remove_null_cols(df):
    mask = pd.DataFrame(df.columns.tolist()).notnull().any(1)
    return df[df.columns[mask]]


def prepare_content(df, bp1):
    bp2 = df[(df.iloc[:, 0] == 'Близкий родственник')].index[0]  # split between deputy and his relatives
    
    mask = df.iloc[:, 0].str.contains('должность указана на')
    if mask.any():
        bp3 = mask.astype(float).idxmax()  # remove footnote
    else:
        bp3 = len(df)
    
    cols = pd.MultiIndex.from_arrays(df.iloc[(bp1+1):(bp1+4), :20].values)
    content1 = df.iloc[bp1+5:bp2, :20].copy().dropna(axis=0, how='all')  # deputy
    content1.columns = cols
    content1 = _remove_null_cols(content1)
    
    content2 = df.iloc[bp2+1:bp3, :20].copy().dropna(axis=0, how='all')  # relatives
    content2.columns = cols
    content2 = _remove_null_cols(content2)
    return content1, content2


def get_indices(df):
    first_level = pd.Series(df.columns.get_level_values(0))
    res_index = first_level[first_level == "Недвижимое имущество"].index[0]
    other_index = first_level[first_level == 'Движимое имущество'].index[0] 

    return res_index, other_index


def _merge_colnames(df):
    cols1 = pd.Series(df.columns.get_level_values(1))
    cols2 = pd.Series(df.columns.get_level_values(2))
    cols2[cols2.isnull()] = cols1[cols2.isnull()]
    return cols2


def parse_real_estate(df, res_index:int, other_index:int):
    '''get real estate'''
    
    res_df = df.iloc[:, res_index:other_index].dropna(axis=0, how='all')
    res_df.columns = _merge_colnames(res_df)
    return res_df.dropna(axis=1).to_dict(orient='record')


def parse_other_estate(df, other_index:int):
    '''get real estate'''
    
    odf = df.iloc[:, other_index:].dropna(axis=0, how='all')
    odf.columns = _merge_colnames(odf)
    
    return odf.dropna(axis=1).to_dict(orient='record')



def get_values(df, key):
    if key in df.columns.get_level_values(0):
        k = idx[key, :]
        r = df.loc[:, k].iloc[:,0]
        return r[r.notnull()].tolist()
    else:
        return []
    

def parse_content(df):
    result = {}
    cdf = df.copy()

    cdf.sort_index(axis=1, inplace=True)
    result = {"income": get_values(cdf, 'Доходы'),
              "spendeturs": get_values(cdf, 'Расходы')}
    
    
    ri, oi = get_indices(df)

    result.update({"real_estate": parse_real_estate(df, ri, oi),
                   "other_estate": parse_other_estate(df, oi)})
    return result
    
    
def parse_declaration(df):
    mask = df.iloc[:, 0] == 'Декларант'
    bp = mask.astype(float).idxmax()
    
    r = get_meta(df, bp)
    
    # split between deputy and his relatives
    c1, c2 = prepare_content(df, bp)
    
    r["deputy"] = parse_content(c1)
    r["relatives"] = parse_content(c2)
    
    return r
