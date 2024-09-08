# 📚 **Scret.me Library Documentation**

Welcome to the comprehensive documentation for the **Scret.me** library! This library facilitates interaction with the Scret.me API, allowing you to send anonymous messages, manage user agents, handle rate limiting, and more. Below you'll find a detailed overview of the library's modules, classes, methods, and examples of how to use them. 🚀

---

## 📂 **Table of Contents**

1. [Core Module](#core-module)
2. [Utils Module](#utils-module)
3. [Setup](#setup)
4. [Examples](#examples)

---

## 📦 **Core Module**

The `core.py` file contains the main classes for interacting with the Scret.me API.

### **Classes**

1. **`UserAgentManager`**: Manages and rotates user agents.
   - **Methods:**
     - `get_random_user_agent()`: Returns a random user agent from the list.
     - `set_custom_user_agent(user_agent)`: Sets a custom user agent.
     - `get_current_user_agent()`: Returns the current user agent.
     - `reset_to_random_user_agent()`: Resets to a random user agent.

2. **`ScretMeResponseHandler`**: Handles API responses.
   - **Methods:**
     - `handle_response(response)`: Processes the API response and prints messages based on validity.

3. **`ScretMeRateLimiter`**: Manages API request rates.
   - **Methods:**
     - `allow_request()`: Checks if a request is allowed based on rate limits.
     - `wait_for_slot()`: Waits until a request slot is available.
     - `reset_rate_limits()`: Resets the rate limits.
     - `set_new_limits(max_requests, period)`: Sets new rate limits.

4. **`ScretMeLogger`**: Handles logging.
   - **Methods:**
     - `log_info(message)`: Logs informational messages.
     - `log_warning(message)`: Logs warning messages.
     - `log_error(message)`: Logs error messages.
     - `log_critical(message)`: Logs critical error messages.

5. **`ScretMeAuth`**: Manages API authentication.
   - **Methods:**
     - `set_api_key(key)`: Sets the API key.
     - `get_auth_headers()`: Returns authentication headers.
     - `refresh_api_key(new_key)`: Refreshes the API key.

6. **`ScretMeProxy`**: Manages proxies and Tor.
   - **Methods:**
     - `set_proxy(proxy)`: Sets a custom proxy.
     - `validate_proxy()`: Validates the proxy.
     - `enable_tor()`: Enables Tor.
     - `disable_tor()`: Disables Tor.
     - `get_proxy()`: Returns the current proxy settings.

7. **`ScretMeAPIError`**: Base exception class for API errors.

8. **`InvalidResponseError`**: Exception for invalid API responses.

9. **`NetworkError`**: Exception for network errors.

10. **`ScretMeAPI`**: Interacts with the Scret.me API.
    - **Methods:**
      - `set_random_user_agent()`: Sets a random user agent.
      - `set_custom_user_agent(user_agent)`: Sets a custom user agent.
      - `send_message()`: Sends a message to the API.
      - `set_custom_device(device_info)`: Sets custom device information.
      - `add_tip(tip_message)`: Adds a tip to the payload.
      - `clear_tips()`: Clears all tips from the payload.
      - `get_message_payload()`: Returns the current message payload.
      - `set_timeout(timeout)`: Sets a timeout for the request.
      - `send_async_message()`: Sends a message asynchronously.

11. **`ScretMeCache`**: Manages cache for responses.
    - **Methods:**
      - `get_from_cache(key)`: Retrieves data from cache.
      - `add_to_cache(key, response)`: Adds data to cache.

12. **`ScretMeAPIStatusChecker`**: Checks the status of the API.
    - **Methods:**
      - `check_status()`: Returns the API status.

13. **`ScretMeRetryPolicy`**: Manages retry policies.
    - **Methods:**
      - `get_backoff_time(attempt)`: Calculates backoff time for retries.
      - `execute_with_retries(func, *args, **kwargs)`: Executes a function with retries.

14. **`ScretMeResponseCache`**: Caches API responses.
    - **Methods:**
      - `add_to_cache(key, response)`: Adds response to cache.
      - `get_from_cache(key)`: Retrieves response from cache.
      - `clear_cache()`: Clears the cache.

---

## 🛠️ **Utils Module**

The `utils.py` file contains utility functions for JSON operations, logging, and IP validation.

### **Functions**

1. **`load_json_from_file(file_name)`**: Loads JSON data from a file.
   - **Parameters:**
     - `file_name` (str): The path to the JSON file.
   - **Returns:** JSON data as a dictionary or `None` on failure.

2. **`save_json_to_file(data, file_name='output.json')`**: Saves JSON data to a file.
   - **Parameters:**
     - `data` (dict): The JSON data to save.
     - `file_name` (str, optional): The file path (default: `'output.json'`).
   - **Returns:** None

3. **`pretty_print_json(data)`**: Formats JSON data for pretty printing.
   - **Parameters:**
     - `data` (str or dict): JSON data to format.
   - **Returns:** Pretty-printed JSON string.

4. **`log_error(message, log_file='errors.log')`**: Logs an error message to a file.
   - **Parameters:**
     - `message` (str): The error message.
     - `log_file` (str, optional): The log file path (default: `'errors.log'`).
   - **Returns:** None

5. **`validate_ip(ip)`**: Validates an IP address.
   - **Parameters:**
     - `ip` (str): The IP address to validate.
   - **Returns:** `True` if valid, otherwise `False`.

6. **`format_device_data(ip, country, city, user_agent, **kwargs)`**: Formats device data for JSON.
   - **Parameters:**
     - `ip` (str): The IP address.
     - `country` (str): The country name.
     - `city` (str): The city name.
     - `user_agent` (str): The user agent.
     - `**kwargs`: Additional device data.
   - **Returns:** JSON string with formatted device data.

---

## 🛠️ **Setup**

To install the Scret.me library, use the following command:

```bash
pip install .
```

This will install the library and its dependencies.

---

## 💡 **Examples**

### **Example 1: Sending a Message**

```python
from scret import ScretMeAPI, ScretMeAuth

# Create an instance with user slug and message
api = ScretMeAPI(user_slug='example_user', message='Hello, Scret.me!')

# Set a custom API key
auth = ScretMeAuth(api_key='your_api_key')
headers = auth.get_auth_headers()

# Send the message
api.send_message()
```

### **Example 2: Using Proxies**

```python
from scret import ScretMeProxy

# Initialize proxy manager
proxy_manager = ScretMeProxy(proxy='http://your.proxy:8080')

# Check if proxy is valid
if proxy_manager.validate_proxy():
    print('Proxy is valid.')
else:
    print('Proxy is invalid.')
```

### **Example 3: Asynchronous Message Sending**

```python
import asyncio
from scret import ScretMeAPI

async def send_message():
    api = ScretMeAPI(user_slug='async_user', message='Hello from async!')
    result = await api.send_async_message()
    print(result)

# Run the async function
asyncio.run(send_message())
```

### **Example 4: Rate Limiting**

```python
from scret import ScretMeRateLimiter

# Create a rate limiter with 5 requests per minute
rate_limiter = ScretMeRateLimiter(max_requests=5, period=60)

# Check if request is allowed
if rate_limiter.allow_request():
    print('Request allowed.')
else:
    print('Rate limit exceeded.')
```

### **Example 5: Logging**

```python
from scret import ScretMeLogger

# Initialize logger
logger = ScretMeLogger(log_file='my_log.log')

# Log messages
logger.log_info('This is an info message.')
logger.log_warning('This is a warning message.')
logger.log_error('This is an error message.')
logger.log_critical('This is a critical message.')
```

### **Exemple 6**

```python
# Import the necessary classes from the scret library
from scret import ScretMeAPI, UserAgentManager, ScretMeProxy

def main():
    # Set up the user details and message
    user_slug = 'example_user'  # Replace with the target user slug
    message = 'Hello from Scret.me library!'  # Replace with the message you want to send

    # Create an instance of UserAgentManager to manage user agents
    user_agent_manager = UserAgentManager()
    
    # Optionally set a custom user agent (or use a random one)
    custom_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    user_agent_manager.set_custom_user_agent(custom_user_agent)
    
    # Create an instance of ScretMeAPI
    api = ScretMeAPI(user_slug=user_slug, message=message)
    
    # Set the user agent for the API request
    api.set_custom_user_agent(user_agent_manager.get_current_user_agent())
    
    # Optionally configure a proxy (if needed)
    # Uncomment and set your proxy details if you need to use a proxy
    # proxy = ScretMeProxy(proxy='http://your.proxy:8080')
    # api.set_proxy(proxy.get_proxy())

    # Send the message
    success = api.send_message()
    
    if success:
        print('Message sent successfully!')
    else:
        print('Failed to send the message.')

if __name__ == '__main__':
    main()
```

---
# By: lalaio1
