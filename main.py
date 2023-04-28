import os
from PIL import Image
import io
import base64
import requests
import json

path = os.getcwd()
contenido = os.listdir(path)


url_foto = 'http://10.0.3.27/fotos/'


def result(response: requests):
    """
    Devuelve la respuesta en formato de diccionario (array)
    :param response:
    :return: dictionary
    """
    try:
        status = response.status_code
        content = json.loads(response.content)
        return {
            "status_response": status,
            "code": status,
            "data": content
        }
    except Exception as ex:
        return {"response error": ex}


def api_post(end_point: str, params: {}):
    """
    Realiza la llamada Post
    :param end_point:
    :param params:
    :return:
    """
    try:
        return result(requests.post(url_foto + end_point,
                                    json=params))
    except Exception as ex:
        print("Error: ")
        print(ex)
        return {
            "Error": ex
        }


# sprint("--------------------------------------------------------------------------------------------------")
for file in contenido:
    if '.jpg' in file:
        try:
            datos = file.split('.')
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("Procesando fotografia: " + file)

            content = Image.open(path + "/" + file)
            img_bytes_arr = io.BytesIO()
            content.save(img_bytes_arr, format='PNG', subsampling=0, quality=100)
            img_bytes_arr = img_bytes_arr.getvalue()
            imgB64 = base64.b64encode(img_bytes_arr)
            param = {
                "CodigoEmpleado": datos[0],
                "FotografiaB64": imgB64.decode('UTF-8')
            }
            response = api_post('SubirFoto', param)
            response = response['data']
            if response:
                print("Foto actualizada")
            else:
                print("Fotografia no actualizada: " + file)
        except Exception as ex:
            print(ex)
            print("Error al procesar: " + file)
