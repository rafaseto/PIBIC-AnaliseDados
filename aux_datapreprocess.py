import pandas as pd



# --------------------------------
# Func. para remover colunas
    
# Modelo da func. antiga
def dropColumns(df):
    df = df.drop(["TDEP"], axis=1)
    df = df.drop(["BSZ"], axis=1)
    df = df.drop(["CALI"], axis=1)
    df = df.drop(["TENS"], axis=1)
    df = df.drop(["DRHO"], axis=1)
    df = df.drop(["DCALI"], axis=1)
    return df

# Modelo da func. nova
def remove_colunas(df, colunas):
    df = df.drop(columns=colunas, errors='ignore')
    return df

'''
Exemplo de uso:
- colunas_para_remover = ['TDEP', 'BSZ', 'CALI', 'TENS', 'DRHO', 'DCALI']
- removeColunas(dlis_df, colunas_para_remover)
'''



# --------------------------------
# Func. para renomear colunas

# Modelo da func. antiga
def BStoBSZ(dlis_df):
    dlis_df[0].rename(columns={'BS': 'BSZ'}, inplace=True)
    return dlis_df

# Modelo da func. nova
# renomeiaColuna(dataframes, "BS", "BSZ")
def renomeiaColuna(df, coluna_antes, coluna_depois):
    df.rename(columns={coluna_antes: coluna_depois}, inplace=True)
    return df

'''
Exemplo de uso:
renomeia_coluna(dlis_df[0], "GR", "Gama Ray")
'''



# --------------------------------
# Func. para adicionar label

# Modelo da func. antiga
def addPocoLabel(df: pd.DataFrame, nPoco):
    match nPoco:
        case 0:
            df["Poco"] = "P-47"
        case 1:
            df["Poco"] = "P-48"
        case 2:
            df["Poco"] = "P-51"
        case 3:
            df["Poco"] = "P-53"
        case 4:
            df["Poco"] = "P-55"
        case 5:
            df["Poco"] = "P-57"

    return df

# Modelo da func.nova
def add_label(dlis_df, label, indexes, labels):
    for i in indexes:
        dlis_df[i][label] = labels[i]

'''
Exemplo de uso:
add_label(dlis_df, "Poco", [0,1,2,3,4,5], ["P-47", "P-48", "P-51", "P-53", "P-55", "P-57"])
'''



# ---------------------------------
# Func. para transformacao NPHI

# Modelo da func. antiga
def NPHItransform(dlis_df):
    dlis_df[0]["NPHI"] = (dlis_df[0]["NPHI"] * 100)
    dlis_df[1]["NPHI"] = (dlis_df[1]["NPHI"] * 100)
    dlis_df[3]["NPHI"] = (dlis_df[3]["NPHI"] * 100)
    return dlis_df

# Modelo da func. nova
def nphi_transform(dlis_df_dict, pocos):
    # 0 a 1 (checar)
    for poco in pocos:
        dlis_df_dict[poco]["NPHI"] *= 100

'''
Exemplo de uso:
nphi_transform(dlis_df, [0, 1, 3])
'''



# --------------------------------
# Func. para remover faixas de profundidade com falha

# Modelo da func. antiga
def removeFalha(dataframes):
    dataframes[0] = dataframes[0].drop(
        dataframes[0][(dataframes[0].profundidade  <= 250) | (dataframes[0].profundidade  >= 360)].index)
    dataframes[1] = dataframes[1].drop(
        dataframes[1][(dataframes[1].profundidade  <= 75) | (dataframes[1].profundidade  >= 210)].index)
    dataframes[2] = dataframes[2].drop(
        dataframes[2][(dataframes[2].profundidade  <= 60) | (dataframes[2].profundidade  >= 260)].index)
    dataframes[3] = dataframes[3].drop(
        dataframes[3][(dataframes[3].profundidade <= 90) | (dataframes[3].profundidade >= 300)].index)
    dataframes[4] = dataframes[4].drop(
        dataframes[4][(dataframes[4].profundidade <= 64) | (dataframes[4].profundidade >= 215)].index)
    dataframes[5] = dataframes[5].drop(
        dataframes[5][(dataframes[5].profundidade <= 90) | (dataframes[5].profundidade >= 320)].index)
    return dataframes


# Modelo da func. nova
def remove_pontos_com_falha(dlis_df_dict, pontos_com_falha):
    # Remove linhas com TDEP maior que o maximo desejado 
    for key, value in dlis_df_dict.items():
        dlis_df_dict[key] = value.drop(value[value['TDEP'] > pontos_com_falha[key][1]].index)

    # Remove linhas com TDEP menor que o minimo desejado
    for key, value in dlis_df_dict.items():
        dlis_df_dict[key] = value.drop(value[value['TDEP'] < pontos_com_falha[key][0]].index)    

# Defina condições de profundidade para cada dataframe
pontos_com_falha = {
    '1847': [250, 360],
    '1848': [75, 210],
    '1851': [60, 260],
    '1853': [90, 300],
    '1855': [64, 215],
    '1857': [90, 320]
}



# --------------------------------
# Func. para adicionar DCALI

# Modelo da func. antiga
def addDCALIfilter(dlis_df):
    for i in range(len(dlis_df)):
        dlis_df[i]['DCALI'] = dlis_df[i]['CALI'] - dlis_df[i]['BSZ']
    for i in range(len(dlis_df)):
        dlis_df[i] = dlis_df[i].drop(
            dlis_df[i][(dlis_df[i].DCALI > 2) | (dlis_df[i].DCALI < -2)].index)
        dlis_df[i] = dlis_df[i].drop(
            dlis_df[i][(dlis_df[i].DRHO > 0.15) | (dlis_df[i].DRHO < -0.15)].index)
    return dlis_df 

# Modelo da func. nova
def add_DCALI(dlis_df_dict):
    for poco in dlis_df_dict.values():
        if 'CALI' in poco.columns and 'BSZ' in poco.columns:
            poco['DCALI'] = poco['CALI'] - poco['BSZ']
        else:
            # Caso CALI ou BSZ estiverem ausentes
            poco['DCALI'] = None

def limita_curva(dlis_df_dict, curva, limite_inferior, limite_superior):
    # remove linhas que tem o valor da curva abaixo do limite inferior
    for key, value in dlis_df_dict.items():
        dlis_df_dict[key] = value.drop(value[value[curva] < limite_inferior].index)

    # remove linhas que tem o valor da curva acima do limite superior
    for key, value in dlis_df_dict.items():
        dlis_df_dict[key] = value.drop(value[value[curva] > limite_superior].index)