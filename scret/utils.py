import json
import logging
import re

logging.basicConfig(filename='errors.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def load_json_from_file(file_name):
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except (IOError, json.JSONDecodeError) as e:
        log_error(f'Erro ao carregar o arquivo JSON: {e}')
        return None
    
def save_json_to_file(data, file_name='output.json'):
    try:
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(f'Dados salvos com sucesso em {file_name}')
    except IOError as e:
        log_error(f'Erro ao salvar o arquivo JSON: {e}')

def pretty_print_json(data):
    if isinstance(data, str):
        try:
            json_data = json.loads(data)
        except json.JSONDecodeError:
            return "Erro: Dados JSON inválidos"
    else:
        json_data = data
    try:
        return json.dumps(json_data, indent=4, ensure_ascii=False)
    except (TypeError, ValueError) as e:
        return f"Erro ao formatar JSON: {e}"

def log_error(message):
    logging.error(message)

def validate_ip(ip):
    ip_pattern = re.compile(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$')
    if ip_pattern.match(ip):
        return all(0 <= int(octet) <= 255 for octet in ip.split('.'))
    return False

def format_device_data(ip, country, city, user_agent, **kwargs):
    device_data = {
        'IPv4': ip,
        'country_name': country,
        'city': city,
        'userAgent': user_agent
    }
    device_data.update(kwargs)
    return json.dumps(device_data, indent=4)