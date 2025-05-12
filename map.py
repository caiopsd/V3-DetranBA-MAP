"""Script for processing and analyzing DETRAN-BA vehicle fleet and service data."""

import pandas as pd
import openpyxl
import streamlit as st
import geopandas as gpd
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
iframe_height = 1200

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
municipios_selecionados = st.multiselect(
    'Selecione municípios para destacar:',
    municipios,
    default=[]
)

# Create a selectbox for choosing the visualization - MOVED OUTSIDE CONDITIONAL
visualization = st.selectbox(
    'Escolha o tipo de dados para visualizar no mapa e nas estatísticas:',
    [
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

# Adicionar seleção de credenciados para visualizações específicas
credenciado_selecionado = None
if visualization == 'Quantidade de CFCs':
    credenciado_selecionado = st.selectbox(
        'Selecione um CFC credenciado (opcional):',
        ['Todos os CFCs'] + list(credenciados_cfc_df['Nome'].drop_duplicates().sort_values())
    )
    if credenciado_selecionado != 'Todos os CFCs':
        municipios_do_credenciado = credenciados_cfc_df[credenciados_cfc_df['Nome'] == credenciado_selecionado]['Município'].tolist()
        municipios_selecionados = municipios_do_credenciado
elif visualization == 'Quantidade de Clínicas':
    credenciado_selecionado = st.selectbox(
        'Selecione uma Clínica credenciada (opcional):',
        ['Todas as Clínicas'] + list(credenciados_clinica_df['Nome'].drop_duplicates().sort_values())
    )
    if credenciado_selecionado != 'Todas as Clínicas':
        municipios_do_credenciado = credenciados_clinica_df[credenciados_clinica_df['Nome'] == credenciado_selecionado]['Município'].tolist()
        municipios_selecionados = municipios_do_credenciado

# Função para normalizar nomes (remover acentos e deixar minúsculo)
def normaliza_nome(nome):
    if not isinstance(nome, str):
        return ''
    # Tratamento especial para Dias d'Ávila
    if 'DIAS D AVILA' in nome.upper():
        return unicodedata.normalize('NFKD', nome.replace('DIAS D AVILA', "DIAS D'AVILA")).encode('ASCII', 'ignore').decode('ASCII').lower().strip()
    return unicodedata.normalize('NFKD', nome).encode('ASCII', 'ignore').decode('ASCII').lower().strip()

# Function to create choropleth map based on selected data
def create_choropleth(data_df, title):
    # Garantir tipos corretos
    df_original = data_df.copy()
    df_original['Id_Município'] = df_original['Id_Município'].astype(str)

    df = data_df.copy()
    df['Id_Município'] = df['Id_Município'].astype(str)

    # Se um credenciado foi selecionado e estamos em uma visualização de quantidade
    if credenciado_selecionado and credenciado_selecionado not in ['Todos os CFCs', 'Todas as Clínicas']:
        # Normalizar os nomes dos municípios do credenciado
        municipios_credenciado = [normaliza_nome(m) for m in municipios_do_credenciado]
        # Filtrar o dataframe para mostrar apenas os municípios do credenciado
        df = df[df['Município'].apply(normaliza_nome).isin(municipios_credenciado)]

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

    # Função para criar conteúdo detalhado do popup com base no tipo de visualização
    def get_popup_html(feature):
        mun_id = str(feature['properties']['id'])
        municipio_nome = feature['properties']['name']
        info = info_dict.get(mun_id)
        
        if not info:
            return f"""<div style='min-width:300px'>
                <h4 style='background-color:#f8f9fa; padding:8px; margin:0; border-radius:4px 4px 0 0; border-bottom:1px solid #dee2e6;'>{municipio_nome}</h4>
                <div style='padding:10px;'><p>Sem dados disponíveis</p></div>
            </div>"""
        
        html = f"""<div style='min-width:300px; max-width:400px; border-radius:4px; box-shadow:0 1px 5px rgba(0,0,0,0.2);'>
            <h4 style='background-color:#f8f9fa; color:#212529; padding:10px; margin:0; border-bottom:1px solid #dee2e6; border-radius:4px 4px 0 0;'>{info['Município']}</h4>
            <div style='padding:15px; max-height:500px; overflow-y:auto;'>"""
        
        # Conteúdo específico com base na visualização selecionada
        if visualization == 'Frota de Veículos':
            html += f"<p style='font-weight:500; margin-bottom:10px;'><b>Total de veículos:</b> {info['Total']:,.0f}</p>"
            html += "<table style='width:100%; border-collapse:collapse; margin-top:10px; border:1px solid #dee2e6;'>"
            html += "<tr style='background-color:#f8f9fa;'><th style='text-align:left; padding:8px; border:1px solid #dee2e6;'>Tipo</th><th style='text-align:right; padding:8px; border:1px solid #dee2e6;'>Quantidade</th></tr>"
            for tipo in ['Automóvel', 'Moto', 'Caminhão', 'Caminhonete', 'Microonibus', 'Onibus', 'Reboque', 'Outros']:
                if tipo in info and info[tipo] > 0:
                    html += f"<tr><td style='padding:8px; border:1px solid #dee2e6;'>{tipo}</td><td style='text-align:right; padding:8px; border:1px solid #dee2e6;'>{info[tipo]:,.0f}</td></tr>"
            html += "</table>"
            
        elif visualization == 'CFCs':
            html += f"<p style='font-weight:500; margin-bottom:10px;'><b>Total de serviços:</b> {info['Total']:,.0f}</p>"
            if 'Cursos Teóricos' in info and 'Cursos Práticos' in info:
                html += "<table style='width:100%; border-collapse:collapse; margin-top:10px; border:1px solid #dee2e6;'>"
                html += "<tr style='background-color:#f8f9fa;'><th style='text-align:left; padding:8px; border:1px solid #dee2e6;'>Tipo</th><th style='text-align:right; padding:8px; border:1px solid #dee2e6;'>Quantidade</th></tr>"
                html += f"<tr><td style='padding:8px; border:1px solid #dee2e6;'>Cursos Teóricos</td><td style='text-align:right; padding:8px; border:1px solid #dee2e6;'>{info['Cursos Teóricos']:,.0f}</td></tr>"
                html += f"<tr><td style='padding:8px; border:1px solid #dee2e6;'>Cursos Práticos</td><td style='text-align:right; padding:8px; border:1px solid #dee2e6;'>{info['Cursos Práticos']:,.0f}</td></tr>"
                html += "</table>"
            
            # Adicionar lista de CFCs
            municipio_norm = normaliza_nome(info['Município'])
            cfcs_no_municipio = cfc_df_24[cfc_df_24['Município CFC'].apply(normaliza_nome) == municipio_norm].drop_duplicates('CNPJ')
            if not cfcs_no_municipio.empty:
                html += f"<div style='margin-top:15px;'>"
                html += f"<h5 style='margin-bottom:8px; padding-bottom:5px; border-bottom:1px solid #dee2e6;'>CFCs no município ({len(cfcs_no_municipio)})</h5>"
                html += "<div style='max-height:200px; overflow-y:auto; border:1px solid #dee2e6; border-radius:4px; padding:5px;'>"
                html += "<ul style='padding-left:20px; margin:5px 0;'>"
                for _, cfc in cfcs_no_municipio.iterrows():
                    html += f"<li style='padding:3px 0;'>{cfc['Razão Social']}</li>"
                html += "</ul></div></div>"
                
        elif visualization == 'Clínicas':
            html += f"<p style='font-weight:500; margin-bottom:10px;'><b>Total de exames:</b> {info['Total']:,.0f}</p>"
            if 'Exames Médicos' in info and 'Exames Psicológicos' in info:
                html += "<table style='width:100%; border-collapse:collapse; margin-top:10px; border:1px solid #dee2e6;'>"
                html += "<tr style='background-color:#f8f9fa;'><th style='text-align:left; padding:8px; border:1px solid #dee2e6;'>Tipo</th><th style='text-align:right; padding:8px; border:1px solid #dee2e6;'>Quantidade</th></tr>"
                html += f"<tr><td style='padding:8px; border:1px solid #dee2e6;'>Exames Médicos</td><td style='text-align:right; padding:8px; border:1px solid #dee2e6;'>{info['Exames Médicos']:,.0f}</td></tr>"
                html += f"<tr><td style='padding:8px; border:1px solid #dee2e6;'>Exames Psicológicos</td><td style='text-align:right; padding:8px; border:1px solid #dee2e6;'>{info['Exames Psicológicos']:,.0f}</td></tr>"
                html += "</table>"
            
            # Adicionar lista de Clínicas
            municipio_norm = normaliza_nome(info['Município'])
            clinicas_no_municipio = clinicas_df_24[clinicas_df_24['Município Clínica'].apply(normaliza_nome) == municipio_norm].drop_duplicates('CNPJ')
            if not clinicas_no_municipio.empty:
                html += f"<div style='margin-top:15px;'>"
                html += f"<h5 style='margin-bottom:8px; padding-bottom:5px; border-bottom:1px solid #dee2e6;'>Clínicas no município ({len(clinicas_no_municipio)})</h5>"
                html += "<div style='max-height:200px; overflow-y:auto; border:1px solid #dee2e6; border-radius:4px; padding:5px;'>"
                html += "<ul style='padding-left:20px; margin:5px 0;'>"
                for _, clinica in clinicas_no_municipio.iterrows():
                    html += f"<li style='padding:3px 0;'>{clinica['Razão Social']}</li>"
                html += "</ul></div></div>"
                
        elif visualization == 'EPIVs':
            html += f"<p style='font-weight:500; margin-bottom:10px;'><b>Total de estampagens:</b> {info['Total']:,.0f}</p>"
            if 'Estampagem' in info:
                html += f"<p>Serviços de estampagem: {info['Estampagem']:,.0f}</p>"
            
            # Adicionar lista de EPIVs
            municipio_norm = normaliza_nome(info['Município'])
            epivs_no_municipio = epiv_df_24[epiv_df_24['Município'].apply(normaliza_nome) == municipio_norm].drop_duplicates('CNPJ')
            if not epivs_no_municipio.empty:
                html += f"<div style='margin-top:15px;'>"
                html += f"<h5 style='margin-bottom:8px; padding-bottom:5px; border-bottom:1px solid #dee2e6;'>EPIVs no município ({len(epivs_no_municipio)})</h5>"
                html += "<div style='max-height:200px; overflow-y:auto; border:1px solid #dee2e6; border-radius:4px; padding:5px;'>"
                html += "<ul style='padding-left:20px; margin:5px 0;'>"
                for _, epiv in epivs_no_municipio.iterrows():
                    html += f"<li style='padding:3px 0;'>{epiv['Razão Social']}</li>"
                html += "</ul></div></div>"
                
        elif visualization in ['ECVs', 'Vistorias DETRAN']:
            html += f"<p style='font-weight:500; margin-bottom:10px;'><b>Total de vistorias:</b> {info['Total']:,.0f}</p>"
            
            # Selecionar as colunas principais para exibição
            colunas_vistoria = [
                'Vistoria Lacrada Veículo 4 Rodas Até 16 Lugares ou Maior 3,5T',
                'Vistoria Lacrada Veículo 2 ou 3 Rodas',
                'Vistoria RENAVE de Veículo 4 Rodas 16 Lugares ou Até 3,5 Ton',
                'Vistoria RENAVE de Veículos de 2 e 3 Rodas',
                'Vistoria Veículo 2 ou 3 Rodas',
                'Vistoria Veículo 4 Rodas Até 16 Lugares ou Até 3,5 Ton'
            ]
            
            # Criar tabela com as principais vistorias
            html += "<table style='width:100%; border-collapse:collapse; margin-top:10px; border:1px solid #dee2e6;'>"
            html += "<tr style='background-color:#f8f9fa;'><th style='text-align:left; padding:8px; border:1px solid #dee2e6;'>Tipo de Vistoria</th><th style='text-align:right; padding:8px; border:1px solid #dee2e6;'>Quantidade</th></tr>"
            
            for col in colunas_vistoria:
                if col in info and info[col] > 0:
                    # Nome simplificado para a tabela
                    nome_curto = col.replace('Vistoria ', '').replace('Veículo ', '')
                    if len(nome_curto) > 30:
                        nome_curto = nome_curto[:27] + '...'
                    html += f"<tr><td style='padding:8px; border:1px solid #dee2e6;'>{nome_curto}</td><td style='text-align:right; padding:8px; border:1px solid #dee2e6;'>{info[col]:,.0f}</td></tr>"
            html += "</table>"
            
            # Adicionar lista de ECVs ou Vistorias DETRAN
            if visualization == 'ECVs':
                municipio_norm = normaliza_nome(info['Município'])
                ecvs_no_municipio = ecv_df_24[ecv_df_24['Município'].apply(normaliza_nome) == municipio_norm].drop_duplicates('CNPJ')
                if not ecvs_no_municipio.empty:
                    html += f"<div style='margin-top:15px;'>"
                    html += f"<h5 style='margin-bottom:8px; padding-bottom:5px; border-bottom:1px solid #dee2e6;'>ECVs no município ({len(ecvs_no_municipio)})</h5>"
                    html += "<div style='max-height:200px; overflow-y:auto; border:1px solid #dee2e6; border-radius:4px; padding:5px;'>"
                    html += "<ul style='padding-left:20px; margin:5px 0;'>"
                    for _, ecv in ecvs_no_municipio.iterrows():
                        html += f"<li style='padding:3px 0;'>{ecv['Razão Social']}</li>"
                    html += "</ul></div></div>"
                    
        elif visualization == 'Pátios':
            html += f"<p style='font-weight:500; margin-bottom:10px;'><b>Total de veículos removidos:</b> {info['Total']:,.0f}</p>"
            if 'Veículos removidos' in info:
                html += f"<p>Serviços de remoção: {info['Veículos removidos']:,.0f}</p>"
            
            # Adicionar lista de Pátios
            municipio_norm = normaliza_nome(info['Município'])
            patios_no_municipio = patio_df_24[patio_df_24['Município'].apply(normaliza_nome) == municipio_norm].drop_duplicates('CNPJ')
            if not patios_no_municipio.empty:
                html += f"<div style='margin-top:15px;'>"
                html += f"<h5 style='margin-bottom:8px; padding-bottom:5px; border-bottom:1px solid #dee2e6;'>Pátios no município ({len(patios_no_municipio)})</h5>"
                html += "<div style='max-height:200px; overflow-y:auto; border:1px solid #dee2e6; border-radius:4px; padding:5px;'>"
                html += "<ul style='padding-left:20px; margin:5px 0;'>"
                for _, patio in patios_no_municipio.iterrows():
                    html += f"<li style='padding:3px 0;'>{patio['Razão Social']}</li>"
                html += "</ul></div></div>"
                
        # Visualizações de quantidade de credenciados
        elif 'Quantidade de' in visualization:
            tipo_credenciado = visualization.replace('Quantidade de ', '')
            html += f"<p style='font-weight:500; margin-bottom:10px;'><b>Total de {tipo_credenciado}:</b> {info['Total']:,.0f}</p>"
            
            # Adicionar lista de credenciados específica para cada tipo
            if tipo_credenciado == 'CFCs':
                municipio_norm = normaliza_nome(info['Município'])
                cfcs_no_municipio = cfc_df_24[cfc_df_24['Município CFC'].apply(normaliza_nome) == municipio_norm].drop_duplicates('CNPJ')
                if not cfcs_no_municipio.empty:
                    html += f"<div style='margin-top:15px;'>"
                    html += f"<h5 style='margin-bottom:8px; padding-bottom:5px; border-bottom:1px solid #dee2e6;'>Lista de CFCs</h5>"
                    html += "<div style='max-height:300px; overflow-y:auto; border:1px solid #dee2e6; border-radius:4px; padding:5px;'>"
                    html += "<ul style='padding-left:20px; margin:5px 0;'>"
                    for _, cfc in cfcs_no_municipio.iterrows():
                        html += f"<li style='padding:3px 0;'>{cfc['Razão Social']}</li>"
                    html += "</ul></div></div>"
            elif tipo_credenciado == 'Clínicas':
                municipio_norm = normaliza_nome(info['Município'])
                clinicas_no_municipio = clinicas_df_24[clinicas_df_24['Município Clínica'].apply(normaliza_nome) == municipio_norm].drop_duplicates('CNPJ')
                if not clinicas_no_municipio.empty:
                    html += f"<div style='margin-top:15px;'>"
                    html += f"<h5 style='margin-bottom:8px; padding-bottom:5px; border-bottom:1px solid #dee2e6;'>Lista de Clínicas</h5>"
                    html += "<div style='max-height:300px; overflow-y:auto; border:1px solid #dee2e6; border-radius:4px; padding:5px;'>"
                    html += "<ul style='padding-left:20px; margin:5px 0;'>"
                    for _, clinica in clinicas_no_municipio.iterrows():
                        html += f"<li style='padding:3px 0;'>{clinica['Razão Social']}</li>"
                    html += "</ul></div></div>"
            
        html += "</div></div>"
        return html

    # Choropleth com bins definidos e cor visível (para legenda e coloração)
    folium.Choropleth(
        geo_data=geojson_data,
        name=title,
        data=df,
        columns=['Id_Município', 'Total'],
        key_on='feature.properties.id',
        nan_fill_color='black',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.8,
        line_weight=1.2,
        legend_name=title,
        bins=bins,
        highlight=True
    ).add_to(m)

    # Adicionar propriedade 'valor' e html_popup ao geojson para uso no tooltip e popup
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
            # Style for larger size and better readability - MATCHING REGION MAP
            style=("background-color: white; color: #333; font-family: sans-serif; font-size: 14px; "
                   "border: 1px solid #bbb; border-radius: 3px; padding: 10px; min-width: 200px; " # Adjusted min-width slightly
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
            max_width=350
        ),
        highlight_function=lambda x: {'weight': 3, 'color': 'blue'},
    ).add_to(m)

    # Adicionar destaque para os municípios selecionados (apenas borda, sem tooltip)
    if municipios_selecionados:
        # Normalizar nomes selecionados
        municipios_sel_norm = set([normaliza_nome(m) for m in municipios_selecionados])
        # Mapear nome normalizado -> id do GeoJSON
        nome2id_geojson = {normaliza_nome(f['properties']['name']): str(f['properties']['id']) for f in geojson_data['features']}
        # Gerar lista de IDs dos municípios selecionados
        mun_ids = [nome2id_geojson[n] for n in municipios_sel_norm if n in nome2id_geojson]
        if mun_ids:
            folium.GeoJson(
                geojson_data,
                name="Municípios Selecionados",
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
                # Não adicionar tooltip aqui!
                highlight_function=lambda x: (
                    {'weight': 4, 'color': 'red'}
                    if str(x['properties']['id']) in mun_ids
                    else {'weight': 0, 'color': 'transparent'}
                ),
                interactive=False
            ).add_to(m)

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

# Create visualization based on selection
if tipo_mapa == 'Mapa de Regiões':
    # Criar um dicionário para mapear municípios para regiões
    municipio_para_regiao = {}
    for regiao, municipios in regioes_ba.items():
        for municipio in municipios:
            municipio_para_regiao[municipio] = regiao

    # Adicionar a coluna de região ao DataFrame
    frota_grouped['Regiao'] = frota_grouped['Município'].apply(lambda x: municipio_para_regiao.get(x.upper(), 'Não classificado'))

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
        if vis_df is not None and 'Município' in vis_df.columns and vis_value_col in vis_df.columns:
            # Ensure Id_Município is string for potential future use, though we key by name here
            vis_df['Id_Município'] = vis_df['Id_Município'].astype(str)
             # Create dict mapping normalized name to the value
            vis_data_dict = vis_df.set_index(vis_df['Município'].apply(normaliza_nome))[vis_value_col].to_dict()
        else:
             # Handle cases where the expected columns aren't present or df is None
             st.warning(f"Dados para '{visualization}' não puderam ser carregados corretamente para o tooltip.")

    # --- Add region, color, and custom tooltip HTML to GeoJSON ---
    for feature in geojson_data['features']:
        municipio_nome_geojson = feature['properties']['name']
        municipio_upper = municipio_nome_geojson.upper()
        municipio_norm = normaliza_nome(municipio_nome_geojson)

        # Add region and color
        regiao = municipio_para_regiao.get(municipio_upper, 'Não classificado')
        cor = cores_regioes.get(regiao, '#CCCCCC')
        feature['properties']['regiao'] = regiao
        feature['properties']['cor'] = cor

        # Get visualization value
        vis_value = vis_data_dict.get(municipio_norm, 'N/A')
        # Format numeric values
        if isinstance(vis_value, (int, float, np.number)):
             vis_value_formatted = f"{vis_value:,.0f}"
        else:
             vis_value_formatted = str(vis_value) # Keep as string if N/A or other non-numeric

        # Construct tooltip HTML
        tooltip_html = f"""<div style='line-height: 1.5;'>
            <strong>Município:</strong> {municipio_nome_geojson}<br>
            <strong>Região:</strong> {regiao}<br>
            <strong>{vis_label_prefix}:</strong> {vis_value_formatted}
        </div>"""
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
                   "border: 1px solid #bbb; border-radius: 3px; padding: 10px; min-width: 220px; "
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

elif visualization == 'Frota de Veículos':
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
if visualization == 'Frota de Veículos':
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