#!/usr/bin/python3

from getopt import error
from classRequest.tst import Tst
from bd.class_mongo import Mongo
from apscheduler.events import EVENT_JOB_ERROR
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
import pytz, time, os
from datetime import datetime

def tst_initial():
    mongo = Mongo(os.environ['MONGO_USER_PROD'], os.environ['MONGO_PASS_PROD'], os.environ['MONGO_HOST_PROD'], os.environ['MONGO_PORT_PROD'], os.environ['MONGO_DB_PROD'], os.environ['AMBIENTE_PROD'])
    erro = Mongo(os.environ['MONGO_USER_PROD'], os.environ['MONGO_PASS_PROD'], os.environ['MONGO_HOST_PROD'], os.environ['MONGO_PORT_PROD'], os.environ['MONGO_DB_PROD'], os.environ['AMBIENTE_PROD'])
    st = Mongo(os.environ['MONGO_USER_PROD'], os.environ['MONGO_PASS_PROD'], os.environ['MONGO_HOST_PROD'], os.environ['MONGO_PORT_PROD'], os.environ['MONGO_DB_PROD'], os.environ['AMBIENTE_PROD'])
    
    mongo._getcoll('contas')
    filiais = mongo.returnQuery()
    fil = []
    list_process = []
    for filial in filiais:
        fil.append(filial)
    
    for f in fil:
        try:
            t = Tst(f,mongo,erro,st)
            lis_process = t.get_process()
            if lis_process is not None:
                for lis in lis_process:
                    t.consulta(lis)
                    t.save_process()
            list_process = []
        except:
            print('Não foi possivel realizar a captura')
            pass
    
    del mongo
    del erro
    del st
    del t
    print('Programa finalizado')

executors = {
    'default': ThreadPoolExecutor(20),      
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 1
}
    
scheduler = BackgroundScheduler(
    executors=executors, job_defaults=job_defaults,
    timezone=pytz.timezone('America/Sao_Paulo')
)

scheduler.add_job(tst_initial, trigger='cron', hour='1')

if __name__ == '__main__':  
    print('Start')
    scheduler.start()
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()