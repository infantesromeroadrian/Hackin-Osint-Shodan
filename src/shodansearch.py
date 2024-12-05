import shodan


class ShodanSearch:
    """
    Clase para realizar búsquedas utilizando la API de Shodan.
    """

    def __init__(self, api_key: str):
        if not api_key or not isinstance(api_key, str):
            raise ValueError("La clave API proporcionada es inválida o no se encuentra definida.")
        self.client = shodan.Shodan(api_key)

    def search(self, query: str, page: int = 1) -> dict:
        if not query or not isinstance(query, str):
            raise ValueError("La consulta proporcionada es inválida o está vacía.")

        try:
            results = self.client.search(query, page=page)
            return results
        except shodan.APIError as api_error:
            print(f"Error en la API de Shodan: {api_error}")
            return {}
        except Exception as e:
            print(f"Error al realizar la petición a la API de Shodan: {e}")
            return {}
