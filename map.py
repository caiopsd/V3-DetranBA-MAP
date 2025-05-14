"""Script for processing and analyzing DETRAN-BA vehicle fleet and service data."""

import pandas as pd
import openpyxl
import streamlit as st
import numpy as np
import folium
import streamlit.components.v1 as components
import json
import shapely.geometry
import unicodedata

st.set_page_config(layout="wide")

# Definição das regiões da Bahia
regioes_ba = {
    'Centro-Norte': [   'AMÉRICA DOURADA',
                        'ANDORINHA',
                        'ANGUERA',
                        'ANTÔNIO CARDOSO',
                        'ANTÔNIO GONÇALVES',
                        'BAIXA GRANDE',
                        'BARRA DO MENDES',
                        'BARRO ALTO',
                        'BOA VISTA DO TUPIM',
                        'CAFARNAUM',
                        'CALDEIRÃO GRANDE',
                        'CAMPO FORMOSO',
                        'CANARANA',
                        'CAPIM GROSSO',
                        'CAÉM',
                        'CENTRAL',
                        'CONCEIÇÃO DA FEIRA',
                        'CONCEIÇÃO DO JACUÍPE',
                        'CORAÇÃO DE MARIA',
                        'ELÍSIO MEDRADO',
                        'FEIRA DE SANTANA',
                        'FILADÉLFIA',
                        'GENTIO DO OURO',
                        'IAÇU',
                        'IBIPEBA',
                        'IBIQUERA',
                        'IBITITÁ',
                        'IPECAETÁ',
                        'IPIRÁ',
                        'IRAQUARA',
                        'IRARÁ',
                        'IRECÊ',
                        'ITABERABA',
                        'ITATIM',
                        'ITIÚBA',
                        'JACOBINA',
                        'JAGUARARI',
                        'JOÃO DOURADO',
                        'JUSSARA',
                        'LAJEDINHO',
                        'LAPÃO',
                        'MACAJUBA',
                        'MAIRI',
                        'MIGUEL CALMON',
                        'MIRANGABA',
                        'MORRO DO CHAPÉU',
                        'MULUNGU DO MORRO',
                        'MUNDO NOVO',
                        'OURIÇANGAS',
                        'OUROLÂNDIA',
                        'PEDRÃO',
                        'PINDOBAÇU',
                        'PINTADAS',
                        'PIRITIBA',
                        'PONTO NOVO',
                        'PRESIDENTE DUTRA',
                        'QUIXABEIRA',
                        'RAFAEL JAMBEIRO',
                        'RUY BARBOSA',
                        'SANTA BÁRBARA',
                        'SANTA TERESINHA',
                        'SANTANÓPOLIS',
                        'SANTO ESTÊVÃO',
                        'SAÚDE',
                        'SENHOR DO BONFIM',
                        'SERRA PRETA',
                        'SERROLÂNDIA',
                        'SOUTO SOARES',
                        'SÃO GABRIEL',
                        'SÃO GONÇALO DOS CAMPOS',
                        'SÃO JOSÉ DO JACUÍPE',
                        'TANQUINHO',
                        'TAPIRAMUTÁ',
                        'TEODORO SAMPAIO',
                        'UIBAÍ',
                        'UMBURANAS',
                        'VÁRZEA DA ROÇA',
                        'VÁRZEA DO POÇO',
                        'VÁRZEA NOVA',
                        'ÁGUA FRIA'],
    'Centro-Sul': [   'ABAÍRA',
                      'AIQUARA',
                      'AMARGOSA',
                      'ANAGÉ',
                      'ANDARAÍ',
                      'APUAREMA',
                      'ARACATU',
                      'BARRA DA ESTIVA',
                      'BARRA DO CHOÇA',
                      'BELO CAMPO',
                      'BOA NOVA',
                      'BOM JESUS DA SERRA',
                      'BONINAL',
                      'BONITO',
                      'BOQUIRA',
                      'BOTUPORÃ',
                      'BREJÕES',
                      'BROTAS DE MACAÚBAS',
                      'BRUMADO',
                      'CAATIBA',
                      'CACULÉ',
                      'CAETANOS',
                      'CAETITÉ',
                      'CANDIBA',
                      'CARAÍBAS',
                      'CATURAMA',
                      'CONDEÚBA',
                      'CONTENDAS DO SINCORÁ',
                      'CORDEIROS',
                      'CRAVOLÂNDIA',
                      'CÂNDIDO SALES',
                      'DOM BASÍLIO',
                      'DÁRIO MEIRA',
                      'ENCRUZILHADA',
                      'GUAJERU',
                      'GUANAMBI',
                      'IBIASSUCÊ',
                      'IBICOARA',
                      'IBICUÍ',
                      'IBIPITANGA',
                      'IBITIARA',
                      'IGAPORÃ',
                      'IGUAÍ',
                      'IPUPIARA',
                      'IRAJUBA',
                      'IRAMAIA',
                      'ITAETÉ',
                      'ITAGI',
                      'ITAMBÉ',
                      'ITAPETINGA',
                      'ITAQUARA',
                      'ITARANTIM',
                      'ITIRUÇU',
                      'ITORORÓ',
                      'ITUAÇU',
                      'IUIÚ',
                      'JACARACI',
                      'JAGUAQUARA',
                      'JEQUIÉ',
                      'JIQUIRIÇÁ',
                      'JITAÚNA',
                      'JUSSIAPE',
                      'LAFAIETE COUTINHO',
                      'LAJEDO DO TABOCAL',
                      'LAGOA REAL',
                      'LAJE',
                      'LENÇÓIS',
                      'LICÍNIO DE ALMEIDA',
                      'LIVRAMENTO DE NOSSA SENHORA',
                      'MACARANI',
                      'MACAÚBAS',
                      'MAETINGA',
                      'MAIQUINIQUE',
                      'MALHADA',
                      'MALHADA DE PEDRAS',
                      'MANOEL VITORINO',
                      'MARACÁS',
                      'MARCIONÍLIO SOUZA',
                      'MATINA',
                      'MILAGRES',
                      'MIRANTE',
                      'MORTUGABA',
                      'MUCUGÊ',
                      'MUTUÍPE',
                      'NOVA CANAÃ',
                      'NOVA ITARANA',
                      'NOVA REDENÇÃO',
                      'NOVO HORIZONTE',
                      'OLIVEIRA DOS BREJINHOS',
                      'PALMAS DE MONTE ALTO',
                      'PALMEIRAS',
                      'PARAMIRIM',
                      'PIATÃ',
                      'PINDAÍ',
                      'PIRIPÁ',
                      'PLANALTINO',
                      'PLANALTO',
                      'POTIRAGUÁ',
                      'POÇÕES',
                      'PRESIDENTE JÂNIO QUADROS',
                      'RIACHO DE SANTANA',
                      'RIBEIRÃO DO LARGO',
                      'RIO DE CONTAS',
                      'RIO DO ANTÔNIO',
                      'RIO DO PIRES',
                      'SANTA INÊS',
                      'SEABRA',
                      'SEBASTIÃO LARANJEIRAS',
                      'SÃO MIGUEL DAS MATAS',
                      'TANHAÇU',
                      'TANQUE NOVO',
                      'TREMEDAL',
                      'UBAÍRA',
                      'URANDI',
                      'UTINGA',
                      'VITÓRIA DA CONQUISTA',
                      'WAGNER',
                      'ÉRICO CARDOSO'],
    'Extremo oeste': [   'ANGICAL',
                         'BAIANÓPOLIS',
                         'BARREIRAS',
                         'BREJOLÂNDIA',
                         'CANÁPOLIS',
                         'CATOLÂNDIA',
                         'COCOS',
                         'CORIBE',
                         'CORRENTINA',
                         'COTEGIPE',
                         'CRISTÓPOLIS',
                         'FORMOSA DO RIO PRETO',
                         'JABORANDI',
                         'LUÍS EDUARDO MAGALHÃES',
                         'MANSIDÃO',
                         'RIACHÃO DAS NEVES',
                         'SANTA MARIA DA VITÓRIA',
                         'SANTA RITA DE CÁSSIA',
                         'SANTANA',
                         'SERRA DOURADA',
                         'SÃO DESIDÉRIO',
                         'SÃO FÉLIX DO CORIBE',
                         'TABOCAS DO BREJO VELHO',
                         'WANDERLEY'],
    'Nordeste': [   'ACAJUTIBA',
                    'ADUSTINA',
                    'ALAGOINHAS',
                    'ANTAS',
                    'APORÁ',
                    'ARACI',
                    'ARAMARI',
                    'ARAÇAS',
                    'BANZAÊ',
                    'BARROCAS',
                    'BIRITINGA',
                    'CANDEAL',
                    'CANSANÇÃO',
                    'CANUDOS',
                    'CAPELA DO ALTO ALEGRE',
                    'CARDEAL DA SILVA',
                    'CIPÓ',
                    'CONCEIÇÃO DO COITÉ',
                    'CONDE',
                    'CORONEL JOÃO SÁ',
                    'CRISÓPOLIS',
                    'CÍCERO DANTAS',
                    'ENTRE RIOS',
                    'ESPLANADA',
                    'EUCLIDES DA CUNHA',
                    'FÁTIMA',
                    'GAVIÃO',
                    'HELIÓPOLIS',
                    'ICHU',
                    'INHAMBUPE',
                    'ITAPICURU',
                    'JANDAÍRA',
                    'JEREMOABO',
                    'LAMARÃO',
                    'MONTE SANTO',
                    'NORDESTINA',
                    'NOVA FÁTIMA',
                    'NOVA SOURE',
                    'NOVO TRIUNFO',
                    'OLINDINA',
                    'PARIPIRANGA',
                    'PEDRO ALEXANDRE',
                    'PÉ DE SERRA',
                    'QUEIMADAS',
                    'QUIJINGUE',
                    'RETIROLÂNDIA',
                    'RIACHÃO DO JACUÍPE',
                    'RIBEIRA DO AMPARO',
                    'RIBEIRA DO POMBAL',
                    'RIO REAL',
                    'SANTA BRÍGIDA',
                    'SANTALUZ',
                    'SERRINHA',
                    'SÁTIRO DIAS',
                    'SÃO DOMINGOS',
                    'SÍTIO DO QUINTO',
                    'TEOFILÂNDIA',
                    'TUCANO',
                    'UAUÁ',
                    'VALENTE'],
    'Regiâo Metropolitana de Salvador': [   'AMÉLIA RODRIGUES',
                                     'ARATUÍPE',
                                     'CABACEIRAS DO PARAGUAÇU',
                                     'CACHOEIRA',
                                     'CAMAÇARI',
                                     'CANDEIAS',
                                     'CASTRO ALVES',
                                     'CATU',
                                     'CONCEIÇÃO DO ALMEIDA',
                                     'CRUZ DAS ALMAS',
                                     "DIAS D'ÁVILA",
                                     'DOM MACEDO COSTA',
                                     'GOVERNADOR MANGABEIRA',
                                     'ITANAGRA',
                                     'ITAPARICA',
                                     'JAGUARIPE',
                                     'LAURO DE FREITAS',
                                     'MADRE DE DEUS',
                                     'MARAGOGIPE',
                                     'MATA DE SÃO JOÃO',
                                     'MUNIZ FERREIRA',
                                     'MURITIBA',
                                     'NAZARÉ',
                                     'POJUCA',
                                     'SALINAS DA MARGARIDA',
                                     'SALVADOR',
                                     'SANTO AMARO',
                                     'SANTO ANTÔNIO DE JESUS',
                                     'SAPEAÇU',
                                     'SAUBARA',
                                     'SIMÕES FILHO',
                                     'SÃO FELIPE',
                                     'SÃO FRANCISCO DO CONDE',
                                     'SÃO FÉLIX',
                                     'SÃO SEBASTIÃO DO PASSÉ',
                                     'TERRA NOVA',
                                     'VARZEDO',
                                     'VERA CRUZ'],
    'Sul': [   'ALCOBAÇA',
               'ALMADINA',
               'ARATACA',
               'AURELINO LEAL',
               'BARRA DO ROCHA',
               'BARRO PRETO',
               'BELMONTE',
               'BUERAREMA',
               'CAIRU',
               'CAMACAN',
               'CAMAMU',
               'CANAVIEIRAS',
               'CARAVELAS',
               'COARACI',
               'EUNÁPOLIS',
               'FIRMINO ALVES',
               'FLORESTA AZUL',
               'GANDU',
               'GONGOGI',
               'GUARATINGA',
               'IBICARAÍ',
               'IBIRAPITANGA',
               'IBIRAPUÃ',
               'IBIRATAIA',
               'IGRAPIÚNA',
               'ILHÉUS',
               'IPIAÚ',
               'ITABELA',
               'ITABUNA',
               'ITACARÉ',
               'ITAGIBÁ',
               'ITAGIMIRIM',
               'ITAJU DO COLÔNIA',
               'ITAJUÍPE',
               'ITAMARAJU',
               'ITAMARI',
               'ITANHÉM',
               'ITAPEBI',
               'ITAPITANGA',
               'ITAPÉ',
               'ITUBERÁ',
               'JUCURUÇU',
               'JUSSARI',
               'LAJEDÃO',
               'MARAÚ',
               'MASCOTE',
               'MEDEIROS NETO',
               'MUCURI',
               'NILO PEÇANHA',
               'NOVA IBIÁ',
               'NOVA VIÇOSA',
               'PAU BRASIL',
               'PIRAÍ DO NORTE',
               'PORTO SEGURO',
               'PRADO',
               'PRESIDENTE TANCREDO NEVES',
               'SANTA CRUZ CABRÁLIA',
               'SANTA CRUZ DA VITÓRIA',
               'SANTA LUZIA',
               'SÃO JOSÉ DA VITÓRIA',
               'TAPEROÁ',
               'TEIXEIRA DE FREITAS',
               'TEOLÂNDIA',
               'UBAITABA',
               'UBATÃ',
               'UNA',
               'URUÇUCA',
               'VALENÇA',
               'VEREDA',
               'WENCESLAU GUIMARÃES'],
    'Vale São-Franciscano': [   'ABARÉ',
                                'BARRA',
                                'BOM JESUS DA LAPA',
                                'BURITIRAMA',
                                'CAMPO ALEGRE DE LOURDES',
                                'CARINHANHA',
                                'CASA NOVA',
                                'CHORROCHÓ',
                                'CURAÇÁ',
                                'FEIRA DA MATA',
                                'GLÓRIA',
                                'IBOTIRAMA',
                                'ITAGUAÇU DA BAHIA',
                                'JUAZEIRO',
                                'MACURURÉ',
                                'MORPARÁ',
                                'MUQUÉM DE SÃO FRANCISCO',
                                'PARATINGA',
                                'PAULO AFONSO',
                                'PILÃO ARCADO',
                                'REMANSO',
                                'RODELAS',
                                'SENTO SÉ',
                                'SERRA DO RAMALHO',
                                'SOBRADINHO',
                                'SÍTIO DO MATO',
                                'XIQUE-XIQUE']
}

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
frota_df_24.loc[frota_df_24['Município'] == 'SALVADOR', 'Id_Município'] = 3849

# When adding data to frota_grouped, make sure to fix Dias d'Ávila name
dias_avila_mask = frota_df_24['Município'].apply(lambda x: 'DIAS' in str(x).upper() and ('AVILA' in str(x).upper() or 'ÁVILA' in str(x).upper()))
if dias_avila_mask.any():
    frota_df_24.loc[dias_avila_mask, 'Município'] = "DIAS D'ÁVILA"

cfc_24 = data['Serviços_CFC_2024']
cfc_df_24 = pd.DataFrame(cfc_24.values)
cfc_df_24.columns = cfc_cols
cfc_df_24 = cfc_df_24.drop([0,1,2,3])
cfc_df_24 = cfc_df_24.iloc[:-2]
cfc_df_24 = cfc_df_24.reset_index(drop=True)
# Ensure CNPJ is string for consistent filtering
cfc_df_24['CNPJ'] = cfc_df_24['CNPJ'].astype(str).str.strip().replace('\\.0$', '', regex=True)
cfc_df_24['Percentual'] = cfc_df_24['Percentual'].apply(lambda x: round(x * 100, 2))
cfc_df_24['Total'] = pd.to_numeric(cfc_df_24['Total'], errors='coerce').fillna(0)

clinicas_24 = data['Serviços_Clinica_2024']
clinicas_df_24 = pd.DataFrame(clinicas_24.values)
clinicas_df_24.columns = clinicas_cols
clinicas_df_24 = clinicas_df_24.drop([0,1,2,3])
clinicas_df_24 = clinicas_df_24.iloc[:-2]
clinicas_df_24 = clinicas_df_24.reset_index(drop=True)
# Ensure CNPJ is string for consistent filtering
clinicas_df_24['CNPJ'] = clinicas_df_24['CNPJ'].astype(str).str.strip().replace('\\.0$', '', regex=True)
clinicas_df_24['Percentual'] = clinicas_df_24['Percentual'].apply(lambda x: round(x * 100, 2))
clinicas_df_24['Total'] = pd.to_numeric(clinicas_df_24['Total'], errors='coerce').fillna(0)

epiv_24 = data['Serviços_EPIV_2024']
epiv_df_24 = pd.DataFrame(epiv_24.values)
epiv_df_24.columns = epiv_cols
epiv_df_24 = epiv_df_24.drop([0,1,2,3])
epiv_df_24 = epiv_df_24.iloc[:-2]
epiv_df_24 = epiv_df_24.reset_index(drop=True)
epiv_df_24['Percentual'] = epiv_df_24['Percentual'].apply(lambda x: round(x * 100, 2))
epiv_df_24['Total'] = pd.to_numeric(epiv_df_24['Total'], errors='coerce').fillna(0)

ecv_24 = data['Serviços_ECV_2024']
ecv_df_24 = pd.DataFrame(ecv_24.values)
ecv_df_24.columns = ecv_cols
ecv_df_24 = ecv_df_24.drop([0,1,2,3])
ecv_df_24 = ecv_df_24.iloc[:-2]
ecv_df_24 = ecv_df_24.reset_index(drop=True)
ecv_df_24['Percentual'] = ecv_df_24['Percentual'].apply(lambda x: round(x * 100, 2))
ecv_df_24['Total'] = pd.to_numeric(ecv_df_24['Total'], errors='coerce').fillna(0)

vistoria_24 = data['Serviços_Vistoria_DETRAN_2024']
vistoria_df_24 = pd.DataFrame(vistoria_24.values)
vistoria_df_24.columns = ecv_cols
vistoria_df_24 = vistoria_df_24.drop([0,1,2,3])
vistoria_df_24 = vistoria_df_24.iloc[:-2]
vistoria_df_24 = vistoria_df_24.reset_index(drop=True)
vistoria_df_24['Percentual'] = vistoria_df_24['Percentual'].apply(lambda x: round(x * 100, 2))
vistoria_df_24['Total'] = pd.to_numeric(vistoria_df_24['Total'], errors='coerce').fillna(0)

patio_24 = data['Serviços_Pátio_2024']
patio_df_24 = pd.DataFrame(patio_24.values)
patio_df_24.columns = patio_cols
patio_df_24 = patio_df_24.drop([0,1,2,3])
patio_df_24 = patio_df_24.iloc[:-2]
patio_df_24 = patio_df_24.reset_index(drop=True)
patio_df_24['Percentual'] = patio_df_24['Percentual'].apply(lambda x: round(x * 100, 2))
patio_df_24['Total'] = pd.to_numeric(patio_df_24['Total'], errors='coerce').fillna(0)

# Carregar dados de população
populacao_df = pd.read_excel('data/populacao.xlsx')
# Renomear colunas para padronização e compatibilidade
populacao_df = populacao_df.rename(columns={'Id_Municipio': 'Id_Município', 'Municipio': 'Município_POP', 'Populacao': 'População'})
# Garantir que Id_Município seja string para merge
populacao_df['Id_Município'] = populacao_df['Id_Município'].astype(str)
# Remover municípios duplicados no dataframe de população, mantendo a primeira ocorrência
populacao_df = populacao_df.drop_duplicates(subset=['Id_Município'], keep='first')

# Calcular totais globais de serviços por CNPJ
cfc_total_servicos_global_por_cnpj = cfc_df_24.groupby('CNPJ')['Total'].sum().reset_index()
clinica_total_servicos_global_por_cnpj = clinicas_df_24.groupby('CNPJ')['Total'].sum().reset_index()
epiv_total_servicos_global_por_cnpj = epiv_df_24.groupby('CNPJ')['Total'].sum().reset_index()
ecv_total_servicos_global_por_cnpj = ecv_df_24.groupby('CNPJ')['Total'].sum().reset_index()
vistoria_total_servicos_global_por_cnpj = vistoria_df_24.groupby('CNPJ')['Total'].sum().reset_index()
patio_total_servicos_global_por_cnpj = patio_df_24.groupby('CNPJ')['Total'].sum().reset_index()

# Criar dataframes agrupados por município
# CFCs - agrupar por município do CFC
cfc_grouped = cfc_df_24.groupby('Id_Município CFC').agg({
    'Município CFC': 'first',
    'Cursos Teóricos': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Cursos Práticos': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Total': lambda x: pd.to_numeric(x, errors='coerce').sum()
}).reset_index().rename(columns={'Id_Município CFC': 'Id_Município', 'Município CFC': 'Município'})

# Fix Dias d'Ávila in cfc_grouped
dias_avila_mask = cfc_grouped['Município'].apply(lambda x: 'DIAS' in str(x).upper() and ('AVILA' in str(x).upper() or 'ÁVILA' in str(x).upper()))
if dias_avila_mask.any():
    cfc_grouped.loc[dias_avila_mask, 'Município'] = "DIAS D'ÁVILA"

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

# Garantir que a coluna de merge em frota_grouped também seja string
frota_grouped['Id_Município'] = frota_grouped['Id_Município'].astype(str)

# Mesclar frota_grouped com populacao_df
frota_grouped = pd.merge(frota_grouped, populacao_df[['Id_Município', 'População']], on='Id_Município', how='left')

populacao_df = populacao_df.rename(columns={'População': 'Total'})
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
    zoom_start=6,  # Reduzindo o zoom para mostrar mais área
    tiles='CartoDB positron',  # Mapa base mais claro
    prefer_canvas=True,
    zoom_control=True,  # Adiciona controles de zoom
    dragging=True,      # Permite arrastar o mapa
    scrollWheelZoom=True,  # Permite zoom com scroll
    doubleClickZoom=True,  # Permite zoom com duplo clique
    boxZoom=True,          # Permite zoom com caixa
    touchZoom=True,        # Permite zoom em dispositivos touch
    height=1200
)

# Calcule os limites da Bahia a partir do geojson
polys = [shapely.geometry.shape(feature['geometry']) for feature in geojson_data['features']]
multi = shapely.geometry.MultiPolygon(polys)
bounds = multi.bounds  # (minx, miny, maxx, maxy)

# Adicione uma pequena margem para melhor visualização
margin = 0.3
bounds = (bounds[0] - margin, bounds[1] - margin, bounds[2] + margin, bounds[3] + margin)

# Ajusta o mapa para mostrar a Bahia
m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])

# Calcule a proporção do shape da Bahia
aspect_ratio = (bounds[2] - bounds[0]) / (bounds[3] - bounds[1])
iframe_width = 2000
iframe_height = 800

# Add title and description
st.title('Mapa Interativo do DETRAN-BA')
st.write('Visualize diferentes dados do DETRAN-BA por município')

# Adicionar seleção do tipo de mapa
tipo_mapa = st.radio(
    'Escolha o tipo de mapa:',
    ['Mapa de Regiões', 'Mapa Padrão']
)

# Configurar o layout para ocupar toda a largura disponível
st.markdown("""
<style>
    .reportview-container .main .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Carregar dados dos CSVs de credenciados
credenciados_cfc_df = pd.read_csv('data/CredenciadosCFC.csv', header=None, names=['Nome', 'Município'])
credenciados_clinica_df = pd.read_csv('data/CredenciadosClinica.csv', header=None, names=['Nome', 'Município'])

# Add multi-select for municipalities
municipios = sorted(frota_grouped['Município'].unique())
# Corrigir o nome do município Dias d'Ávila
municipios = [m.replace('DIAS D AVILA', "DIAS D'AVILA") if m == 'DIAS D AVILA' else m for m in municipios]

# Esta variável armazena municípios selecionados diretamente pelo usuário via multiselect
municipios_selecionados_geral = st.multiselect(
    'Selecione municípios para destacar (geral):',
    municipios,
    default=[],
    key='geral_municipios_multiselect'
)

# Variáveis para armazenar municípios selecionados por diferentes filtros
municipios_cfc_razao = []  # Municípios selecionados via filtro CFC Razão Social
municipios_cfc_cnpj = []   # Municípios selecionados via filtro CFC CNPJ
municipios_clinica_razao = []  # Municípios selecionados via filtro Clínica Razão Social
municipios_clinica_cnpj = []   # Municípios selecionados via filtro Clínica CNPJ

# Create a selectbox for choosing the visualization - MOVED OUTSIDE CONDITIONAL
visualization = st.selectbox(
    'Escolha o tipo de dados para visualizar no mapa e nas estatísticas:',
    [
        'Visão Geral',
        'Frota de Veículos',
        'CFCs', 'Quantidade de CFCs',
        'Clínicas', 'Quantidade de Clínicas',
        'EPIVs', 'Quantidade de EPIVs',
        'ECVs', 'Quantidade de ECVs',
        'Vistorias DETRAN', 'Quantidade de Vistorias DETRAN',
        'Pátios', 'Quantidade de Pátios'
    ]
)

# Create a selectbox for choosing the visualization
if tipo_mapa == 'Mapa Padrão':
    # The visualization selectbox is now defined above, no need to redefine here.
    # We just need to make sure the logic uses the 'visualization' variable correctly.
    pass # No action needed here as visualization is already set globally
# REMOVED ELSE BLOCK:
# else:
#     # Para o mapa de regiões, não precisamos de seleção de visualização PARA O MAPA
#     # Mas as estatísticas ainda usarão a seleção do 'visualization' global
#     pass # visualization remains as selected globally

# Initialize selection variables to avoid NameError
escolha_razao_cfc = 'Todos (Razão Social)'
escolha_cnpj_cfc = 'Todos (CNPJ)'
escolha_razao_clinica = 'Todas (Razão Social)'
escolha_cnpj_clinica = 'Todos (CNPJ)'

# Adicionar seleção de credenciados para visualizações específicas
# credenciado_selecionado will store the NAME of the chosen entity for filtering inside create_choropleth
# municipios_selecionados (global) will store the list of municipalities to highlight, potentially overridden by these selections.
credenciado_selecionado = None # Holds the name of the selected credenciado

if visualization == 'Quantidade de CFCs':
    col1_cfc, col2_cfc = st.columns(2)
    with col1_cfc:
        opcoes_razao_cfc = ['Todos (Razão Social)'] + list(credenciados_cfc_df['Nome'].drop_duplicates().sort_values())
        escolha_razao_cfc = st.selectbox(
            'Filtrar por CFC (Razão Social):',
            options=opcoes_razao_cfc,
            index=0,
            key='sel_cfc_razao'
        )
    with col2_cfc:
        cnpjs_cfc_list = ['Todos (CNPJ)'] + sorted(list(cfc_df_24['CNPJ'].dropna().astype(str).unique()))
        escolha_cnpj_cfc = st.selectbox(
            'Filtrar por CFC (CNPJ):',
            options=cnpjs_cfc_list,
            index=0,
            key='sel_cfc_cnpj'
        )

    if escolha_razao_cfc != 'Todos (Razão Social)':
        # Ao invés de sobrescrever municipios_selecionados, populamos municipios_cfc_razao
        municipios_cfc_razao = credenciados_cfc_df[credenciados_cfc_df['Nome'] == escolha_razao_cfc]['Município'].tolist()
    else:
        municipios_cfc_razao = []

    if escolha_cnpj_cfc != 'Todos (CNPJ)':
        # Ao invés de sobrescrever municipios_selecionados, populamos municipios_cfc_cnpj
        municipios_cfc_cnpj = cfc_df_24[cfc_df_24['CNPJ'].astype(str) == escolha_cnpj_cfc]['Município Cidadão'].unique().tolist()
    else:
        municipios_cfc_cnpj = []

elif visualization == 'Quantidade de Clínicas':
    col1_clinica, col2_clinica = st.columns(2)
    with col1_clinica:
        opcoes_razao_clinica = ['Todas (Razão Social)'] + list(credenciados_clinica_df['Nome'].drop_duplicates().sort_values())
        escolha_razao_clinica = st.selectbox(
            'Filtrar por Clínica (Razão Social):',
            options=opcoes_razao_clinica,
            index=0,
            key='sel_clinica_razao'
        )
    with col2_clinica:
        cnpjs_clinica_list = ['Todos (CNPJ)'] + sorted(list(clinicas_df_24['CNPJ'].dropna().astype(str).unique()))
        escolha_cnpj_clinica = st.selectbox(
            'Filtrar por Clínica (CNPJ):',
            options=cnpjs_clinica_list,
            index=0,
            key='sel_clinica_cnpj'
        )

    if escolha_razao_clinica != 'Todas (Razão Social)':
        # Ao invés de sobrescrever municipios_selecionados, populamos municipios_clinica_razao
        municipios_clinica_razao = credenciados_clinica_df[credenciados_clinica_df['Nome'] == escolha_razao_clinica]['Município'].tolist()
    else:
        municipios_clinica_razao = []

    if escolha_cnpj_clinica != 'Todos (CNPJ)':
        # Ao invés de sobrescrever municipios_selecionados, populamos municipios_clinica_cnpj
        municipios_clinica_cnpj = clinicas_df_24[clinicas_df_24['CNPJ'].astype(str) == escolha_cnpj_clinica]['Município Cidadão'].unique().tolist()
    else:
        municipios_clinica_cnpj = []

# Função para ativar o destaque adequado para o credenciado selecionado
# Esta função agora seleciona o conjunto de municípios apropriado com base na visualização e nas seleções
def get_municipios_por_credenciado_filtro():
    # Determinar qual filtro por credenciado está ativo
    if visualization == 'Quantidade de CFCs':
        if escolha_razao_cfc != 'Todos (Razão Social)':
            return municipios_cfc_razao
        elif escolha_cnpj_cfc != 'Todos (CNPJ)':
            return municipios_cfc_cnpj
    elif visualization == 'Quantidade de Clínicas':
        if escolha_razao_clinica != 'Todos (Razão Social)':
            return municipios_clinica_razao
        elif escolha_cnpj_clinica != 'Todos (CNPJ)':
            return municipios_clinica_cnpj
    # Se nenhum filtro por credenciado estiver ativo, retorna a lista vazia
    return []

# Função para normalizar nomes (remover acentos e deixar minúsculo)
def normaliza_nome(nome):
    if not isinstance(nome, str):
        return ''
    
    nome_upper = nome.upper() # For special name checks

    # Tratamento especial para Dias d'Ávila
    if 'DIAS D AVILA' in nome_upper or "DIAS D'AVILA" in nome_upper or 'DIAS DAVILA' in nome_upper:
        return 'dias davila'

    # General normalization (accents, case, strip)
    # Wrap in try-except for robustness, though isinstance check should prevent most issues
    try:
        base_normalized = unicodedata.normalize('NFKD', nome).encode('ASCII', 'ignore').decode('ASCII').lower().strip()
    except Exception:
        # Fallback if normalization fails unexpectedly for a string
        base_normalized = nome.lower().strip()

    # Specific handling for Xique Xique to ensure "xique-xique" is the canonical form
    # This allows "Xique Xique", "xiquexique", and "Xique-Xique" to all match
    if base_normalized == 'xique xique' or base_normalized == 'xiquexique':
        return 'xique-xique'
    
    return base_normalized

# Create dataframes for number of accredited service providers
cfc_credenciados = cfc_df_24.groupby('Id_Município CFC').agg({
    'Município CFC': 'first',
    'CNPJ': 'nunique'
}).reset_index().rename(columns={'Id_Município CFC': 'Id_Município', 'Município CFC': 'Município', 'CNPJ': 'Total'})

clinicas_credenciadas = clinicas_df_24.groupby('Id_Município Clínica').agg({
    'Município Clínica': 'first',
    'CNPJ': 'nunique'
}).reset_index().rename(columns={'Id_Município Clínica': 'Id_Município', 'Município Clínica': 'Município', 'CNPJ': 'Total'})

epiv_credenciados = epiv_df_24.groupby('Id_Município').agg({
    'Município': 'first',
    'CNPJ': 'nunique'
}).reset_index().rename(columns={'CNPJ': 'Total'})

ecv_credenciados = ecv_df_24.groupby('Id_Município').agg({
    'Município': 'first',
    'CNPJ': 'nunique'
}).reset_index().rename(columns={'CNPJ': 'Total'})

vistoria_credenciados = vistoria_df_24.groupby('Id_Município').agg({
    'Município': 'first',
    'CNPJ': 'nunique'
}).reset_index().rename(columns={'CNPJ': 'Total'})

patio_credenciados = patio_df_24.groupby('Id_Município').agg({
    'Município': 'first',
    'CNPJ': 'nunique'
}).reset_index().rename(columns={'CNPJ': 'Total'})

# Function to create a comprehensive popup HTML for a municipality
def criar_popup_detalhado(municipio_nome):
    """
    Creates detailed HTML for a comprehensive popup showing all data for a municipality
    """
    # Normalize the municipality name for lookup
    municipio_norm = normaliza_nome(municipio_nome)
    
    # Create HTML structure
    html = f"""<div style='min-width:700px; max-width:1000px; border-radius:4px; box-shadow:0 1px 5px rgba(0,0,0,0.2);'>
        <h3 style='background-color:#007bff; color:white; padding:15px; margin:0; border-radius:4px 4px 0 0;'>{municipio_nome}</h3>
        <div style='padding:15px; max-height:600px; overflow-y:auto;'>"""
    
    # Informações de População (se disponíveis)
    populacao_municipio = frota_grouped.loc[frota_grouped['Município'].apply(normaliza_nome) == municipio_norm, 'População']
    if not populacao_municipio.empty and pd.notna(populacao_municipio.iloc[0]):
        pop_valor = populacao_municipio.iloc[0]
        html += f"""
        <div style='text-align:right; margin-bottom:10px; padding-bottom:10px; border-bottom:1px solid #eee;'>
            <strong style='font-size:1.1em;'>População:</strong> <span style='font-size:1.1em;'>{pop_valor:,.0f}</span>
        </div>
        """
    else:
         # Mesmo se não houver população, normaliza para evitar erros no popup.
        populacao_municipio = pd.Series([None])
    
    # 1. Frota de Veículos
    frota_mun = frota_grouped[frota_grouped['Município'].apply(normaliza_nome) == municipio_norm]
    if not frota_mun.empty:
        total_frota = frota_mun['Total'].iloc[0]
        html += f"""
        <div style='margin-bottom:20px; border:1px solid #e0e0e0; border-radius:4px; padding:10px;'>
            <h4 style='margin-top:0; border-bottom:1px solid #e0e0e0; padding-bottom:8px; color:#007bff;'>
                Frota de Veículos <span style='float:right; font-size:16px;'>Total: {total_frota:,.0f}</span>
            </h4>
            <table style='width:100%; border-collapse:collapse;'>
                <tr style='background-color:#f5f5f5;'>
                    <th style='text-align:left; padding:8px; border:1px solid #ddd;'>Tipo</th>
                    <th style='text-align:right; padding:8px; border:1px solid #ddd;'>Quantidade</th>
                    <th style='text-align:right; padding:8px; border:1px solid #ddd;'>% do Total</th>
                </tr>
        """
        for tipo in ['Automóvel', 'Moto', 'Caminhão', 'Caminhonete', 'Microonibus', 'Onibus', 'Reboque', 'Trator', 'Outros']:
            if tipo in frota_mun.columns and pd.notna(frota_mun[tipo].iloc[0]) and frota_mun[tipo].iloc[0] > 0:
                valor = frota_mun[tipo].iloc[0]
                percentual = (valor / total_frota * 100) if total_frota > 0 else 0
                html += f"""
                <tr>
                    <td style='padding:8px; border:1px solid #ddd;'>{tipo}</td>
                    <td style='text-align:right; padding:8px; border:1px solid #ddd;'>{valor:,.0f}</td>
                    <td style='text-align:right; padding:8px; border:1px solid #ddd;'>{percentual:.1f}%</td>
                </tr>
                """
        html += "</table></div>"
    
    # --- Nova Seção: Resumo de Serviços Disponíveis ---
    html += """
    <div style='margin-bottom:20px; border:1px solid #e0e0e0; border-radius:4px; padding:10px;'>
        <h4 style='margin-top:0; border-bottom:1px solid #e0e0e0; padding-bottom:8px; color:#333333;'>
            Serviços com Dados no Município
        </h4>
        <div style='display:flex; flex-wrap:wrap; gap:20px; padding-top:10px; font-size:0.95em;'>
    """

    # Verificar disponibilidade para cada serviço
    # CFCs
    cfc_mun_check = cfc_grouped[cfc_grouped['Município'].apply(normaliza_nome) == municipio_norm]
    cfcs_no_municipio_check = cfc_df_24[cfc_df_24['Município CFC'].apply(normaliza_nome) == municipio_norm].drop_duplicates('CNPJ')
    tem_dados_cfc = (not cfc_mun_check.empty and cfc_mun_check['Total'].iloc[0] > 0) or (not cfcs_no_municipio_check.empty)
    html += f"""<span>CFCs: <span style='color:{"green" if tem_dados_cfc else "red"};'>{"✔" if tem_dados_cfc else "❌"}</span></span>"""

    # Clínicas
    clinica_mun_check = clinicas_grouped[clinicas_grouped['Município'].apply(normaliza_nome) == municipio_norm]
    clinicas_no_municipio_check = clinicas_df_24[clinicas_df_24['Município Clínica'].apply(normaliza_nome) == municipio_norm].drop_duplicates('CNPJ')
    tem_dados_clinica = (not clinica_mun_check.empty and clinica_mun_check['Total'].iloc[0] > 0) or (not clinicas_no_municipio_check.empty)
    html += f"""<span>Clínicas: <span style='color:{"green" if tem_dados_clinica else "red"};'>{"✔" if tem_dados_clinica else "❌"}</span></span>"""

    # EPIVs
    epiv_mun_check = epiv_grouped[epiv_grouped['Município'].apply(normaliza_nome) == municipio_norm]
    epivs_no_municipio_check = epiv_df_24[epiv_df_24['Município'].apply(normaliza_nome) == municipio_norm].drop_duplicates('CNPJ')
    tem_dados_epiv = (not epiv_mun_check.empty and epiv_mun_check['Total'].iloc[0] > 0) or (not epivs_no_municipio_check.empty)
    html += f"""<span>EPIVs: <span style='color:{"green" if tem_dados_epiv else "red"};'>{"✔" if tem_dados_epiv else "❌"}</span></span>"""

    # ECVs
    ecv_mun_check = ecv_grouped[ecv_grouped['Município'].apply(normaliza_nome) == municipio_norm]
    ecvs_no_municipio_check = ecv_df_24[ecv_df_24['Município'].apply(normaliza_nome) == municipio_norm].drop_duplicates('CNPJ')
    tem_dados_ecv = (not ecv_mun_check.empty and ecv_mun_check['Total'].iloc[0] > 0) or (not ecvs_no_municipio_check.empty)
    html += f"""<span>ECVs: <span style='color:{"green" if tem_dados_ecv else "red"};'>{"✔" if tem_dados_ecv else "❌"}</span></span>"""

    # Vistorias DETRAN
    vistoria_mun_check = vistoria_grouped[vistoria_grouped['Município'].apply(normaliza_nome) == municipio_norm]
    tem_dados_vistoria = (not vistoria_mun_check.empty and vistoria_mun_check['Total'].iloc[0] > 0)
    html += f"""<span>Vistorias DETRAN: <span style='color:{"green" if tem_dados_vistoria else "red"};'>{"✔" if tem_dados_vistoria else "❌"}</span></span>"""

    # Pátios
    patio_mun_check = patio_grouped[patio_grouped['Município'].apply(normaliza_nome) == municipio_norm]
    patios_no_municipio_check = patio_df_24[patio_df_24['Município'].apply(normaliza_nome) == municipio_norm].drop_duplicates('CNPJ')
    tem_dados_patio = (not patio_mun_check.empty and patio_mun_check['Total'].iloc[0] > 0) or (not patios_no_municipio_check.empty)
    html += f"""<span>Pátios: <span style='color:{"green" if tem_dados_patio else "red"};'>{"✔" if tem_dados_patio else "❌"}</span></span>"""

    html += """</div></div>""" # Fechar div de Resumo de Serviços Disponíveis
    
    # 2. CFCs
    cfc_mun = cfc_grouped[cfc_grouped['Município'].apply(normaliza_nome) == municipio_norm]
    cfcs_no_municipio = cfc_df_24[cfc_df_24['Município CFC'].apply(normaliza_nome) == municipio_norm].drop_duplicates('CNPJ')
    
    if not cfc_mun.empty or not cfcs_no_municipio.empty:
        total_cfc = cfc_mun['Total'].iloc[0] if not cfc_mun.empty and pd.notna(cfc_mun['Total'].iloc[0]) else 0
        
        html += f"""
        <div style='margin-bottom:20px; border:1px solid #e0e0e0; border-radius:4px; padding:10px;'>
            <h4 style='margin-top:0; border-bottom:1px solid #e0e0e0; padding-bottom:8px; color:#28a745;'>
                Centros de Formação de Condutores (CFCs) <span style='float:right; font-size:16px;'>Total de Serviços: {total_cfc:,.0f}</span>
            </h4>
        """
        
        if not cfc_mun.empty:
            html += """
            <table style='width:100%; border-collapse:collapse; margin-bottom:15px;'>
                <tr style='background-color:#f5f5f5;'>
                    <th style='text-align:left; padding:8px; border:1px solid #ddd;'>Tipo de Serviço</th>
                    <th style='text-align:right; padding:8px; border:1px solid #ddd;'>Quantidade</th>
                </tr>
            """
            if 'Cursos Teóricos' in cfc_mun.columns and pd.notna(cfc_mun['Cursos Teóricos'].iloc[0]):
                html += f"""
                <tr>
                    <td style='padding:8px; border:1px solid #ddd;'>Cursos Teóricos</td>
                    <td style='text-align:right; padding:8px; border:1px solid #ddd;'>{cfc_mun['Cursos Teóricos'].iloc[0]:,.0f}</td>
                </tr>
                """
            if 'Cursos Práticos' in cfc_mun.columns and pd.notna(cfc_mun['Cursos Práticos'].iloc[0]):
                html += f"""
                <tr>
                    <td style='padding:8px; border:1px solid #ddd;'>Cursos Práticos</td>
                    <td style='text-align:right; padding:8px; border:1px solid #ddd;'>{cfc_mun['Cursos Práticos'].iloc[0]:,.0f}</td>
                </tr>
                """
            html += "</table>"
        
        if not cfcs_no_municipio.empty:
            html += f"""
            <h5 style='margin-top:15px; margin-bottom:8px;'>CFCs no município ({len(cfcs_no_municipio)})</h5>
            <div style='max-height:150px; overflow-y:auto; border:1px solid #ddd; border-radius:4px; padding:10px;'>
                <table style='width:100%; border-collapse:collapse;'>
                    <tr style='background-color:#f5f5f5;'>
                        <th style='text-align:left; padding:8px; border:1px solid #ddd;'>Razão Social</th>
                        <th style='text-align:left; padding:8px; border:1px solid #ddd;'>CNPJ</th>
                        <th style='text-align:right; padding:8px; border:1px solid #ddd;'>Total Serviços (Global)</th>
                    </tr>
            """
            for _, cfc_row in cfcs_no_municipio.iterrows():
                cnpj_atual = cfc_row['CNPJ']
                razao_social_atual = cfc_row['Razão Social']
                total_servicos_df = cfc_total_servicos_global_por_cnpj[cfc_total_servicos_global_por_cnpj['CNPJ'] == cnpj_atual]
                total_servicos_valor = total_servicos_df['Total'].iloc[0] if not total_servicos_df.empty else 0
                html += f"""
                <tr>
                    <td style='padding:8px; border:1px solid #ddd;'>{razao_social_atual}</td>
                    <td style='padding:8px; border:1px solid #ddd;'>{cnpj_atual}</td>
                    <td style='text-align:right; padding:8px; border:1px solid #ddd;'>{total_servicos_valor:,.0f}</td>
                </tr>
                """
            html += "</table></div>"
        html += "</div>"
    
    # 3. Clínicas
    clinica_mun = clinicas_grouped[clinicas_grouped['Município'].apply(normaliza_nome) == municipio_norm]
    clinicas_no_municipio = clinicas_df_24[clinicas_df_24['Município Clínica'].apply(normaliza_nome) == municipio_norm].drop_duplicates('CNPJ')
    
    if not clinica_mun.empty or not clinicas_no_municipio.empty:
        total_clinica = clinica_mun['Total'].iloc[0] if not clinica_mun.empty and pd.notna(clinica_mun['Total'].iloc[0]) else 0
        
        html += f"""
        <div style='margin-bottom:20px; border:1px solid #e0e0e0; border-radius:4px; padding:10px;'>
            <h4 style='margin-top:0; border-bottom:1px solid #e0e0e0; padding-bottom:8px; color:#dc3545;'>
                Clínicas <span style='float:right; font-size:16px;'>Total de Exames: {total_clinica:,.0f}</span>
            </h4>
        """
        
        if not clinica_mun.empty:
            html += """
            <table style='width:100%; border-collapse:collapse; margin-bottom:15px;'>
                <tr style='background-color:#f5f5f5;'>
                    <th style='text-align:left; padding:8px; border:1px solid #ddd;'>Tipo de Exame</th>
                    <th style='text-align:right; padding:8px; border:1px solid #ddd;'>Quantidade</th>
                </tr>
            """
            if 'Exames Médicos' in clinica_mun.columns and pd.notna(clinica_mun['Exames Médicos'].iloc[0]):
                html += f"""
                <tr>
                    <td style='padding:8px; border:1px solid #ddd;'>Exames Médicos</td>
                    <td style='text-align:right; padding:8px; border:1px solid #ddd;'>{clinica_mun['Exames Médicos'].iloc[0]:,.0f}</td>
                </tr>
                """
            if 'Exames Psicológicos' in clinica_mun.columns and pd.notna(clinica_mun['Exames Psicológicos'].iloc[0]):
                html += f"""
                <tr>
                    <td style='padding:8px; border:1px solid #ddd;'>Exames Psicológicos</td>
                    <td style='text-align:right; padding:8px; border:1px solid #ddd;'>{clinica_mun['Exames Psicológicos'].iloc[0]:,.0f}</td>
                </tr>
                """
            html += "</table>"
        
        if not clinicas_no_municipio.empty:
            html += f"""
            <h5 style='margin-top:15px; margin-bottom:8px;'>Clínicas no município ({len(clinicas_no_municipio)})</h5>
            <div style='max-height:150px; overflow-y:auto; border:1px solid #ddd; border-radius:4px; padding:10px;'>
                <table style='width:100%; border-collapse:collapse;'>
                    <tr style='background-color:#f5f5f5;'>
                        <th style='text-align:left; padding:8px; border:1px solid #ddd;'>Razão Social</th>
                        <th style='text-align:left; padding:8px; border:1px solid #ddd;'>CNPJ</th>
                        <th style='text-align:right; padding:8px; border:1px solid #ddd;'>Total Serviços (Global)</th>
                    </tr>
            """
            for _, clinica_row in clinicas_no_municipio.iterrows():
                cnpj_atual = clinica_row['CNPJ']
                razao_social_atual = clinica_row['Razão Social']
                total_servicos_df = clinica_total_servicos_global_por_cnpj[clinica_total_servicos_global_por_cnpj['CNPJ'] == cnpj_atual]
                total_servicos_valor = total_servicos_df['Total'].iloc[0] if not total_servicos_df.empty else 0
                html += f"""
                <tr>
                    <td style='padding:8px; border:1px solid #ddd;'>{razao_social_atual}</td>
                    <td style='padding:8px; border:1px solid #ddd;'>{cnpj_atual}</td>
                    <td style='text-align:right; padding:8px; border:1px solid #ddd;'>{total_servicos_valor:,.0f}</td>
                </tr>
                """
            html += "</table></div>"
        html += "</div>"
    
    # --- Detalhes EPIVs ---
    epiv_mun_detalhe = epiv_grouped[epiv_grouped['Município'].apply(normaliza_nome) == municipio_norm]
    epivs_no_municipio_detalhe = epiv_df_24[epiv_df_24['Município'].apply(normaliza_nome) == municipio_norm].drop_duplicates('CNPJ')

    if not epiv_mun_detalhe.empty or not epivs_no_municipio_detalhe.empty:
        total_epiv = epiv_mun_detalhe['Total'].iloc[0] if not epiv_mun_detalhe.empty and pd.notna(epiv_mun_detalhe['Total'].iloc[0]) else 0
        html += f"""
        <div style='margin-bottom:20px; border:1px solid #e0e0e0; border-radius:4px; padding:10px;'>
            <h4 style='margin-top:0; border-bottom:1px solid #e0e0e0; padding-bottom:8px; color:#fd7e14;'>
                EPIVs (Estampagens) <span style='float:right; font-size:16px;'>Total: {total_epiv:,.0f}</span>
            </h4>
        """
        if not epiv_mun_detalhe.empty and 'Estampagem' in epiv_mun_detalhe.columns and pd.notna(epiv_mun_detalhe['Estampagem'].iloc[0]):
            valor_estampagem = epiv_mun_detalhe['Estampagem'].iloc[0]
            html += f"""
            <table style='width:100%; border-collapse:collapse; margin-bottom:15px;'>
                <tr style='background-color:#f5f5f5;'>
                    <th style='text-align:left; padding:8px; border:1px solid #ddd;'>Tipo de Serviço</th>
                    <th style='text-align:right; padding:8px; border:1px solid #ddd;'>Quantidade</th>
                </tr>
                <tr>
                    <td style='padding:8px; border:1px solid #ddd;'>Estampagem</td>
                    <td style='text-align:right; padding:8px; border:1px solid #ddd;'>{valor_estampagem:,.0f}</td>
                </tr>
            </table>
            """
        if not epivs_no_municipio_detalhe.empty:
            html += f"""
            <h5 style='margin-top:15px; margin-bottom:8px;'>EPIVs no município ({len(epivs_no_municipio_detalhe)})</h5>
            <div style='max-height:150px; overflow-y:auto; border:1px solid #ddd; border-radius:4px; padding:10px;'>
                <table style='width:100%; border-collapse:collapse;'>
                    <tr style='background-color:#f5f5f5;'>
                        <th style='text-align:left; padding:8px; border:1px solid #ddd;'>Razão Social</th>
                        <th style='text-align:left; padding:8px; border:1px solid #ddd;'>CNPJ</th>
                        <th style='text-align:right; padding:8px; border:1px solid #ddd;'>Total Serviços (Global)</th>
                    </tr>
            """
            for _, epiv_row in epivs_no_municipio_detalhe.iterrows():
                cnpj_atual = epiv_row['CNPJ']
                razao_social_atual = epiv_row['Razão Social']
                total_servicos_df = epiv_total_servicos_global_por_cnpj[epiv_total_servicos_global_por_cnpj['CNPJ'] == cnpj_atual]
                total_servicos_valor = total_servicos_df['Total'].iloc[0] if not total_servicos_df.empty else 0
                html += f"""
                <tr>
                    <td style='padding:8px; border:1px solid #ddd;'>{razao_social_atual}</td>
                    <td style='padding:8px; border:1px solid #ddd;'>{cnpj_atual}</td>
                    <td style='text-align:right; padding:8px; border:1px solid #ddd;'>{total_servicos_valor:,.0f}</td>
                </tr>
                """
            html += "</table></div>"
        html += "</div>"

    # --- Detalhes ECVs ---
    ecv_mun_detalhe = ecv_grouped[ecv_grouped['Município'].apply(normaliza_nome) == municipio_norm]
    ecvs_no_municipio_detalhe = ecv_df_24[ecv_df_24['Município'].apply(normaliza_nome) == municipio_norm].drop_duplicates('CNPJ')
    colunas_vistoria_ecv = [
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
        'Outras'
    ]
    if not ecv_mun_detalhe.empty or not ecvs_no_municipio_detalhe.empty:
        total_ecv = ecv_mun_detalhe['Total'].iloc[0] if not ecv_mun_detalhe.empty and pd.notna(ecv_mun_detalhe['Total'].iloc[0]) else 0
        html += f"""
        <div style='margin-bottom:20px; border:1px solid #e0e0e0; border-radius:4px; padding:10px;'>
            <h4 style='margin-top:0; border-bottom:1px solid #e0e0e0; padding-bottom:8px; color:#6f42c1;'>
                ECVs (Vistorias Credenciadas) <span style='float:right; font-size:16px;'>Total: {total_ecv:,.0f}</span>
            </h4>
        """
        if not ecv_mun_detalhe.empty:
            html += """
            <table style='width:100%; border-collapse:collapse; margin-bottom:15px;'>
                <tr style='background-color:#f5f5f5;'>
                    <th style='text-align:left; padding:8px; border:1px solid #ddd;'>Tipo de Vistoria (ECV)</th>
                    <th style='text-align:right; padding:8px; border:1px solid #ddd;'>Quantidade</th>
                </tr>
            """
            for col_vist in colunas_vistoria_ecv:
                if col_vist in ecv_mun_detalhe.columns and pd.notna(ecv_mun_detalhe[col_vist].iloc[0]) and ecv_mun_detalhe[col_vist].iloc[0] > 0:
                    nome_curto = col_vist.replace('Vistoria ', '').replace('Veículo ', '')[:40] + ('...' if len(col_vist.replace('Vistoria ', '').replace('Veículo ', '')) > 40 else '')
                    html += f"""
                    <tr>
                        <td style='padding:8px; border:1px solid #ddd;'>{nome_curto}</td>
                        <td style='text-align:right; padding:8px; border:1px solid #ddd;'>{ecv_mun_detalhe[col_vist].iloc[0]:,.0f}</td>
                    </tr>
                    """
            html += "</table>"
        if not ecvs_no_municipio_detalhe.empty:
            html += f"""
            <h5 style='margin-top:15px; margin-bottom:8px;'>ECVs no município ({len(ecvs_no_municipio_detalhe)})</h5>
            <div style='max-height:150px; overflow-y:auto; border:1px solid #ddd; border-radius:4px; padding:10px;'>
                <table style='width:100%; border-collapse:collapse;'>
                    <tr style='background-color:#f5f5f5;'>
                        <th style='text-align:left; padding:8px; border:1px solid #ddd;'>Razão Social</th>
                        <th style='text-align:left; padding:8px; border:1px solid #ddd;'>CNPJ</th>
                        <th style='text-align:right; padding:8px; border:1px solid #ddd;'>Total Serviços (Global)</th>
                    </tr>
            """
            for _, ecv_row in ecvs_no_municipio_detalhe.iterrows():
                cnpj_atual = ecv_row['CNPJ']
                razao_social_atual = ecv_row['Razão Social']
                total_servicos_df = ecv_total_servicos_global_por_cnpj[ecv_total_servicos_global_por_cnpj['CNPJ'] == cnpj_atual]
                total_servicos_valor = total_servicos_df['Total'].iloc[0] if not total_servicos_df.empty else 0
                html += f"""
                <tr>
                    <td style='padding:8px; border:1px solid #ddd;'>{razao_social_atual}</td>
                    <td style='padding:8px; border:1px solid #ddd;'>{cnpj_atual}</td>
                    <td style='text-align:right; padding:8px; border:1px solid #ddd;'>{total_servicos_valor:,.0f}</td>
                </tr>
                """
            html += "</table></div>"
        html += "</div>"

    # --- Detalhes Vistorias DETRAN ---
    vistoria_mun_detalhe = vistoria_grouped[vistoria_grouped['Município'].apply(normaliza_nome) == municipio_norm]
    # CNPJ/Razão Social para Vistorias DETRAN podem vir do vistoria_df_24 se existirem lá como em ECVs
    vistorias_detran_no_municipio = vistoria_df_24[vistoria_df_24['Município'].apply(normaliza_nome) == municipio_norm].drop_duplicates('CNPJ')
    # Usar mesmas colunas de vistoria que ECV para consistência na apresentação
    colunas_vistoria_detran = colunas_vistoria_ecv 

    if not vistoria_mun_detalhe.empty or (not vistorias_detran_no_municipio.empty and 'CNPJ' in vistorias_detran_no_municipio.columns):
        total_vistoria_detran = vistoria_mun_detalhe['Total'].iloc[0] if not vistoria_mun_detalhe.empty and pd.notna(vistoria_mun_detalhe['Total'].iloc[0]) else 0
        html += f"""
        <div style='margin-bottom:20px; border:1px solid #e0e0e0; border-radius:4px; padding:10px;'>
            <h4 style='margin-top:0; border-bottom:1px solid #e0e0e0; padding-bottom:8px; color:#17a2b8;'>
                Vistorias DETRAN <span style='float:right; font-size:16px;'>Total: {total_vistoria_detran:,.0f}</span>
            </h4>
        """
        if not vistoria_mun_detalhe.empty:
            html += """
            <table style='width:100%; border-collapse:collapse; margin-bottom:15px;'>
                <tr style='background-color:#f5f5f5;'>
                    <th style='text-align:left; padding:8px; border:1px solid #ddd;'>Tipo de Vistoria (DETRAN)</th>
                    <th style='text-align:right; padding:8px; border:1px solid #ddd;'>Quantidade</th>
                </tr>
            """
            for col_vist_d in colunas_vistoria_detran:
                if col_vist_d in vistoria_mun_detalhe.columns and pd.notna(vistoria_mun_detalhe[col_vist_d].iloc[0]) and vistoria_mun_detalhe[col_vist_d].iloc[0] > 0:
                    nome_curto_d = col_vist_d.replace('Vistoria ', '').replace('Veículo ', '')[:40] + ('...' if len(col_vist_d.replace('Vistoria ', '').replace('Veículo ', '')) > 40 else '')
                    html += f"""
                    <tr>
                        <td style='padding:8px; border:1px solid #ddd;'>{nome_curto_d}</td>
                        <td style='text-align:right; padding:8px; border:1px solid #ddd;'>{vistoria_mun_detalhe[col_vist_d].iloc[0]:,.0f}</td>
                    </tr>
                    """
            html += "</table>"
        if not vistorias_detran_no_municipio.empty and 'Razão Social' in vistorias_detran_no_municipio.columns and 'CNPJ' in vistorias_detran_no_municipio.columns:
            html += f"""
            <h5 style='margin-top:15px; margin-bottom:8px;'>Entidades de Vistoria DETRAN no município ({len(vistorias_detran_no_municipio)})</h5>
            <div style='max-height:150px; overflow-y:auto; border:1px solid #ddd; border-radius:4px; padding:10px;'>
                <table style='width:100%; border-collapse:collapse;'>
                    <tr style='background-color:#f5f5f5;'>
                        <th style='text-align:left; padding:8px; border:1px solid #ddd;'>Razão Social</th>
                        <th style='text-align:left; padding:8px; border:1px solid #ddd;'>CNPJ</th>
                        <th style='text-align:right; padding:8px; border:1px solid #ddd;'>Total Serviços (Global)</th>
                    </tr>
            """
            for _, vd_row in vistorias_detran_no_municipio.iterrows():
                cnpj_atual = vd_row['CNPJ']
                razao_social_atual = vd_row['Razão Social']
                # Vistorias DETRAN might not have all CNPJs in vistoria_total_servicos_global_por_cnpj if some are direct DETRAN
                total_servicos_df = vistoria_total_servicos_global_por_cnpj[vistoria_total_servicos_global_por_cnpj['CNPJ'] == cnpj_atual]
                total_servicos_valor = total_servicos_df['Total'].iloc[0] if not total_servicos_df.empty else 0
                html += f"""
                <tr>
                    <td style='padding:8px; border:1px solid #ddd;'>{razao_social_atual}</td>
                    <td style='padding:8px; border:1px solid #ddd;'>{cnpj_atual}</td>
                    <td style='text-align:right; padding:8px; border:1px solid #ddd;'>{total_servicos_valor:,.0f}</td>
                </tr>
                """
            html += "</table></div>"
        elif not vistorias_detran_no_municipio.empty:
             html += "<p style='font-size:0.9em; color:#555;'>Vistorias realizadas diretamente pelo DETRAN ou informações de Razão Social/CNPJ não disponíveis para listagem.</p>"
        html += "</div>"

    # --- Detalhes Pátios ---
    patio_mun_detalhe = patio_grouped[patio_grouped['Município'].apply(normaliza_nome) == municipio_norm]
    patios_no_municipio_detalhe = patio_df_24[patio_df_24['Município'].apply(normaliza_nome) == municipio_norm].drop_duplicates('CNPJ')

    if not patio_mun_detalhe.empty or not patios_no_municipio_detalhe.empty:
        total_patio = patio_mun_detalhe['Total'].iloc[0] if not patio_mun_detalhe.empty and pd.notna(patio_mun_detalhe['Total'].iloc[0]) else 0
        html += f"""
        <div style='margin-bottom:20px; border:1px solid #e0e0e0; border-radius:4px; padding:10px;'>
            <h4 style='margin-top:0; border-bottom:1px solid #e0e0e0; padding-bottom:8px; color:#ffc107; text-shadow: 1px 1px 1px #aaa;'>
                Pátios <span style='float:right; font-size:16px;'>Total Veículos Removidos: {total_patio:,.0f}</span>
            </h4>
        """
        if not patio_mun_detalhe.empty and 'Veículos removidos' in patio_mun_detalhe.columns and pd.notna(patio_mun_detalhe['Veículos removidos'].iloc[0]):
            valor_veiculos_removidos = patio_mun_detalhe['Veículos removidos'].iloc[0]
            html += f"""
            <table style='width:100%; border-collapse:collapse; margin-bottom:15px;'>
                <tr style='background-color:#f5f5f5;'>
                    <th style='text-align:left; padding:8px; border:1px solid #ddd;'>Tipo de Serviço</th>
                    <th style='text-align:right; padding:8px; border:1px solid #ddd;'>Quantidade</th>
                </tr>
                <tr>
                    <td style='padding:8px; border:1px solid #ddd;'>Veículos Removidos</td>
                    <td style='text-align:right; padding:8px; border:1px solid #ddd;'>{valor_veiculos_removidos:,.0f}</td>
                </tr>
            </table>
            """
        if not patios_no_municipio_detalhe.empty:
            html += f"""
            <h5 style='margin-top:15px; margin-bottom:8px;'>Pátios no município ({len(patios_no_municipio_detalhe)})</h5>
            <div style='max-height:150px; overflow-y:auto; border:1px solid #ddd; border-radius:4px; padding:10px;'>
                <table style='width:100%; border-collapse:collapse;'>
                    <tr style='background-color:#f5f5f5;'>
                        <th style='text-align:left; padding:8px; border:1px solid #ddd;'>Razão Social</th>
                        <th style='text-align:left; padding:8px; border:1px solid #ddd;'>CNPJ</th>
                        <th style='text-align:right; padding:8px; border:1px solid #ddd;'>Total Serviços (Global)</th>
                    </tr>
            """
            for _, patio_row in patios_no_municipio_detalhe.iterrows():
                cnpj_atual = patio_row['CNPJ']
                razao_social_atual = patio_row['Razão Social']
                total_servicos_df = patio_total_servicos_global_por_cnpj[patio_total_servicos_global_por_cnpj['CNPJ'] == cnpj_atual]
                total_servicos_valor = total_servicos_df['Total'].iloc[0] if not total_servicos_df.empty else 0
                html += f"""
                <tr>
                    <td style='padding:8px; border:1px solid #ddd;'>{razao_social_atual}</td>
                    <td style='padding:8px; border:1px solid #ddd;'>{cnpj_atual}</td>
                    <td style='text-align:right; padding:8px; border:1px solid #ddd;'>{total_servicos_valor:,.0f}</td>
                </tr>
                """
            html += "</table></div>"
        html += "</div>"

    # REMOVED the old summary table for other services
    # # 4. Outros serviços (EPIVs, ECVs, Vistorias, Pátios) - mostrar resumos
    # ... (old code removed)

    html += "</div></div>" # Fechar div principal do popup
    return html

# Function to create choropleth map based on selected data
def create_choropleth(data_df, title):
    # Garantir tipos corretos
    # df_original = data_df.copy() # Original line, but df_original wasn't used later
    # df_original['Id_Município'] = df_original['Id_Município'].astype(str)

    df = data_df.copy() # This df will be filtered by credenciado and used for info_dict
    df['Id_Município'] = df['Id_Município'].astype(str)

    # Se um credenciado foi selecionado e estamos em uma visualização de quantidade
    municipios_credenciado = get_municipios_por_credenciado_filtro()
    
    if municipios_credenciado:
        # A specific credenciado (by name or derived from CNPJ) is selected.
        # Filter the main choropleth data 'df' to these municipalities.
        # This ensures the choropleth itself only shows data for the selected credenciado's municipalities.
        municipios_para_filtrar_df_norm = [normaliza_nome(m) for m in municipios_credenciado]
        if 'Município' in df.columns:
            df = df[df['Município'].apply(normaliza_nome).isin(municipios_para_filtrar_df_norm)]
        else:
            # Fallback for dataframes that might be structured differently (e.g., using 'Município CFC')
            # Attempt to find a relevant municipality column if 'Município' is not present
            mun_col_found = False
            for col_name in ['Município CFC', 'Município Clínica', 'Nome Município']: # Add other possibilities if needed
                if col_name in df.columns:
                    df = df[df[col_name].apply(normaliza_nome).isin(municipios_para_filtrar_df_norm)]
                    mun_col_found = True
                    break
            if not mun_col_found:
                st.warning(f"Não foi possível filtrar o mapa pelos municípios do credenciado selecionado. Coluna de município não encontrada. Visualização: {visualization}")
    # 'df' is now filtered by credenciado (if any). This 'df' will be used for popups via info_dict.

    # --- Create a separate DataFrame for choropleth layer values and bin calculation ---
    df_for_bins_and_choropleth = df.copy() # Start with credenciado-filtered data
    if 'Total' in df_for_bins_and_choropleth.columns:
        # Filter out non-positive totals for bin calculation and choropleth coloring
        df_for_bins_and_choropleth = df_for_bins_and_choropleth[df_for_bins_and_choropleth['Total'] > 0]
    else:
        st.warning(f"Coluna 'Total' não encontrada para choropleth de '{title}'.")
        df_for_bins_and_choropleth = pd.DataFrame() # Ensure it's empty

    bins = None
    choropleth_can_be_drawn = False

    if not df_for_bins_and_choropleth.empty and \
       'Total' in df_for_bins_and_choropleth.columns and \
       not df_for_bins_and_choropleth['Total'].dropna().empty:

        min_val_float = df_for_bins_and_choropleth['Total'].min()
        max_val_float = df_for_bins_and_choropleth['Total'].max()

        if pd.notna(min_val_float) and pd.notna(max_val_float):
            if min_val_float == max_val_float:
                # Single unique positive value after filters.
                # Let Folium handle with quantile; provide an int for bins.
                # Using a list like [min_val_float, min_val_float + some_small_value] often fails ColorBrewer (needs >=3 bins).
                bins = 5  # Tell Folium to determine 5 quantile classes.
                choropleth_can_be_drawn = True
            elif min_val_float < max_val_float:
                num_desired_classes = 5 # Aim for this many classes if creating a list of bins
                # Linspace over float for better distribution, then convert to unique sorted ints
                raw_bin_points = np.linspace(min_val_float, max_val_float, num_desired_classes + 1)
                calculated_bins_list = sorted(list(set([int(b) for b in raw_bin_points])))

                # ColorBrewer scales (like 'YlOrRd') need a list of at least 3 bin edges, or an integer.
                # If calculated_bins_list is used, len(calculated_bins_list) - 1 is the number of colors.
                # So, len(calculated_bins_list) - 1 >= 3  =>  len(calculated_bins_list) >= 4.
                if len(calculated_bins_list) >= 4:
                    bins = calculated_bins_list
                    choropleth_can_be_drawn = True
                elif len(calculated_bins_list) == 2: # Only 2 unique points, not enough for a list for ColorBrewer.
                    # Fallback to integer bins for Folium to calculate quantiles.
                    bins = 5 # Or 4; an integer value.
                    choropleth_can_be_drawn = True
                else: # Only 1 unique point after int conversion, or other edge case.
                    bins = 5 # Integer for quantiles.
                    choropleth_can_be_drawn = True
            # else: max_val_float < min_val_float (should not happen with .min() and .max())

            if not choropleth_can_be_drawn and pd.notna(min_val_float): # If logic above failed but we have valid min/max
                 st.info(f"Não foi possível definir faixas (bins) de forma ideal para '{title}'. Tentando fallback.")
                 bins = 5 # Fallback to integer bins
                 choropleth_can_be_drawn = True
        else: # min/max are NaN
            st.info(f"Valores 'Total' são NaN ou inválidos para '{title}' após filtros. Não é possível calcular bins.")
    else: # df_for_bins_and_choropleth is empty or 'Total' problematic
        st.info(f"Não há dados com 'Total' positivo para '{title}' após filtros. Camada Choropleth não será desenhada.")

    # Adicionar camada base branca para o fundo do mapa (ALWAYS ADD THIS)
    folium.GeoJson(
        geojson_data,
        style_function=lambda x: {
            'fillColor': 'white',
            'color': '#666',
            'weight': 1,
            'fillOpacity': 1
        }
    ).add_to(m)

    # Preparar dicionário de dados para acesso rápido (uses 'df' which is credenciado-filtered, not Total>0 filtered)
    info_dict = df.set_index('Id_Município').to_dict(orient='index')

    # Função para criar conteúdo detalhado do popup com base no tipo de visualização
    def get_popup_html(feature):
        mun_id = str(feature['properties']['id'])
        municipio_nome = feature['properties']['name']
        info = info_dict.get(mun_id)
        
        # Special handling for Visão Geral
        if visualization == 'Visão Geral':
            return criar_popup_detalhado(municipio_nome)
        
        if not info:
            return f"""<div style='min-width:300px'>
                <h4 style='background-color:#f8f9fa; padding:8px; margin:0; border-radius:4px 4px 0 0; border-bottom:1px solid #dee2e6;'>{municipio_nome}</h4>
                <div style='padding:10px;'><p>Sem dados disponíveis</p></div>
            </div>"""
        
        html = f"""<div style='min-width:450px; max-width:600px; border-radius:4px; box-shadow:0 1px 5px rgba(0,0,0,0.2);'>
            <h4 style='background-color:#f8f9fa; color:#212529; padding:10px; margin:0; border-bottom:1px solid #dee2e6; border-radius:4px 4px 0 0;'>{info['Município']}</h4>
            <div style='padding:15px; max-height:500px; overflow-y:auto;'>"""
        
        # Conteúdo específico com base na visualização selecionada
        if visualization == 'Frota de Veículos':
            html += f"<p style='font-weight:500; margin-bottom:10px;'><b>Total de veículos:</b> {info['Total']:,.0f}</p>"
            html += "<table style='width:100%; border-collapse:collapse; margin-top:10px; border:1px solid #dee2e6;'>"
            html += "<tr style='background-color:#f8f9fa;'><th style='text-align:left; padding:8px; border:1px solid #dee2e6;'>Tipo</th><th style='text-align:right; padding:8px; border:1px solid #dee2e6;'>Quantidade</th></tr>"
            for tipo in ['Automóvel', 'Moto', 'Caminhão', 'Caminhonete', 'Microonibus', 'Onibus', 'Reboque', 'Trator', 'Outros']:
                if tipo in info and info[tipo] > 0:
                    html += f"<tr><td style='padding:8px; border:1px solid #dee2e6;'>{tipo}</td><td style='text-align:right; padding:8px; border:1px solid #dee2e6;'>{info[tipo]:,.0f}</td></tr>"
            html += "</table>"
            
        elif visualization == 'CFCs':
            html += f"<p style='font-weight:500; margin-bottom:10px;'><b>Total de serviços:</b> {info['Total']:,.0f}</p>"
            if 'Cursos Teóricos' in info and 'Cursos Práticos' in info:
                html += "<table style='width:100%; border-collapse:collapse; margin-bottom:15px;'>"
                html += "<tr style='background-color:#f5f5f5;'><th style='text-align:left; padding:8px; border:1px solid #ddd;'>Tipo de Serviço</th><th style='text-align:right; padding:8px; border:1px solid #ddd;'>Quantidade</th></tr>"
                html += f"<tr><td style='padding:8px; border:1px solid #ddd;'>Cursos Teóricos</td><td style='text-align:right; padding:8px; border:1px solid #ddd;'>{info['Cursos Teóricos']:,.0f}</td></tr>"
                html += f"<tr><td style='padding:8px; border:1px solid #ddd;'>Cursos Práticos</td><td style='text-align:right; padding:8px; border:1px solid #ddd;'>{info['Cursos Práticos']:,.0f}</td></tr>"
                html += "</table>"
            
            # Adicionar lista de CFCs com novo estilo de tabela
            municipio_norm = normaliza_nome(info['Município'])
            cfcs_no_municipio = cfc_df_24[cfc_df_24['Município CFC'].apply(normaliza_nome) == municipio_norm].drop_duplicates('CNPJ')
            if not cfcs_no_municipio.empty:
                html += f"<div style='margin-top:15px;'>"
                html += f"<h5 style='margin-top:15px; margin-bottom:8px;'>CFCs no município ({len(cfcs_no_municipio)})</h5>"
                html += "<div style='max-height:150px; overflow-y:auto; border:1px solid #ddd; border-radius:4px; padding:10px;'>"
                html += "<table style='width:100%; border-collapse:collapse;'>"
                html += "<tr style='background-color:#f5f5f5;'>"
                html += "<th style='text-align:left; padding:8px; border:1px solid #ddd;'>Razão Social</th>"
                html += "<th style='text-align:left; padding:8px; border:1px solid #ddd;'>CNPJ</th>"
                html += "<th style='text-align:right; padding:8px; border:1px solid #ddd;'>Total Serviços (Global)</th>"
                html += "</tr>"
                for _, cfc_row in cfcs_no_municipio.iterrows():
                    cnpj_atual = cfc_row['CNPJ']
                    razao_social_atual = cfc_row['Razão Social']
                    total_servicos_df = cfc_total_servicos_global_por_cnpj[cfc_total_servicos_global_por_cnpj['CNPJ'] == cnpj_atual]
                    total_servicos_valor = total_servicos_df['Total'].iloc[0] if not total_servicos_df.empty else 0
                    html += f"<tr>"
                    html += f"<td style='padding:8px; border:1px solid #ddd;'>{razao_social_atual}</td>"
                    html += f"<td style='padding:8px; border:1px solid #ddd;'>{cnpj_atual}</td>"
                    html += f"<td style='text-align:right; padding:8px; border:1px solid #ddd;'>{total_servicos_valor:,.0f}</td>"
                    html += f"</tr>"
                html += "</table></div></div>"
                
        elif visualization == 'Clínicas':
            html += f"<p style='font-weight:500; margin-bottom:10px;'><b>Total de exames:</b> {info['Total']:,.0f}</p>"
            if 'Exames Médicos' in info and 'Exames Psicológicos' in info:
                html += "<table style='width:100%; border-collapse:collapse; margin-bottom:15px;'>"
                html += "<tr style='background-color:#f5f5f5;'><th style='text-align:left; padding:8px; border:1px solid #ddd;'>Tipo de Exame</th><th style='text-align:right; padding:8px; border:1px solid #ddd;'>Quantidade</th></tr>"
                html += f"<tr><td style='padding:8px; border:1px solid #ddd;'>Exames Médicos</td><td style='text-align:right; padding:8px; border:1px solid #ddd;'>{info['Exames Médicos']:,.0f}</td></tr>"
                html += f"<tr><td style='padding:8px; border:1px solid #ddd;'>Exames Psicológicos</td><td style='text-align:right; padding:8px; border:1px solid #ddd;'>{info['Exames Psicológicos']:,.0f}</td></tr>"
                html += "</table>"
            
            # Adicionar lista de Clínicas com novo estilo de tabela
            municipio_norm = normaliza_nome(info['Município'])
            clinicas_no_municipio = clinicas_df_24[clinicas_df_24['Município Clínica'].apply(normaliza_nome) == municipio_norm].drop_duplicates('CNPJ')
            if not clinicas_no_municipio.empty:
                html += f"<div style='margin-top:15px;'>"
                html += f"<h5 style='margin-top:15px; margin-bottom:8px;'>Clínicas no município ({len(clinicas_no_municipio)})</h5>"
                html += "<div style='max-height:150px; overflow-y:auto; border:1px solid #ddd; border-radius:4px; padding:10px;'>"
                html += "<table style='width:100%; border-collapse:collapse;'>"
                html += "<tr style='background-color:#f5f5f5;'>"
                html += "<th style='text-align:left; padding:8px; border:1px solid #ddd;'>Razão Social</th>"
                html += "<th style='text-align:left; padding:8px; border:1px solid #ddd;'>CNPJ</th>"
                html += "<th style='text-align:right; padding:8px; border:1px solid #ddd;'>Total Serviços (Global)</th>"
                html += "</tr>"
                for _, clinica_row in clinicas_no_municipio.iterrows():
                    cnpj_atual = clinica_row['CNPJ']
                    razao_social_atual = clinica_row['Razão Social']
                    total_servicos_df = clinica_total_servicos_global_por_cnpj[clinica_total_servicos_global_por_cnpj['CNPJ'] == cnpj_atual]
                    total_servicos_valor = total_servicos_df['Total'].iloc[0] if not total_servicos_df.empty else 0
                    html += f"<tr>"
                    html += f"<td style='padding:8px; border:1px solid #ddd;'>{razao_social_atual}</td>"
                    html += f"<td style='padding:8px; border:1px solid #ddd;'>{cnpj_atual}</td>"
                    html += f"<td style='text-align:right; padding:8px; border:1px solid #ddd;'>{total_servicos_valor:,.0f}</td>"
                    html += f"</tr>"
                html += "</table></div></div>"
                
        elif visualization == 'EPIVs':
            html += f"<p style='font-weight:500; margin-bottom:10px;'><b>Total de estampagens:</b> {info['Total']:,.0f}</p>"
            # REMOVED: if 'Estampagem' in info:
            # REMOVED:     html += f"<p>Serviços de estampagem: {info['Estampagem']:,.0f}</p>"
            
            # Adicionar lista de EPIVs com estilo de tabela
            municipio_norm = normaliza_nome(info['Município'])
            epivs_no_municipio = epiv_df_24[epiv_df_24['Município'].apply(normaliza_nome) == municipio_norm].drop_duplicates('CNPJ')
            if not epivs_no_municipio.empty:
                html += f"<div style='margin-top:15px;'>"
                html += f"<h5 style='margin-top:15px; margin-bottom:8px;'>EPIVs no município ({len(epivs_no_municipio)})</h5>"
                html += "<div style='max-height:150px; overflow-y:auto; border:1px solid #ddd; border-radius:4px; padding:10px;'>"
                html += "<table style='width:100%; border-collapse:collapse;'>"
                html += "<tr style='background-color:#f5f5f5;'>"
                html += "<th style='text-align:left; padding:8px; border:1px solid #ddd;'>Razão Social</th>"
                html += "<th style='text-align:left; padding:8px; border:1px solid #ddd;'>CNPJ</th>"
                html += "<th style='text-align:right; padding:8px; border:1px solid #ddd;'>Total Serviços (Global)</th>"
                html += "</tr>"
                for _, epiv_row in epivs_no_municipio.iterrows():
                    cnpj_atual = epiv_row['CNPJ']
                    razao_social_atual = epiv_row['Razão Social']
                    total_servicos_df = epiv_total_servicos_global_por_cnpj[epiv_total_servicos_global_por_cnpj['CNPJ'] == cnpj_atual]
                    total_servicos_valor = total_servicos_df['Total'].iloc[0] if not total_servicos_df.empty else 0
                    html += f"<tr>"
                    html += f"<td style='padding:8px; border:1px solid #ddd;'>{razao_social_atual}</td>"
                    html += f"<td style='padding:8px; border:1px solid #ddd;'>{cnpj_atual}</td>"
                    html += f"<td style='text-align:right; padding:8px; border:1px solid #ddd;'>{total_servicos_valor:,.0f}</td>"
                    html += f"</tr>"
                html += "</table></div></div>"
                
        elif visualization in ['ECVs', 'Vistorias DETRAN']:
            html += f"<p style='font-weight:500; margin-bottom:10px;'><b>Total de vistorias:</b> {info['Total']:,.0f}</p>"
            
            # Define the comprehensive list of all ECV/Vistoria service types
            all_ecv_service_types = [
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
                'Outras'
            ]
            
            # Criar tabela com as vistorias e suas quantidades
            html += "<table style='width:100%; border-collapse:collapse; margin-bottom:15px;'>"
            html += "<tr style='background-color:#f5f5f5;'><th style='text-align:left; padding:8px; border:1px solid #ddd;'>Tipo de Vistoria</th><th style='text-align:right; padding:8px; border:1px solid #ddd;'>Quantidade</th></tr>"
            
            for col in all_ecv_service_types: # Iterate over the comprehensive list
                if col in info and pd.notna(info[col]) and info[col] > 0:
                    # Nome simplificado para a tabela
                    nome_curto = col.replace('Vistoria ', '').replace('Veículo ', '')
                    if len(nome_curto) > 40: # Adjusted length for better readability
                        nome_curto = nome_curto[:37] + '...'
                    html += f"<tr><td style='padding:8px; border:1px solid #ddd;'>{nome_curto}</td><td style='text-align:right; padding:8px; border:1px solid #ddd;'>{info[col]:,.0f}</td></tr>"
            html += "</table>"
            
            # Adicionar lista de ECVs ou Vistorias DETRAN com estilo de tabela
            municipio_norm = normaliza_nome(info['Município'])
            entities_df = pd.DataFrame()
            global_totals_df = pd.DataFrame()
            list_title = ""

            if visualization == 'ECVs':
                entities_df = ecv_df_24[ecv_df_24['Município'].apply(normaliza_nome) == municipio_norm].drop_duplicates('CNPJ')
                global_totals_df = ecv_total_servicos_global_por_cnpj
                list_title = f"ECVs no município ({len(entities_df)})"
            elif visualization == 'Vistorias DETRAN': # Vistorias DETRAN might be direct or by credenciados
                # Assuming vistoria_df_24 contains credenciado info similar to ecv_df_24 for this part
                entities_df = vistoria_df_24[vistoria_df_24['Município'].apply(normaliza_nome) == municipio_norm]
                if 'CNPJ' in entities_df.columns: # Only proceed if CNPJ column exists to avoid errors
                    entities_df = entities_df.drop_duplicates('CNPJ')
                else: # If no CNPJ, we can't list by CNPJ, so clear the df
                    entities_df = pd.DataFrame()
                global_totals_df = vistoria_total_servicos_global_por_cnpj
                list_title = f"Entidades de Vistoria DETRAN no município ({len(entities_df)})"

            if not entities_df.empty and 'CNPJ' in entities_df.columns and 'Razão Social' in entities_df.columns:
                html += f"<div style='margin-top:15px;'>"
                html += f"<h5 style='margin-top:15px; margin-bottom:8px;'>{list_title}</h5>"
                html += "<div style='max-height:150px; overflow-y:auto; border:1px solid #ddd; border-radius:4px; padding:10px;'>"
                html += "<table style='width:100%; border-collapse:collapse;'>"
                html += "<tr style='background-color:#f5f5f5;'>"
                html += "<th style='text-align:left; padding:8px; border:1px solid #ddd;'>Razão Social</th>"
                html += "<th style='text-align:left; padding:8px; border:1px solid #ddd;'>CNPJ</th>"
                html += "<th style='text-align:right; padding:8px; border:1px solid #ddd;'>Total Serviços (Global)</th>"
                html += "</tr>"
                for _, entity_row in entities_df.iterrows():
                    cnpj_atual = entity_row['CNPJ']
                    razao_social_atual = entity_row['Razão Social']
                    total_servicos_val = 0
                    if not global_totals_df.empty and 'CNPJ' in global_totals_df.columns and 'Total' in global_totals_df.columns:
                        total_servicos_series = global_totals_df[global_totals_df['CNPJ'] == cnpj_atual]['Total']
                        if not total_servicos_series.empty:
                            total_servicos_val = total_servicos_series.iloc[0]
                    html += f"<tr>"
                    html += f"<td style='padding:8px; border:1px solid #ddd;'>{razao_social_atual}</td>"
                    html += f"<td style='padding:8px; border:1px solid #ddd;'>{cnpj_atual}</td>"
                    html += f"<td style='text-align:right; padding:8px; border:1px solid #ddd;'>{total_servicos_val:,.0f}</td>"
                    html += f"</tr>"
                html += "</table></div></div>"
            elif visualization == 'Vistorias DETRAN' and entities_df.empty:
                 html += "<p style='font-size:0.9em; color:#555; margin-top:10px;'>Vistorias podem ser realizadas diretamente pelo DETRAN ou informações de Razão Social/CNPJ não estão disponíveis para listagem detalhada aqui.</p>"
                    
        elif visualization == 'Pátios':
            html += f"<p style='font-weight:500; margin-bottom:10px;'><b>Total de veículos removidos:</b> {info['Total']:,.0f}</p>"
            # REMOVED: if 'Veículos removidos' in info:
            # REMOVED:     html += f"<p>Serviços de remoção: {info['Veículos removidos']:,.0f}</p>"
            
            # Adicionar lista de Pátios com estilo de tabela
            municipio_norm = normaliza_nome(info['Município'])
            patios_no_municipio = patio_df_24[patio_df_24['Município'].apply(normaliza_nome) == municipio_norm].drop_duplicates('CNPJ')
            if not patios_no_municipio.empty:
                html += f"<div style='margin-top:15px;'>"
                html += f"<h5 style='margin-top:15px; margin-bottom:8px;'>Pátios no município ({len(patios_no_municipio)})</h5>"
                html += "<div style='max-height:150px; overflow-y:auto; border:1px solid #ddd; border-radius:4px; padding:10px;'>"
                html += "<table style='width:100%; border-collapse:collapse;'>"
                html += "<tr style='background-color:#f5f5f5;'>"
                html += "<th style='text-align:left; padding:8px; border:1px solid #ddd;'>Razão Social</th>"
                html += "<th style='text-align:left; padding:8px; border:1px solid #ddd;'>CNPJ</th>"
                html += "<th style='text-align:right; padding:8px; border:1px solid #ddd;'>Total Serviços (Global)</th>"
                html += "</tr>"
                for _, patio_row in patios_no_municipio.iterrows():
                    cnpj_atual = patio_row['CNPJ']
                    razao_social_atual = patio_row['Razão Social']
                    total_servicos_df = patio_total_servicos_global_por_cnpj[patio_total_servicos_global_por_cnpj['CNPJ'] == cnpj_atual]
                    total_servicos_valor = total_servicos_df['Total'].iloc[0] if not total_servicos_df.empty else 0
                    html += f"<tr>"
                    html += f"<td style='padding:8px; border:1px solid #ddd;'>{razao_social_atual}</td>"
                    html += f"<td style='padding:8px; border:1px solid #ddd;'>{cnpj_atual}</td>"
                    html += f"<td style='text-align:right; padding:8px; border:1px solid #ddd;'>{total_servicos_valor:,.0f}</td>"
                    html += f"</tr>"
                html += "</table></div></div>"
                
        # Visualizações de quantidade de credenciados
        elif 'Quantidade de' in visualization:
            tipo_credenciado = visualization.replace('Quantidade de ', '') # e.g., "CFCs", "Clínicas"
            # info['Total'] here comes from the *credenciados dataframes (e.g., cfc_credenciados['Total'] which is count of CNPJs)
            html += f"<p style='font-weight:500; margin-bottom:10px;'><b>Total de {tipo_credenciado}:</b> {info['Total']:,.0f}</p>"
            
            municipio_norm = normaliza_nome(info['Município'])
            
            entities_df = pd.DataFrame()
            global_totals_df = pd.DataFrame()
            municipality_column_name = 'Município' # Default for EPIV, ECV, Vistoria, Pátio
            list_title_prefix = tipo_credenciado

            if tipo_credenciado == 'CFCs':
                entities_df = cfc_df_24[cfc_df_24['Município CFC'].apply(normaliza_nome) == municipio_norm].drop_duplicates('CNPJ')
                global_totals_df = cfc_total_servicos_global_por_cnpj
                municipality_column_name = 'Município CFC' # Specific to cfc_df_24 structure for municipality name
            elif tipo_credenciado == 'Clínicas':
                entities_df = clinicas_df_24[clinicas_df_24['Município Clínica'].apply(normaliza_nome) == municipio_norm].drop_duplicates('CNPJ')
                global_totals_df = clinica_total_servicos_global_por_cnpj
                municipality_column_name = 'Município Clínica' # Specific to clinicas_df_24
            elif tipo_credenciado == 'EPIVs':
                entities_df = epiv_df_24[epiv_df_24['Município'].apply(normaliza_nome) == municipio_norm].drop_duplicates('CNPJ')
                global_totals_df = epiv_total_servicos_global_por_cnpj
            elif tipo_credenciado == 'ECVs':
                entities_df = ecv_df_24[ecv_df_24['Município'].apply(normaliza_nome) == municipio_norm].drop_duplicates('CNPJ')
                global_totals_df = ecv_total_servicos_global_por_cnpj
            elif tipo_credenciado == 'Vistorias DETRAN': # Assuming this means entities performing vistorias
                entities_df = vistoria_df_24[vistoria_df_24['Município'].apply(normaliza_nome) == municipio_norm].drop_duplicates('CNPJ')
                global_totals_df = vistoria_total_servicos_global_por_cnpj
                list_title_prefix = "Entidades de Vistoria DETRAN" # More descriptive title
            elif tipo_credenciado == 'Pátios':
                entities_df = patio_df_24[patio_df_24['Município'].apply(normaliza_nome) == municipio_norm].drop_duplicates('CNPJ')
                global_totals_df = patio_total_servicos_global_por_cnpj

            if not entities_df.empty:
                html += f"<div style='margin-top:15px;'>"
                # Use list_title_prefix for the heading
                html += f"<h5 style='margin-top:15px; margin-bottom:8px;'>{list_title_prefix} no município ({len(entities_df)})</h5>"
                html += "<div style='max-height:150px; overflow-y:auto; border:1px solid #ddd; border-radius:4px; padding:10px;'>"
                html += "<table style='width:100%; border-collapse:collapse;'>"
                html += "<tr style='background-color:#f5f5f5;'>"
                html += "<th style='text-align:left; padding:8px; border:1px solid #ddd;'>Razão Social</th>"
                html += "<th style='text-align:left; padding:8px; border:1px solid #ddd;'>CNPJ</th>"
                html += "<th style='text-align:right; padding:8px; border:1px solid #ddd;'>Total Serviços (Global)</th>"
                html += "</tr>"
                for _, entity_row in entities_df.iterrows():
                    cnpj_atual = entity_row['CNPJ']
                    razao_social_atual = entity_row['Razão Social']
                    
                    total_servicos_val = 0 # Default
                    if not global_totals_df.empty and 'CNPJ' in global_totals_df.columns and 'Total' in global_totals_df.columns:
                        total_servicos_series = global_totals_df[global_totals_df['CNPJ'] == cnpj_atual]['Total']
                        if not total_servicos_series.empty:
                            total_servicos_val = total_servicos_series.iloc[0]
                            
                    html += f"<tr>"
                    html += f"<td style='padding:8px; border:1px solid #ddd;'>{razao_social_atual}</td>"
                    html += f"<td style='padding:8px; border:1px solid #ddd;'>{cnpj_atual}</td>"
                    html += f"<td style='text-align:right; padding:8px; border:1px solid #ddd;'>{total_servicos_val:,.0f}</td>"
                    html += f"</tr>"
                html += "</table></div></div>"
            
        html += "</div></div>"
        return html

    # Choropleth com bins definidos e cor visível (para legenda e coloração)
    # This is now conditional and uses the correct dataframe and robust bins
    if visualization == 'Visão Geral':
        # For Visão Geral, use folium.GeoJson with a style_function for uniform color
        # This avoids ColorBrewer issues when not using bins.
        folium.GeoJson(
            geojson_data,
            name=title,
            style_function=lambda x: {
                'fillColor': '#f0f0f0', # Uniform light grey
                'color': '#666', # Border color
                'weight': 1.2, # Border weight
                'fillOpacity': 0.7
            },
            highlight_function=lambda x: {'weight': 3, 'color': 'blue', 'fillOpacity': 0.8},
            # Tooltip and Popup should be added separately if needed for Visão Geral GeoJson
            # For simplicity, we are relying on the later generic GeoJson layer for popups.
        ).add_to(m)
        # Note: The generic GeoJson layer added later handles tooltips/popups for all views, including Visão Geral.

    if choropleth_can_be_drawn and bins is not None: # Existing logic for other views
        folium.Choropleth(
            geo_data=geojson_data,
            name=title,
            data=df_for_bins_and_choropleth, # Use the dataframe filtered for positive Totals for coloring
            columns=['Id_Município', 'Total'],
            key_on='feature.properties.id',
            nan_fill_color='lightgrey', # For actual NaNs in data if any slip through or for areas not in df_for_bins
            fill_color='YlOrRd',
            fill_opacity=0.7,
            line_opacity=0.8,
            line_weight=1.2,
            legend_name=title,
            bins=bins, # This will be an integer or a list with >=3 elements
            highlight=True
        ).add_to(m)
    # else: The base white layer is already added, so no specific else needed here for map appearance.

    # Adicionar propriedade 'valor' e html_popup ao geojson para uso no tooltip e popup
    # This uses the 'df' (credenciado-filtered) via info_dict for comprehensive popups
    for feature in geojson_data['features']:
        mun_id = str(feature['properties']['id'])
        info = info_dict.get(mun_id)
        if info:
            feature['properties']['valor'] = info['Total']
            # Pré-renderizar o HTML do popup e armazenar como propriedade
            feature['properties']['html_popup'] = get_popup_html(feature)
        else:
            feature['properties']['valor'] = 'Sem dados'
            feature['properties']['html_popup'] = f"""<div style='min-width:300px'>
                <h4 style='background-color:#f8f9fa; padding:8px; margin:0; border-radius:4px 4px 0 0; border-bottom:1px solid #dee2e6;'>{feature['properties']['name']}</h4>
                <div style='padding:10px;'><p>Sem dados disponíveis</p></div>
            </div>"""

    # Tooltip customizado e popup
    popup_max_w = 1000 if visualization == 'Visão Geral' else 600
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
            fields=['name', 'valor'], # Apenas o nome do município e o valor
            aliases=['Município:', title], # Alias correspondente, usando o título da visualização para o valor
            labels=True,
            sticky=True,
            # Style for larger size and better readability - MATCHING REGION MAP
            style=("background-color: white; color: #333; font-family: sans-serif; font-size: 14px; "
                   "border: 1px solid #bbb; border-radius: 3px; padding: 10px; min-width: 220px; " # Adjusted min-width
                   "box-shadow: 2px 2px 5px rgba(0,0,0,0.2);"),
            localize=True,
            parse_html=True,
            max_width=300,
        ),
        popup=folium.GeoJsonPopup(
            fields=['html_popup'],
            aliases=[''],
            labels=False,
            style=("background-color: white; color: #333; font-size: 12px;"),
            parse_html=True,
            max_width=popup_max_w # Use the dynamic value here
        ),
        highlight_function=lambda x: {'weight': 3, 'color': 'blue'},
    ).add_to(m)

    # Adicionar camadas de destaque para os diferentes tipos de seleção
    # 1. Destaque para municípios selecionados diretamente (vermelho)
    if municipios_selecionados_geral:
        # Normalizar nomes selecionados
        municipios_sel_norm = set([normaliza_nome(m) for m in municipios_selecionados_geral])
        # Mapear nome normalizado -> id do GeoJSON
        nome2id_geojson = {normaliza_nome(f['properties']['name']): str(f['properties']['id']) for f in geojson_data['features']}
        # Gerar lista de IDs dos municípios selecionados
        mun_ids = [nome2id_geojson[n] for n in municipios_sel_norm if n in nome2id_geojson]
        if mun_ids:
            folium.GeoJson(
                geojson_data,
                name="Municípios Selecionados (Geral)",
                style_function=lambda x: {
                    'fillColor': 'transparent',
                    'color': 'red',
                    'weight': 3,
                    'fillOpacity': 0
                } if str(x['properties']['id']) in mun_ids else {
                    'fillColor': 'transparent',
                    'color': 'transparent',
                    'weight': 0,
                    'fillOpacity': 0
                },
                interactive=False
            ).add_to(m)

    # 2. Destaque para municípios selecionados via CFC Razão Social (azul)
    if municipios_cfc_razao:
        # Normalizar nomes selecionados
        municipios_sel_norm = set([normaliza_nome(m) for m in municipios_cfc_razao])
        # Mapear nome normalizado -> id do GeoJSON
        nome2id_geojson = {normaliza_nome(f['properties']['name']): str(f['properties']['id']) for f in geojson_data['features']}
        # Gerar lista de IDs dos municípios selecionados
        mun_ids = [nome2id_geojson[n] for n in municipios_sel_norm if n in nome2id_geojson]
        if mun_ids:
            folium.GeoJson(
                geojson_data,
                name="Municípios Selecionados (CFC Razão Social)",
                style_function=lambda x: {
                    'fillColor': 'transparent',
                    'color': 'blue',
                    'weight': 3,
                    'fillOpacity': 0
                } if str(x['properties']['id']) in mun_ids else {
                    'fillColor': 'transparent',
                    'color': 'transparent',
                    'weight': 0,
                    'fillOpacity': 0
                },
                interactive=False
            ).add_to(m)

    # 3. Destaque para municípios selecionados via CFC CNPJ (verde)
    if municipios_cfc_cnpj:
        # Normalizar nomes selecionados
        municipios_sel_norm = set([normaliza_nome(m) for m in municipios_cfc_cnpj])
        # Mapear nome normalizado -> id do GeoJSON
        nome2id_geojson = {normaliza_nome(f['properties']['name']): str(f['properties']['id']) for f in geojson_data['features']}
        # Gerar lista de IDs dos municípios selecionados
        mun_ids = [nome2id_geojson[n] for n in municipios_sel_norm if n in nome2id_geojson]
        if mun_ids:
            folium.GeoJson(
                geojson_data,
                name="Municípios Selecionados (CFC CNPJ)",
                style_function=lambda x: {
                    'fillColor': 'transparent',
                    'color': 'green',
                    'weight': 3,
                    'fillOpacity': 0
                } if str(x['properties']['id']) in mun_ids else {
                    'fillColor': 'transparent',
                    'color': 'transparent',
                    'weight': 0,
                    'fillOpacity': 0
                },
                interactive=False
            ).add_to(m)

    # 4. Destaque para municípios selecionados via Clínica Razão Social (roxo)
    if municipios_clinica_razao:
        # Normalizar nomes selecionados
        municipios_sel_norm = set([normaliza_nome(m) for m in municipios_clinica_razao])
        # Mapear nome normalizado -> id do GeoJSON
        nome2id_geojson = {normaliza_nome(f['properties']['name']): str(f['properties']['id']) for f in geojson_data['features']}
        # Gerar lista de IDs dos municípios selecionados
        mun_ids = [nome2id_geojson[n] for n in municipios_sel_norm if n in nome2id_geojson]
        if mun_ids:
            folium.GeoJson(
                geojson_data,
                name="Municípios Selecionados (Clínica Razão Social)",
                style_function=lambda x: {
                    'fillColor': 'transparent',
                    'color': 'purple',
                    'weight': 3,
                    'fillOpacity': 0
                } if str(x['properties']['id']) in mun_ids else {
                    'fillColor': 'transparent',
                    'color': 'transparent',
                    'weight': 0,
                    'fillOpacity': 0
                },
                interactive=False
            ).add_to(m)

    # 5. Destaque para municípios selecionados via Clínica CNPJ (laranja)
    if municipios_clinica_cnpj:
        # Normalizar nomes selecionados
        municipios_sel_norm = set([normaliza_nome(m) for m in municipios_clinica_cnpj])
        # Mapear nome normalizado -> id do GeoJSON
        nome2id_geojson = {normaliza_nome(f['properties']['name']): str(f['properties']['id']) for f in geojson_data['features']}
        # Gerar lista de IDs dos municípios selecionados
        mun_ids = [nome2id_geojson[n] for n in municipios_sel_norm if n in nome2id_geojson]
        if mun_ids:
            folium.GeoJson(
                geojson_data,
                name="Municípios Selecionados (Clínica CNPJ)",
                style_function=lambda x: {
                    'fillColor': 'transparent',
                    'color': 'orange',
                    'weight': 3,
                    'fillOpacity': 0
                } if str(x['properties']['id']) in mun_ids else {
                    'fillColor': 'transparent',
                    'color': 'transparent',
                    'weight': 0,
                    'fillOpacity': 0
                },
                interactive=False
            ).add_to(m)

# Create visualization based on selection
if tipo_mapa == 'Mapa de Regiões':
    # Criar um dicionário para mapear municípios para regiões
    municipio_para_regiao = {}
    for regiao, municipios in regioes_ba.items():
        for municipio in municipios:
            # Normalizar o nome para garantir correspondência consistente
            municipio_norm = normaliza_nome(municipio)
            municipio_para_regiao[municipio_norm] = regiao
            # Também armazenar a versão original para backup
            municipio_para_regiao[municipio] = regiao

    # Adicionar a coluna de região ao DataFrame
    frota_grouped['Regiao'] = frota_grouped['Município'].apply(
        lambda x: municipio_para_regiao.get(normaliza_nome(x), 
               municipio_para_regiao.get(x.upper(), 'Não classificado'))
    )

    # Special handling for Dias d'Ávila
    dias_avila_mask = frota_grouped['Município'].apply(lambda x: 'DIAS' in x.upper() and ('AVILA' in x.upper() or 'ÁVILA' in x.upper()))
    if dias_avila_mask.any():
        frota_grouped.loc[dias_avila_mask, 'Regiao'] = 'Regiâo Metropolitana de Salvador'

    # Agrupar por região
    regioes_grouped = frota_grouped.groupby('Regiao').agg({
        'Total': 'sum'
    }).reset_index()

    # Criar um mapa de cores para as regiões
    cores_regioes = {
        'Centro-Norte': '#32CD32',  # Verde
        'Centro-Sul': '#FFFF00',  # Amarelo
        'Extremo oeste': '#9370DB',  # Roxo
        'Nordeste': '#8B4513',  # Marrom
        'Regiâo Metropolitana de Salvador': '#1E90FF',  # Azul
        'Sul': '#FFA500',  # Laranja
        'Vale São-Franciscano': '#FF69B4'  # Rosa
    }

    # --- Prepare data for the selected visualization ---
    vis_df = None
    vis_value_col = 'Total'
    vis_label_prefix = 'Valor' # Default label
    vis_data_dict = {}

    # Map visualization selection to the correct dataframe and label
    vis_mapping = {
        'Visão Geral': (populacao_df, 'População'),
        'Frota de Veículos': (frota_grouped, 'Total Veículos'),
        'CFCs': (cfc_grouped, 'Serviços CFCs'),
        'Clínicas': (clinicas_grouped, 'Exames Clínicas'),
        'EPIVs': (epiv_grouped, 'Serviços EPIVs'),
        'ECVs': (ecv_grouped, 'Vistorias ECVs'),
        'Vistorias DETRAN': (vistoria_grouped, 'Vistorias DETRAN'),
        'Pátios': (patio_grouped, 'Veículos Removidos'),
        'Quantidade de CFCs': (cfc_credenciados, 'Qtd. CFCs'),
        'Quantidade de Clínicas': (clinicas_credenciadas, 'Qtd. Clínicas'),
        'Quantidade de EPIVs': (epiv_credenciados, 'Qtd. EPIVs'),
        'Quantidade de ECVs': (ecv_credenciados, 'Qtd. ECVs'),
        'Quantidade de Vistorias DETRAN': (vistoria_credenciados, 'Qtd. Vistorias'), # Assuming same structure
        'Quantidade de Pátios': (patio_credenciados, 'Qtd. Pátios')
    }

    if visualization in vis_mapping:
        vis_df, vis_label_prefix = vis_mapping[visualization]
        
        # Determine the correct column names based on the specific DataFrame
        actual_municipio_column_name = 'Município_POP' if vis_df is populacao_df else 'Município'
        actual_value_column_name = 'Total' # Consistent for all vis_mapping due to prior renaming or structure
        
        # Check if the dataframe and necessary columns exist
        if vis_df is not None and \
           actual_municipio_column_name in vis_df.columns and \
           actual_value_column_name in vis_df.columns:
            
            # Ensure Id_Município is string for potential future use, though we key by name here
            if 'Id_Município' in vis_df.columns:
                 vis_df['Id_Município'] = vis_df['Id_Município'].astype(str)
            
            # Fix Dias d'Ávila in the visualization dataframe using the correct column
            dias_avila_mask = vis_df[actual_municipio_column_name].apply(lambda x: 'DIAS' in str(x).upper() and ('AVILA' in str(x).upper() or 'ÁVILA' in str(x).upper()))
            if dias_avila_mask.any():
                vis_df.loc[dias_avila_mask, actual_municipio_column_name] = "DIAS D'ÁVILA"
            
            # Create dict mapping normalized name to the value, using correct columns
            vis_data_dict = vis_df.set_index(
                vis_df[actual_municipio_column_name].apply(normaliza_nome)
            )[actual_value_column_name].to_dict()
            
            # Also add a special key for Dias d'Ávila to ensure it's found
            dias_davila_data = vis_df[
                vis_df[actual_municipio_column_name].apply(lambda x: 'DIAS' in str(x).upper() and ('AVILA' in str(x).upper() or 'ÁVILA' in str(x).upper()))
            ]
            if not dias_davila_data.empty:
                dias_davila_value = dias_davila_data[actual_value_column_name].iloc[0]
                # Add multiple variations of the name for lookup
                vis_data_dict['dias davila'] = dias_davila_value
                vis_data_dict['dias d avila'] = dias_davila_value
                vis_data_dict["dias d'avila"] = dias_davila_value
        else:
            # Handle cases where the expected columns aren't present or df is None
            st.warning(f"Dados para '{visualization}' não puderam ser carregados corretamente para o tooltip. Verifique as colunas esperadas: '{actual_municipio_column_name}' e '{actual_value_column_name}' no DataFrame correspondente.")

    # --- Add region, color, and custom tooltip HTML to GeoJSON ---
    for feature in geojson_data['features']:
        municipio_nome_geojson = feature['properties']['name']
        municipio_upper = municipio_nome_geojson.upper()
        municipio_norm = normaliza_nome(municipio_nome_geojson)

        # Add region and color
        regiao = None
        
        # Special handling for Dias d'Ávila
        if 'DIAS' in municipio_upper and ('AVILA' in municipio_upper or 'ÁVILA' in municipio_upper):
            regiao = 'Regiâo Metropolitana de Salvador'
        else:
            regiao = municipio_para_regiao.get(municipio_norm, 
                    municipio_para_regiao.get(municipio_upper, 'Não classificado'))
        
        cor = cores_regioes.get(regiao, '#CCCCCC')
        feature['properties']['regiao'] = regiao
        feature['properties']['cor'] = cor

        # Get visualization value with special handling for Dias d'Ávila
        vis_value = 'N/A'
        if 'DIAS' in municipio_upper and ('AVILA' in municipio_upper or 'ÁVILA' in municipio_upper):
            # Try multiple key variants for Dias d'Ávila
            for key in ['dias davila', 'dias d avila', "dias d'avila"]:
                if key in vis_data_dict:
                    vis_value = vis_data_dict[key]
                    break
        else:
            vis_value = vis_data_dict.get(municipio_norm, 'N/A')
        
        # Format numeric values
        if isinstance(vis_value, (int, float, np.number)):
            vis_value_formatted = f"{vis_value:,.0f}"
        else:
            vis_value_formatted = str(vis_value) # Keep as string if N/A or other non-numeric

        # Construct tooltip HTML
        # Get population data safely using the GeoJSON municipality ID
        current_mun_id_geojson = str(feature['properties']['id'])
        pop_data_series = populacao_df.loc[populacao_df['Id_Município'] == current_mun_id_geojson, 'Total']
        
        populacao_display_string = "N/A" # Default if not found or NaN
        if not pop_data_series.empty:
            pop_value = pop_data_series.iloc[0]
            if pd.notna(pop_value):
                populacao_display_string = f"{pop_value:,.0f}"

        tooltip_html = f"""<div style='line-height: 1.5;'>
            <strong>Município:</strong> {municipio_nome_geojson}<br>
            <strong>Região:</strong> {regiao}<br>
            <strong>População:</strong> {populacao_display_string}""" # No <br> here initially

        # Only add the visualization-specific line if the visualization is NOT 'Visão Geral'
        # for the region map, because 'Visão Geral' for region map statistics already implies population,
        # and we have a dedicated population line above.
        if visualization != 'Visão Geral':
            tooltip_html += f"""<br>
            <strong>{vis_label_prefix}:</strong> {vis_value_formatted}"""
        
        tooltip_html += "</div>" # Close the div
        feature['properties']['tooltip_html'] = tooltip_html

    # --- Create GeoJSON layer with regions and custom tooltip ---
    folium.GeoJson(
        geojson_data,
        name='Regiões da Bahia',
        style_function=lambda x: {
            'fillColor': x['properties']['cor'],
            'color': '#666',
            'weight': 1,
            'fillOpacity': 0.7
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['tooltip_html'], # Use the pre-formatted HTML property
            aliases=[''],      # Aliases are ignored when labels=False
            labels=False,      # Do not show the field name ('tooltip_html')
            sticky=True,
            # Style for larger size and better readability
            style=("background-color: white; color: #333; font-family: sans-serif; font-size: 14px; "
                   "border: 1px solid #bbb; border-radius: 3px; padding: 10px; min-width: 220px; " # Adjusted min-width slightly
                   "box-shadow: 2px 2px 5px rgba(0,0,0,0.2);")
        ),
        highlight_function=lambda x: {'weight': 2, 'color':'black', 'fillOpacity': 0.85} # Optional: enhance highlight
    ).add_to(m)

    # Adicionar legenda
    legend_html = '''
    <div style="position: fixed; bottom: 50px; right: 50px; z-index: 1000; background-color: white; 
                padding: 10px; border: 2px solid grey; border-radius: 5px;">
        <p><strong>Regiões da Bahia</strong></p>
    '''
    for regiao, cor in cores_regioes.items():
        legend_html += f'''
        <p>
            <span style="background-color: {cor}; padding: 0 10px; margin-right: 5px;">&nbsp;</span>
            {regiao}
        </p>
        '''
    legend_html += '</div>'
    m.get_root().html.add_child(folium.Element(legend_html))

    # --- Add highlighting for selected municipalities on the Region Map ---
    # For Region Map, highlighting should ALWAYS come from the general multiselect widget's state,
    # independent of any overrides to the `municipios_selecionados` variable by CFC/Clinic filters.
    municipios_para_destaque_na_regiao = st.session_state.get('geral_municipios_multiselect', [])

    if municipios_para_destaque_na_regiao:
        # Normalizar nomes selecionados from the general multiselect for region map highlighting
        municipios_sel_norm_regiao = set([normaliza_nome(m) for m in municipios_para_destaque_na_regiao])
        # Mapear nome normalizado -> id do GeoJSON
        nome2id_geojson_regiao = {normaliza_nome(f['properties']['name']): str(f['properties']['id']) for f in geojson_data['features']}
        # Gerar lista de IDs dos municípios selecionados for region map highlighting
        mun_ids_to_highlight_regiao = [nome2id_geojson_regiao[n] for n in municipios_sel_norm_regiao if n in nome2id_geojson_regiao]

        if mun_ids_to_highlight_regiao:
            folium.GeoJson(
                geojson_data,
                name="Destaque Municípios Selecionados Região",
                style_function=lambda x: {
                    'fillColor': 'transparent',
                    'color': 'red',
                    'weight': 3,
                    'fillOpacity': 0
                } if str(x['properties']['id']) in mun_ids_to_highlight_regiao else {
                    'fillColor': 'transparent',
                    'color': 'transparent',
                    'weight': 0,
                    'fillOpacity': 0
                },
                tooltip=None,
                interactive=False
            ).add_to(m)

    # Adicionar camadas de destaque para os diferentes tipos de seleção no mapa de regiões
    
    # 1. Destaque para municípios selecionados diretamente (vermelho)
    if municipios_selecionados_geral:
        # Normalizar nomes selecionados
        municipios_sel_norm = set([normaliza_nome(m) for m in municipios_selecionados_geral])
        # Mapear nome normalizado -> id do GeoJSON
        nome2id_geojson = {normaliza_nome(f['properties']['name']): str(f['properties']['id']) for f in geojson_data['features']}
        # Gerar lista de IDs dos municípios selecionados
        mun_ids = [nome2id_geojson[n] for n in municipios_sel_norm if n in nome2id_geojson]
        if mun_ids:
            folium.GeoJson(
                geojson_data,
                name="Municípios Selecionados (Geral)",
                style_function=lambda x: {
                    'fillColor': 'transparent',
                    'color': 'red',
                    'weight': 3,
                    'fillOpacity': 0
                } if str(x['properties']['id']) in mun_ids else {
                    'fillColor': 'transparent',
                    'color': 'transparent',
                    'weight': 0,
                    'fillOpacity': 0
                },
                interactive=False
            ).add_to(m)
    
    # 2. Destaque para municípios selecionados via CFC Razão Social (azul)
    if municipios_cfc_razao:
        # Normalizar nomes selecionados
        municipios_sel_norm = set([normaliza_nome(m) for m in municipios_cfc_razao])
        # Mapear nome normalizado -> id do GeoJSON
        nome2id_geojson = {normaliza_nome(f['properties']['name']): str(f['properties']['id']) for f in geojson_data['features']}
        # Gerar lista de IDs dos municípios selecionados
        mun_ids = [nome2id_geojson[n] for n in municipios_sel_norm if n in nome2id_geojson]
        if mun_ids:
            folium.GeoJson(
                geojson_data,
                name="Municípios Selecionados (CFC Razão Social)",
                style_function=lambda x: {
                    'fillColor': 'transparent',
                    'color': 'blue',
                    'weight': 3,
                    'fillOpacity': 0
                } if str(x['properties']['id']) in mun_ids else {
                    'fillColor': 'transparent',
                    'color': 'transparent',
                    'weight': 0,
                    'fillOpacity': 0
                },
                interactive=False
            ).add_to(m)
    
    # 3. Destaque para municípios selecionados via CFC CNPJ (verde)
    if municipios_cfc_cnpj:
        # Normalizar nomes selecionados
        municipios_sel_norm = set([normaliza_nome(m) for m in municipios_cfc_cnpj])
        # Mapear nome normalizado -> id do GeoJSON
        nome2id_geojson = {normaliza_nome(f['properties']['name']): str(f['properties']['id']) for f in geojson_data['features']}
        # Gerar lista de IDs dos municípios selecionados
        mun_ids = [nome2id_geojson[n] for n in municipios_sel_norm if n in nome2id_geojson]
        if mun_ids:
            folium.GeoJson(
                geojson_data,
                name="Municípios Selecionados (CFC CNPJ)",
                style_function=lambda x: {
                    'fillColor': 'transparent',
                    'color': 'green',
                    'weight': 3,
                    'fillOpacity': 0
                } if str(x['properties']['id']) in mun_ids else {
                    'fillColor': 'transparent',
                    'color': 'transparent',
                    'weight': 0,
                    'fillOpacity': 0
                },
                interactive=False
            ).add_to(m)
    
    # 4. Destaque para municípios selecionados via Clínica Razão Social (roxo)
    if municipios_clinica_razao:
        # Normalizar nomes selecionados
        municipios_sel_norm = set([normaliza_nome(m) for m in municipios_clinica_razao])
        # Mapear nome normalizado -> id do GeoJSON
        nome2id_geojson = {normaliza_nome(f['properties']['name']): str(f['properties']['id']) for f in geojson_data['features']}
        # Gerar lista de IDs dos municípios selecionados
        mun_ids = [nome2id_geojson[n] for n in municipios_sel_norm if n in nome2id_geojson]
        if mun_ids:
            folium.GeoJson(
                geojson_data,
                name="Municípios Selecionados (Clínica Razão Social)",
                style_function=lambda x: {
                    'fillColor': 'transparent',
                    'color': 'purple',
                    'weight': 3,
                    'fillOpacity': 0
                } if str(x['properties']['id']) in mun_ids else {
                    'fillColor': 'transparent',
                    'color': 'transparent',
                    'weight': 0,
                    'fillOpacity': 0
                },
                interactive=False
            ).add_to(m)
    
    # 5. Destaque para municípios selecionados via Clínica CNPJ (laranja)
    if municipios_clinica_cnpj:
        # Normalizar nomes selecionados
        municipios_sel_norm = set([normaliza_nome(m) for m in municipios_clinica_cnpj])
        # Mapear nome normalizado -> id do GeoJSON
        nome2id_geojson = {normaliza_nome(f['properties']['name']): str(f['properties']['id']) for f in geojson_data['features']}
        # Gerar lista de IDs dos municípios selecionados
        mun_ids = [nome2id_geojson[n] for n in municipios_sel_norm if n in nome2id_geojson]
        if mun_ids:
            folium.GeoJson(
                geojson_data,
                name="Municípios Selecionados (Clínica CNPJ)",
                style_function=lambda x: {
                    'fillColor': 'transparent',
                    'color': 'orange',
                    'weight': 3,
                    'fillOpacity': 0
                } if str(x['properties']['id']) in mun_ids else {
                    'fillColor': 'transparent',
                    'color': 'transparent',
                    'weight': 0,
                    'fillOpacity': 0
                },
                interactive=False
            ).add_to(m)

elif visualization == 'Visão Geral':
    # For comprehensive view, use frota_grouped as a base for the choropleth
    create_choropleth(populacao_df, 'Total')
elif visualization == 'Frota de Veículos':
    # create_choropleth will use the global `municipios_selecionados` which may have been overridden by CFC/Clinic filters.
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
elif visualization == 'Quantidade de CFCs':
    create_choropleth(cfc_credenciados, 'Número de CFCs Credenciados')
elif visualization == 'Quantidade de Clínicas':
    create_choropleth(clinicas_credenciadas, 'Número de Clínicas Credenciadas')
elif visualization == 'Quantidade de EPIVs':
    create_choropleth(epiv_credenciados, 'Número de EPIVs Credenciados')
elif visualization == 'Quantidade de ECVs':
    create_choropleth(ecv_credenciados, 'Número de ECVs Credenciados')
elif visualization == 'Quantidade de Vistorias DETRAN':
    create_choropleth(vistoria_credenciados, 'Número de Vistorias DETRAN Credenciadas')
elif visualization == 'Quantidade de Pátios':
    create_choropleth(patio_credenciados, 'Número de Pátios Credenciados')

# Display the map
map_html = m._repr_html_()
components.html(map_html, width=iframe_width, height=iframe_height, scrolling=False)

# Show regional statistics AFTER the map if the region map is selected
if tipo_mapa == 'Mapa de Regiões':
    # Adicionar estatísticas das regiões
    st.subheader('Estatísticas por Região')

    # Calcular estatísticas por região
    stats_regioes = frota_grouped.groupby('Regiao').agg({
        'Total': ['sum', 'mean', 'count']
    }).round(2)
    stats_regioes.columns = ['Total de Veículos', 'Média por Município', 'Número de Municípios']
    stats_regioes = stats_regioes.reset_index()

    # Exibir estatísticas em colunas
    cols = st.columns(3)
    for i, regiao in enumerate(stats_regioes['Regiao']):
        col_idx = i % 3
        with cols[col_idx]:
            st.markdown(f"**{regiao}**")
            st.write(f"Total de Veículos: {stats_regioes.loc[i, 'Total de Veículos']:,.0f}")
            st.write(f"Média por Município: {stats_regioes.loc[i, 'Média por Município']:,.0f}")
            st.write(f"Número de Municípios: {stats_regioes.loc[i, 'Número de Municípios']:,.0f}")
            st.write("---")

st.markdown(
    '''
    <style>
    iframe {
        height: 1200px !important;
        width: 100% !important;
        max-width: none !important;
        padding: 20px !important;
        box-sizing: border-box !important;
        overflow: hidden !important;
    }
    .folium-map {
        height: 100% !important;
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }
    .leaflet-container {
        height: 100% !important;
        width: 100% !important;
        overflow: hidden !important;
    }
    .stApp {
        max-width: 100% !important;
        padding: 20px !important;
        overflow-x: hidden !important;
    }
    .block-container {
        max-width: 95% !important;
        margin: 0 auto !important;
        padding-left: 2.5% !important;
        padding-right: 2.5% !important;
        padding-top: 60px !important;
        padding-bottom: 20px !important;
        overflow-x: hidden !important;
    }
    div[data-testid="stVerticalBlock"] {
        padding-left: 10px !important;
        padding-right: 10px !important;
        overflow-x: hidden !important;
    }
    div.stTitle {
        margin-top: 20px !important;
        padding-top: 20px !important;
    }
    h1 {
        padding-top: 20px !important;
        margin-top: 20px !important;
    }
    /* Remover barras de rolagem */
    ::-webkit-scrollbar {
        display: none !important;
    }
    html {
        overflow-x: hidden !important;
        max-width: 100% !important;
        width: 100% !important;
    }
    body {
        overflow-x: hidden !important;
        max-width: 100% !important;
        width: 100% !important;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

# Show additional statistics based on selection
st.subheader('Estatísticas')
if visualization == 'Visão Geral':
    st.subheader('Estatísticas Gerais do Estado da Bahia') # More descriptive title
    
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric('Total de Veículos (Frota)', f"{frota_df_24['Total'].apply(pd.to_numeric, errors='coerce').sum():,.0f}")
        st.metric('Serviços CFCs', f"{cfc_grouped['Total'].apply(pd.to_numeric, errors='coerce').sum():,.0f}")
        st.metric('CFCs Credenciados', f"{cfc_credenciados['Total'].apply(pd.to_numeric, errors='coerce').sum():,.0f}")
        st.metric('População Total (Estado)', f"{populacao_df['Total'].sum():,.0f}")
        
    with col2:
        st.metric('Exames Clínicas', f"{clinicas_grouped['Total'].apply(pd.to_numeric, errors='coerce').sum():,.0f}")
        st.metric('Clínicas Credenciadas', f"{clinicas_credenciadas['Total'].apply(pd.to_numeric, errors='coerce').sum():,.0f}")
        st.metric('Serviços EPIVs', f"{epiv_grouped['Total'].apply(pd.to_numeric, errors='coerce').sum():,.0f}")

    with col3:
        st.metric('EPIVs Credenciadas', f"{epiv_credenciados['Total'].apply(pd.to_numeric, errors='coerce').sum():,.0f}")
        st.metric('Vistorias ECVs', f"{ecv_grouped['Total'].apply(pd.to_numeric, errors='coerce').sum():,.0f}")
        st.metric('ECVs Credenciadas', f"{ecv_credenciados['Total'].apply(pd.to_numeric, errors='coerce').sum():,.0f}")
        
    with col4:
        st.metric('Vistorias DETRAN (Serv.)', f"{vistoria_grouped['Total'].apply(pd.to_numeric, errors='coerce').sum():,.0f}")
        st.metric('Vist. DETRAN Cred.', f"{vistoria_df_24['CNPJ'].nunique():,.0f}") # Correctly count unique CNPJs from the original dataframe
        st.metric('Veículos Removidos (Pátios)', f"{patio_grouped['Total'].apply(pd.to_numeric, errors='coerce').sum():,.0f}")
        st.metric('Pátios Credenciados', f"{patio_credenciados['Total'].apply(pd.to_numeric, errors='coerce').sum():,.0f}")

    # Only show the detailed popup instruction if it's Visão Geral on the Standard Map
    if visualization == 'Visão Geral' and tipo_mapa == 'Mapa Padrão':
        st.info("Clique em um município no mapa para ver todos os dados detalhados no popup.")
elif visualization == 'Frota de Veículos':
    tipos_veiculos = [
        'Automóvel', 'Moto', 'Caminhão', 'Caminhonete', 'Microonibus',
        'Motor-Casa', 'Onibus', 'Reboque', 'Trator', 'Outros'
    ]
    totais = {tipo: frota_df_24[tipo].apply(pd.to_numeric, errors='coerce').sum() for tipo in tipos_veiculos}
    total_geral = frota_df_24['Total'].apply(pd.to_numeric, errors='coerce').sum()
    totais['Total Geral de Veículos'] = total_geral
    # Ordenar por valor decrescente
    tipos_ordenados = sorted(totais.keys(), key=lambda x: totais[x], reverse=True)
    # Exibir em linhas de 4 colunas
    for i in range(0, len(tipos_ordenados), 4):
        cols = st.columns(4)
        for j, tipo in enumerate(tipos_ordenados[i:i+4]):
            with cols[j]:
                if tipo == 'Total Geral de Veículos':
                    st.metric(tipo, f"{totais[tipo]:,.0f}")
                else:
                    st.metric(f'Total de {tipo}', f"{totais[tipo]:,.0f}")
elif visualization in ['Quantidade de CFCs', 'Quantidade de Clínicas', 'Quantidade de EPIVs', 
                      'Quantidade de ECVs', 'Quantidade de Vistorias DETRAN', 'Quantidade de Pátios']:
    selected_df = {
        'Quantidade de CFCs': cfc_credenciados,
        'Quantidade de Clínicas': clinicas_credenciadas,
        'Quantidade de EPIVs': epiv_credenciados,
        'Quantidade de ECVs': ecv_credenciados,
        'Quantidade de Vistorias DETRAN': vistoria_credenciados,
        'Quantidade de Pátios': patio_credenciados
    }[visualization]
    
    total_cred = selected_df['Total'].sum()
    n_mun = len(selected_df)
    n_total_mun = len(frota_grouped)  # usa frota como base de todos os municípios
    media_geral = total_cred / n_total_mun if n_total_mun > 0 else 0
    media_com_cred = selected_df['Total'].mean() if n_mun > 0 else 0
    mediana = selected_df['Total'].median() if n_mun > 0 else 0
    maximo = selected_df['Total'].max() if n_mun > 0 else 0
    minimo = selected_df['Total'].min() if n_mun > 0 else 0
    desvio = selected_df['Total'].std() if n_mun > 0 else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric('Total de Credenciados', f"{total_cred:,.0f}")
        st.metric('Média Geral', f"{media_geral:,.2f}")
    with col2:
        st.metric('Municípios com Credenciados', f"{n_mun:,.0f}")
        st.metric('Média c/ Credenciados', f"{media_com_cred:,.2f}")
    with col3:
        st.metric('Mediana', f"{mediana:,.0f}")
        st.metric('Máx / Mín', f"{maximo:,.0f} / {minimo:,.0f}")
        st.metric('Desvio Padrão', f"{desvio:,.2f}")
else:
    selected_df = {
        'CFCs': cfc_grouped,
        'Clínicas': clinicas_grouped,
        'EPIVs': epiv_grouped,
        'ECVs': ecv_grouped,
        'Vistorias DETRAN': vistoria_grouped,
        'Pátios': patio_grouped
    }[visualization]
    
    total_serv = selected_df['Total'].sum()
    n_mun = len(selected_df)
    n_total_mun = len(frota_grouped)  # usa frota como base de todos os municípios
    media_geral = total_serv / n_total_mun if n_total_mun > 0 else 0
    media_com_serv = selected_df['Total'].mean() if n_mun > 0 else 0
    mediana = selected_df['Total'].median() if n_mun > 0 else 0
    maximo = selected_df['Total'].max() if n_mun > 0 else 0
    minimo = selected_df['Total'].min() if n_mun > 0 else 0
    desvio = selected_df['Total'].std() if n_mun > 0 else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric('Total de Serviços', f"{total_serv:,.0f}")
        st.metric('Média Geral', f"{media_geral:,.2f}")
    with col2:
        st.metric('Municípios com Serviços', f"{n_mun:,.0f}")
        st.metric('Média c/ Serviços', f"{media_com_serv:,.2f}")
    with col3:
        st.metric('Mediana', f"{mediana:,.0f}")
        st.metric('Máx / Mín', f"{maximo:,.0f} / {minimo:,.0f}")
        st.metric('Desvio Padrão', f"{desvio:,.2f}")

# Adicionar legenda para os tipos de destaque quando algum estiver em uso
if (municipios_selecionados_geral or municipios_cfc_razao or municipios_cfc_cnpj or 
    municipios_clinica_razao or municipios_clinica_cnpj):
    
    highlight_legend_html = '''
    <div style="position: fixed; bottom: 50px; left: 50px; z-index: 1000; background-color: white; 
                padding: 10px; border: 2px solid grey; border-radius: 5px;">
        <p><strong>Tipos de Destaque</strong></p>
    '''
    
    if municipios_selecionados_geral:
        highlight_legend_html += f'''
        <p>
            <span style="color: red; font-size: 18px;">—</span>
            Seleção Geral
        </p>
        '''
    
    if municipios_cfc_razao:
        highlight_legend_html += f'''
        <p>
            <span style="color: blue; font-size: 18px;">—</span>
            CFC (Razão Social)
        </p>
        '''
    
    if municipios_cfc_cnpj:
        highlight_legend_html += f'''
        <p>
            <span style="color: green; font-size: 18px;">—</span>
            CFC (CNPJ)
        </p>
        '''
    
    if municipios_clinica_razao:
        highlight_legend_html += f'''
        <p>
            <span style="color: purple; font-size: 18px;">—</span>
            Clínica (Razão Social)
        </p>
        '''
    
    if municipios_clinica_cnpj:
        highlight_legend_html += f'''
        <p>
            <span style="color: orange; font-size: 18px;">—</span>
            Clínica (CNPJ)
        </p>
        '''
    
    highlight_legend_html += '</div>'
    m.get_root().html.add_child(folium.Element(highlight_legend_html))

# Removed the duplicate map display that was here