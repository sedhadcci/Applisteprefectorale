import streamlit as st
import pandas as pd

# Chargement du fichier de base depuis GitHub
@st.cache
def load_base_data():
    base_url = "https://github.com/sedhadcci/Applisteprefectorale/raw/main/ListeprefectoralBASE.xlsx"
    return pd.read_excel(base_url, header=None)  # Pas de noms de colonne

# Fonction pour effectuer la correspondance
def perform_lookup(input_codes, base_df):
    filter_condition = base_df.iloc[:, 0].isin(input_codes)
    result_df = base_df[filter_condition]
    return result_df

# Interface Streamlit
st.title("Application pour correspondance de CODE")

uploaded_file = st.file_uploader("Choisissez un fichier texte avec les codes", type=["txt"])

if uploaded_file:
    input_txt = uploaded_file.read().decode("utf-8")
    input_codes = input_txt.strip().split('\n')

    base_df = load_base_data()
    base_df.dropna(subset=[0], inplace=True)  # Élimine les NaN de la première colonne (index 0)

    # Spécifiez les colonnes à utiliser
    base_columns = [0, 4, 5, 8, 18, 11, 13, 14, 21, 16]  # Colonnes par indice

    # Filtrer les colonnes
    base_df_filtered = base_df.iloc[:, base_columns]

    # Effectuer la correspondance
    result_df = perform_lookup(input_codes, base_df_filtered)

    # Afficher le résultat
    st.write(result_df)

    # Option pour télécharger le fichier résultant
    st.download_button(
        "Télécharger le fichier Excel après correspondance",
        data=result_df.to_excel(index=False),
        file_name="resultat_correspondance.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
