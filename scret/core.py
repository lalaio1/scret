import requests
import json
import time
import random
import logging
import aiohttp
import threading
from requests.exceptions import RequestException, Timeout, ProxyError

class UserAgentManager:
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
            'Mozilla/5.0 (Linux; Android 11; Pixel 4 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.54',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0'
        ]
        self.current_user_agent = self.get_random_user_agent()

    def get_random_user_agent(self):
        return random.choice(self.user_agents)

    def set_custom_user_agent(self, user_agent):
        self.current_user_agent = user_agent

    def get_current_user_agent(self):
        return self.current_user_agent

    def reset_to_random_user_agent(self):
        self.current_user_agent = self.get_random_user_agent()
        
    def list_user_agents(self):
        return self.user_agents
        
class ScretMeResponseHandler:
    @staticmethod
    def handle_response(response):
        try:
            data = response.json()
            
            # Verifique se 'isValid' está presente e se é True
            if isinstance(data, dict) and data.get('isValid'):
                print(f'[+] Mensagem enviada com sucesso.')
                return data
            
            if 'error' in data:
                print(f'[-] Erro da API: {data["error"]}')
            else:
                print('[-] A API retornou uma resposta inválida.')

            return None
        except ValueError:
            print('[-] Não foi possível interpretar a resposta JSON.')
            return None
        except Exception as e:
            print(f'[-] Erro inesperado ao processar a resposta: {e}')
            return None
        
class ScretMeRateLimiter:
    def __init__(self, max_requests, period):
        """
        :param max_requests: Número máximo de requisições permitidas.
        :param period: Período de tempo (em segundos) para o limite.
        """
        self.max_requests = max_requests
        self.period = period
        self.requests = 0
        self.start_time = time.time()
        self.lock = threading.Lock()  # Adiciona um lock para sincronização

    def allow_request(self):
        with self.lock:  # Garante que apenas uma thread possa acessar o bloco de código por vez
            current_time = time.time()
            if current_time - self.start_time > self.period:
                self.requests = 0
                self.start_time = current_time
            if self.requests < self.max_requests:
                self.requests += 1
                return True
            return False

    def wait_for_slot(self):
        while not self.allow_request():
            time.sleep(1)

    def reset_rate_limits(self):
        with self.lock:
            self.requests = 0
            self.start_time = time.time()

    def set_new_limits(self, max_requests, period):
        with self.lock:
            self.max_requests = max_requests
            self.period = period

        
class ScretMeLogger:
    
    def __init__(self, log_file='scretme.log', level=logging.INFO):
        self.logger = self._setup_logger(log_file, level)
        
    def _setup_logger(self, log_file, level):
        """
        Configura o logger para a biblioteca.
        """
        logger = logging.getLogger()
        logger.setLevel(level)

        if not logger.hasHandlers():
            handler = logging.FileHandler(log_file)
            handler.setLevel(level)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger

    def log_info(self, message):
        """Log de informações."""
        self.logger.info(message)

    def log_warning(self, message):
        """Log de avisos."""
        self.logger.warning(message)

    def log_error(self, message):
        """Log de erros."""
        self.logger.error(message)

    def log_critical(self, message):
        """Log de erros críticos."""
        self.logger.critical(message)

class ScretMeAuth:
    
    def __init__(self, api_key=None):
        self.api_key = api_key
    
    def set_api_key(self, key):
        self.api_key = key

    def get_auth_headers(self):
        if self.api_key:
            return {
                'Authorization': f'Bearer {self.api_key}'
            }
        else:
            raise ValueError("API key não está definida.")
    
    def refresh_api_key(self, new_key):
        self.api_key = new_key

class ScretMeProxy:
    def __init__(self, proxy=None, use_tor=False):
        self.proxy = proxy
        self.use_tor = use_tor
        self.tor_proxy = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }

    def set_proxy(self, proxy):
        """Configura um proxy customizado."""
        self.proxy = proxy

    def validate_proxy(self):
        try:
            response = requests.get('https://httpbin.org/ip', proxies=self.get_proxy(), timeout=5)
            response.raise_for_status()  # Levanta uma exceção para códigos de status não bem-sucedidos
            return response.status_code == 200
        except Timeout:
            print('[-] O proxy levou muito tempo para responder.')
            return False
        except ProxyError:
            print('[-] Erro com o proxy fornecido.')
            return False
        except RequestException as e:
            print(f'[-] Erro de requisição: {e}')
            return False

    def enable_tor(self):
        self.use_tor = True

    def disable_tor(self):
        self.use_tor = False

    def get_proxy(self):
        if self.use_tor:
            return self.tor_proxy
        return {'http': self.proxy, 'https': self.proxy} if self.proxy else {}
    
class ScretMeAPIError(Exception):
    pass

class InvalidResponseError(ScretMeAPIError):
    pass

class NetworkError(ScretMeAPIError):
    pass

class ScretMeAPI:
    BASE_URL = 'https://api.scret.me/v1/message'
    DEFAULT_HEADERS = {
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9,pt;q=0.8',
        'Referer': 'https://scret.me/',
        'Referrer-Policy': 'strict-origin-when-cross-origin',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site'
    }
    MAX_RETRIES = 3

    def __init__(self, user_slug, message, retries=MAX_RETRIES):
        self.cache = ScretMeCache()
        self.user_slug = user_slug
        self.message = message
        self.retries = retries
        self.user_agent_manager = UserAgentManager()  # Adicionando o gerenciador de User-Agent
        self.payload = self._build_payload()

    def _build_payload(self):
        """Monta o payload da requisição com os dados do usuário e do dispositivo."""
        device_info = {
            'country_code': 'US',
            'country_name': 'United States',
            'city': 'Washington, D.C.',
            'postal': '20001',
            'latitude': 38.895111,
            'longitude': -77.036369,
            'IPv4': '173.166.164.121',
            'state': 'District Of Columbia',
            'userAgent': self.user_agent_manager.get_current_user_agent()  # Obtém o User-Agent atual
        }
        return {
            'slug': self.user_slug,
            'content': self.message,
            'device': json.dumps(device_info),
            'tips': []
        }
    
    def _send_request(self):
        try:
            response = requests.post(self.BASE_URL, json=self.payload, headers=self.DEFAULT_HEADERS)
            response.raise_for_status()  # Levanta uma exceção para códigos de status não bem-sucedidos
            return response.json()
        except requests.HTTPError as e:
            raise InvalidResponseError(f'Erro HTTP: {e.response.status_code}') from e
        except requests.RequestException as e:
            raise NetworkError(f'Erro de rede: {e}') from e

    def set_random_user_agent(self):
        """Define um User-Agent aleatório."""
        self.user_agent_manager.reset_to_random_user_agent()

    def set_custom_user_agent(self, user_agent):
        """Define um User-Agent customizado."""
        self.user_agent_manager.set_custom_user_agent(user_agent)

    def send_message(self):
        headers = self.DEFAULT_HEADERS.copy()
        headers['User-Agent'] = self.user_agent_manager.get_current_user_agent()  # Atualiza o User-Agent
        for attempt in range(1, self.retries + 1):
            try:
                response = requests.post(self.BASE_URL, json=self.payload, headers=headers)
                data = ScretMeResponseHandler.handle_response(response)
                if data:
                    print(f'[+] Mensagem enviada com sucesso para {self.user_slug}')
                    return True
            except InvalidResponseError as e:
                print(f'[-] Tentativa {attempt} de {self.retries} falhou: {e}')
            except requests.RequestException as e:
                print(f'[-] Erro de rede: {e}')
            time.sleep(random.uniform(1, 3))  

    def set_custom_device(self, device_info):
        self.payload['device'] = json.dumps(device_info)

    def add_tip(self, tip_message):
        self.payload['tips'].append(tip_message)

    def clear_tips(self):
        self.payload['tips'] = []

    def get_message_payload(self):
        return self.payload

    def set_timeout(self, timeout):
        self.timeout = timeout

    async def send_async_message(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.BASE_URL, json=self.payload, headers=self.DEFAULT_HEADERS) as response:
                    response.raise_for_status()
                    data = await response.json()
                    result = ScretMeResponseHandler.handle_response(data)
                    return result
        except aiohttp.ClientResponseError as e:
            logging.error(f'Erro na resposta da API: {e.message}')
            raise ScretMeAPIError(f'Erro na resposta da API: {e.message}')
        except aiohttp.ClientError as e:
            logging.error(f'Erro de rede com a API: {e}')
            raise NetworkError(f'Erro de rede com a API: {e}')
        except Exception as e:
            logging.error(f'Erro inesperado: {e}')
            raise ScretMeAPIError(f'Erro inesperado: {e}')
            
class ScretMeCache:
    def __init__(self):
        self.cache = {}

    def get_from_cache(self, key):
        return self.cache.get(key)

    def add_to_cache(self, key, response):
        self.cache[key] = response


class ScretMeAPIStatusChecker:
    @staticmethod
    def check_status():
        try:
            response = requests.get('https://api.scret.me/status')
            if response.status_code == 200:
                return response.json().get('status', 'unknown')
            return 'API offline'
        except requests.RequestException:
            return 'Erro de conexão com a API'

class ScretMeRetryPolicy:
    def __init__(self, max_retries, backoff_factor=1.0):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        
    def get_backoff_time(self, attempt):
        return self.backoff_factor * (2 ** (attempt - 1))

    def execute_with_retries(self, func, *args, **kwargs):
        for attempt in range(1, self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == self.max_retries:
                    raise
                time.sleep(self.get_backoff_time(attempt))

class ScretMeCache:
    def __init__(self):
        self.cache = {}

    def get_from_cache(self, key):
        return self.cache.get(key)

    def add_to_cache(self, key, response):
        self.cache[key] = response

    def clear_cache(self):
        self.cache = {}