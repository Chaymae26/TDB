import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def install_dependencies():
    import subprocess
    subprocess.check_call(['pip', 'install', 'matplotlib==3.4.0'])

st.set_page_config(page_title="Tableau de Bord", page_icon=":bar_chart:",layout="wide")
st.title(":bar_chart: Tableau de Bord")
st.markdown('<style>div.block-container{padding-top:3rem;}</style>', unsafe_allow_html=True)
st.subheader("Bienvenue! 👋 Veillez Choisir une Option pour Votre Tableau de Bord")

def main(option, uploaded_file, selected_year, selected_category,selected_direction,selected_impacted_dir):
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)

        if selected_year and selected_year != 'Toutes':
            df = df[df['Année'] == selected_year]
        if selected_category and selected_category != 'Toutes':
            df = df[df['Catégorie'] == selected_category]
        if selected_direction and selected_direction != 'Toutes':
            df = df[df['Direction Responsable'] == selected_direction]
        if selected_impacted_dir and selected_impacted_dir != 'Toutes':
            df = df[df['Direction Impactée'] == selected_impacted_dir]
        if option == "Tableau de Bord Risques":
            afficher_graphiques_risques(df)
        elif option == "Tableau de Bord Incidents":
            afficher_graphiques_incidents(df)

       

def afficher_graphiques_risques(df):
    top_risques = df.sort_values(by='Criticité Nette Actuelle', ascending=False).head(15)

    # Create subplots with larger figsize
    fig, axs = plt.subplots(1, 2, figsize=(18, 8))

    # Plot the bar chart
    axs[0].barh(top_risques['Risques'], top_risques['Criticité Nette Actuelle'])
    axs[0].set_xlabel('Criticité Nette Actuelle')
    axs[0].set_ylabel('Risques')
    axs[0].set_title('Top risques par criticité nette', fontsize=16, fontweight='bold')

    # Plot the risk map
    impact = df['Impact']
    probabilite = df['Probabilité']
    sc = axs[1].scatter(probabilite, impact, c=impact * probabilite, cmap='RdYlGn_r', s=1000, alpha=0.7, edgecolors="grey", linewidth=2)
    plt.colorbar(sc, ax=axs[1], label='Criticité')
    axs[1].set_xlabel('Probabilité')
    axs[1].set_ylabel('Impact')
    axs[1].set_title('Cartographie des Risques', fontsize=16, fontweight='bold')
    axs[1].grid(True)

    # Show the plot
    st.pyplot(fig)

    kri_counts = df['Etat Criticité'].value_counts()

    # Create a pie chart
    fig, axs = plt.subplots(1, 2, figsize=(20, 8), gridspec_kw={'wspace': 0.2})

    # Plot the pie chart
    axs[0].pie(kri_counts, labels=kri_counts.index, autopct='%1.1f%%', startangle=90, colors=['#04B431','#FFBF00','#DF0101'], wedgeprops=dict(width=0.5))
    axs[0].set_title('Etat de la Criticité', fontsize=16, fontweight='bold')
    axs[0].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

    df['Année'] = df['Année'].astype(str).str.split('.').str[0]

    risks_by_year = df.groupby('Année').size()

    # Plot the line chart
    axs[1].plot(risks_by_year.index, risks_by_year.values, marker='o', linestyle='-')
    axs[1].set_xlabel('Année')
    axs[1].set_ylabel('Nombre de Risques')
    axs[1].set_title('Evolution du Nombre des Risques par Année', fontsize=16, fontweight='bold')

    # Adjust layout
    plt.tight_layout()

    # Show the plot
    st.pyplot(fig)

def afficher_graphiques_incidents(df):
    # Ajoutez ici les graphiques pour les incidents
    st.write("Graphiques pour les Incidents")

def custom_sidebar():

    st.markdown(
        """
        <style>
            .stApp header {
                background-color:LightGray !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

def run_app():
    uploaded_file = None 
    year_filter = None
    Category_filter = None
    Direction_filter = None
    Impacted_filter = None

    install_dependencies()
    custom_sidebar()

    col1, col2 = st.columns([3, 4])

    with col1:
        option = st.selectbox("", ["Tableau de Bord Risques", "Tableau de Bord Incidents"])

    with col2:
        if option == "Tableau de Bord Risques":
            uploaded_file = st.file_uploader("", key="risques")

        elif option == "Tableau de Bord Incidents":
            uploaded_file = st.file_uploader("", key="incidents")

    if uploaded_file is not None:
        with st.sidebar:
            st.title("Filtres")
        years = sorted(set(pd.read_excel(uploaded_file)['Année']))
        years.insert(0, "Toutes")  # Insert "Toutes" option at the beginning
        year_filter = st.sidebar.selectbox("Filtrer par Année", years)
        
        if year_filter == "Toutes":
            year_filter = None  # Reset filter

        Category = sorted(set(pd.read_excel(uploaded_file)['Catégorie']))
        Category.insert(0, "Toutes")  # Insert "Toutes" option at the beginning
        Category_filter = st.sidebar.selectbox("Filtrer par Catégorie", Category)
        
        if Category_filter == "Toutes":
            Category_filter = None  # Reset filter

        Direction = sorted(set(pd.read_excel(uploaded_file)['Direction Responsable']))
        Direction.insert(0, "Toutes")  # Insert "Toutes" option at the beginning
        Direction_filter = st.sidebar.selectbox("Filtrer par Direction Responsable", Direction)
        
        if Direction_filter == "Toutes":
            Direction_filter = None  # Reset filter

        Direction_imp = sorted(set(pd.read_excel(uploaded_file)['Direction Responsable']))
        Direction_imp.insert(0, "Toutes")  # Insert "Toutes" option at the beginning
        Impacted_filter = st.sidebar.selectbox("Filtrer par Direction Impactée", Direction_imp)
        
        if Impacted_filter == "Toutes":
            Impacted_filter = None  # Reset filter

    if option:
        main(option, uploaded_file, year_filter,Category_filter,Direction_filter,Impacted_filter)
    
if __name__ == "__main__":
    run_app()
