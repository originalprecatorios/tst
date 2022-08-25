
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import math
import regex as re
from selenium_class.tribunal import Trabalhista

class Tst:
    def __init__(self,pData,pBd, pError,pStatus):
        self._data = pData
        self._bdMongo = pBd
        self._bdMongo._getcoll('tst')
        self._error = pError
        self._error._getcoll('error')
        self._status = pStatus
        self._status._getcoll('notificacoes')
    
    def get_process(self):
        url = "https://consultaprocessual.tst.jus.br/consultaProcessual/empregadorForm.do?nomeParte={}&stCheckBox=on&consulta=Consultar".format(self._data['name'].replace(' ','+').replace('Ç','%C3%87'))

        payload={}
        headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Cookie': 'JSESSIONID=gt_yY93hBC0kPaDfljCEC1E0nVyqlSeCBc2oPxc5.consultaprocessual-17-6rg6h; GUEST_LANGUAGE_ID=pt_BR; _ga=GA1.3.2142184665.1658435346; _gid=GA1.3.1469203059.1658435346; f263b1cd9862a48e18557620e69f984e=90c4f54de12643f33a044d6671209292; INSTANCIA=consulta-processual; JSESSIONID=dx-tz2eNfYUPLJuAGj2tnvbplpAaktM7PKGFlky6.consultaprocessual-17-6rg6h; GUEST_LANGUAGE_ID=pt_BR',
        'Referer': 'https://consultaprocessual.tst.jus.br/consultaProcessual/consultaTstNumUnica.do',
        'Sec-Fetch-Dest': 'iframe',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"'
        }

        response = requests.request("GET", url, headers=headers, data=payload, timeout=30)

        if response.text.find('Não foi encontrado nenhum processo dessa parte') >= 0 or response.text.find('504 Gateway Time-out') >= 0:
            return None
        else:
            soup = BeautifulSoup(response.text, 'html.parser')
            pag = int(soup.find_all('span', class_='pagebanner')[0].text.split(' ')[0])
            paginas = math.ceil(pag/20)
            dados = soup.find_all('table', id='processo')[0].text.split('Processo Número Único: \n')
            self.list_process = []
            for p in range(0,paginas):
                if dados is not None:
                    for dado in range(1,len(dados)):
                        try:
                            self.list_process.append(dados[dado].split(' - ')[1].split('\n')[0])
                        except:
                            continue
                    if p+1 != paginas:
                        dados = self.new_page(p+2)
            return self.list_process

    def new_page(self,pagina):
        url = "https://consultaprocessual.tst.jus.br/consultaProcessual/empregadorForm.do?stCheckBox=on&nomeParte={}&consultar=1&consulta=Consultar&d-4028298-p={}".format(self._data['name'].replace(' ','+').replace('Ç','%C3%87'),pagina)

        payload={}
        headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': 'https://consultaprocessual.tst.jus.br/consultaProcessual/empregadorForm.do?nomeParte=EMPRESA+DE+TRANSPORTES+PAJU%C3%87ARA+LTDA.&stCheckBox=on&consulta=Consultar',
        'Cookie': 'JSESSIONID=gt_yY93hBC0kPaDfljCEC1E0nVyqlSeCBc2oPxc5.consultaprocessual-17-6rg6h; GUEST_LANGUAGE_ID=pt_BR; _ga=GA1.3.2142184665.1658435346; _gid=GA1.3.1469203059.1658435346; f263b1cd9862a48e18557620e69f984e=90c4f54de12643f33a044d6671209292; INSTANCIA=consulta-processual; JSESSIONID=dx-tz2eNfYUPLJuAGj2tnvbplpAaktM7PKGFlky6.consultaprocessual-17-6rg6h; GUEST_LANGUAGE_ID=pt_BR',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'iframe',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1'
        }

        response = requests.request("GET", url, headers=headers, data=payload,timeout=30)
        if response.text.find('Não foi encontrado nenhum processo dessa parte') >= 0 or response.text.find('504 Gateway Time-out') >= 0:
            return None
        else:
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.find_all('table', id='processo')[0].text.split('Processo Número Único: \n')
    
    def consulta(self,pProcess):
        self._processo = pProcess.replace('-','').replace('.','')
        self.processo = pProcess
        try:

            url = f"https://consultaprocessual.tst.jus.br/consultaProcessual/consultaTstNumUnica.do?consulta=Consultar&conscsjt=&numeroTst={self.processo.split('-')[0]}&digitoTst={self.processo.split('-')[1].split('.')[0]}&anoTst={self.processo.split('.')[1].split('.')[0]}&orgaoTst={self.processo.split('.')[2].split('.')[0]}&tribunalTst={self.processo.split('.')[3].split('.')[0]}&varaTst={self.processo.split('.')[4].split('.')[0]}&submit=Consultar"

            response = requests.get(url,timeout=30)

            self._soup = BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            err = {'data':str(datetime.today()).split(' ')[0].replace('-',''),
                    'tipo_captura': 'numero do processo',
                    'dado_utilizado': self._processo,
                    'sistema': 'tst',
                    'erro': e.msg,
                    'funcao' : 'erro na função consulta',
            }
            self._error.addData(err)
            return

    def save_process(self):
        try:
            if self._soup.text.find('Por favor, digite os números do áudio:') >= 0:
                t = Trabalhista(self._bdMongo,self._data['cnpj_matriz'],self._data['name'], self._error,self._status,self.processo)
                self.consulta(self.processo)
                self.save_process()
            else:
                self.movimento()
                recorrente = self.recorrent()
                recorrido = self.recorrido()

                if recorrente is None and recorrido is None:
                    recorrente = 'inexistente'
                    recorrido = 'inexistente'
                try:
                    orgao = self._soup.text.split('Órgão Judicante:')[1].split('\n')[0].strip()
                    relator = self._soup.text.split('Relator:')[1].split('\n')[0].strip() if self._soup.text.find('Relator:') >= 0 else self._soup.text.split('Relatora:')[1].split('\n')[0].strip()
                except:
                    orgao = 'inexistente'
                    relator = 'inexistente'
                    
                proc = {
                    'cnpj': self._data['cnpj_matriz'],
                    'numero_processo' : self.processo,
                    'orgao_julgador': orgao,
                    'data_distribuicao': self._distribuicao,
                    'relator': relator,
                    'recorrente': recorrente,
                    'recorrido': recorrido,
                    'movimentacao': self._movimentacao,
                    'data_captura': str(datetime.today()).split(' ')[0].replace('-',''),
                    'site': 'https://www.tst.jus.br/'
                }
                
                self._bdMongo._getcoll('tst')
                modifica = {'$set': proc}
                busca = {'numero_processo':self.processo}
                retorna_dados = self._verifica_dados(self.processo)
                if retorna_dados is None:
                    self._bdMongo.addData(proc)
                    retorna_dados = self._verifica_dados(self.processo)
                    self._grau = '0'
                    new = {
                        'tipo': 'tst',
                        'grau' : self._grau,
                        'processo': self.processo,
                        'id_processo': str(self._inf['_id']),
                        'cnpj' : self._data['cnpj_matriz'],
                        'cnpj_base': self._data['cnpj_base'],
                        'data_captura': str(datetime.today()).split(' ')[0].replace('-',''),
                        'created_at': datetime.today(),
                        'read' : False,
                        'ocorrencias': ['Novo processo capturado']
                        }
                    
                    self._status.addData(new)
                else:
                    self._bdMongo.updateOne_Query(busca, modifica)
                
                print('Dados Salvo no banco numero_processo:{} tst'.format(self._processo))
        
        except Exception as e:
            err = {'data':str(datetime.today()).split(' ')[0].replace('-',''),
                    'tipo_captura': 'numero do processo',
                    'dado_utilizado': self._processo,
                    'sistema': 'tst',
                    'funcao' : 'erro na função save_process',
            }
            self._error.addData(err)
            return
        
    def movimento(self):
        self._movimentacao = []
        self._dic = {}

        for movi in range(0,len(self._soup.find_all("tr", class_="historicoProcesso"))):
            self._dic['data'] = self._soup.find_all("tr", class_="historicoProcesso")[movi].find_all("td", class_="historicoProcesso")[0].text.replace('\n','')
            self._dic['descricao'] =  self._soup.find_all("tr", class_="historicoProcesso")[movi].find_all("td", class_="historicoProcesso")[1].text.replace('\n','')
            self._movimentacao.append(self._dic)
            self._dic = {}
        self._distribuicao = self._soup.find_all("tr", class_="historicoProcesso")[-1].find_all("td", class_="historicoProcesso")[0].text.replace('\n','')
    
    def _verifica_dados(self,pNum):
            arr = {'numero_processo':pNum, 'cnpj': self._data['cnpj_matriz']}
            dados = self._bdMongo.returnBusca(arr)
            for dado in dados:
                self._inf = dado
                return True

    def quant_string(self,text,substring):
        total_occurrences = text.count(substring)

        return total_occurrences
    
    def recorrent(self):
        qtd = self.quant_string(self._soup.text,'Agravante(s) e Recorrente(s):')
        if  qtd == 1:
            return self._soup.text.split('Agravante(s) e Recorrente(s):')[1].split('\n')[1].strip()
        elif qtd > 1:
            return self._soup.text.split('Agravante(s) e Recorrente(s):')[1].split('\n')[1].strip()+' E OUTROS'
        
        qtd = self.quant_string(self._soup.text,'Agravante(s):')
        if qtd >= 1:
            return self._soup.text.split('Agravante(s):')[1].split('\n')[1].strip()
        elif qtd > 1:
            return self._soup.text.split('Agravante(s):')[1].split('\n')[1].strip()+' E OUTROS'
        
        qtd = self.quant_string(self._soup.text,'Embargante:')
        if qtd == 1:
            return self._soup.text.split('Embargante:')[1].split('\n')[1].strip()
        elif qtd > 1:
            return self._soup.text.split('Embargante:')[1].split('\n')[1].strip()+' E OUTROS'
        
        qtd = self.quant_string(self._soup.text,'Recorrente(s):')
        if qtd == 1:
            return self._soup.text.split('Recorrente(s):')[1].split('\n')[1].strip()
        elif qtd > 1:
            return self._soup.text.split('Recorrente(s):')[1].split('\n')[1].strip()+' E OUTROS'
        
        qtd = self.quant_string(self._soup.text,'Agravante(s) e Agravado(s):')
        if qtd == 1:
            return self._soup.text.split('Agravante(s) e Agravado(s):')[1].split('\n')[1].strip()
        elif qtd > 1:
            return self._soup.text.split('Agravante(s) e Agravado(s):')[1].split('\n')[1].strip()+' E OUTROS'
        
        qtd = self.quant_string(self._soup.text,'Agravante(s) e Agravado (s): \n')
        if qtd == 1:
            return self._soup.text.split('Agravante(s) e Agravado (s): \n')[1].split('\n')[0].strip()
        elif qtd > 1:
            return self._soup.text.split('Agravante(s) e Agravado (s): \n')[1].split('\n')[0].strip()+' E OUTROS'

            
    def recorrido(self):
        qtd = self.quant_string(self._soup.text,'Agravado(s) e Recorrido(s):')
        if  qtd == 1:
            return self._soup.text.split('Agravado(s) e Recorrido(s):')[1].split('\n')[1].strip()
        elif qtd > 1:
            return self._data['name']+' E OUTROS'
            #return self._soup.text.split('Agravado(s) e Recorrido(s):')[1].split('\n')[1].strip()+' E OUTROS'
        
        qtd = self.quant_string(self._soup.text,'Agravado (s): \n')
        if qtd == 1:
            return self._soup.text.split('Agravado (s): \n')[1].split('\n')[1].strip()
        elif qtd > 1:
            return self._data['name']+' E OUTROS'

        qtd = self.quant_string(self._soup.text,'Agravado(s):')
        if qtd == 1:
            return self._soup.text.split('Agravado(s):')[1].split('\n')[1].strip()
        elif qtd > 1:
            return self._data['name']+' E OUTROS'
            #return self._soup.text.split('Agravado(s):')[1].split('\n')[1].strip()+' E OUTROS'
        
        qtd = self.quant_string(self._soup.text,'Embargado(a):')
        if qtd == 1:
            return self._soup.text.split('Embargado(a):')[1].split('\n')[1].strip()
        elif qtd > 1:
            return self._data['name']+' E OUTROS'
            #return self._soup.text.split('Embargado(a):')[1].split('\n')[1].strip()+' E OUTROS'
        
        qtd = self.quant_string(self._soup.text,'Recorrido(s):')
        if qtd == 1:
            return self._soup.text.split('Recorrido(s):')[1].split('\n')[1].strip()
        elif qtd > 1:
            return self._data['name']+' E OUTROS'
            #return self._soup.text.split('Recorrido(s):')[1].split('\n')[1].strip()+' E OUTROS'

        qtd = self.quant_string(self._soup.text,'Agravante(s) e Agravado (s): \n')
        if qtd == 1:
            return self._soup.text.split('Agravante(s) e Agravado (s): \n')[1].split('\n')[0].strip()
        elif qtd > 1:
            return self._soup.text.split('Agravante(s) e Agravado (s): \n')[1].split('\n')[0].strip()+' E OUTROS'