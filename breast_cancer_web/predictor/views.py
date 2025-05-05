from django.shortcuts import render
import requests
import json

def predict(request):
    if request.method == 'POST':
        try:
            form_data = {
                'BIRADS': int(request.POST['BI-RADS']),
                'Age': int(request.POST['Age']),
                'Shape': int(request.POST['Shape']),
                'Margin': int(request.POST['Margin']),
                'Density': int(request.POST['Density'])
            }

            headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
            response = requests.post(
                'http://localhost:8001/predict',
                data=json.dumps([form_data]),
                headers=headers
            )
            response.raise_for_status()  

            result = response.json()
            prediction = result['predictions'][0]
            prob_benigno = result['probabilities'][0][0]
            prob_maligno = result['probabilities'][0][1]

            return render(request, 'index.html', {
                'result': {
                    'prediction': prediction,
                    'prob_benigno': prob_benigno,
                    'prob_maligno': prob_maligno
                }
            })

        except Exception as e:
            return render(request, 'index.html', {'error': str(e)})

    return render(request, 'index.html')