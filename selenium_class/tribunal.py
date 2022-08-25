from pdb import pm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time, math
from datetime import datetime


class Trabalhista:

    def __init__(self, pMongo,pCnpj,pNome, pError,pStatus,pProcesso):
        try:
            self._mongo = pMongo
            self._mongo._getcoll('trt')
            self._error = pError
            self._error._getcoll('error')
            self._status = pStatus
            self._status._getcoll('status')
            self._cnpj = pCnpj
            self._nome = pNome
            self.processo = pProcesso
            self._link = 'https://www.tst.jus.br/web/pje'

            self._driver = webdriver.Firefox()
            self._driver.maximize_window()


            '''self._options = webdriver.ChromeOptions()
            self._options.add_argument("--start-maximized")
            self.prefs = {'download.default_directory': self._pasta, 'download.prompt_for_download': False, 'plugins.always_open_pdf_externally': True}
            self._options.add_experimental_option('prefs', self.prefs)
            self._driver = webdriver.Chrome(options=self._options)'''
            self._driver.get(self._link)
            time.sleep(5)
            self._driver.close()
        except Exception as e:
            err = {'data':str(datetime.today()).split(' ')[0].replace('-',''),
                    'tipo_captura': 'nome',
                    'dado_utilizado': self._nome,
                    'sistema': 'stj',
                    'erro': e.msg,
                    'funcao' : 'erro na função init',
            }
            self._error.addData(err)
            return
    
    def get_number(self):
        try:
            WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.NAME, "numeroTst"))).send_keys(self.processo.split('-')[0])
            WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.NAME, "digitoTst"))).send_keys(self.processo.split('-')[1].split('.')[0])
            WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.NAME, "anoTst"))).send_keys(self.processo.split('.')[1].split('.')[0])
            WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.NAME, "orgaoTst"))).send_keys(self.processo.split('.')[2].split('.')[0])
            WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.NAME, "tribunalTst"))).send_keys(self.processo.split('.')[3].split('.')[0])
            WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.NAME, "varaTst"))).send_keys(self.processo.split('.')[4].split('.')[0])
            WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.NAME, "submit"))).click()


            time.sleep(1)
            WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "idParteNome"))).send_keys(self._nome)
            WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "idBotaoPesquisarFormularioExtendido"))).click()
            time.sleep(1)
            WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "idBotaoMarcarTodos"))).click()
            time.sleep(1)
            WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "idBotaoRefinar"))).click()
            time.sleep(1)
            WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "idJulgadorOrigemTipoBlocoLabel"))).click()
            time.sleep(1)
            WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "idOrigemUFItem26"))).find_element(By.TAG_NAME, 'a').click()
            time.sleep(1)
            WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "idBotaoPesquisarRefinandoFormularioExtendido"))).click()
            time.sleep(1)

            quantidade = WebDriverWait(self._driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, "clsMensagemLinha"))).text.split('em')[1].split('registro')[0].strip()
            paginas = math.ceil(int(quantidade)/40)
            processos = []
            for pagina in range(0,paginas):
                WebDriverWait(self._driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, "clsListaProcessoFormatoVerticalBlocoExterno")))
                linhas = self._driver.find_elements(By.CLASS_NAME, 'clsListaProcessoFormatoVerticalBlocoExterno')
                for linha in range (1,len(linhas)):
                    processos.append(linhas[linha].find_elements(By.TAG_NAME, 'a')[0].text)

                if pagina+1 != paginas:
                    WebDriverWait(self._driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, "classSpanPaginacaoImagensDireita"))).find_elements(By.TAG_NAME, 'a')[0].click()
                    time.sleep(1)
            return processos
        except Exception as e:
            err = {'data':str(datetime.today()).split(' ')[0].replace('-',''),
                    'tipo_captura': 'nome',
                    'dado_utilizado': self._nome,
                    'sistema': 'stj',
                    'funcao' : 'erro na função get_number',
            }
            self._error.addData(err)
            return

    def login(self,pProcess):
        try:
            self._processo = pProcess
            print('function login')
            self._driver.get(self._link)
            WebDriverWait(self._driver, 2).until(EC.presence_of_element_located((By.ID, "frmPesquisa")))
            self._driver.find_element(By.ID,'frmPesquisa').find_elements(By.TAG_NAME,'input')[0].send_keys(self._processo.split('/')[0])
            time.sleep(2)
            self._driver.find_element(By.ID,'frmPesquisa').find_element(By.TAG_NAME,'button').click()
            time.sleep(2)
        except Exception as e:
            err = {'data':str(datetime.today()).split(' ')[0].replace('-',''),
                    'tipo_captura': 'nome',
                    'dado_utilizado': self._nome,
                    'sistema': 'stj',
                    'funcao' : 'erro na função login',
            }
            self._error.addData(err)
            return
    
    def get_process(self):
        try:
            print('function get_process')
            self._driver.switch_to.window(self._driver.window_handles[1])
            time.sleep(3)
            WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "idProcessoDetalhesBloco1")))
            proc = {
                    'cnpj' : self._cnpj,
                    'numero_processo' : self._processo,
                    'tipo_processo': WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "idProcessoDetalhesBloco1"))).text.split('PROCESSO:\n')[1].split('\n')[0],
                    'data_distribuicao': WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "idProcessoDetalhesBloco1"))).text.split('AUTUAÇÃO:\n')[1].split('\n')[0],
                    'assunto': WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "idProcessoDetalhesBloco2"))).text.split('ASSUNTO(S):\n')[1].split('\n')[0],
                    'data_captura': str(datetime.today()).split(' ')[0].replace('-',''),
                    'site': self._link,
                    
                }
            try:
                proc['relator'] =  WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "idProcessoDetalhesBloco2"))).text.split('RELATOR(A):\n')[1].split('\n')[0]
            except:
                proc['relator'] = 'Relator não consta neste processo'
            try:
                proc['recorrente'] = WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "idProcessoDetalhesBloco1"))).text.split('AGRAVANTE :\n')[1].split('\n')[0]
            except:
                try:
                    proc['recorrente'] = WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "idProcessoDetalhesBloco1"))).text.split('RECORRENTE:\n')[1].split('\n')[0]
                except:
                    proc['recorrente'] = WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "idProcessoDetalhesBloco1"))).text.split('SUSCITANTE:\n')[1].split('\n')[0]
            try:
                proc['recorrido'] = WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "idProcessoDetalhesBloco1"))).text.split('AGRAVADO :\n')[1].split('\n')[0]
            except:
                try:
                    proc['recorrido'] = WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "idProcessoDetalhesBloco1"))).text.split('RECORRIDO :\n')[1].split('\n')[0]
                except:
                    proc['recorrido'] = WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "idProcessoDetalhesBloco1"))).text.split('SUSCITADO :\n')[1].split('\n')[0]
            try:
                proc['orgao_judicial'] = WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "idProcessoDetalhesBloco1"))).text.split('LOCALIZAÇÃO:\n')[1].split('\n')[0]
            except:
                proc['orgao_judicial'] = WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "idProcessoDetalhesBloco3"))).text.split('TRIBUNAL DE ORIGEM:\n')[1].split('\n')[0]

            WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "idSpanAbaFases"))).find_element(By.TAG_NAME,'a').click()
            WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "classDivFaseLinha")))
            dados = self._driver.find_elements(By.CLASS_NAME,'classDivFaseLinha')

            self._movimentacao = []
            self._dic = {}
            for dado in range(0,len(dados)):
                self._dic['data'] = dados[dado].find_element(By.CLASS_NAME,'classSpanFaseData').text
                self._dic['descricao'] = dados[dado].find_element(By.CLASS_NAME,'classSpanFaseTexto').text
                self._movimentacao.append(self._dic)
                self._dic = {}

            proc['movimentacao'] = self._movimentacao
            modifica = {'$set': proc}
            busca = {'numero_processo':self._processo}
            retorna_dados = self._verifica_dados(self._processo)
            if retorna_dados is None:
                self._mongo.addData(proc)
                retorna_dados = self._verifica_dados(self._processo)
                new = {
                'created_date': str(datetime.today()).split(' ')[0].replace('-',''),
                'created_time': str(datetime.today()).split(' ')[1][:8],
                'robot': 'stj',
                'situation': 'novo processo capturado',
                'process': self._processo,
                'collection': 'stj',
                'id_collection' : str(self._inf['_id'])
                }

                self._status.addData(new)
            else:
                self._mongo.updateOne_Query(busca, modifica)
            
            print('Dados Salvo no banco numero_processo:{} STJ'.format(self._processo))
            self._driver.close()
            self._driver.switch_to.window(self._driver.window_handles[0])
        except Exception as e:
            err = {'data':str(datetime.today()).split(' ')[0].replace('-',''),
                    'tipo_captura': 'nome',
                    'dado_utilizado': self._nome,
                    'sistema': 'stj',
                    'funcao' : 'erro na função get_process',
            }
            self._error.addData(err)
            return

    def _verifica_dados(self,pNum):
        arr = {'numero_processo':pNum}
        dados = self._mongo.returnBusca(arr)
        for dado in dados:
            self._inf = dado
            return True
    
    def close(self):
        self._driver.close()