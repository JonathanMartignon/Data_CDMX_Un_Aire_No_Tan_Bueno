import streamlit as st
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pydeck as pdk
import webbrowser



@st.cache(suppress_st_warning=True)
def leer_datos():
    # Ciclistas
    ciclistas = pd.read_csv('../Datos/contador-ciclistas.csv')
    # mercados
    mercados = pd.read_csv('../Datos/mercados-publicos.csv')
    # Indice IMECA 2020
    indice_2020 = pd.read_csv('../Datos/imeca_2020.csv')
    #Calidad del aire
    calidad_aire = pd.read_csv('../Datos/prueba_datos_calidad_aire.csv')
    # Tiraderos clandestinos
    tiraderos_clandestinos = pd.read_csv('../Datos/tiraderos-clandestinos-al-cierre-de-2017.csv')
    # Nivel de plomo
    nivel_plomo = pd.read_csv('../Datos/red_manual_plomo.csv',skiprows=8)
    # Afluencia transporte
    afluencia_transport_df = pd.read_csv('../Datos/afluencia-preliminar-en-transporte-publico.csv')
    # Escuelas públicas
    escuelas_publicas = pd.read_csv('../Datos/Escuelas/escuelas-publicas.csv')
    # Escuelas privadas
    escuelas_privadas = pd.read_csv('../Datos/Escuelas/escuelas-privadas.csv')
    # Mercados
    mercados_df = pd.read_csv('../Datos/mercados-publicos.csv')
    # Parquímetros
    parquimetros_df = pd.read_csv('../Datos/prueba-parquimetros.csv')
    # Áreas Verdes
    areas_verdes = pd.read_csv('../Datos/cdmx_areas_verdes_2017.csv')
    # Estaciones_Ecobici
    estaciones_Ecobici = pd.read_csv('../Datos/estaciones-de-ecobici.csv')
    # Data Preprocesing
    data = pd.read_csv('../Notebook/Data_prep.csv')
    # Data2 Preprocesing
    data2 = pd.read_csv('../Notebook/data_preprocessed_streamlit.csv')
    
    
    return calidad_aire, indice_2020, areas_verdes, escuelas_publicas, escuelas_privadas, tiraderos_clandestinos, nivel_plomo, ciclistas, mercados, estaciones_Ecobici, parquimetros_df, data, data2
    

calidad_aire, indice_2020, areas_verdes, escuelas_publicas, escuelas_privadas, tiraderos_clandestinos, nivel_plomo, ciclistas, mercados, estaciones_Ecobici, parquimetros_df, data, data2 = leer_datos()


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


#Mapa tiraderos

latitud_tir = []
longitud_tir = []

for i in range(len(tiraderos_clandestinos)):
    if type(tiraderos_clandestinos['latitud'][i]) != float:
        latitud_tir.append(np.float64(tiraderos_clandestinos['latitud'][i]))
        
    if type(tiraderos_clandestinos['longitud'][i]) != float:
        longitud_tir.append(np.float64(tiraderos_clandestinos['longitud'][i]))
tiraderos_ubicacion = pd.DataFrame(latitud_tir, columns=['lat'])
tiraderos_ubicacion['lon'] = longitud_tir

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


# Front
st.title("CDMX Un aire no tan bueno")

menu = st.sidebar.radio('Menu',('Inicio','Datos', 'Calculadora IMECA', 'Delegaciones más contaminadas', 'Resultados','Extra','Referencias'))
st.sidebar.write('Autores:')

if st.sidebar.button('Ortega Ibarra Jaime Jesus'):
    joi = 'https://www.linkedin.com/in/joiortega1/'
    webbrowser.open_new_tab(joi)
    
if st.sidebar.button('Martiñón Luna Jonathan José'):
    jonny = 'https://www.linkedin.com/in/jonathan-marti%C3%B1%C3%B3n-793192204/'
    webbrowser.open_new_tab(jonny)

if menu == 'Inicio':
    
    st.write('De acuerdo con diversas fuentes como: El Financiero, Excelsior y Forbes, la Ciudad de México (CDMX) se encuentra como la quinta Urbe más contaminada a nivel mundial. Esto gracias al contador en tiempo real de Greenpeace, que permite rastrear por ciudad el costo de la contaminación del aire durante la pandemia de Covid-19.')

    st.write('La Ciudad de México ocupa el quinto lugar de 28 urbes en registrar 11,000 muertes vinculadas a contaminación del aire en la primera mitad del 2020, lo que equivale a un costo de 5.5 mil millones de dólares, de acuerdo a dicho contador.')

    cdmx = Image.open('../Imagenes/trafic_cdmx.jpg')
    st.image(cdmx, caption='Afluencia Vehícular. Credit: Adriana Zehbrauskas para The New York Times',use_column_width=True)

if menu == 'Datos':
    st.subheader('Datos')
    option = st.selectbox('Selecciona una opción para ver los datos',('Calidad del Aire', 'Indices de Contaminación', 'Niveles de Plomo en el aire',
                          'Tiraderos Clandestinos en CDMX', 'Areas verdes en CDMX', 'Escuelas en CDMX', 
                          'Mercados Públicos en CDMX', 'Afluencia de Ciclistas','Parquímetros en CDMX'))
    
    if option == 'Areas verdes en CDMX':
        st.dataframe(areas_verdes)
        
        if st.checkbox('Ver mapa'):
            midpoint = (np.average(areas_ubicacion['lat']), np.average(areas_ubicacion['lon']))
            st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
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
        
        if st.checkbox("Promedio de Contaminantes Noreste"):
            noreste = Image.open('../Imagenes/Promedio de Contaminantes presentes en el Noreste 2020.png')
            
            st.image(noreste,use_column_width=True)
        if st.checkbox("Promedio de Contaminantes Suroeste"):
            suroeste = Image.open('../Imagenes/Promedio de Contaminantes presentes en el Suroeste 2020.png')            
            st.image(suroeste,use_column_width=True) 
            
        if st.checkbox("Promedio de Contaminantes Noroeste"):
            Noroeste = Image.open('../Imagenes/Promedio de Contaminantes presentes en el Noroeste 2020.png')
            st.image(Noroeste,use_column_width=True)
            
        if st.checkbox("Promedio de Contaminantes Sureste"):
            Sureste = Image.open('../Imagenes/Promedio de Contaminantes presentes en el Sureste 2020.png')
            st.image(Sureste,use_column_width=True) 
        
    elif option == 'Tiraderos Clandestinos en CDMX':
        st.dataframe(tiraderos_clandestinos)
        st.markdown('Tiraderos clandestinos por Alcaldía')
        st.pyplot(tiraderos_alcaldias)
        
        if st.checkbox('Ver mapa'):
            midpoint = (np.average(tiraderos_ubicacion['lat']), np.average(tiraderos_ubicacion['lon']))
            st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=midpoint[0],
         longitude=midpoint[1],
         zoom=11,
         pitch=10,
     ),
     layers=[
         pdk.Layer(
             'HexagonLayer',
            data=tiraderos_ubicacion,
            get_position='[lon, lat]',
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
         ),
         pdk.Layer(
             'ScatterplotLayer',
             data=tiraderos_ubicacion,
             get_position='[lon, lat]',
             get_color='[10, 100, 10, 140]',
             get_radius=200,
         ),
         
     ],
 ))
            
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
        
        if st.checkbox("Afluencia de rutas 2019"):
            ruta_2019 = Image.open('../Imagenes/Ciclistas2019.png')
            st.image(ruta_2019,use_column_width=True)
            
        if st.checkbox("Afluencia de rutas 2020"):
            ruta_2020 = Image.open('../Imagenes/Ciclistas2020.png')
            st.image(ruta_2020,use_column_width=True)            
        st.dataframe(estaciones_Ecobici)
        
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
        
    elif option == 'Parquímetros en CDMX':
        st.dataframe(parquimetros_df)
        
        if st.checkbox("Ver parquímetros por Delegación"):
            park_alc = Image.open('../Imagenes/Parquímetros_públicos_por_alcaldía.png')
            st.image(park_alc,use_column_width=True)
            
        if st.checkbox("ver parquímetros por colonia"):
            park_col = Image.open('../Imagenes/Parquímetros_públicos_por_colonia.png')
            st.image(park_col,use_column_width=True)    
        
        
elif menu == 'Calculadora IMECA':
    st.subheader('Calculadora IMECA')

    contaminantes = ['Nivel de Ozono (O3)', 'Monóxido de Carbono (CO)', 'Partículas Suspendidas (PM10)',
                     'Bióxido de Azufre (SO2)', 'Bióxido de nitrógeno (NO2)']
   
    ozono = st.slider('Selecciona un nivel de concentración de ozono (O3)', 0.0, 1.0, 0.5, 0.01)
    #st.write('Nivel de ozono (O3): ', ozono, 'ppm')

    Co = st.slider('Selecciona un nivel de concentración de Monóxido de carbono (C0)', 0, 20, 10, 1)
    #st.write('Nivel de Monóxido de carbono (C0): ', Co, 'ppm')

    Pm10 = st.slider('Selecciona un nivel de concentración de partículas suspendidas fracción respirable (PM10)', 0, 400, 120, 1)
    #st.write('Nivel de partículas suspendidas fracción respirable (PM10): ', Pm10, 'µ/m3')

    So2 = st.slider('Selecciona un nivel de concentración de Bióxido de azufre (SO2)', 0.0, 1.0, 0.5, 0.01)
    #st.write('Nivel de Bióxido de azufre (SO2): ', So2, 'ppm')

    No2 = st.slider('Selecciona un nivel de concentración de Bióxido de nitrógeno (NO2)', 0.0, 1.0, 0.5, 0.01)
    #st.write('Nivel de Bióxido de nitrógeno (NO2): ', No2)

    st.write('El índice IMECA para cada contaminante es el siguiente: ')
    
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
    st.subheader('Delegaciones más contaminadas')
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril','Mayo','Junio','Julio',
                                      'Agosto','Septiembre','Octubre','Noviembre','Diciembre']
    st.write('Las siguientes gráficas muestran el índice de cada uno de los contaminantes en las diferentes delegaciones por mes.')
    mes = st.selectbox('Selecciona un mes',(meses))
    for i in range(len(meses)):
        if mes == meses[i]:
            ruta = '../Imagenes/'+meses[i]+'.png'
            graf_mes = Image.open(ruta)
            st.image(graf_mes,use_column_width=True)

        
elif menu == 'Resultados':
    st.subheader('Resultados')
    st.write('Dado el conjunto de datos obtenido durante el preprocesamiento')
    st.dataframe(data2)
    st.write('Lo cual nos da la siguiente correlación')
    ruta = '../Imagenes/corr_data_prep.png'
    corr_prep2 = Image.open(ruta)
    st.image(corr_prep2,use_column_width=True)
    st.write('Como podemos observar, no se encuentra correlación alguna entre variables, por lo que iniciamos el modelo para ver si este problema persistía, en lo cual nos arrojo un MSE cuyo valor era bastante alto, dentro del Notebook podemos observar los resultados obtenidos')
    st.write('Tambien podemos obtener la correlación entre los diferentes atributos y los diferentes contaminantes')
    corr_particulas = st.selectbox('Selecciona un contaminante',('Ozono', 'Dióxido de Azufre', 'Dióxido de Nitrógeno', 'Monóxido de Carbono', 'Partículas PM10'))
    if corr_particulas == 'Ozono':
        ruta = '../Imagenes/ozono_corr.png'
        ozono = Image.open(ruta)
        st.image(ozono,use_column_width=True)
    if corr_particulas == 'Dióxido de Azufre':
        ruta = '../Imagenes/azufre_corr.png'
        azufre = Image.open(ruta)
        st.image(azufre,use_column_width=True)
    if corr_particulas == 'Dióxido de Nitrógeno':
        ruta = '../Imagenes/nitrogeno_corr.png'
        nitrogeno = Image.open(ruta)
        st.image(nitrogeno,use_column_width=True)
    if corr_particulas == 'Monóxido de Carbono':
        ruta = '../Imagenes/carbono_corr.png'
        carbono = Image.open(ruta)
        st.image(carbono,use_column_width=True)
    if corr_particulas == 'Partículas PM10':
        ruta = '../Imagenes/particulas_corr.png'
        particulas = Image.open(ruta)
        st.image(particulas,use_column_width=True)
    st.write('\n Dentro del apartado Extra podremos observar otro análisis')
    

elif menu == 'Extra':
    st.subheader('Extra')
    st.write('Como parte del modelado, se decició crear el siguiente DataFrame, el cual muestra todos los índices trabajados por Alcaldía')
    st.dataframe(data)
    if st.checkbox('Ver correlación entre atributos'):
        ruta = '../Imagenes/Correlacion_dataprep.png'
        corr_prep = Image.open(ruta)
        st.image(corr_prep,use_column_width=True)
    st.write('Mediante una regresión logística, hemos logrado clasificar dichos atributos, devolviendo así el estatus del clima en cada una de las Alcaldías demtro de la Ciudad de México')
    if st.checkbox('Ver Gráfica 3D'):
        ruta = '../Imagenes/contaminantes_3d.png'
        image_3d = Image.open(ruta)
        st.image(image_3d,use_column_width=True)
    st.write('Dando el siguiente resultado')
    ruta = '../Imagenes/predict.png'
    pred = Image.open(ruta)
    st.image(pred,use_column_width=True)
        
    
    
    
elif menu == 'Referencias':
    st.subheader('Referencias')
    url_esc_pub = 'https://datos.cdmx.gob.mx/explore/dataset/escuelas-publicas/table/'
    if st.button('Escuelas Públicas'):
        webbrowser.open_new_tab(url_esc_pub)
        
    url_esc_priv = 'https://datos.cdmx.gob.mx/explore/dataset/escuelas-privadas/table/'
    if st.button('Escuelas Privadas'):
        webbrowser.open_new_tab(url_esc_priv)
    
    mercados_cdmx = 'https://datos.cdmx.gob.mx/explore/dataset/mercados-publicos/table/'
    if st.button('Mercados CDMX'):
        webbrowser.open_new_tab(mercados_cdmx)
    
    parquimetros_cdmx = 'https://datos.cdmx.gob.mx/explore/dataset/prueba-parquimetros/table/'
    if st.button('Parquímetros CDMX'):
        webbrowser.open_new_tab(parquimetros_cdmx)
        
    estaciones_ecobici = 'https://datos.cdmx.gob.mx/explore/dataset/estaciones-de-ecobici/table/'
    if st.button('Estaciones ECOBICI'):
        webbrowser.open_new_tab(estaciones_ecobici)
        
    areas_v = 'https://datos.cdmx.gob.mx/explore/dataset/cdmx_areas_verdes_2017/table/'
    if st.button('Áreas Verdes'):
        webbrowser.open_new_tab(areas_v)
    
    cont_ciclistas = 'https://datos.cdmx.gob.mx/explore/dataset/contador-ciclistas/table/'
    if st.button('Contador de Ciclistas'):
        webbrowser.open_new_tab(cont_ciclistas)
    
    calidad_aire = 'https://datos.cdmx.gob.mx/explore/dataset/prueba_datos_calidad_aire/table/'
    if st.button('Calidad del Aire'):
        webbrowser.open_new_tab(calidad_aire)
        
    contaminantes = 'https://datos.cdmx.gob.mx/explore/dataset/contaminantes/table/'
    if st.button('Concentraciones de contaminantes'):
        webbrowser.open_new_tab(contaminantes)
        
    datos_abiertos = 'https://datos.cdmx.gob.mx/'
    if st.button('Datos Abiertos CDMX'):
        webbrowser.open_new_tab(datos_abiertos)