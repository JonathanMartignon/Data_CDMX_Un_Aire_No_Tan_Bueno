import streamlit as st
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pydeck as pdk


@st.cache(suppress_st_warning=True)
def leer_datos():
    #Calidad del aire
    calidad_aire = pd.read_csv('https://github.com/JonathanMartignon/Data_CDMX_Un_Aire_No_Tan_Bueno/blob/main/Datos/prueba_datos_calidad_aire.csv?raw=True')

    #Indices de contaminacion
    indice_2020 = pd.read_csv('https://github.com/JonathanMartignon/Data_CDMX_Un_Aire_No_Tan_Bueno/blob/main/Datos/imeca_2020.csv?raw=True')

    #Areas Verdes
    areas_verdes = pd.read_csv('https://github.com/JonathanMartignon/Data_CDMX_Un_Aire_No_Tan_Bueno/blob/main/Datos/cdmx_areas_verdes_2017.csv?raw=True')
    
    #Escuelas_publicas
    escuelas_publicas = pd.read_csv('https://github.com/JonathanMartignon/Data_CDMX_Un_Aire_No_Tan_Bueno/blob/main/Datos/Escuelas/escuelas-publicas.csv?raw=true')

    #Escuelas privadas
    escuelas_privadas = pd.read_csv('https://github.com/JonathanMartignon/Data_CDMX_Un_Aire_No_Tan_Bueno/blob/main/Datos/Escuelas/escuelas-privadas.csv?raw=true')

    #Tiraderos clandestinos
    tiraderos_clandestinos = pd.read_csv('https://github.com/JonathanMartignon/Data_CDMX_Un_Aire_No_Tan_Bueno/blob/main/Datos/tiraderos-clandestinos-al-cierre-de-2017.csv?raw=True')
    
    nivel_plomo = pd.read_csv('https://github.com/JonathanMartignon/Data_CDMX_Un_Aire_No_Tan_Bueno/blob/main/Datos/red_manual_plomo.csv?raw=True',skiprows=8)
    
    ciclistas = pd.read_csv('https://github.com/JonathanMartignon/Data_CDMX_Un_Aire_No_Tan_Bueno/blob/main/Datos/contador-ciclistas.csv?raw=True')
    
    mercados = pd.read_csv('https://github.com/JonathanMartignon/Data_CDMX_Un_Aire_No_Tan_Bueno/blob/main/Datos/mercados-publicos.csv?raw=True')
    
    return calidad_aire, indice_2020, areas_verdes, escuelas_publicas, escuelas_privadas, tiraderos_clandestinos, nivel_plomo, ciclistas, mercados
    

calidad_aire, indice_2020, areas_verdes, escuelas_publicas, escuelas_privadas, tiraderos_clandestinos, nivel_plomo, ciclistas, mercados = leer_datos()


# Mapa areas verdes

latitud = []
longitud = []

for i in range(len(areas_verdes)):
    if type(areas_verdes['Geo Point'][i]) != float:
        lat, lon = areas_verdes['Geo Point'][i].split(',')
        latitud.append(np.float(lat))
        longitud.append(np.float64(lon))
        
        
areas_ubicacion = pd.DataFrame(latitud, columns=['lat'])
areas_ubicacion['lon'] = longitud


# Mapa mercados

latitud_merc = []
longitud_merc = []

for i in range(len(mercados)):
    if type(mercados['coord'][i]) != float:
        lat, lon = mercados['coord'][i].split(',')
        latitud_merc.append(np.float(lat))
        longitud_merc.append(np.float64(lon))
        
        
mercados_ubicacion = pd.DataFrame(latitud_merc, columns=['lat'])
mercados_ubicacion['lon'] = longitud_merc

# Escuelas publicas delegacion

delegacion = []
for i in range(len(escuelas_publicas)):
    if type(escuelas_publicas['Domicilio'][i]) != float:
        deleg = escuelas_publicas['Domicilio'][i].split("DELEGACION")
        if len(deleg) > 1:
            delegacion.append(deleg[1].split(',')[0])
        else:
            delegacion.append('NO DISPONIBLE')      
    else:
        delegacion.append('NO DISPONIBLE')
        
delegacion = pd.DataFrame(delegacion)
delegacion.columns = ['delegacion']

escuelas_publicas_alcaldia = sns.factorplot("delegacion", data=delegacion, 
                                aspect=2, kind="count", palette="GnBu", 
                                margin_titles=True,  order = delegacion['delegacion'].value_counts().index)
escuelas_publicas_alcaldia.set_xticklabels(rotation=70)



escuelas_privadas_alcaldia = sns.factorplot("ALCALDÍA", data=escuelas_privadas, 
                                         aspect=2, kind="count", palette="GnBu", 
                                         margin_titles=True,  order = escuelas_privadas['ALCALDÍA'].value_counts().index)
escuelas_privadas_alcaldia.set_xticklabels(rotation=70)


#Tiraderos Clandestinos

tiraderos_alcaldias = sns.factorplot("alcaldia", data=tiraderos_clandestinos, 
                                         aspect=2, kind="count", palette="GnBu", 
                                         margin_titles=True, order = tiraderos_clandestinos['alcaldia'].value_counts().index)
tiraderos_alcaldias.set_xticklabels(rotation=70)



# Calculo IMECA

def IMECA(ozono, Co, Pm10, So2, No2):
    imecao3 = (ozono * 100) / 0.11
    imecaco = (Co * 100) / 11
    if Pm10 <= 120:
        imecapm10 = Pm10 * 0.833
    elif Pm10 >= 121 and Pm10 <= 320:
        imecapm10 = (Pm10 * 0.5) + 40
    elif Pm10 > 320:
        imecapm10 = Pm10 * 0.625
    imecaso2 = (So2 * 100 ) / 0.13
    imecano2 = (No2 * 100 ) / 0.21
    indice = [int(imecao3), int(imecaco), int(imecapm10), int(imecaso2), int(imecano2)]
    return indice



# Front
st.title("CDMX Un aire no tan bueno")
st.subheader('Ortega Ibarra Jaime Jesus')
st.subheader('Martiñón Luna Jonathan José')

st.write('De acuerdo con diversas fuentes como: El Financiero, Excelsior y Forbes, la Ciudad de México (CDMX) se encuentra como la quinta Urbe más contaminada a nivel mundial. Esto gracias al contador en tiempo real de Greenpeace, que permite rastrear por ciudad el costo de la contaminación del aire durante la pandemia de Covid-19.')

st.write('La Ciudad de México ocupa el quinto lugar de 28 urbes en registrar 11,000 muertes vinculadas a contaminación del aire en la primera mitad del 2020, lo que equivale a un costo de 5.5 mil millones de dólares, de acuerdo a dicho contador.')

cdmx = Image.open('trafic_cdmx.jpg')
st.image(cdmx, caption='Afluencia Vehícular. Credit: Adriana Zehbrauskas para The New York Times',use_column_width=True)

st.markdown('**Menú**')
menu = st.selectbox('Selecciona una opción',('Datos', 'Calculadora IMECA', 'Delegaciones más contaminadas', 'Resultados'))

if menu == 'Datos':
    option = st.selectbox('Selecciona una opción para ver los datos',('Calidad del Aire', 'Indices de Contaminación', 'Niveles de Plomo en el aire',
                          'Tiraderos Clandestinos en CDMX', 'Areas verdes en CDMX', 'Escuelas en CDMX', 
                          'Mercados Públicos en CDMX', 'Afluencia de Ciclistas'))
    if option == 'Areas verdes en CDMX':
        st.dataframe(areas_verdes)
        if st.checkbox('Ver mapa'):
            midpoint = (np.average(areas_ubicacion['lat']), np.average(areas_ubicacion['lon']))
            st.pydeck_chart(pdk.Deck(
     map_style='cali-terrain',
     initial_view_state=pdk.ViewState(
         latitude=midpoint[0],
         longitude=midpoint[1],
         zoom=11,
         pitch=10,
     ),
     layers=[
         pdk.Layer(
             'ScatterplotLayer',
             data=areas_ubicacion,
             get_position='[lon, lat]',
             get_color='[10, 100, 10, 140]',
             get_radius=200,
         ),
     ],
 ))
    elif option == 'Calidad del Aire':
        st.dataframe(calidad_aire)
    elif option == 'Indices de Contaminación':
        st.dataframe(indice_2020)
    elif option == 'Tiraderos Clandestinos en CDMX':
        st.dataframe(tiraderos_clandestinos)
        st.markdown('Tiraderos clandestinos por Alcaldía')
        st.pyplot(tiraderos_alcaldias)    
    elif option == 'Escuelas en CDMX':
        st.dataframe(escuelas_publicas)
        st.markdown('Escuelas Públicas por Alcaldía')
        st.pyplot(escuelas_publicas_alcaldia)
        st.dataframe(escuelas_privadas)
        st.markdown('Escuelas Privadas por Alcaldía')
        st.pyplot(escuelas_privadas_alcaldia)
    elif option == 'Niveles de Plomo en el aire':
        st.dataframe(nivel_plomo)
    elif option == 'Afluencia de Ciclistas':
        st.dataframe(ciclistas)
    elif option == 'Mercados Públicos en CDMX':
        st.dataframe(mercados)
        if st.checkbox("Ver mapa"):
            midpoint = (np.average(mercados_ubicacion['lat']), np.average(mercados_ubicacion['lon']))
            st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=midpoint[0],
         longitude=midpoint[1],
         zoom=11,
         pitch=50,
     ),
     layers=[
         pdk.Layer(
             'ScatterplotLayer',
             data=areas_ubicacion,
             get_position='[lon, lat]',
             get_color='[10, 100, 100, 140]',
             get_radius=200,
         ),
     ],
 ))
        
elif menu == 'Calculadora IMECA':
        

    contaminantes = ['Nivel de Ozono (O3)', 'Monóxido de Carbono (CO)', 'Partículas Suspendidas (PM10)',
                     'Bióxido de Azufre (SO2)', 'Bióxido de nitrógeno (NO2)']
   
    ozono = st.slider('Selecciona un nivel de concentración de ozono (O3)', 0.0, 1.0, 0.5, 0.01)
    st.write('Nivel de ozono (O3): ', ozono, 'ppm')

    Co = st.slider('Selecciona un nivel de concentración de Monóxido de carbono (C0)', 0, 20, 10, 1)
    st.write('Nivel de Monóxido de carbono (C0): ', Co, 'ppm')

    Pm10 = st.slider('Selecciona un nivel de concentración de partículas suspendidas fracción respirable (PM10)', 0, 400, 120, 1)
    st.write('Nivel de partículas suspendidas fracción respirable (PM10): ', Pm10, 'µ/m3')

    So2 = st.slider('Selecciona un nivel de concentración de Bióxido de azufre (SO2)', 0.0, 1.0, 0.5, 0.01)
    st.write('Nivel de Bióxido de azufre (SO2): ', So2, 'ppm')

    No2 = st.slider('Selecciona un nivel de concentración de Bióxido de nitrógeno (NO2)', 0.0, 1.0, 0.5, 0.01)
    st.write('Nivel de Bióxido de nitrógeno (NO2): ', No2, 'ppm')

    st.write('El índice IMECA para cada contaminante es el siguiente: ')

     

    indice = IMECA(ozono, Co, Pm10, So2, No2)
    for i in range(len(contaminantes)):
        if indice[i] < 100:
            st.write('Indice **IMECA** para ', contaminantes[i],' es :',indice[i],', Categoría: **Satisfactorio**')
        if indice[i] > 100 and indice[i] < 201:
            st.write('Indice **IMECA** para ', contaminantes[i],' es :',indice[i],', Categoría: **No Satisfactorio**')
        if indice[i] > 200 and indice[i] < 301:
            st.write('Indice **IMECA** para ', contaminantes[i],' es :',indice[i],', Categoría: **Mala**')
        if indice[i] > 300:
            st.write('Indice **IMECA** para ', contaminantes[i],' es :',indice[i],', Categoría: **Muy mala**')
            
            
elif menu == 'Delegaciones más contaminadas':
    delegaciones = ['Gustavo A. Madero', 'Coyoacán', 'Benito Juarez',
                          'Milpa Alta', 'Azcapotzalco', 'Miguel Hidalgo', 
                          'Cuauhtémoc', 'Iztapalapa', 'Xochimilco', 'Venustiano Carranza', 
                            'Álvaro Obregón', 'Tlalpan', 'Magdalena Contreras', 'Cuajimalpa','Iztacalco']
    deleg = st.selectbox('Selecciona una delegación para mas información',(delegaciones))
    
elif menu == 'Resultados':
    st.write('Aquí va lo que salga de tu modelo')
    df = pd.DataFrame(np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],columns=['lat', 'lon'])
    st.dataframe(df)
    st.map(df)
    
    


