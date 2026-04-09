import requests
import re

def extract_product_id(url: str) -> int | None:
    try:
        product_id = re.search(r'/producto/(\d+)', url)
        return int(product_id.group(1))
    except Exception as e:
        print(f'Error: {e}')
        return None

def get_product_pcfactory(product_id: int) ->  tuple | None:
    try:
        url_price = f'https://api.pcfactory.cl/pcfactory-services-catalogo/v1/catalogo/productos/{product_id}/precio'
        url_name = f'https://api.pcfactory.cl/pcfactory-services-catalogo/v1/catalogo/productos/{product_id}'
        url_image = f"https://assets.pcfactory.cl/public/foto/{product_id}/1_500.jpg"
        headers = {'User-Agent': 'Mozilla/5.0'}

        response_price = requests.get(url_price, headers=headers)
        response_price.raise_for_status()
        price = response_price.json()

        response_name = requests.get(url_name, headers=headers)
        response_name.raise_for_status()
        name = response_name.json()

        return name['nombre'], price['precio']['efectivo'], url_image
    except Exception as e:
        print(f'Error: {e}')
        return None

def get_product_from_url(url: str) -> tuple | None:
    product_id = extract_product_id(url)
    if product_id is None:
        return None
    return get_product_pcfactory(product_id)