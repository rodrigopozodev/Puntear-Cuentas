# main.py

import pandas as pd
from utils.excel_reader import read_excel
from utils.matcher import complete_matching, debe_matching, haber_matching
from utils.logger import setup_logger

def main():
    setup_logger()
    
    # Cargar archivos Excel
    debe_data = read_excel('path_to_debe_file.xlsx')
    haber_data = read_excel('path_to_haber_file.xlsx')
    
    # Realizar punteo completo
    complete_matches = complete_matching(debe_data, haber_data)
    
    # Realizar punteo solo de Debe
    debe_matches = debe_matching(debe_data, haber_data)
    
    # Realizar punteo solo de Haber
    haber_matches = haber_matching(debe_data, haber_data)
    
    # Aquí se pueden agregar más acciones, como guardar resultados o imprimir
    print("Punteo completo:", complete_matches)
    print("Punteo Debe:", debe_matches)
    print("Punteo Haber:", haber_matches)

if __name__ == "__main__":
    main()