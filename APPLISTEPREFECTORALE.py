import streamlit as st
import pandas as pd

# Chargement du fichier de base depuis GitHub
@st.cache
def load_base_data():
    base_url = "https://github.com/sedhadcci/Applisteprefectorale/raw/main/ListeprefectoralBASE.xlsx"
    return pd.read_excel(base_url)

# Fonction pour effectuer la correspondance
def perform_lookup(input_df, base_df):
    merged_df = pd.merge(input_df, base_df, how="left", left_on="CODE", right_on="CODE")
    return merged_df

# Interface Streamlit
st.title("Application pour correspondance de CODE")

uploaded_file = st.file_uploader("Choisissez un fichier Excel", type=["xlsx"])

if uploaded_file:
    input_df = pd.read_excel(uploaded_file)

    # Nettoyage des données : supprimer les lignes où la colonne 'CODE' est vide
    input_df.dropna(subset=['CODE'], inplace=True)
    
    base_df = load_base_data()
    base_df.dropna(subset=['CODE'], inplace=True)

    # Spécifiez les colonnes à utiliser
    base_columns = [0, 4, 5, 8, 18, 11, 13, 14, 21, 16]  # Par exemple, la colonne 0 pour "CODE", la colonne 4 pour "SIRET PREF", etc.

    # Filtrer les colonnes
    base_df_filtered = base_df.iloc[:, base_columns]

    # Effectuer la correspondance
    result_df = perform_lookup(input_df, base_df_filtered)

    # Afficher le résultat
    st.write(result_df)

    # Option pour télécharger le fichier résultant
    st.download_button(
        "Télécharger le fichier Excel après correspondance",
        data=result_df.to_excel(index=False),
        file_name="resultat_correspondance.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
