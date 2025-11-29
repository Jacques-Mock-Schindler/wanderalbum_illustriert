# swisstopo_app.py
import base64
import sys

def create_swisstopo_link(gpx_url):
    """
    Erstellt einen swisstopo-App Link basierend auf einer GPX-URL.
    """
    # 1. URL in Bytes umwandeln (Base64 benötigt Bytes, keine Strings)
    url_bytes = gpx_url.encode('utf-8')
    
    # 2. Base64 codieren
    encoded_bytes = base64.b64encode(url_bytes)
    
    # 3. Bytes zurück in String wandeln, um sie an den Link anzuhängen
    encoded_string = encoded_bytes.decode('utf-8')
    
    # 4. Fertigen Link zurückgeben
    return f"https://swisstopo.app/u/{encoded_string}"

if __name__ == "__main__":
    # Prüfen, ob eine URL übergeben wurde
    if len(sys.argv) > 1:
        url_input = sys.argv[1] # Das erste Argument nach dem Dateinamen
        print(create_swisstopo_link(url_input))
    else:
        print("Bitte eine URL angeben.")