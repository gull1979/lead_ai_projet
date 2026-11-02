import streamlit as st
import requests

# Configuration de la page Streamlit pour un affichage large et professionnel
st.set_page_config(layout="wide", page_title="AgriTech Yield Predictor")

col_gauche, col_droite = st.columns([1, 2], gap="large")
with col_gauche:
    st.title("🌱 Assistant de Prédiction de Rendement Agricole")
    st.write("Ajustez les paramètres contextuels et les additifs pour estimer le rendement de la culture.")

with col_droite:
    # Intégration de la vidéo officielle de la FAO
    video_url = "https://jedha-projet.s3.eu-west-3.amazonaws.com/cover-fao-4b.mp4"
    st.components.v1.html(
            f'<video width="100%" autoplay loop muted playsinline style="border-radius: 8px;"><source src="{video_url}" type="video/mp4"></video>',
        )

# 1. Dictionnaires de correspondance pour afficher en français et envoyer en anglais à l'API
areas_dict = {
    'Albanie': 'Albania', 'Autriche': 'Austria', 'Bosnie-Herzégovine': 'Bosnia-Herzegovinia', 
    'Bulgarie': 'Bulgaria', 'Croatie': 'Croatia', 'République Tchèque': 'Czech_Republic', 
    'Danemark': 'Denmark', 'Finlande': 'Finland', 'France': 'France', 'Allemagne': 'Germany', 
    'Grèce': 'Greece', 'Hongrie': 'Hungary', 'Islande': 'Iceland', 'Irlande': 'Ireland', 
    'Italie': 'Italy', 'Lettonie': 'Latvia', 'Lituanie': 'Lithuania', 'Malte': 'Malta', 
    'Pays-Bas': 'Netherlands', 'Pologne': 'Poland', 'Portugal': 'Portugal', 'Roumanie': 'Romania', 
    'Slovaquie': 'Slovakia', 'Slovénie': 'Slovenia', 'Suède': 'Sweden', 'Suisse': 'Switzerland', 
    'Ukraine': 'Ukraine', 'Royaume-Uni': 'United_Kingdom', 'Moldavie': 'Moldova', 
    'Belgique': 'Belgium', 'Îles Féroé': 'Faeroes', 'Luxembourg': 'Luxembourg', 
    'Monténégro': 'Montenegro', 'Serbie': 'Serbia'
}

items_dict = {
    'Pommes': 'Apples', 'Abricots': 'Apricots', 'Orge': 'Barley', 'Haricots secs': 'Beans, dry', 
    'Fèves et féveroles sèches': 'Broad beans and horse beans, dry', 
    'Fèves et féveroles fraîches': 'Broad beans and horse beans, green', 'Choux': 'Cabbages', 
    'Carottes et navets': 'Carrots and turnips', 'Choux-fleurs et brocolis': 'Cauliflowers and broccoli', 
    'Cerises': 'Cherries', 'Châtaignes (en coque)': 'Chestnuts, in shell', 
    'Piments et poivrons verts': 'Chillies and peppers, green (Capsicum spp. and Pimenta spp.)', 
    'Concombres et cornichons': 'Cucumbers and gherkins', 'Aubergines': 'Eggplants (aubergines)', 
    'Raisins': 'Grapes', 'Ail vert (frais)': 'Green garlic', 'Houblon (cônes)': 'Hop cones', 
    'Maïs': 'Maize (corn)', 'Avoine': 'Oats', 
    'Oignons et échalotes (secs)': 'Onions and shallots, dry (excluding dehydrated)', 
    'Pêches et nectarines': 'Peaches and nectarines', 'Poires': 'Pears', 'Prunes et prunelles': 'Plums and sloes', 
    'Pommes de terre': 'Potatoes', 'Courges, potirons et potimarrons': 'Pumpkins, squash and gourds', 
    'Seigle': 'Rye', 'Griottes (cerises acides)': 'Sour cherries', 'Soja': 'Soya beans', 
    'Épinards': 'Spinach', 'Graines de tournesol': 'Sunflower seed', 'Tomates': 'Tomatoes', 
    'Tabac brut': 'Unmanufactured tobacco', 'Vesces': 'Vetches', 'Pastèques': 'Watermelons', 
    'Blé': 'Wheat', 'Cultures à fibres (équivalent fibre)': 'Fibre Crops, Fibre Equivalent', 
    'Oléagineux (équivalent tourteaux)': 'Oilcrops, Cake Equivalent', 
    'Oléagineux (équivalent huile)': 'Oilcrops, Oil Equivalent', 'Asperges': 'Asparagus', 
    'Autres céréales (non classées)': 'Cereals n.e.c.', 'Groseilles / Cassis': 'Currants', 
    'Lin textile (brut ou roui)': 'Flax, raw or retted', 'Groseilles à maquereau': 'Gooseberries', 
    'Millet': 'Millet', 'Céréales mélangées (Méteil)': 'Mixed grain', 'Pois secs': 'Peas, dry', 
    'Pois frais': 'Peas, green', 'Graines de colza': 'Rape or colza seed', 'Fraises': 'Strawberries', 
    'Triticale': 'Triticale', 'Noix (en coque)': 'Walnuts, in shell', 'Amandes (en coque)': 'Almonds, in shell', 
    'Framboises': 'Raspberries', 'Laitues et chicorées': 'Lettuce and chicory', 'Graines de lin': 'Linseed', 
    'Coings': 'Quinces', 'Sorgho': 'Sorghum', 'Noisettes (en coque)': 'Hazelnuts, in shell', 
    'Myrtilles': 'Blueberries', 'Lupins': 'Lupins'
}

areas_fr = list(areas_dict.keys())
items_fr = list(items_dict.keys())

# 2. Implantation du Layout en 2 colonnes principales (Gauche : Contexte, Droite : Intrants)
col_gauche2 , col_droite2  = st.columns([1, 2], gap="large")

with col_gauche2 :
    st.subheader("📋 Contexte Agricole")
    Area_fr_selected = st.selectbox(
        "Zone géographique (Area)", 
        options=areas_fr, 
        index=areas_fr.index("France") if "France" in areas_fr else 0
    )
    Item_fr_selected = st.selectbox(
        "Type de culture (Item)", 
        options=items_fr, 
        index=items_fr.index("Blé") if "Blé" in items_fr else 0
    )
    
    st.write("---")
    submit = st.button("🚀 Calculer la prédiction", use_container_width=True)

with col_droite2 :
    st.subheader("📊 Gestion des Additifs")
    
    tab1, tab2 = st.tabs(["💧 Fertilisation (Nutriments) en tonne(s)", "🛡️ Protection des cultures (Pesticides) en tonne(s)"])
    
    with tab1:
        st.info("Ajustement des macro-éléments du sol (Valeurs initiales basées sur la moyenne globale)")
        
        st.write("**Azote total (N)**")
        sub_col1, sub_col2 = st.columns([3, 1])
        with sub_col1:
            n_slider = st.slider("N_slider", min_value=6, max_value=2402000, value=386157, step=1000, label_visibility="collapsed")
        with sub_col2:
            Nutrient_nitrogen = st.number_input("N_input", min_value=6, max_value=2402000, value=n_slider, step=1000, label_visibility="collapsed")
        
        st.write("**Phosphate total (P2O5)**")
        sub_col3, sub_col4 = st.columns([3, 1])
        with sub_col3:
            p_slider = st.slider("P_slider", min_value=3, max_value=795000, value=95099, step=500, label_visibility="collapsed")
        with sub_col4:
            Nutrient_phosphate = st.number_input("P_input", min_value=3, max_value=795000, value=p_slider, step=500, label_visibility="collapsed")
        
        st.write("**Potasse totale (K2O)**")
        sub_col5, sub_col6 = st.columns([3, 1])
        with sub_col5:
            k_slider = st.slider("K_slider", min_value=0, max_value=1033500, value=102760, step=500, label_visibility="collapsed")
        with sub_col6:
            Nutrient_potash = st.number_input("K_input", min_value=0, max_value=1033500, value=k_slider, step=500, label_visibility="collapsed")
        
    with tab2:
        st.info("Ajustement des traitements chimiques (Valeurs initiales basées sur la moyenne globale)")
        
        st.write("**Fongicides et Bactéricides**")
        sub_col7, sub_col8 = st.columns([3, 1])
        with sub_col7:
            f_slider = st.slider("F_slider", min_value=0, max_value=63175, value=5354, step=50, label_visibility="collapsed")
        with sub_col8:
            Fungicides = st.number_input("F_input", min_value=0, max_value=63175, value=f_slider, step=50, label_visibility="collapsed")
        
        st.write("**Herbicides**")
        sub_col9, sub_col10 = st.columns([3, 1])
        with sub_col9:
            h_slider = st.slider("H_slider", min_value=0, max_value=62187, value=5188, step=50, label_visibility="collapsed")
        with sub_col10:
            Herbicides = st.number_input("H_input", min_value=0, max_value=62187, value=h_slider, step=50, label_visibility="collapsed")
        
        st.write("**Insecticides**")
        sub_col11, sub_col12 = st.columns([3, 1])
        with sub_col11:
            i_slider = st.slider("I_slider", min_value=0, max_value=21348, value=1600, step=10, label_visibility="collapsed")
        with sub_col12:
            Insecticides = st.number_input("I_input", min_value=0, max_value=21348, value=i_slider, step=10, label_visibility="collapsed")
        
        st.write("**Rodenticides (Raticides)**")
        sub_col13, sub_col14 = st.columns([3, 1])
        with sub_col13:
            r_slider = st.slider("R_slider", min_value=0, max_value=1755, value=30, step=1, label_visibility="collapsed")
        with sub_col14:
            Rodenticides = st.number_input("R_input", min_value=0, max_value=1755, value=r_slider, step=1, label_visibility="collapsed")
        
        st.write("**Total des Pesticides**")
        sub_col15, sub_col16 = st.columns([3, 1])
        with sub_col15:
            t_slider = st.slider("T_slider", min_value=1, max_value=99694, value=13284, step=100, label_visibility="collapsed")
        with sub_col16:
            Pesticides_total = st.number_input("T_input", min_value=1, max_value=99694, value=t_slider, step=100, label_visibility="collapsed")

# 3. Logique de traitement et de communication avec l'API lors du clic
if submit:
    Area_en = areas_dict[Area_fr_selected]
    Item_en = items_dict[Item_fr_selected]
    
    payload = {
        "Area": Area_en,
        "Item": Item_en,
        "Nutrient_nitrogen_N_total": float(Nutrient_nitrogen),
        "Nutrient_phosphate_P2O5_total": float(Nutrient_phosphate),
        "Nutrient_potash_K2O_total": float(Nutrient_potash),
        "Fungicides_and_Bactericides": float(Fungicides),
        "Herbicides": float(Herbicides),
        "Insecticides": float(Insecticides),
        "Pesticides_total": float(Pesticides_total),
        "Rodenticides": float(Rodenticides)
    }
    
    with st.spinner("Calcul de la prédiction par l'API en cours..."):
        try:
            response = requests.post("http://localhost:8000/predict", json=payload)
            
            if response.status_code == 200:
                result = response.json()
                st.success(f"### 🎯 Rendement estimé : **{result['prediction']:.2f}** kg/ha")
            else:
                st.error(f"❌ Erreur renvoyée par l'API (Code {response.status_code}) : {response.text}")
                
        except requests.exceptions.ConnectionError:
            st.error("⚠️ Impossible de joindre l'API FastAPI. Assurez-vous qu'elle s'exécute correctement en arrière-plan (port 8000).")