"""Script for processing and analyzing DETRAN-BA vehicle fleet and service data."""

import pandas as pd
import openpyxl
import streamlit as st
import geopandas as gpd
import numpy as np
import folium
from streamlit_folium import st_folium
import json
import shapely.geometry

data = openpyxl.load_workbook(
    'data/Anexo 3 - Solicitação Quantidade Serviços Prestados por Tipo BA GERAL - '
    'Atualizado 20250409.xlsx', 
    data_only=True
)

data_frota = openpyxl.load_workbook(
    'data/Novo Anexo 1 - Solicitação de Frota BA 2022_2023_2024_2025 em 20250107.xlsx', 
    data_only=True
)

clinicas_cols = [
    'Id_Município Cidadão', 
    'Número CIRETRAN Município Cidadão', 
    'Nome CIRETRAN Município Cidadão', 
    'Município Cidadão',
    'Id_Município Clínica', 
    'Número CIRETRAN Clínica', 
    'Nome CIRETRAN Clínica', 
    'Município Clínica', 
    'CNPJ', 
    'Razão Social', 
    'Exames Médicos', 
    'Exames Psicológicos', 
    'Total', 
    'Percentual'
]

cfc_cols = [
    'Id_Município Cidadão', 
    'Número CIRETRAN Município Cidadão', 
    'Nome CIRETRAN Município Cidadão', 
    'Município Cidadão',
    'Id_Município CFC', 
    'Número CIRETRAN CFC', 
    'Nome CIRETRAN CFC', 
    'Município CFC', 
    'CNPJ', 
    'Razão Social', 
    'Cursos Teóricos',
    'Cursos Práticos', 
    'Total', 
    'Percentual'
]

epiv_cols = [
    'Id_Município', 
    'Número CIRETRAN', 
    'Nome CIRETRAN', 
    'Município',
    'CNPJ', 
    'Razão Social', 
    'Estampagem', 
    'Total', 
    'Percentual'
]

patio_cols = [
    'Id_Município', 
    'Número CIRETRAN', 
    'Nome CIRETRAN', 
    'Município',
    'CNPJ', 
    'Razão Social', 
    'Veículos removidos', 
    'Total', 
    'Percentual'
]

ecv_cols = [
    'Id_Município',
    'Número CIRETRAN',
    'Nome CIRETRAN',
    'Município',
    'CNPJ',
    'Razão Social',
    'Vistoria Lacrada Veículo 4 Rodas Até 16 Lugares ou Maior 3,5T',
    'Vistoria Lacrada Veículo Carga PBT Mais 3,5T',
    'Vistoria Lacrada Veículo Combinado Veículo P/Unidade',
    'Vistoria Lacrada Veículo Passageiro com Lotação Acima de 16 Lugares',
    'Vistoria Lacrada Veículo 2 ou 3 Rodas',
    'Vistoria RENAVE de Veículo 4 Rodas 16 Lugares ou Até 3,5 Ton',
    'Vistoria RENAVE de Veículos de 2 e 3 Rodas',
    'Vistoria Veículo Carga com PBT Acima de 3,5T',
    'Vistoria Veicular de Combinações de Veículos por Unidade',
    'Vistoria Veículo 2 ou 3 Rodas',
    'Vistoria Veículo 4 Rodas Até 16 Lugares ou Até 3,5 Ton',
    'Vistoria Veículo Passageiros com Capacidade Acima de 16 Lugares',
    'Outras',
    'Total',
    'Percentual'
]

frota_cols = [
    'Id_Município', 
    'Número CIRETRAN', 
    'Nome CIRETRAN', 
    'Município',
    'Automóvel',
    'Caminhão',
    'Caminhonete',
    'Microonibus',
    'Moto',
    'Motor-Casa',
    'Onibus',
    'Reboque',
    'Trator',
    'Outros',
    'Total', 
    'Percentual'
]

frota_24 = data_frota['2025']
frota_df_24 = pd.DataFrame(frota_24.values)
frota_df_24 = frota_df_24.drop(columns=[16,17,18,19,20,21,22,23,24,25,26])
frota_df_24.columns = frota_cols
frota_df_24 = frota_df_24.drop([0, 1, 2, 3])
frota_df_24 = frota_df_24.iloc[:-2]
frota_df_24 = frota_df_24.reset_index(drop=True)
frota_df_24['Percentual'] = frota_df_24['Percentual'].apply(lambda x: round(x * 100, 2))
frota_df_24['Id_Município'][frota_df_24['Município'] == 'SALVADOR'] = 3849

cfc_24 = data['Serviços_CFC_2024']
cfc_df_24 = pd.DataFrame(cfc_24.values)
cfc_df_24.columns = cfc_cols
cfc_df_24 = cfc_df_24.drop([0,1,2,3])
cfc_df_24 = cfc_df_24.iloc[:-2]
cfc_df_24 = cfc_df_24.reset_index(drop=True)
cfc_df_24['Percentual'] = cfc_df_24['Percentual'].apply(lambda x: round(x * 100, 2))

clinicas_24 = data['Serviços_Clinica_2024']
clinicas_df_24 = pd.DataFrame(clinicas_24.values)
clinicas_df_24.columns = clinicas_cols
clinicas_df_24 = clinicas_df_24.drop([0,1,2,3])
clinicas_df_24 = clinicas_df_24.iloc[:-2]
clinicas_df_24 = clinicas_df_24.reset_index(drop=True)
clinicas_df_24['Percentual'] = clinicas_df_24['Percentual'].apply(lambda x: round(x * 100, 2))

epiv_24 = data['Serviços_EPIV_2024']
epiv_df_24 = pd.DataFrame(epiv_24.values)
epiv_df_24.columns = epiv_cols
epiv_df_24 = epiv_df_24.drop([0,1,2,3])
epiv_df_24 = epiv_df_24.iloc[:-2]
epiv_df_24 = epiv_df_24.reset_index(drop=True)
epiv_df_24['Percentual'] = epiv_df_24['Percentual'].apply(lambda x: round(x * 100, 2))

ecv_24 = data['Serviços_ECV_2024']
ecv_df_24 = pd.DataFrame(ecv_24.values)
ecv_df_24.columns = ecv_cols
ecv_df_24 = ecv_df_24.drop([0,1,2,3])
ecv_df_24 = ecv_df_24.iloc[:-2]
ecv_df_24 = ecv_df_24.reset_index(drop=True)
ecv_df_24['Percentual'] = ecv_df_24['Percentual'].apply(lambda x: round(x * 100, 2))

vistoria_24 = data['Serviços_Vistoria_DETRAN_2024']
vistoria_df_24 = pd.DataFrame(vistoria_24.values)
vistoria_df_24.columns = ecv_cols
vistoria_df_24 = vistoria_df_24.drop([0,1,2,3])
vistoria_df_24 = vistoria_df_24.iloc[:-2]
vistoria_df_24 = vistoria_df_24.reset_index(drop=True)
vistoria_df_24['Percentual'] = vistoria_df_24['Percentual'].apply(lambda x: round(x * 100, 2))

patio_24 = data['Serviços_Pátio_2024']
patio_df_24 = pd.DataFrame(patio_24.values)
patio_df_24.columns = patio_cols
patio_df_24 = patio_df_24.drop([0,1,2,3])
patio_df_24 = patio_df_24.iloc[:-2]
patio_df_24 = patio_df_24.reset_index(drop=True)
patio_df_24['Percentual'] = patio_df_24['Percentual'].apply(lambda x: round(x * 100, 2))

# Criar dataframes agrupados por município
# CFCs - agrupar por município do CFC
cfc_grouped = cfc_df_24.groupby('Id_Município CFC').agg({
    'Município CFC': 'first',
    'Cursos Teóricos': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Cursos Práticos': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Total': lambda x: pd.to_numeric(x, errors='coerce').sum()
}).reset_index().rename(columns={'Id_Município CFC': 'Id_Município', 'Município CFC': 'Município'})

# Clínicas - agrupar por município da clínica
clinicas_grouped = clinicas_df_24.groupby('Id_Município Clínica').agg({
    'Município Clínica': 'first',
    'Exames Médicos': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Exames Psicológicos': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Total': lambda x: pd.to_numeric(x, errors='coerce').sum()
}).reset_index().rename(columns={'Id_Município Clínica': 'Id_Município', 'Município Clínica': 'Município'})

# Frota - agrupar por município
frota_grouped = frota_df_24.groupby('Id_Município').agg({
    'Município': 'first',
    'Automóvel': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Caminhão': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Caminhonete': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Microonibus': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Moto': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Motor-Casa': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Onibus': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Reboque': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Trator': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Outros': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Total': lambda x: pd.to_numeric(x, errors='coerce').sum()
}).reset_index()

# EPIVs - agrupar por município
epiv_grouped = epiv_df_24.groupby('Id_Município').agg({
    'Município': 'first',
    'Estampagem': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Total': lambda x: pd.to_numeric(x, errors='coerce').sum()
}).reset_index()

# ECVs - agrupar por município
ecv_grouped = ecv_df_24.groupby('Id_Município').agg({
    'Município': 'first',
    'Vistoria Lacrada Veículo 4 Rodas Até 16 Lugares ou Maior 3,5T': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Vistoria Lacrada Veículo Carga PBT Mais 3,5T': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Vistoria Lacrada Veículo Combinado Veículo P/Unidade': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Vistoria Lacrada Veículo Passageiro com Lotação Acima de 16 Lugares': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Vistoria Lacrada Veículo 2 ou 3 Rodas': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Vistoria RENAVE de Veículo 4 Rodas 16 Lugares ou Até 3,5 Ton': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Vistoria RENAVE de Veículos de 2 e 3 Rodas': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Vistoria Veículo Carga com PBT Acima de 3,5T': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Vistoria Veicular de Combinações de Veículos por Unidade': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Vistoria Veículo 2 ou 3 Rodas': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Vistoria Veículo 4 Rodas Até 16 Lugares ou Até 3,5 Ton': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Vistoria Veículo Passageiros com Capacidade Acima de 16 Lugares': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Outras': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Total': lambda x: pd.to_numeric(x, errors='coerce').sum()
}).reset_index()

# Vistorias DETRAN - agrupar por município
vistoria_grouped = vistoria_df_24.groupby('Id_Município').agg({
    'Município': 'first',
    'Vistoria Lacrada Veículo 4 Rodas Até 16 Lugares ou Maior 3,5T': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Vistoria Lacrada Veículo Carga PBT Mais 3,5T': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Vistoria Lacrada Veículo Combinado Veículo P/Unidade': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Vistoria Lacrada Veículo Passageiro com Lotação Acima de 16 Lugares': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Vistoria Lacrada Veículo 2 ou 3 Rodas': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Vistoria RENAVE de Veículo 4 Rodas 16 Lugares ou Até 3,5 Ton': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Vistoria RENAVE de Veículos de 2 e 3 Rodas': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Vistoria Veículo Carga com PBT Acima de 3,5T': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Vistoria Veicular de Combinações de Veículos por Unidade': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Vistoria Veículo 2 ou 3 Rodas': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Vistoria Veículo 4 Rodas Até 16 Lugares ou Até 3,5 Ton': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Vistoria Veículo Passageiros com Capacidade Acima de 16 Lugares': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Outras': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Total': lambda x: pd.to_numeric(x, errors='coerce').sum()
}).reset_index()

# Pátios - agrupar por município
patio_grouped = patio_df_24.groupby('Id_Município').agg({
    'Município': 'first',
    'Veículos removidos': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Total': lambda x: pd.to_numeric(x, errors='coerce').sum()
}).reset_index()

# Garantir que Id_Município seja string em todos os dataframes
for df in [cfc_grouped, clinicas_grouped, frota_grouped, epiv_grouped, ecv_grouped, vistoria_grouped, patio_grouped]:
    df['Id_Município'] = df['Id_Município'].astype(str)

# Load GeoJSON data
with open('data/geo-ba.json', 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

# Create the base map centered on Bahia
m = folium.Map(
    location=[-12.5, -41.7],
    zoom_start=7,
    tiles=None,  # Remove o mapa base
    prefer_canvas=True,
    zoom_control=False,  # Remove os botões de zoom
    dragging=False,      # Desabilita o pan
    scrollWheelZoom=False,  # Desabilita zoom com scroll
    doubleClickZoom=False,  # Desabilita zoom com duplo clique
    boxZoom=False,          # Desabilita zoom com caixa
    touchZoom=False         # Desabilita zoom em dispositivos touch
)
# Garante que as opções estejam desabilitadas mesmo após a criação
m.options['dragging'] = False
m.options['scrollWheelZoom'] = False
m.options['doubleClickZoom'] = False
m.options['boxZoom'] = False
m.options['touchZoom'] = False

# Calcule os limites da Bahia a partir do geojson
polys = [shapely.geometry.shape(feature['geometry']) for feature in geojson_data['features']]
multi = shapely.geometry.MultiPolygon(polys)
bounds = multi.bounds  # (minx, miny, maxx, maxy)

# Expande o limite superior (maxy) para dar mais espaço acima
expand = 0.8  # valor menor para deixar a Bahia maior na tela
bounds = (bounds[0], bounds[1], bounds[2], bounds[3] + expand)

# Ajusta o mapa para mostrar apenas a Bahia e restringe o pan/zoom
m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
m.options['maxBounds'] = [[bounds[1], bounds[0]], [bounds[3], bounds[2]]]

# Add title and description
st.title('Mapa Interativo do DETRAN-BA')
st.write('Visualize diferentes dados do DETRAN-BA por município')

# Create a selectbox for choosing the visualization
visualization = st.selectbox(
    'Escolha o tipo de visualização:',
    ['Frota de Veículos', 'CFCs', 'Clínicas', 'EPIVs', 'ECVs', 'Vistorias DETRAN', 'Pátios']
)

# Function to create choropleth map based on selected data
def create_choropleth(data_df, title):
    # Garantir tipos corretos
    df = data_df.copy()
    df['Id_Município'] = df['Id_Município'].astype(str)

    # Depuração: mostrar estatísticas dos valores
    print('Resumo dos valores de Total:')
    print(df['Total'].describe())
    print(df[['Id_Município', 'Município', 'Total']].head(10))

    # Remover municípios sem valor
    df = df[df['Total'] > 0]

    # Calcule bins igualmente espaçados entre min e max
    num_bins = 4  # número de faixas desejadas
    min_val = int(df['Total'].min())
    max_val = int(df['Total'].max())
    bins = list(np.linspace(min_val, max_val, num_bins + 1))
    bins = [int(b) for b in bins]
    if len(bins) < 3:
        bins = [min_val, (min_val + max_val) // 2, max_val]

    # Adicionar camada base branca para o fundo do mapa
    folium.GeoJson(
        geojson_data,
        style_function=lambda x: {
            'fillColor': 'white',
            'color': '#666',
            'weight': 1,
            'fillOpacity': 1
        }
    ).add_to(m)

    # Preparar dicionário de dados para acesso rápido
    info_dict = df.set_index('Id_Município').to_dict(orient='index')

    # Função para buscar info do município
    def get_popup_html(feature):
        mun_id = str(feature['properties']['id'])
        info = info_dict.get(mun_id)
        if info:
            html = f"<b>{info['Município']}</b><br>"
            html += f"Total: {info['Total']:,.0f}"
            return html
        else:
            return "Sem dados"

    # Choropleth com bins definidos e cor visível (para legenda e coloração)
    folium.Choropleth(
        geo_data=geojson_data,
        name=title,
        data=df,
        columns=['Id_Município', 'Total'],
        key_on='feature.properties.id',
        nan_fill_color='blue',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.8,
        line_weight=1.2,
        legend_name=title,
        bins=bins,
        highlight=True
    ).add_to(m)

    # Adicionar propriedade 'valor' ao geojson para tooltip
    for feature in geojson_data['features']:
        mun_id = str(feature['properties']['id'])
        info = info_dict.get(mun_id)
        if info:
            feature['properties']['valor'] = info['Total']
        else:
            feature['properties']['valor'] = 'Sem dados'

    # Tooltip customizado: nome do município e valor do serviço/frota
    folium.GeoJson(
        geojson_data,
        name=title + " Tooltip",
        style_function=lambda x: {
            'fillColor': 'transparent',
            'color': '#666',
            'weight': 1,
            'fillOpacity': 0
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['name', 'valor'],
            aliases=['Município:', 'Quantidade:'],
            labels=True,
            sticky=True,
            style=("background-color: white; color: #333; font-size: 12px; border: 1px solid #666; border-radius: 3px; padding: 4px;"),
            localize=True,
            parse_html=True,
            max_width=300,
        ),
        highlight_function=lambda x: {'weight': 3, 'color': 'blue'},
    ).add_to(m)

# Create visualization based on selection
if visualization == 'Frota de Veículos':
    create_choropleth(frota_grouped, 'Total de Veículos')
elif visualization == 'CFCs':
    create_choropleth(cfc_grouped, 'Total de Serviços CFCs')
elif visualization == 'Clínicas':
    create_choropleth(clinicas_grouped, 'Total de Exames em Clínicas')
elif visualization == 'EPIVs':
    create_choropleth(epiv_grouped, 'Total de Serviços EPIVs')
elif visualization == 'ECVs':
    create_choropleth(ecv_grouped, 'Total de Vistorias ECVs')
elif visualization == 'Vistorias DETRAN':
    create_choropleth(vistoria_grouped, 'Total de Vistorias DETRAN')
elif visualization == 'Pátios':
    create_choropleth(patio_grouped, 'Total de Veículos Removidos')

# Display the map
st_folium(m, width=700, height=500)

# Show additional statistics based on selection
st.subheader('Estatísticas')
if visualization == 'Frota de Veículos':
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric('Total de Veículos', f"{frota_df_24['Total'].sum():,.0f}")
    with col2:
        st.metric('Total de Motos', f"{frota_df_24['Moto'].sum():,.0f}")
    with col3:
        st.metric('Total de Automóveis', f"{frota_df_24['Automóvel'].sum():,.0f}")
else:
    selected_df = {
        'CFCs': cfc_grouped,
        'Clínicas': clinicas_grouped,
        'EPIVs': epiv_grouped,
        'ECVs': ecv_grouped,
        'Vistorias DETRAN': vistoria_grouped,
        'Pátios': patio_grouped
    }[visualization]
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric('Total de Serviços', f"{selected_df['Total'].sum():,.0f}")
    with col2:
        st.metric('Número de Municípios', f"{len(selected_df):,.0f}")