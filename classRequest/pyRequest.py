#!/usr/bin/python3
from datetime import datetime
from pdb import pm
from PIL import Image
import os, json, time, requests
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.firefox.options import Options
from pathlib import Path

class Pje:

    def __init__(self, pMongo, pCapcha,pTribunal,pGrau,pId,pSenha,pEmpresas):
        print('Iniciando RPA')
        self._url = {}
        self._pje = {}
        self._captcha = pCapcha
        self._bdMongo = pMongo
        if pTribunal == '2':
            self._bdMongo._check_collection('trt2_1_grau')
        else:
            self._bdMongo._check_collection('trt15_1_grau')
        self._empresas = pEmpresas

        self._trt = pTribunal
        self._url_principal = 'https://pje.trt{}.jus.br/'.format(self._trt)
        self._grau = pGrau
        self._pasta = '/tmp/PJE/TRT/'
        if not os.path.exists(self._pasta):
            os.makedirs(self._pasta)
        try:
            fp = webdriver.FirefoxProfile()
            fp.set_preference("browser.download.folderList", 2)
            fp.set_preference("browser.download.manager.showWhenStarting", False)
            fp.set_preference("browser.download.dir", self._pasta)
            fp.set_preference("browser.helperApps.neverAsk.saveToDisk",
                            "text/plain, application/octet-stream, application/binary, text/csv, application/csv, application/excel, text/comma-separated-values, text/xml, application/xml")
            fp.set_preference("pdfjs.disabled", True)
            options = Options()
            options.add_argument("--headless")
            self.driver = webdriver.Firefox(firefox_profile=fp)


            '''
            self.option = webdriver.ChromeOptions()
            self.prefs = {'download.default_directory': self._pasta, 'download.prompt_for_download': False, 'plugins.always_open_pdf_externally': True}
            self.option.add_experimental_option('prefs', self.prefs)
            self.option.add_argument('--start-maximized')
            self.option.add_argument('--ignore-certificate-errors')
            self.driver = webdriver.Chrome(chrome_options=self.option)
            self.driver.maximize_window()

            '''
            self.driver.get(self._url_principal) 
            time.sleep(2) 

            self.wait = WebDriverWait(self.driver, 5)
            self.wait.until(ec.visibility_of_element_located((By.ID, "username"))).send_keys(pId)
            self.wait.until(ec.visibility_of_element_located((By.ID, "password"))).send_keys(pSenha)
            self.wait.until(ec.visibility_of_element_located((By.ID, "btnEntrar"))).click()

            time.sleep(2)
        except:
            self.driver.close()

                  
    
    def login(self,pProcesso,pIntancia,pGrau):
        print('Realizando login')
        self._processo = pProcesso
        self._instancia = pIntancia
        self._grau = pGrau

        if self._grau == '1' and self._trt == '2':
            self._bdMongo._check_collection('trt2_1_grau')
        elif self._grau == '2' and self._trt == '2':
            self._bdMongo._check_collection('trt2_2_grau')
        elif self._grau == '1' and self._trt == '15':
            self._bdMongo._check_collection('trt15_1_grau')
        else:
            self._bdMongo._check_collection('trt15_2_grau')


        self._pasta = '/tmp/PJE/TRT{}/GRAU{}/{}/'.format(self._trt,self._grau,self._processo.replace('-','').replace('.',''))
        if not os.path.exists(self._pasta):
            os.makedirs(self._pasta)
        
        self._url = 'https://pje.trt{}.jus.br/consultaprocessual/detalhe-processo/{}'.format(self._trt,self._processo)
        self.driver.get(self._url)
        time.sleep(1)

        self.wait = WebDriverWait(self.driver, 6)
        cont = 0
        try:
            while True:
                try:

                    try:
                        WebDriverWait(self.driver, 2).until(ec.visibility_of_element_located((By.ID, "instrucoesCaptcha"))).text
                        self.get_token()
                        return True,'1'
                    except:
                        pass  

                    if int(WebDriverWait(self.driver, 2).until(ec.visibility_of_element_located((By.ID, "painel-escolha-processo"))).text[:1]) == 1:
                        self.get_token()
                        return True,'1'
                    
                    elif int(WebDriverWait(self.driver, 2).until(ec.visibility_of_element_located((By.ID, "painel-escolha-processo"))).text[:1]) >= 2:
                        self.driver.find_element_by_id('painel-escolha-processo').find_elements_by_tag_name('button')[self._instancia].click()
                        self.get_token()
                        return True,'2'

                    else:
                        print('O processo {} não existe no sistema TRT{}'.format(self._processo,self._trt))
                        return False,'0'

                except:
                    try:
                        if WebDriverWait(self.driver, 2).until(ec.visibility_of_element_located((By.ID, "imagemCaptcha"))):
                            if cont <= 3:
                                cont += 1
                                continue
                            else:
                                print('Não foi possivel realizar o captcha')
                                return False,'0'
                    except:
                    
                        if self.driver.find_element_by_id('painel-escolha-processo').text.find('0 processos encontrados:') >= 0:
                            print('O processo {} não existe no sistema TRT{}'.format(self._processo,self._trt))
                            return False,'0'
                        else:
                            pass
 
        except:
            return False,'0'
    
    def get_token(self):
        WebDriverWait(self.driver, 2).until(ec.visibility_of_element_located((By.ID, "imagemCaptcha")))
        element = self.wait.until(ec.visibility_of_element_located((By.ID, "imagemCaptcha")))
        location = element.location
        size = element.size
        self.driver.save_screenshot(os.path.join(self._pasta,"pageImage.png"))

        # crop image
        x = location['x']
        y = location['y']
        width = location['x']+size['width']
        height = location['y']+size['height']
        im = Image.open(os.path.join(self._pasta,"pageImage.png"))
        im = im.crop((int(x), int(y), int(width), int(height)))
        im.save(os.path.join(self._pasta,'element.png'))
        os.system('rm {}'.format(os.path.join(self._pasta,"pageImage.png")))

        im = os.path.join(self._pasta,'element.png')               
        self.solve = self._captcha.resolve_normal(im)
        #self.solve = ''
        self.wait.until(ec.visibility_of_element_located((By.ID, "captchaInput"))).send_keys(self.solve)
        os.system('rm {}'.format(os.path.join(self._pasta,'element.png')))
        
        self.wait.until(ec.visibility_of_element_located((By.ID, "btnEnviar"))).click()
        self.wait.until(ec.visibility_of_element_located((By.ID, "timeline")))
        time.sleep(1)

        # GOOGLE CHROME
        '''self._captcha_token = self.driver.get_cookies()[0]['value']
        self._acesso_terceiro = self.driver.get_cookies()[1]['value']
        self._resposta_desafio = self.driver.get_cookies()[2]['value']
        self._token_desafio = self.driver.get_cookies()[3]['value']
        self._access_token_1g = self.driver.get_cookies()[4]['value']
        self._refresh_token = self.driver.get_cookies()[5]['value']
        self._xsrf_token = self.driver.get_cookies()[6]['value']
        self._access_token_footer = self.driver.get_cookies()[7]['value']
        self._acesso_token = self.driver.get_cookies()[8]['value']'''

        self._captcha_token = self.driver.get_cookies()[7]['value']
        self._acesso_terceiro = self.driver.get_cookies()[8]['value']
        self._resposta_desafio = self.driver.get_cookies()[6]['value']
        self._token_desafio = self.driver.get_cookies()[5]['value']
        self._access_token_1g = self.driver.get_cookies()[4]['value']
        self._refresh_token = self.driver.get_cookies()[3]['value']
        self._xsrf_token = self.driver.get_cookies()[2]['value']
        self._access_token_footer = self.driver.get_cookies()[1]['value']
        self._acesso_token = self.driver.get_cookies()[0]['value']
        time.sleep(1)
                        
        
    def get_information(self):
        print('Capturando as informações do sistema')
        url = "https://pje.trt{}.jus.br/pje-consulta-api/api/processos/dadosbasicos/{}".format(self._trt,self._processo)
        headers = self.get_headers()
        self._ret_response = requests.request("GET", url, headers=headers)

        
        url = "https://pje.trt{}.jus.br/pje-consulta-api/api/processos/{}?tokenCaptcha={}".format(self._trt,self._ret_response.text.split(':')[1].split(',')[0].strip(),self._captcha_token)
        headers = self.get_headers()
        response = requests.request("GET", url, headers=headers)

        self._information = json.loads(response.text)
        print('Login efetuado')
        return self._information


    def get_headers(self):
        headers = {
        'authority': 'pje.trt{}.jus.br'.format(self._trt),
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'acessoterceirostoken': '{}'.format(self._acesso_terceiro),
        'authorization': 'Bearer {}'.format(self._access_token_1g),
        'content-type': 'application/json',
        'cookie': 'access_token={}; access_token_footer={}; refresh_token={}; Xsrf-Token={}; access_token_1g={}; tokenDesafio={}; respostaDesafio={}; captchaToken={}; acessoTerceirosToken={}'
        .format(self._acesso_token,self._access_token_footer,self._refresh_token,self._xsrf_token,self._access_token_1g,self._token_desafio,self._resposta_desafio,self._captcha_token,self._acesso_terceiro),
        'referer': 'https://pje.trt{}.jus.br/consultaprocessual/detalhe-processo/{}/{}'.format(self._trt,self._processo,self._grau),
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        'x-grau-instancia': '{}'.format(self._grau)
        }

        return headers

    
    def save_information(self,pList):
        if self._grau == '1':
            self.get_download(pList)
            reclamante = self.get_reclamante(pList)
            reclamado = self.get_reclamado(pList)
            self._pje = {
                'numero_processo': pList['numero'],
                'trt' : self._trt,
                'grau' : self._grau,
                'comarca' : pList['orgaoJulgador'],
                'tipo_acao': pList['assuntos'][0]['descricao'],
                'reclamante': reclamante,
                'reclamado': reclamado,
                'forum': 'Tribunal Regional do Trabalho da {}Regiao'.format(self._trt),
                'vara': pList['orgaoJulgador'],
                'data_distribuicao': pList['distribuidoEm'] if 'distribuidoEm' in pList else None,
                'atuado': pList['autuadoEm'],
                'juiz': self._juiz,
                'valor_causa': pList['valorDaCausa'],
                'data_processamento': str(datetime.today()).split(' ')[0].replace('-',''),
            }

            dic = {}
            movimentos = []


            dic['descricao'] = pList['itensProcesso'][0]['titulo']
            dic['data'] = pList['itensProcesso'][0]['data']
            movimentos.append(dic)
            dic = {}
            
            self._pje['movimento'] = movimentos

        else:
            reclamante = self.get_reclamante(pList)
            reclamado = self.get_reclamado(pList)
            self._pje = {
                'numero_processo': pList['numero'],
                'trt' : self._trt,
                'grau' : self._grau,
                'tipo_recurso': pList['assuntos'][0]['descricao'],
                '{}'.format(pList['poloAtivo'][0]['tipo']).lower(): reclamante,
                '{}'.format(pList['poloPassivo'][0]['tipo']).lower(): reclamado,
                'turma_julgador': pList['orgaoJulgadorColegiado'],
                'relator': pList['pessoaRelator'],
                'data_distribuicao': pList['distribuidoEm'] if 'distribuidoEm' in pList else None,
                'atuado': pList['autuadoEm'],
                'valor_causa': pList['valorDaCausa'],
                'data_processamento': str(datetime.today()).split(' ')[0].replace('-',''),
            }

            dic = {}
            movimentos = []

            dic['descricao'] = pList['itensProcesso'][0]['titulo']
            dic['data'] = pList['itensProcesso'][0]['data']
            movimentos.append(dic)
            dic = {}
            
            self._pje['movimento'] = movimentos

        modifica = {'$set': self._pje}
        busca = {'numero_processo':pList['numero']}
        retorna_dados = self._verifica_dados(pList['numero'])
        if retorna_dados is None:
            self._bdMongo.addData(self._pje)
        else:
            self._bdMongo.updateOne_Query(busca, modifica)
        
        print('Dados Salvo no banco numero_processo:{} grau: {} trt:{}'.format(self._processo, self._grau, self._trt))
    
    def get_download(self,pList_download):
        key = True
        for num_documento in pList_download['itensProcesso']:
            if 'id' in num_documento:
                url = "https://pje.trt{}.jus.br/pje-consulta-api/api/processos/{}/documentos/{}/conteudo?tokenCaptcha={}".format(self._trt,self._ret_response.text.split(':')[1].split(',')[0].strip(),num_documento['id'],self._captcha_token)
                headers = self.get_headers()
                response = requests.request("GET", url, headers=headers)
                local = os.path.join(self._pasta,"{}_{}.pdf".format(num_documento['titulo'].replace(' ','').replace('/','-'),num_documento['idUnicoDocumento']))
                pdf = open("{}".format(local), 'wb')
                pdf.write(response.content)
                pdf.close()
                time.sleep(2)
                
                self._juiz = self.get_information_pdf()
                os.system('rm {}'.format(local))
                break
    
    def get_reclamante(self,pLista):
        desc = []
        if len(pLista['poloAtivo']) > 1:
            for lista in pLista['poloAtivo']:
                for empresa in self._empresas:
                    if lista['nome'].find(empresa['nome']) >= 0:
                        return lista['nome'].strip() 
            return pLista['poloAtivo'][0]['nome'].strip()
        else:
            return pLista['poloAtivo'][0]['nome'].strip()


    def get_reclamado(self,pLista):
        desc = []
        if len(pLista['poloPassivo']) > 1:
            for lista in pLista['poloPassivo']:
                for empresa in self._empresas:
                    if lista['nome'].find(empresa['nome']) >= 0:
                        return lista['nome'].strip()

            return pLista['poloPassivo'][0]['nome'].strip()
        else:
            return pLista['poloPassivo'][0]['nome'].strip()


    def get_information_pdf(self):
        print('Capturando nome do juiz')
        try:
            modifica = os.path.join(self._pasta,os.listdir(self._pasta)[0]).replace('.pdf', '.txt')
            os.system('pdftotext {0} {1}'.format(os.path.join(self._pasta,os.listdir(self._pasta)[0]), modifica))
            arquivo = open(modifica, 'r')
            conteudo = arquivo.read()
            os.system('rm {}'.format(modifica))
            juiz = conteudo.split('Assinado eletronicamente por:')[1].split('-')[0].strip()
            return juiz
            
        except:
            os.rename(os.path.join(self._pasta,os.listdir(self._pasta)[0]), os.path.join(self._pasta,'contestacao.pdf'))
            modifica = os.path.join(self._pasta,os.listdir(self._pasta)[0]).replace('.pdf', '.txt')
            os.system('pdftotext {0} {1}'.format(os.path.join(self._pasta,os.listdir(self._pasta)[0]), modifica))
            arquivo = open(modifica, 'r')
            conteudo = arquivo.read()
            os.system('rm {}'.format(modifica))
            juiz = conteudo.split('Assinado eletronicamente por:')[1].split('-')[0].strip()

            return juiz

    def _verifica_dados(self,pNum):
        arr = {'numero_processo':pNum, 'grau': self._grau, 'trt':self._trt}
        dados = self._bdMongo.returnBusca(arr)
        for dado in dados:
            return True
