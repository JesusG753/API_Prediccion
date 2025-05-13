from django.shortcuts import render
import requests
import json
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def predict(request):
    if request.method == 'POST':
        try:
            form_data = {
                'masa_corporal': float(request.POST['masa_corporal']),
                'tension_arterial': float(request.POST['tension_arterial']),
                'peso': float(request.POST['peso']),
                'actividad_total': float(request.POST['actividad_total']),
                'medida_cintura': float(request.POST['medida_cintura']),
                'estatura': float(request.POST['estatura']),
                'edad': int(request.POST['edad']),
                'valor_insulina': float(request.POST['valor_insulina']),
                'sueno_horas': float(request.POST['sueno_horas']),
                'valor_colesterol_ldl': float(request.POST['valor_colesterol_ldl'])
            }
            logger.debug(f"Datos del formulario: {form_data}")

            headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
            api_url = f'http://localhost:8001/predict'
            logger.debug(f"URL de la API: {api_url}")
            logger.debug(f"Datos enviados: {json.dumps([form_data])}")

            response = requests.post(
                api_url,
                data=json.dumps([form_data]),
                headers=headers,
                timeout=10  
            )
            response.raise_for_status()  

            # Procesar la respuesta
            result = response.json()
            logger.debug(f"Respuesta de la API: {result}")

            prediction = result['predictions'][0]
            prob_benigno = result['probabilities'][0][0]
            prob_maligno = result['probabilities'][0][1]

            return render(request, 'index.html', {
                'result': {
                    'prediction': prediction,
                    'prob_benigno': prob_benigno,
                    'prob_maligno': prob_maligno,
                }
            })

        except requests.exceptions.ConnectionError as ce:
            logger.error(f"Error de conexión con la API: {str(ce)}")
            return render(request, 'index.html', {'error': 'No se pudo conectar con el servidor de predicción. Asegúrate de que la API esté ejecutándose en http://localhost:8001.'})
        except requests.exceptions.Timeout as te:
            logger.error(f"Timeout al conectar con la API: {str(te)}")
            return render(request, 'index.html', {'error': 'La solicitud al servidor de predicción tomó demasiado tiempo. Intenta de nuevo.'})
        except requests.exceptions.HTTPError as he:
            logger.error(f"Error HTTP al consultar la API: {str(he)}")
            return render(request, 'index.html', {'error': f'Error en la API: {str(he)}'})
        except Exception as e:
            logger.error(f"Error inesperado: {str(e)}")
            return render(request, 'index.html', {'error': f'Error: {str(e)}'})

    return render(request, 'index.html')