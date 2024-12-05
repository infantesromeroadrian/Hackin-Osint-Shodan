import requests
import re


def has_valid_credentials(instance):
    """
    Verifica si una instancia de DVWA tiene configuradas las credenciales por defecto en varios puertos.
    """
    sess = requests.Session()
    proto = 'https' if instance.get('ssl') else 'http'
    puertos = [instance.get('port', 80), 8080, 443]  # Puertos comunes

    for puerto in puertos:
        login_page = f"{proto}://{instance['ip_str']}:{puerto}/login.php"
        for attempt in range(3):  # Reintenta hasta 3 veces
            try:
                response = sess.get(login_page, verify=False, timeout=5)
                if response.status_code == 200:
                    break
                print(f"[!] Reintentando {instance['ip_str']}:{puerto} (Intento {attempt + 1}/3)")
            except requests.exceptions.RequestException as e:
                if attempt == 2:  # Último intento fallido
                    print(f"[!] Conexión fallida para {instance['ip_str']}:{puerto}: {e}")
                    return False

        if response.status_code != 200:
            print(f"[!] Error en la respuesta del servidor ({instance['ip_str']}:{puerto}). Respuesta: {response.status_code}")
            continue

        # Extrae el token CSRF
        try:
            token = re.search(r"user_token' value='([0-9a-f]+)'", response.text).group(1)
        except Exception as e:
            print(f"[!] Error al obtener el token CSRF para el host {instance['ip_str']}:{puerto}: {e}")
            continue

        # Intenta hacer login
        try:
            response = sess.post(
                login_page,
                data=f"username=admin&password=password&user_token={token}&Login=Login",
                allow_redirects=False,
                verify=False,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            if response.status_code == 302 and response.headers.get('Location') == 'index.php':
                print(f"[+] Credenciales por defecto válidas en {instance['ip_str']}:{puerto}")
                return True
        except Exception as e:
            print(f"[!] Error al enviar las credenciales por defecto para el host {instance['ip_str']}:{puerto}: {e}")

    return False

