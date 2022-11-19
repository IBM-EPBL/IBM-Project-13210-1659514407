from flask import Flask, request, render_template
import requests

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/y_predict', methods=['POST'])
def y_predict():
    '''
    For rendering results on HTML GUI
    '''
    x_test = [[int(x) for x in request.form.values()]]
    print("xtest= ", x_test)
    # sc = load('scalar.save')

    # NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
    API_KEY = "c0AaDte5MvL14V1NwKhlSgGHH34bvKX_VN8iFiLyAPQ5"
    token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
                                                                                         API_KEY,
                                                                                     "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    mltoken = token_response.json()["access_token"]

    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {
        "input_data": [{"field": [['cylinders', 'displacement', 'horsepower', 'weight', 'model year', 'origin']],
                        "values": x_test}]}

    response_scoring = requests.post(
        'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/pm/predictions?version=2022-11-19',
        json=payload_scoring,
        headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    prediction = response_scoring.json()
    print(prediction)
    output = prediction['predictions'][0]['values'][0]
    output = output[0]
    print(output)
    if (output <= 9):
        pred = "Worst performance with mileage " + str(output) +"mpg. Carry extra fuel"
    if (output > 9 and output <= 17.5):
        pred = "Low performance with mileage " + str(output)+"mpg. Don't go for long distance"
    if (output > 17.5 and output <= 29):
        pred = "Medium performance with mileage " + str(output) + "mpg. Go for a ride nearby."
    if (output > 29 and output <= 46):
        pred = "High performance with mileage " + str(output) +"mpg. Go for a healthy ride"
    if (output > 46):
        pred = "Hurray!! That's a very high performance with mileage" + str(output) +"mpg. You can plan for a Tour"

    return render_template('index.html', prediction_text='{}'.format(pred))


if __name__ == "__main__":
    app.run(debug=True)
