import json
import pandas as pd
from unidecode import unidecode

# Ler o arquivo CSV de população
df_populacao = pd.read_csv('populacao.csv')
# Criar dicionário de nome -> id
municipios_pop = {unidecode(nome): str(id_mun) 
                 for nome, id_mun in zip(df_populacao['Municipio'], df_populacao['Id_Municipio'])}

# Ler o arquivo GeoJSON
with open('data/geo-ba.json', 'r', encoding='utf-8') as f:
    geojson = json.load(f)

# Contador para verificar quantas alterações foram feitas
alteracoes = 0
nao_encontrados = []

# Atualizar os IDs
for feature in geojson['features']:
    nome_municipio = unidecode(feature['properties']['name'])
    nome_municipio = nome_municipio.upper()
    if nome_municipio in municipios_pop:
        novo_id = municipios_pop[nome_municipio]
        if feature['properties']['id'] != novo_id:
            print(f"Atualizando {feature['properties']['name']}: {feature['properties']['id']} -> {novo_id}")
            feature['properties']['id'] = novo_id
            alteracoes += 1
    else:
        nao_encontrados.append(feature['properties']['name'])

# Salvar o arquivo atualizado
with open('data/geo-ba.json', 'w', encoding='utf-8') as f:
    json.dump(geojson, f, ensure_ascii=False, indent=2)

print(f"\nTotal de alterações feitas: {alteracoes}")
if nao_encontrados:
    print("\nMunicípios não encontrados no arquivo de população:")
    for municipio in sorted(nao_encontrados):
        print(f"- {municipio}") 