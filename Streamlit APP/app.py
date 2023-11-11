import streamlit as st
import numpy as np
import pickle
import requests

# Model yükleniyor
filename = 'Notebooks/titanic_model.sav'
model = pickle.load(open(filename, 'rb'))


# Eğitim verisinde kullanılan mapping'ler
title_mapping = {"Bay": 1, "Hanım": 2, "Bayan": 3, "Usta": 4, "Doktor": 5, "Özgü": 6}
embarked_mapping = {"Southampton, İngiltere": 1, "Cherbourg, Fransa": 2, "Queesntown, İrlanda": 3}
sex_mapping = {"Erkek": 0, "Kadın": 1}
ports_range = ('Southampton, İngiltere', 'Cherbourg, Fransa', 'Queesntown, İrlanda')

st.title('Titanik Hayatta Kalma Tahmin Uygulaması')

# Kullanıcı girişleri
pclass = st.selectbox('Sınıfınız (1=Business, 2=Ekonomi, 3=Alt Sınıf)', [1, 2, 3])
sex = st.selectbox('Cinsiyetiniz', ['Erkek', 'Kadın'])
title = st.selectbox('Ünvanınız', ['Bay', 'Hanım', 'Bayan', 'Usta', 'Doktor', 'Özgü'])
age = st.slider('Yaşınız', 0, 90, 28)
sibsp = st.slider('Titanikteki kardeş/eş sayınız', 0, 8, 0)
parch = st.slider('Titanikteki ebeveyn/çocuk sayınız', 0, 6, 0)
embarked = st.selectbox('Gemiye hangi limandan bindiniz?', ports_range)

# Tahmin
response = requests.post("http://fastapi:8000/predict", json={
        "pclass": pclass,
        "sex": sex,
        "title": title,
        "age": age,
        "sibsp": sibsp,
        "parch": parch,
        "embarked": embarked
 })

res = response.json()
if res['survive'] == 'Survived':
    st.success(f"%{round(res['proba'], 2)} ihtimalle hayatta kalırdınız.")
else:
    st.error(f"%{round((100 - res['proba']), 2)} ihtimalle hayatta kalmazdınız.")
