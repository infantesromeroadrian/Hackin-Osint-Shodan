import folium
import json
import os

def crear_mapa(input_file, output_file="mapa_shodan.html"):
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"El archivo {input_file} no existe.")

    with open(input_file, "r") as file:
        try:
            resultados = json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error al leer el archivo JSON: {e}")

    if "matches" not in resultados or not resultados["matches"]:
        raise ValueError("El archivo JSON no contiene resultados válidos.")

    mapa = folium.Map(location=[20, 0], zoom_start=2)

    for resultado in resultados.get("matches", []):
        location = resultado.get("location", {})
        latitude = location.get("latitude")
        longitude = location.get("longitude")
        ip_address = resultado.get("ip_str", "No disponible")
        hostname = ", ".join(resultado.get("hostnames", [])) or "No disponible"
        ciudad = location.get("city", "No disponible")
        pais = location.get("country_name", "No disponible")
        credenciales = resultado.get("default_credentials", "No disponible")

        color = "green" if credenciales == True else "blue"

        if latitude and longitude:
            popup_info = f"""
            <strong>IP:</strong> {ip_address}<br>
            <strong>Hostnames:</strong> {hostname}<br>
            <strong>Ciudad:</strong> {ciudad}<br>
            <strong>País:</strong> {pais}<br>
            <strong>Credenciales por defecto:</strong> {credenciales}<br>
            """
            folium.Marker(
                location=[latitude, longitude],
                popup=popup_info,
                icon=folium.Icon(color=color, icon="info-sign"),
            ).add_to(mapa)

    mapa.save(output_file)
    print(f"Mapa interactivo creado: {output_file}")


if __name__ == "__main__":
    try:
        crear_mapa("src/resultados_shodan.json")
    except Exception as e:
        print(f"Error: {e}")

