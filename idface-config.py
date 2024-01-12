import requests
import json
import pandas as pd

def login_and_configure(ip, login, password):
    try:
        # Dados de login no formato JSON
        login_data = {
            'login': 'admin',
            'password': password
        }

        url_login = f"http://{ip}/login.fcgi"
        response_login = requests.post(url_login, data=json.dumps(login_data), headers={"Content-Type": "application/json"})

        # Verificar o status da resposta
        if response_login.status_code == 200:
            response_data = response_login.json()
            session = response_data.get("session")
            print(f"Login bem-sucedido para o dispositivo {ip}. Sessão: {session}")

            # Troque aqui as informações do seu servidor VoIP
            config_data = {
                "pjsip": {
                    "enabled": "1",
                    "server_ip": "serv-teste",
                    "server_port": "7060",
                    "server_outbound_port": "10000",
                    "server_outbound_port_range": "10000"                               
                }
            }

            url_config = f"http://{ip}/set_configuration.fcgi?session={session}"
            response_config = requests.post(url_config, data=json.dumps(config_data), headers={"Content-Type": "application/json"})

            # Verificar o status da resposta da configuração
            if response_config.status_code == 200:
                print(f"Configuração bem-sucedida para o dispositivo {ip}.")
            else:
                print(f"Erro na configuração para o dispositivo {ip}. Código de status: {response_config.status_code}\n{response_config.text}")
        else:
            print(f"Erro no login para o dispositivo {ip}. Código de status: {response_login.status_code}\n{response_login.text}")

    except Exception as e:
        print(f"Erro ao processar o dispositivo {ip}: {e}")

# Substitua 'seu_arquivo.xlsx' pelo caminho do seu arquivo xlsx
file_path = 'dados.xlsx'

try:
    # Ler o arquivo xlsx para um DataFrame do Pandas
    df = pd.read_excel(file_path)

    # Verificar se a coluna 'ip_local' está presente
    if 'ip_local' in df.columns:
        # Iterar sobre as linhas e chamar a função login_and_configure para cada dispositivo
        for index, row in df.iterrows():
            ip = row['ip_local']
            login = row['campo_name_modulo']
            password = row['campo_passwd']
            
            login_and_configure(ip, login, password)

    else:
        print("A coluna 'ip_local' não foi encontrada no arquivo xlsx.")

except Exception as e:
    print(f"Erro ao ler dados do arquivo xlsx: {e}")
