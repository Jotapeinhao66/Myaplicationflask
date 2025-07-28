import pandas as pd
import numpy as np

def load_and_clean_data(gdp_cons_path='DatosGDPCONS2.csv', internet_path='Porcentaje_acceso_internet.csv'):
    """
    Loads, cleans, and merges the GDP/Consumption and Internet usage dataframes.

    Args:
        gdp_cons_path (str): Path to the GDP and Consumption data CSV file.
        internet_path (str): Path to the Internet usage data CSV file.

    Returns:
        pd.DataFrame: A cleaned and filtered DataFrame containing merged data.
                      Filtered to include countries with a population >= 5,000,000.
    """
    try:
        df_gdp_cons = pd.read_csv(gdp_cons_path, delimiter=';', low_memory=False)
        df_internet = pd.read_csv(internet_path, delimiter=';', low_memory=False)

        merged_df = pd.merge(df_gdp_cons, df_internet, left_on='Paises', right_on='Country Name', how='inner')

        merged_df = merged_df.drop(columns=['Country Code', 'Indicator Name', 'Indicator Code', 'Country Name'])

        cols_to_convert = ['GDP Pais', 'Demanda per capita', 'Consumo', '2022', 'Población']
        for col in cols_to_convert:
            if col in merged_df.columns:
                merged_df[col] = merged_df[col].astype(str).str.replace(',', '.')
                merged_df[col] = pd.to_numeric(merged_df[col], errors='coerce')

        merged_df_cleaned = merged_df.dropna()

        merged_df_cleaned = merged_df_cleaned.rename(columns={'2022': 'porcentaje de uso de internet', 'Demanda per capita': 'Demanda per capita'})

        # Filter the data based on Population >= 5 Million
        merged_df_filtered = merged_df_cleaned[merged_df_cleaned['Población'] >= 5000000].copy()

        return merged_df_filtered

    except FileNotFoundError as e:
        print(f"Error loading file: {e}")
        return None
    except Exception as e:
        print(f"An error occurred during data processing: {e}")
        import traceback
        traceback.print_exc()
        return None
