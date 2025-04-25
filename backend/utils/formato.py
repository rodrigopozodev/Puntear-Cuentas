def asignar_indice_punteo(df):
    # Si la columna no existe, se crea vacía
    if 'Indice_Punteo' not in df.columns:
        df['Indice_Punteo'] = None
    return df
