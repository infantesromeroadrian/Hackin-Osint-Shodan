# OSINT Automation with Shodan and DVWA

Este proyecto utiliza la API de Shodan para automatizar la búsqueda y análisis de servicios y dispositivos accesibles públicamente en Internet. Además, evalúa la seguridad de instancias de DVWA (Damn Vulnerable Web Application) para determinar si tienen credenciales predeterminadas activas.

---

## 🚀 **Características del Proyecto**

1. **Búsqueda en Shodan**:
  - Consulta servidores y dispositivos accesibles en Internet.
  - Filtros predefinidos (por ejemplo, Apache, Nginx, cámaras IP).
  - Opción para realizar consultas personalizadas.

2. **Verificación de Seguridad**:
  - Identifica servidores con contraseñas predeterminadas (por ejemplo, `admin/password`).
  - Evalúa el estado de seguridad de instancias DVWA.

3. **Visualización Geográfica**:
  - Genera mapas interactivos con Folium para mostrar la ubicación de los dispositivos encontrados.

4. **Manejo de Errores**:
  - Reintentos automáticos en conexiones fallidas.
  - Exclusión de servidores con respuestas no válidas (`404`, `403`).

---

## 📂 **Estructura del Proyecto**

```markdown
OSINT/
├── src/
│   ├── login_automation.py     \# Verifica credenciales predeterminadas en servidores DVWA
│   ├── pyshodan.py            \# Script principal para búsquedas y análisis
│   ├── shodansearch.py        \# Clase para interactuar con la API de Shodan
│   ├── mapa_shodan.py         \# Genera mapas interactivos con los resultados
│   ├── resultados_shodan.json \# Resultados crudos obtenidos de Shodan
│   └── resultados_validos.json\# Resultados filtrados con análisis adicional
├── .env                       \# Archivo para almacenar claves de API de forma segura
├── README.md                  \# Documentación del proyecto
```

---

## 📋 **Requisitos Previos**

1. **Python 3.8 o superior**
2. **Bibliotecas necesarias**:
  - `shodan`
  - `requests`
  - `folium`
  - `python-dotenv`
3. **Clave API de Shodan**:
  - Regístrate en [Shodan.io](https://shodan.io) para obtener una clave API.

---

## ⚙️ **Configuración**

1. **Clonar el Repositorio**:
  git clone https://github.com/tu_usuario/osint-shodan.git
  cd osint-shodan

2. **Crear un Entorno Virtual**:
  python -m venv venv
  source venv/bin/activate  # En Windows: .\venv\Scripts\activate

3. **Instalar Dependencias**:
  pip install -r requirements.txt

4. **Configurar la Clave API**:
  Crea un archivo .env en la raíz del proyecto con el siguiente contenido:
  SHODAN_API_KEY=tu_clave_api

## 🧑‍💻 **Uso**

1. **Ejecutar el Script Principal**
  python src/pyshodan.py
  Selecciona entre búsquedas predefinidas (Apache, Nginx, cámaras, etc.) o ingresa tu propia consulta personalizada.

2. **Generar Mapas Interactivos**
  python src/mapa_shodan.py
  Los resultados filtrados se visualizan en un mapa guardado como mapa_shodan.html.

## 🌟 **Funciones Principales**

1. **Búsqueda en Shodan**
  - Usa el menú interactivo para seleccionar la consulta.
  - Los resultados se filtran automáticamente para excluir servidores con errores comunes (404, 403).

2. **Verificación de Credenciales**
  - Los dispositivos se prueban contra credenciales predeterminadas (admin/password).
  - Si las credenciales son válidas, se registra en el análisis.

3. **Exportación de Resultados**
  - resultados_shodan.json: Resultados crudos de Shodan.
  - resultados_validos.json: Resultados filtrados y analizados.

4. **Mapas Interactivos**
  - Los dispositivos válidos se mapean según su ubicación geográfica.
  - Los resultados se visualizan en un archivo HTML (mapa_shodan.html).

## 📖 **Ejemplo de Flujo**

1. **Ejecutar el script principal**:
  Entrada: "apache"
  Salida:
  Resultado 1
  Dirección IP: 192.168.1.1
  Hostnames: ejemplo.com
  Localización:
    Ciudad: Nueva York
    Región: NY
    País: United States (US)
    Coordenadas: 40.7128, -74.0060
  Credenciales por defecto: False

2. **Generar mapa interactivo**:
  - Resultado: mapa_shodan.html con los dispositivos encontrados.

## 🛠️ **Personalización**

1. **Añadir Nuevas Consultas**:
  - Modifica la función mostrar_menu en pyshodan.py para incluir más opciones predefinidas.

2. **Filtrar por País**:
  - Modifica la consulta agregando country:XX, donde XX es el código del país:
  query = "apache country:US"

## ⚠️ **Advertencia Legal**

Este proyecto debe ser utilizado únicamente con fines educativos y éticos. No intentes realizar análisis en dispositivos que no tengas permiso explícito para explorar. El uso indebido de estas herramientas podría violar leyes locales e internacionales.

## 📧 **Contacto**

- Autor: Adrián Infantes
- Correo: infantesromeroadrian@gmail.com
- Proyecto en GitHub: osint-shodan