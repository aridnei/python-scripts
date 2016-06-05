"""FTP Client
Conecta a servidor FTP baixa e renomeia arquivo para Microsoft Windows

Required: Python 2.7 or later
"""

from ftplib import FTP
import logging
import os
import subprocess

# Declara variaveis
FTPHOST='ftp.host.com'
LOGFILENAME='ftplogfile.log'

# Configura rotina para registro de LOGs
logging.basicConfig( level=logging.INFO,
                     filename=LOGFILENAME,
                     format='%(asctime)s %(message)s',
                     datefmt='%Y%m%d %H:%M:%S')

logging.info('### Inicia processo ###')

# Abre diretorio local de trabalho
os.chdir('C:/diretorio_local/')

# Conecta no servidor FTP
ftpconn = FTP(FTPHOST)
logging.info('Connecta em %s', FTPHOST)

# Autentica no servidor FTP
msg = ftpconn.login('ftp_username','ftp_username')
logging.info('%s', msg)

# Abre diretorio remoto
msg = ftpconn.cwd('diretorio')
logging.info('%s', msg)

# Lista arquivos no servidor FTP usando prefixo/mascara
file_list = ftpconn.nlst('filename*')

# Encontrou arquivos?
if len(file_list) < 1:
    logging.info('Nao existem arquivos')

    # Fecha conexão com o servidor FTP
    msg = ftpconn.quit()
    logging.info('Desconecta de %s', FTPHOST)
    logging.info('%s', msg)

else:
    # Processa lista de arquivo encontrados
    for filename in file_list:

        # Guarda nome original do arquivo
        fullfilename = ftpconn.dir(filename)
        logging.info('%s', fullfilename)

        # Baixa arquivo
        msgtransf = ftpconn.retrbinary('RETR ' + filename, open(filename, 'wb').write )
        logging.info('Recebe arquivo %s', filename)
        logging.info('%s', msgtransf)

        # Renomeia arquivo baixado
        msgmove = ftpconn.rename(filename, 'BAIXADO_' + filename)
        logging.info('Renomeia para BAIXADO_%s', filename)
        logging.info('%s', msgmove)

    # Fecha conexao com servidor FTP
    msg = ftpconn.quit()
    logging.info('Desconecta de %s', FTPHOST)
    logging.info('%s', msg)

logging.info('### Encerra processo ###')
logging.info('--------------------------------------------------')
