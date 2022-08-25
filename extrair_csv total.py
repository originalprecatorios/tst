import pandas as pd
from pymongo import MongoClient
import locale
from bd.class_mongo import Mongo
from decouple import config
from regex import I


def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://original_user:original2022!@192.168.0.30:27017/monitora?authSource=original'
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)
    return conn[db]


def read_mongo(db, collection, query={}, host='192.168.0.30', port=27017, username='original_user', password='original2022!', no_id=True, instancia=''):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)

    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query)
    #db.trt2_2_grau.find({ 'numero_processo': { '$nin': ["1001904-35.2016.5.02.0442", "1001829-34.2017.5.02.0709" ] } })

    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor))

    # Delete the _id
    if no_id and '_id' in df:
        del df['_id']

    return df

def movimento(df,instancia):
    arquivado = False
    palavras = [
    'Remetido para o Tribunal Regional do Trabalho',
    'Remetido para o Tribunal Superior do Trabalho',
    'Arquivo definitivamente',
    'Enviado para Arquivo',
    ]

    palavras_chave = [
    'Remetido',
    'Remetido',
    'definitivamente',
    'Enviado',
    ]

    palavras_segundarias = [
    'Tribunal Regional',
    'Tribunal Superior',
    'Arquivo',
    'Arquivados'
    ]

    for i in df.index:
        movi = df['movimentacao'][i]
        try:
            for m in range(0,len(movi)):
                for p in palavras_chave:
                    if df['movimentacao'][i][m]['descricao'].find(p) >= 0:

                        for p in palavras_segundarias:
                            if df['movimentacao'][i][m]['descricao'].find(p) >= 0:
                                df = df.drop(i)
                                arquivado = True
                                break

                if arquivado is True:
                    arquivado = False
                    break        
                
        except:
            continue
    
    
    df['movimento_data'] = ''
    for i in df.index:
        if df['movimentacao'][i][0]['descricao'].find(' em ') >= 0 and df['movimentacao'][i][0]['descricao'].find('/')>= 0:
            if df['movimentacao'][i][0]['descricao'].split(' em ')[1][:1].isnumeric():
                df['movimentacao'][i][0]['descricao'] = df['movimentacao'][i][0]['descricao'].split(' em ')[0]
        try:

            if df['movimentacao'][i][0]['data'].find('/') >= 0:
                df['movimento_data'][i] = df['movimentacao'][i][0]['data']
            else:
                dia = df['movimentacao'][i][0]['data'][8:10]
                mes = df['movimentacao'][i][0]['data'][5:7]
                ano = df['movimentacao'][i][0]['data'][:4]
                df['movimento_data'][i] = dia+'/'+mes+'/'+ano
            
            desc = df['movimentacao'][i][0]['descricao']
            df['movimentacao'][i] = desc
        except:
            continue
    return df


if __name__ == '__main__':
    mongo = Mongo(config('MONGO_USER_PROD'), config('MONGO_PASS_PROD'), config('MONGO_HOST_PROD'), config('MONGO_PORT_PROD'), config('MONGO_DB_PROD'), config('AMBIENTE_PROD'))
    mongo._getcoll('contas')
    filiais = mongo.returnQuery()
    fil = []
    list_process = []
    for filial in filiais:
        fil.append(filial)
    
    for f in fil:
        try:
            search = {'cnpj': f['cnpj_matriz']}
            df1 = read_mongo('monitora', 'tst', search, '192.168.0.30', 27017)
            df1 = df1.drop(columns=['data_captura'])
            df1 = movimento(df1,'1')
            df1 = df1[['numero_processo',  'cnpj', 'data_distribuicao', 'orgao_julgador', 'relator', 'recorrente', 'recorrido', 'movimentacao', 'movimento_data', 'site']]
            df1 = df1.rename(columns={'numero_processo': 'Número do Processo',
            'data_distribuicao': 'Data da Distribuição',
            'orgao_julgador': 'Orgão Juduciário',
            'relator': 'Relator',
            'cnpj': 'CNPJ',
            'recorrente': 'Recorrente',
            'recorrido': 'Recorrido',
            'movimentacao': 'Última Movimentação',
            'movimento_data': 'Data do Última Movimentação',
            'site': 'Site',
            })
            df1.to_excel("total TST_{}.xlsx".format(f['cnpj_matriz'].replace('.','').replace('/','').replace('-','')),sheet_name='tst', index=False)
        except:
            continue