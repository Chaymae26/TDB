import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import numpy as np
import plotly.graph_objects as go


st.set_page_config(page_title="Tableau de Bord", page_icon=":bar_chart:",layout="wide")
st.title(":bar_chart: Tableau de Bord")
st.markdown('<style>div.block-container{padding-top:3rem;}</style>', unsafe_allow_html=True)
st.subheader("Bienvenue! 👋 Veillez Choisir une Option pour Votre Tableau de Bord")

def main(option, uploaded_file, selected_year, selected_category, selected_direction, selected_impacted_dir, selected_Criticity, kri_total_risques, kri_hotels_risques, kri_siege_risques,kri_response_time,kri_criticity,kri_critic_risks):
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
        if selected_Criticity and selected_Criticity != 'Toutes':
            df = df[df['Etat Criticité'] == selected_Criticity]
        if option == "Tableau de Bord Risques":
            afficher_graphiques_risques(df)
        elif option == "Tableau de Bord Incidents":
            afficher_graphiques_incidents(df)

def afficher_graphiques_risques(df):

    risks_by_type = df['Typologie Risques'].value_counts()

    top_risks_by_type = risks_by_type.sort_values(ascending=False).head(10)

    fig, axs = plt.subplots(1, 2, figsize=(18, 8), gridspec_kw={'wspace': 0.2})

    bars = axs[0].barh(top_risks_by_type.index[::-1], top_risks_by_type.values[::-1], color='steelblue')

    for bar in bars:
        width = bar.get_width()
        axs[0].annotate('{:.0f}'.format(width),
                    xy=(width, bar.get_y() + bar.get_height() / 2),
                    xytext=(3, 0),
                    textcoords="offset points",
                    ha='left', va='center')

    axs[0].set_xlabel('Criticité Nette Actuelle')
    axs[0].set_title('Récurrence des Typologies des Risques', fontsize=16, fontweight='bold')

    plt.tight_layout()

    # Cartographie des Risques
    impact = df['Impact']
    probabilite = df['Probabilité']

    sc = axs[1].scatter(probabilite, impact, c=impact * probabilite, cmap='RdYlGn_r', s=1050, alpha=0.7, edgecolors="grey", linewidth=2)

    risk_counts = df.groupby(['Probabilité', 'Impact']).size().reset_index(name='count')

    for i in range(len(risk_counts)):
        axs[1].text(risk_counts['Probabilité'][i], risk_counts['Impact'][i], risk_counts['count'][i], ha='center', va='center')

    plt.colorbar(sc, ax=axs[1], label='Criticité')
    axs[1].set_xlabel('Probabilité')
    axs[1].set_ylabel('Impact')
    axs[1].set_title('Cartographie des Risques', fontsize=16, fontweight='bold')
    axs[1].grid(True)

    st.pyplot(fig)
    
    kri_counts = df['Etat Criticité'].value_counts()

    fig, axs = plt.subplots(1, 2, figsize=(20, 8), gridspec_kw={'wspace': 0.2})

    # Etat de la Criticité
    axs[0].pie(kri_counts, labels=kri_counts.index, autopct='%1.1f%%', startangle=90, colors=['#FFD700','#32CD32','#FF8C00','#DF0101'], wedgeprops=dict(width=0.5), textprops={'fontsize': 12})
    axs[0].set_title('Etat de la Criticité', fontsize=16, fontweight='bold')
    axs[0].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

    df['Année'] = df['Année'].astype(str).str.split('.').str[0]

    risks_by_year = df.groupby('Année').size()

    # Evolution du Nombre des Risques par Année
    axs[1].plot(risks_by_year.index, risks_by_year.values, marker='o', linestyle='-')
    axs[1].set_xlabel('Année')
    axs[1].set_ylabel('Nombre de Risques')
    axs[1].set_title('Evolution du Nombre des Risques par Année', fontsize=16, fontweight='bold')

    for i, txt in enumerate(risks_by_year.values):
            axs[1].annotate(txt, (risks_by_year.index[i], risks_by_year.values[i]), textcoords="offset points", xytext=(0,11), ha='center', fontsize = 12)

    plt.tight_layout()

    st.pyplot(fig)

    risks_per_direction = df.groupby('Direction Responsable')['Typologie Risques'].count().reset_index()
    criticity_per_direction = df.groupby('Direction Responsable')['Criticité Nette Actuelle'].mean().reset_index()
    risks_per_impacted_direction = df.groupby('Direction Impactée')['Typologie Risques'].count().reset_index()
    criticity_per_impacted_direction = df.groupby('Direction Impactée')['Criticité Nette Actuelle'].mean().reset_index()

    # Répartition du Nombre des Risques et Criticité par Direction Responsable
    st.markdown("<h5 style='text-align: center; font-weight: bold;'>Répartition du Nombre des Risques et Criticité par Direction Responsable</h5>", unsafe_allow_html=True)
    bar_chart1 = alt.Chart(risks_per_direction).mark_bar().encode(
        x=alt.X('Direction Responsable', axis=alt.Axis(labelAngle=65)),
        y='Typologie Risques',
        color=alt.value('blue')
    ).properties(
        width=600,
        height=400
    )

    line_chart1 = alt.Chart(criticity_per_direction).mark_line(color='red').encode(
        x=alt.X('Direction Responsable', axis=alt.Axis(labelAngle=65)),
        y='Criticité Nette Actuelle'
    ).properties(
        width=600,
        height=400
    )

    combined_chart1 = alt.layer(bar_chart1, line_chart1).resolve_scale(y='independent')
    st.altair_chart(combined_chart1, use_container_width=True)

    # Répartition du Nombre des Risques et Criticité par Direction Impactée
    st.markdown("<h5 style='text-align: center; font-weight: bold;'>Répartition du Nombre des Risques et Criticité par Direction Impactée<h5>", unsafe_allow_html=True)
    bar_chart2 = alt.Chart(risks_per_impacted_direction).mark_bar().encode(
        x=alt.X('Direction Impactée', axis=alt.Axis(labelAngle=65)),
        y='Typologie Risques',
        color=alt.value('green')
    ).properties(
        width=600,
        height=400
    )

    line_chart2 = alt.Chart(criticity_per_impacted_direction).mark_line(color='orange').encode(
        x=alt.X('Direction Impactée', axis=alt.Axis(labelAngle=65)),
        y='Criticité Nette Actuelle'
    ).properties(
        width=600,
        height=400
    )

    combined_chart2 = alt.layer(bar_chart2, line_chart2).resolve_scale(y='independent')
    st.altair_chart(combined_chart2, use_container_width=True)

    fig, axs = plt.subplots(1, 2, figsize=(20, 8), gridspec_kw={'wspace': 0.2})

    Risk_count = df['Etat Risque'].value_counts()
    Action_count = df["Etat Plan d'Actions"].value_counts()

    # Etat des Risques
    axs[0].pie(Risk_count, labels=Risk_count.index, autopct='%1.1f%%', startangle=90, colors=['#04B431','#FFBF00','#DF0101'], wedgeprops=dict(width=0.5), textprops={'fontsize': 12})
    axs[0].set_title('Etat des Risques', fontsize=20, fontweight='bold')
    axs[0].axis('equal')  

    # Etat Plan d'Actions
    axs[1].pie(Action_count, labels=Action_count.index, autopct='%1.1f%%', startangle=90, colors=['#04B431','#FFBF00','#DF0101','#3374FF'], wedgeprops=dict(width=0.5), textprops={'fontsize': 12})
    axs[1].set_title("Etat Plan d'Actions", fontsize=20, fontweight='bold')
    axs[1].axis('equal')

    plt.tight_layout()

    st.pyplot(fig)


    col1, col2 = st.columns([2, 2])

    with col1:

        st.markdown("<h5 style='text-align: center; font-weight: bold;'>Impact Financier par Année<h5>", unsafe_allow_html=True)

        df['Année'] = df['Année'].astype(str).str.split('.').str[0]

        impact_by_year = df.groupby('Année')['Impact Financier'].sum().reset_index()

        # Impact Financier par Année
        line_chart = alt.Chart(impact_by_year).mark_line(color='steelblue').encode(
            x=alt.X('Année', title='Année', axis=alt.Axis(labelAngle=0)),
            y=alt.Y('Impact Financier', title='Impact Financier'),
            tooltip=['Année', alt.Tooltip('Impact Financier', title='Impact Financier', format=',')]
        ).properties(
            width=400,
            height=300
        )

        st.altair_chart(line_chart, use_container_width=True)

    with col2:

        st.markdown("<h5 style='text-align: center; font-weight: bold;'>Impact Financier par Direction<h5>", unsafe_allow_html=True)
        
        bar_data = df.groupby('Direction Impactée')['Impact Financier'].sum().reset_index()
        top_5_impacted_directions = bar_data.sort_values(by='Impact Financier', ascending=False).head(5)

         # Impact Financier par Direction
        bar_chart = alt.Chart(top_5_impacted_directions).mark_bar(color='steelblue').encode(
            x=alt.X('Direction Impactée', title='Direction Impactée', sort='-y', axis=alt.Axis(labelAngle=65)),
            y=alt.Y('Impact Financier', title='Impact Financier'),
            tooltip=['Direction Impactée', alt.Tooltip('Impact Financier', title='Impact Financier', format=',')]
        ).properties(
            width=400,
            height=400
        )

        st.altair_chart(bar_chart, use_container_width=True)
    

def rating_meter(rating):
        st.markdown("<h5 style='text-align: center; font-weight: bold;'>Niveau de Criticité Global<h5>", unsafe_allow_html=True)
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=rating,
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={'axis': {'range': [None, 20]},
                'steps': [
                    {'range': [0, 5], 'color': "green"},
                    {'range': [5, 10], 'color': "gold"},
                    {'range': [10, 15], 'color': "orange"},
                    {'range': [15, 20], 'color': "Red"}],
                'bar': {'color': 'black', 'thickness' : 0.05},
                'threshold': {
                    'line': {'color': "black", 'width': 6},
                    'thickness': 1,
                    'value': rating}}))
                
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))

        fig.add_annotation(x=0.485, y=1, xref="paper", yref="paper",
                        text="Légende:",
                        font=dict(size=15, color="black"),
                        showarrow=False)
        fig.add_annotation(x=0.52, y=0.94, xref="paper", yref="paper",
                        text=" 0 - 5 : Faible       5 - 10 : Modérée",
                        font=dict(size=15, color="grey"),
                        showarrow=False)
        fig.add_annotation(x=0.52, y=0.89, xref="paper", yref="paper",
                        text="10 - 15 : Forte     15 - 20 : Critique",
                        font=dict(size=15, color="grey"),
                        showarrow=False)

        st.plotly_chart(fig, use_container_width=True)

def afficher_graphiques_incidents(df):

    col1, col2, col3 = st.columns([2, 0.5, 2])

    with col1:
        st.markdown("<h5 style='text-align: center; font-weight: bold;'>Récurrence des Typologies des Incidents<h5>", unsafe_allow_html=True)
        bar_data = df['Typologie Incidents'].value_counts().reset_index()
        bar_data.columns = ['Typologie Incidents', 'Réccurence']

        bar_chart = alt.Chart(bar_data).mark_bar(color='SandyBrown').encode(
            y=alt.Y('Typologie Incidents', title='Typologie Incidents', sort='-x'),
            x=alt.X('Réccurence', title='Réccurence'),
            tooltip=['Typologie Incidents', alt.Tooltip('Réccurence', title='Réccurence')]
        ).properties(
            width=700,
            height=400
        )

        st.altair_chart(bar_chart, use_container_width=True)

    with col2:
        st.write("")  # Empty placeholder for space

    with col3:
        overall_criticity = df['Criticité Nette Actuelle'].mean()
        rating_meter(overall_criticity)

    col1, col2 = st.columns([2, 2])

    with col1:
        st.markdown("<h5 style='text-align: center; font-weight: bold;'>Etat Incidents<h5>", unsafe_allow_html=True)

        fig, ax = plt.subplots(1, 1, figsize=(15, 11), gridspec_kw={'wspace': 0.2})

        Inc_count = df['Etat Incident'].value_counts()

        # Etat des Incidents
        ax.pie(Inc_count, labels=Inc_count.index, autopct='%1.1f%%', startangle=90, colors=['#04B431','#FFBF00','#DF0101'], wedgeprops=dict(width=0.55), textprops={'fontsize': 20})
        ax.axis('equal')  

        plt.tight_layout()

        st.pyplot(fig)


    with col2:
        st.markdown("<h5 style='text-align: center; font-weight: bold;'>Etat Plan d'actions<h5>", unsafe_allow_html=True)

        fig, ax = plt.subplots(1, 1, figsize=(25, 20), gridspec_kw={'wspace': 0.2})

        Action_plan = df["Etat Plan d'Actions"].value_counts()

        # Etat Plan d'actions
        ax.pie(Action_plan, labels=Action_plan.index, autopct='%1.1f%%', startangle=90, colors=['#04B431','#FFBF00','#DF0101','#3374FF'], wedgeprops=dict(width=0.55), textprops={'fontsize': 35})
        ax.axis('equal')  

        plt.tight_layout()

        st.pyplot(fig)

    Incidents_per_direction = df.groupby('Direction Responsable')['Typologie Incidents'].count().reset_index()
    criticity_per_direction = df.groupby('Direction Responsable')['Criticité Nette Actuelle'].mean().reset_index()
    Incidents_per_impacted_direction = df.groupby('Direction Impactée')['Typologie Incidents'].count().reset_index()
    criticity_per_impacted_direction = df.groupby('Direction Impactée')['Criticité Nette Actuelle'].mean().reset_index()

    # Répartition du Nombre des Incidents et Criticité par Direction Responsable
    st.markdown("<h5 style='text-align: center; font-weight: bold;'>Répartition du Nombre des Incidents et Criticité par Direction Responsable</h5>", unsafe_allow_html=True)
    bar_chart1 = alt.Chart(Incidents_per_direction).mark_bar().encode(
        x=alt.X('Direction Responsable', axis=alt.Axis(labelAngle=65)),
        y='Typologie Incidents',
        color=alt.value('DeepSkyBlue'),
        tooltip=[alt.Tooltip('Direction Responsable', title='Direction Responsable'), alt.Tooltip('Typologie Incidents', title='Nombre d\'incidents')]
    ).properties(
        width=600,
        height=400
    )

    line_chart1 = alt.Chart(criticity_per_direction).mark_line(color='red').encode(
        x=alt.X('Direction Responsable', axis=alt.Axis(labelAngle=65)),
        y='Criticité Nette Actuelle'
    ).properties(
        width=600,
        height=400
    )

    combined_chart1 = alt.layer(bar_chart1, line_chart1).resolve_scale(y='independent')
    st.altair_chart(combined_chart1, use_container_width=True)

    # Répartition du Nombre des Incidents et Criticité par Direction Impactée
    st.markdown("<h5 style='text-align: center; font-weight: bold;'>Répartition du Nombre des Incidents et Criticité par Direction Impactée<h5>", unsafe_allow_html=True)
    bar_chart2 = alt.Chart(Incidents_per_impacted_direction).mark_bar().encode(
        x=alt.X('Direction Impactée', axis=alt.Axis(labelAngle=65)),
        y='Typologie Incidents',
        color=alt.value('MediumSeaGreen'),
        tooltip=[alt.Tooltip('Direction Impactée', title='Direction Impactée'), alt.Tooltip('Typologie Incidents', title="Nombre d'incidents")]
    ).properties(
        width=600,
        height=400
    )

    line_chart2 = alt.Chart(criticity_per_impacted_direction).mark_line(color='orange').encode(
        x=alt.X('Direction Impactée', axis=alt.Axis(labelAngle=65)),
        y='Criticité Nette Actuelle'
    ).properties(
        width=600,
        height=400
    )

    combined_chart2 = alt.layer(bar_chart2, line_chart2).resolve_scale(y='independent')
    st.altair_chart(combined_chart2, use_container_width=True)

    col1, col2 = st.columns([2, 2])

    with col1:

        st.markdown("<h5 style='text-align: center; font-weight: bold;'>Etat de la Criticité<h5>", unsafe_allow_html=True)

        kri_counts = df['Etat Criticité'].value_counts()

        fig, ax = plt.subplots(1, 1, figsize=(25, 16), gridspec_kw={'wspace': 0.2})

        # Etat de la Criticité
        ax.pie(kri_counts, labels=kri_counts.index, autopct='%1.1f%%', startangle=90, colors=['#FFD700','#32CD32','#FF8C00','#DF0101'], wedgeprops=dict(width=0.6), textprops={'fontsize': 35})
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

        plt.tight_layout()

        st.pyplot(fig)

    with col2:

        st.markdown("<h5 style='text-align: center; font-weight: bold;'>Evolution du Nombre d'incidents par Année<h5>", unsafe_allow_html=True)

        fig, ax = plt.subplots(1, 1, figsize=(20, 15), gridspec_kw={'wspace': 0.2})

        df['Année'] = df['Année'].astype(str).str.split('.').str[0]

        inc_by_year = df.groupby('Année').size()

        # Evolution du Nombre des incidents par Année
        ax.plot(inc_by_year.index, inc_by_year.values, marker='o', linestyle='-', linewidth=2.5)
        ax.set_xlabel('Année', fontsize = 30)
        ax.set_ylabel("Nombre d'incidents", fontsize = 30)
        ax.tick_params(axis='both', which='major', labelsize=25)

        for i, txt in enumerate(inc_by_year.values):
            ax.annotate(txt, (inc_by_year.index[i], inc_by_year.values[i]), textcoords="offset points", xytext=(0,17), ha='center', fontsize = 25)

        plt.tight_layout()

        st.pyplot(fig)

    col1, col2 = st.columns([2, 2])

    with col1:

        st.markdown("<h5 style='text-align: center; font-weight: bold;'>Impact Financier par Année<h5>", unsafe_allow_html=True)

        df['Année'] = df['Année'].astype(str).str.split('.').str[0]

        impact_by_year = df.groupby('Année')['Impact Financier'].sum().reset_index()

        # Impact Financier par Année
        line_chart = alt.Chart(impact_by_year).mark_line(color='steelblue').encode(
            x=alt.X('Année', title='Année', axis=alt.Axis(labelAngle=0)),
            y=alt.Y('Impact Financier', title='Impact Financier'),
            tooltip=['Année', alt.Tooltip('Impact Financier', title='Impact Financier', format=',')]
        ).properties(
            width=400,
            height=300
        )

        st.altair_chart(line_chart, use_container_width=True)

    with col2:

        st.markdown("<h5 style='text-align: center; font-weight: bold;'>Impact Financier par Direction<h5>", unsafe_allow_html=True)
        
        bar_data = df.groupby('Direction Impactée')['Impact Financier'].sum().reset_index()
        top_5_impacted_directions = bar_data.sort_values(by='Impact Financier', ascending=False).head(5)

         # Impact Financier par Direction
        bar_chart = alt.Chart(top_5_impacted_directions).mark_bar(color='tomato').encode(
            x=alt.X('Direction Impactée', title='Direction Impactée', sort='-y', axis=alt.Axis(labelAngle=65)),
            y=alt.Y('Impact Financier', title='Impact Financier'),
            tooltip=['Direction Impactée', alt.Tooltip('Impact Financier', title='Impact Financier', format=',')]
        ).properties(
            width=400,
            height=400
        )

        st.altair_chart(bar_chart, use_container_width=True)


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
    Criticity_filter = None
    kri_total_risques = None
    kri_hotels_risques = None
    kri_siege_risques = None
    kri_response_time = None
    kri_critic_risks = None
    kri_criticity = None
    

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

        if option == "Tableau de Bord Risques":

            df = pd.read_excel(uploaded_file)

            kri_total_risques = df['Typologie Risques'].count()
            kri_hotels_risques = df[df['Catégorie'] == 'Hôtel']['Typologie Risques'].count()
            kri_siege_risques = df[df['Catégorie'] == 'Siège']['Typologie Risques'].count()
            kri_response_time = round(df['Temps de Résolution en Semaines'].mean(), 2)
            kri_criticity = round(df['Criticité Nette Actuelle'].mean(),2)
            kri_critic_risks = df[df['Etat Criticité'] == 'Critique'].shape[0]

            st.markdown("## 💡 Key Risk Indicators")
            col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1.75])
            col1.metric("Total Risques", kri_total_risques)
            col2.metric("Risques Hôtel", kri_hotels_risques)
            col3.metric("Risques Siège", kri_siege_risques)
            col4.metric("Criticité Moyenne", kri_criticity)
            col5.metric("Risque Critiques", kri_critic_risks)
            col6.metric("Temps de Résolution Moyen (Semaines)", kri_response_time)

            st.write("---")  # Add a horizontal line
            st.write("")  # Add an empty line


            with st.sidebar:
                st.title("Filtres")
            years = sorted(set(pd.read_excel(uploaded_file)['Année']))
            years.insert(0, "Toutes")  
            year_filter = st.sidebar.selectbox("Filtrer par Année", years)
            
            if year_filter == "Toutes":
                year_filter = None 

            Category = sorted(set(map(str, pd.read_excel(uploaded_file)['Catégorie'])))
            Category.insert(0, "Toutes")
            Category_filter = st.sidebar.selectbox("Filtrer par Catégorie", Category)
            
            if Category_filter == "Toutes":
                Category_filter = None 

            Direction = sorted(set(pd.read_excel(uploaded_file)['Direction Responsable']))
            Direction.insert(0, "Toutes")  
            Direction_filter = st.sidebar.selectbox("Filtrer par Direction Responsable", Direction)
            
            if Direction_filter == "Toutes":
                Direction_filter = None  

            Direction_imp = sorted(set(pd.read_excel(uploaded_file)['Direction Responsable']))
            Direction_imp.insert(0, "Toutes") 
            Impacted_filter = st.sidebar.selectbox("Filtrer par Direction Impactée", Direction_imp)
            
            if Impacted_filter == "Toutes":
                Impacted_filter = None 
            
            Criticity = sorted(set(pd.read_excel(uploaded_file)['Etat Criticité']))
            Criticity.insert(0, "Toutes") 
            Criticity_filter = st.sidebar.selectbox("Filtrer par Etat Criticité", Criticity)
            
            if Criticity_filter == "Toutes":
                Criticity_filter = None 

        if option == "Tableau de Bord Incidents":

            df = pd.read_excel(uploaded_file)

            kri_total_risques = df['Typologie Incidents'].count()
            kri_hotels_risques = df[df['Catégorie'] == 'Hôtel']['Typologie Incidents'].count()
            kri_siege_risques = df[df['Catégorie'] == 'Siège']['Typologie Incidents'].count()
            kri_response_time = round(df['Temps de Résolution en Semaines'].mean(), 2)
            kri_criticity = round(df['Criticité Nette Actuelle'].mean(),2)
            kri_critic_risks = df[df['Etat Criticité'] == 'Critique'].shape[0]

            st.markdown("## 💡 Key Risk Indicators")
            col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1.75])
            col1.metric("Total Incidents", kri_total_risques)
            col2.metric("Incidents Hôtel", kri_hotels_risques)
            col3.metric("Incidents Siège", kri_siege_risques)
            col4.metric("Criticité Moyenne", kri_criticity)
            col5.metric("Incidents Critiques", kri_critic_risks)
            col6.metric("Temps de Résolution Moyen (Semaines)", kri_response_time)

            st.write("---")  # Add a horizontal line
            st.write("")  # Add an empty line


            with st.sidebar:
                st.title("Filtres")
            years = sorted(set(pd.read_excel(uploaded_file)['Année']))
            years.insert(0, "Toutes")  
            year_filter = st.sidebar.selectbox("Filtrer par Année", years)
            
            if year_filter == "Toutes":
                year_filter = None 

            Category = sorted(set(map(str, pd.read_excel(uploaded_file)['Catégorie'])))
            Category.insert(0, "Toutes")
            Category_filter = st.sidebar.selectbox("Filtrer par Catégorie", Category)
            
            if Category_filter == "Toutes":
                Category_filter = None 

            Direction = sorted(set(pd.read_excel(uploaded_file)['Direction Responsable']))
            Direction.insert(0, "Toutes")  
            Direction_filter = st.sidebar.selectbox("Filtrer par Direction Responsable", Direction)
            
            if Direction_filter == "Toutes":
                Direction_filter = None  

            Direction_imp = sorted(set(pd.read_excel(uploaded_file)['Direction Responsable']))
            Direction_imp.insert(0, "Toutes") 
            Impacted_filter = st.sidebar.selectbox("Filtrer par Direction Impactée", Direction_imp)
            
            if Impacted_filter == "Toutes":
                Impacted_filter = None 
            
            Criticity = sorted(set(pd.read_excel(uploaded_file)['Etat Criticité']))
            Criticity.insert(0, "Toutes") 
            Criticity_filter = st.sidebar.selectbox("Filtrer par Etat Criticité", Criticity)
            
            if Criticity_filter == "Toutes":
                Criticity_filter = None 

    if option:
        main(option, uploaded_file, year_filter,Category_filter,Direction_filter,Impacted_filter,Criticity_filter,kri_total_risques, kri_hotels_risques, kri_siege_risques,kri_response_time,kri_criticity,kri_critic_risks)

    
    
if __name__ == "__main__":
    run_app()
