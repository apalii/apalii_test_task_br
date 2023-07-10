from collections import defaultdict

from flask import Flask, request, render_template

from fedex_client import FedexWebClient

app = Flask(__name__)
"""
Developer Exercise
We have built api.zenkraft.com to create a common interface for all shipping carrier APIs.
Currently, we have integrations with many of the popular carriers such as FedEx. UPS, DHL,
DPD and more.
The competency exercise is to create an online form where the user can enter a tracking
number and press enter /or click a button. The page will do the following:

1. Accept a FedEx tracking number (122816215025810)

2. When the user clicks ‘Submit’ a callout will be made to FedEx to retrieve tracking

3. The Fedex response should be parsed and converted into a JSON response in the
format similar to what is shown here under the response tab:
https://zenkraft.com/docs/api#track

4. The json response should be display in a div below the ‘submit’ button
"""


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('track.html')

    tracking_number = request.form.get('tracking_number')
    fedex_client = FedexWebClient()
    resp = fedex_client.track(tracking_number)

    track = resp['output']['completeTrackResults'][0]['trackResults'][0]

    dates = defaultdict(lambda: None)
    for obj in track['dateAndTimes']:
        dates[obj['type']] = obj['dateTime']

    return {
        "tracking_number": tracking_number,
        "carrier": track['trackingNumberInfo']['carrierCode'],
        "delivered": True if track['latestStatusDetail']['code'] == 'DL' else False,
        "estimated_delivery": dates['ESTIMATED_DELIVERY'],
        "delivery_date": dates['ACTUAL_DELIVERY'],
        "status": track['latestStatusDetail']['description'],
        "tracking_stage": track['latestStatusDetail']['statusByLocale'],
        "checkpoints": []
    }


if __name__ == '__main__':
    app.run(debug=True)
