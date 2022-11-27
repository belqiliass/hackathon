import streamlit as st
import math
import pandas as pd

with st.sidebar:
    st.title('PIF2S')
    mode = st.radio("choose mode:", ["single input", "whole dataset"], 0)

def get_num_detectors(surface, coef_K, hauteur, detector_type="fumée"):
    if detector_type == "fumée":
        if surface <= 80:
            D = 6.7
            Amax = 80
            
        else : 
            D = 5.8
            Amax = 60

    if detector_type == "thérmovélocimétrique":
        if surface <= 40:
            D = 5.7
            Amax = 40
            
        else : 
            D = 4.4
            Amax = 30

    if detector_type == "thérmovélocimétrique":
        if surface <= 40:
            D = 4.6
            Amax = 24
            
        else : 
            D = 3.6
            Amax = 18

    Am_m2 = Amax*coef_K

    ratio_L_2D = math.ceil(hauteur/(2*D))
    ratio_S_An = math.ceil(surface/Am_m2)

    num_detectors = max(ratio_L_2D, ratio_S_An)

    return num_detectors

if mode == "single input":
    surface = st.number_input("Please input the local's area", value=1)
    hauteur = st.number_input("Please input the local's height", value=1)
    detector_type = st.text_input("Please input the detector's type", value="fumée").lower()
    coef_K = st.number_input("Please input the local's coef_K", value=1)
    
    num_detectors = get_num_detectors(surface, coef_K, hauteur, detector_type)
    st.markdown("number of detectors is "+str(num_detectors))


if mode == "whole dataset":
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, sep=";")

        list_surface = df["surface en (m²)"].apply(lambda x: x.replace(",", ".")).astype(float).tolist()
        list_hauteur = df["L Local en (m)"].apply(lambda x: x.replace(",", ".")).astype(float).tolist()
        list_coef_K = df["Coef K de Local"].apply(lambda x: x.replace(",", ".")).astype(float).tolist()

        print(list_surface)
        print(list_hauteur)
        print(list_coef_K)

        list_um_detectors = []

        for surface, hauteur, coef_K in zip(list_surface, list_hauteur, list_coef_K):
            list_um_detectors.append(get_num_detectors(surface, coef_K, hauteur))

        res_df = pd.DataFrame({"surface en (m²)" : list_surface, "L Local en (m)" : list_hauteur, "Coef K de Local": coef_K, "nbre de detecteurs à prévoir" : list_um_detectors})

        st.dataframe(res_df)    


        