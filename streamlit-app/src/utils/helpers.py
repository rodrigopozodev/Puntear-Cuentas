def load_data(file_path):
    """Carga datos desde un archivo y devuelve el contenido."""
    import pandas as pd
    return pd.read_csv(file_path)

def format_data(data):
    """Formatea los datos para su visualización."""
    return data.dropna().reset_index(drop=True)

def get_unique_values(data, column):
    """Devuelve los valores únicos de una columna específica."""
    return data[column].unique()