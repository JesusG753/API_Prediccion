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
                'sexo': int(request.POST['sexo']),
                'edad': int(request.POST['edad']),
                'concentracion_hemoglobina': float(request.POST['concentracion_hemoglobina']),
                'temperatura_ambiente': float(request.POST['temperatura_ambiente']),
                'valor_acido_urico': float(request.POST['valor_acido_urico']),
                'valor_albumina': float(request.POST['valor_albumina']),
                'valor_colesterol_hdl': float(request.POST['valor_colesterol_hdl']),
                'valor_colesterol_ldl': float(request.POST['valor_colesterol_ldl']),
                'valor_colesterol_total': float(request.POST['valor_colesterol_total']),
                'valor_creatina': float(request.POST[ 'valor_creatina']),
                'resultado_glucosa': float(request.POST['resultado_glucosa']),
                'valor_insulina': float(request.POST['valor_insulina']),
                'valor_trigliceridos': float(request.POST['valor_trigliceridos']),
                'resultado_glucosa_promedio': float(request.POST['resultado_glucosa_promedio']),
                'valor_hemoglobina_glucosilada': float(request.POST['valor_hemoglobina_glucosilada']),
                'valor_ferritina': float(request.POST['valor_ferritina']),
                'valor_folato': float(request.POST['valor_folato']),
                'valor_homocisteina': float(request.POST['valor_homocisteina']),
                'valor_proteinac_reactiva': float(request.POST['valor_proteinac_reactiva']),
                'valor_transferrina': float(request.POST['valor_transferrina']),
                'valor_vitamina_bdoce': float(request.POST['valor_vitamina_bdoce']),
                'valor_vitamina_d': float(request.POST['valor_vitamina_d']),
                'peso': float(request.POST['peso']),
                'estatura': float(request.POST['estatura']),
                'medida_cintura': float(request.POST['medida_cintura']),
                'segundamedicion_peso': float(request.POST['segundamedicion_peso']),
                'segundamedicion_estatura': float(request.POST['segundamedicion_estatura']),
                'distancia_rodilla_talon': float(request.POST['distancia_rodilla_talon']),
                'circunferencia_de_la_pantorrilla': float(request.POST['circunferencia_de_la_pantorrilla']),
                'segundamedicion_cintura': float(request.POST['segundamedicion_cintura']),
                'tension_arterial': float(request.POST['tension_arterial']),
                'sueno_horas': float(request.POST['sueno_horas']),
                'masa_corporal': float(request.POST['masa_corporal']),
                'actividad_total': float(request.POST['actividad_total'])
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