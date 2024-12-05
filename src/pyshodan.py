import os
import json
import requests
from dotenv import load_dotenv
from shodansearch import ShodanSearch
from login_automation import has_valid_credentials


def mostrar_menu():
    """
    Muestra un menú con opciones de búsqueda al usuario.
    """
    print("\nOpciones de búsqueda:")
    print("1. Buscar servidores Apache (predeterminado).")
    print("2. Buscar servidores Nginx.")
    print("3. Buscar cámaras IP.")
    print("4. Buscar dispositivos con contraseñas predeterminadas.")
    print("5. Buscar servidores Redis.")
    print("6. Buscar servidores vulnerables a Log4Shell (CVE-2021-44228).")
    print("7. Introducir una consulta personalizada.")
    opcion = input("\nSelecciona una opción (1-7): ")
    return opcion


def obtener_consulta(opcion):
    """
    Devuelve la consulta de Shodan basada en la opción elegida por el usuario.

    Args:
        opcion (str): La opción seleccionada por el usuario.

    Returns:
        str: La consulta para Shodan.
    """
    consultas = {
        "1": "apache",
        "2": "nginx",
        "3": "webcam",
        "4": "default password",
        "5": "port:6379",
        "6": "vuln:cve-2021-44228",
    }
    if opcion in consultas:
        return consultas[opcion]
    elif opcion == "7":
        return input("Introduce tu consulta personalizada para Shodan: ")
    else:
        print("Opción no válida. Usando la búsqueda predeterminada: Apache.")
        return "apache"


def main():
    """
    Función principal que permite al usuario elegir entre búsquedas predeterminadas o personalizadas,
    ejecuta la consulta en Shodan, y procesa los resultados.
    """
    load_dotenv()
    shodan_api_key = os.getenv("SHODAN_API_KEY")

    if not shodan_api_key:
        raise ValueError("La clave API de SHODAN no está definida en las variables de entorno.")

    shodan_search = ShodanSearch(shodan_api_key)

    # Mostrar menú y obtener consulta
    opcion = mostrar_menu()
    query = obtener_consulta(opcion)

    try:
        resultados = shodan_search.search(query, page=1)
    except Exception as e:
        print(f"Error durante la búsqueda en Shodan: {e}")
        return

    if 'matches' not in resultados or not resultados['matches']:
        print("No se encontraron resultados.")
        return

    dispositivos_validos = []
    for resultado in resultados["matches"]:
        ip = resultado.get("ip_str", "No disponible")
        port = resultado.get("port", 80)
        proto = "https" if resultado.get("ssl") else "http"
        url = f"{proto}://{ip}:{port}/login.php"
        try:
            response = requests.get(url, verify=False, timeout=5)
            if response.status_code in [404, 403]:
                print(f"[!] Excluido {ip}:{port} - Respuesta: {response.status_code}")
                continue
            dispositivos_validos.append(resultado)
        except requests.exceptions.Timeout:
            print(f"[!] Timeout en {ip}:{port}")
            continue
        except requests.exceptions.SSLError as ssl_error:
            print(f"[!] Error SSL en {ip}:{port}: {ssl_error}")
            continue
        except requests.exceptions.RequestException as e:
            print(f"[!] Error al verificar {url}: {e}")
            continue

    for i, dispositivo in enumerate(dispositivos_validos[:10], start=1):
        print(f"\nResultado {i}")
        print(f"Dirección IP: {dispositivo.get('ip_str', 'No disponible')}")
        print(f"Hostnames: {', '.join(dispositivo.get('hostnames', [])) or 'No disponible'}")
        localizacion = dispositivo.get('location', {})
        print("Localización:")
        print(f"  Ciudad: {localizacion.get('city', 'No disponible')}")
        print(f"  Región: {localizacion.get('region_code', 'No disponible')}")
        print(f"  País: {localizacion.get('country_name', 'No disponible')} ({localizacion.get('country_code', 'No disponible')})")
        print(f"  Coordenadas: {localizacion.get('latitude', 'No disponible')}, {localizacion.get('longitude', 'No disponible')}")
        dispositivo["default_credentials"] = has_valid_credentials(dispositivo)
        print(f"Credenciales por defecto: {dispositivo['default_credentials']}")

    # Guarda resultados válidos en un archivo JSON
    with open("resultados_validos.json", "w") as file:
        json.dump(dispositivos_validos, file, indent=4)
    print("\nResultados válidos guardados en 'resultados_validos.json'.")


if __name__ == "__main__":
    main()
