import logging
from urllib.parse import urljoin

import requests
import simplejson

LOGGER = logging.getLogger(__name__)


class BaseConfig:
    BASE_URL = "https://apis-sandbox.fedex.com"


class FedexAuthMixin:
    def authenticate(self):
        url = urljoin(BaseConfig.BASE_URL, "/oauth/token")
        payload = {
            "grant_type": "client_credentials",
            "client_id": "l7ecac81c1e42b46ec9eab51a7d8134e09",
            "client_secret": "baf2dbabe32a4a9aa8fb3eac42555329"
        }
        headers = {
            'Content-Type': "application/x-www-form-urlencoded"
        }
        response = requests.post(url, headers=headers, data=payload)
        return response.json()['access_token']


class FedexWebClient(FedexAuthMixin):
    SERVICE_NAME = "Fedex"

    def track(self, tracking_id="797806677146"):
        url = urljoin(BaseConfig.BASE_URL, "/track/v1/trackingnumbers")
        token = self.authenticate()
        payload = {
            "includeDetailedScans": True,
            "trackingInfo": [
                {
                    "trackingNumberInfo": {
                        "trackingNumber": f"{tracking_id}",
                    }
                }
            ]
        }
        headers = {
            'Content-Type': "application/json",
            'Authorization': f"Bearer {token}"
        }
        response = requests.post(url, data=simplejson.dumps(payload), headers=headers)

        return response.json()


"""
{
  "carrier": "fedex",
  "delivered": true,
  "estimated_delivery": "2021-06-07T00:00:00.000Z",
  "delivery_date": "2021-06-07T00:00:00.000Z",
  "tracking_number": "567293923024",
  "status": "Delivered to a mailbox",
  "tracking_stage": "DELIVERED",
  "checkpoints": [
    {
      "description": "Delivered to a mailbox",
      "status": "Delivered to a mailbox",
      "tracking_stage": "DELIVERED",
      "time": "2021-06-07T10:46:07.000+1000"
    }
  ]
}
"""
response = {'transactionId': 'b14581e0-d907-43e6-8cff-d87fd6fccfdb',
            'output': {'completeTrackResults': [{'trackingNumber': '122816215025810',
                                                 'trackResults': [
                                                     {'trackingNumberInfo': {'trackingNumber': '122816215025810',
                                                                             'trackingNumberUniqueId': '12013~122816215025810~FDEG',
                                                                             'carrierCode': 'FDXG'},
                                                      'additionalTrackingInfo': {'nickname': '',
                                                                                 'packageIdentifiers': [
                                                                                     {'type': 'CUSTOMER_REFERENCE',
                                                                                      'values': ['PO#174724'],
                                                                                      'trackingNumberUniqueId': '',
                                                                                      'carrierCode': ''}],
                                                                                 'hasAssociatedShipments': False},
                                                      'shipperInformation': {'address': {'city': 'POST FALLS',
                                                                                         'stateOrProvinceCode': 'ID',
                                                                                         'countryCode': 'US',
                                                                                         'residential': False,
                                                                                         'countryName': 'United States'}},
                                                      'recipientInformation': {'address': {'city': 'NORTON',
                                                                                           'stateOrProvinceCode': 'VA',
                                                                                           'countryCode': 'US',
                                                                                           'residential': False,
                                                                                           'countryName': 'United States'}},
                                                      'latestStatusDetail': {'code': 'DL',
                                                                             'derivedCode': 'DL',
                                                                             'statusByLocale': 'Delivered',
                                                                             'description': 'Delivered',
                                                                             'scanLocation': {'city': 'Norton',
                                                                                              'stateOrProvinceCode': 'VA',
                                                                                              'countryCode': 'US',
                                                                                              'residential': False,
                                                                                              'countryName': 'United States'}},
                                                      'dateAndTimes': [{'type': 'ACTUAL_DELIVERY',
                                                                        'dateTime': '2014-01-09T13:31:00-05:00'},
                                                                       {'type': 'ACTUAL_PICKUP',
                                                                        'dateTime': '2016-08-01T00:00:00-06:00'},
                                                                       {'type': 'SHIP',
                                                                        'dateTime': '2020-08-15T00:00:00-06:00'}],
                                                      'availableImages': [{'type': 'SIGNATURE_PROOF_OF_DELIVERY'}],
                                                      'specialHandlings': [{'type': 'DIRECT_SIGNATURE_REQUIRED',
                                                                            'description': 'Direct Signature Required',
                                                                            'paymentType': 'OTHER'}],
                                                      'packageDetails': {
                                                          'packagingDescription': {'type': 'YOUR_PACKAGING',
                                                                                   'description': 'Package'},
                                                          'physicalPackagingType': 'PACKAGE',
                                                          'sequenceNumber': '1',
                                                          'count': '1',
                                                          'weightAndDimensions': {
                                                              'weight': [{'value': '21.5', 'unit': 'LB'},
                                                                         {'value': '9.75', 'unit': 'KG'}],
                                                              'dimensions': [{'length': 22,
                                                                              'width': 17,
                                                                              'height': 10,
                                                                              'units': 'IN'},
                                                                             {'length': 55, 'width': 43, 'height': 25,
                                                                              'units': 'CM'}]},
                                                          'packageContent': []},
                                                      'shipmentDetails': {'possessionStatus': True},
                                                      'scanEvents': [{'date': '2014-01-09T13:31:00-05:00',
                                                                      'eventType': 'DL',
                                                                      'eventDescription': 'Delivered',
                                                                      'exceptionCode': '',
                                                                      'exceptionDescription': '',
                                                                      'scanLocation': {'streetLines': [''],
                                                                                       'city': 'Norton',
                                                                                       'stateOrProvinceCode': 'VA',
                                                                                       'postalCode': '24273',
                                                                                       'countryCode': 'US',
                                                                                       'residential': False,
                                                                                       'countryName': 'United States'},
                                                                      'locationType': 'DELIVERY_LOCATION',
                                                                      'derivedStatusCode': 'DL',
                                                                      'derivedStatus': 'Delivered'},
                                                                     {'date': '2014-01-09T04:18:00-05:00',
                                                                      'eventType': 'OD',
                                                                      'eventDescription': 'On FedEx vehicle for delivery',
                                                                      'exceptionCode': '',
                                                                      'exceptionDescription': '',
                                                                      'scanLocation': {'streetLines': [''],
                                                                                       'city': 'KINGSPORT',
                                                                                       'stateOrProvinceCode': 'TN',
                                                                                       'postalCode': '37663',
                                                                                       'countryCode': 'US',
                                                                                       'residential': False,
                                                                                       'countryName': 'United States'},
                                                                      'locationId': '0376',
                                                                      'locationType': 'VEHICLE',
                                                                      'derivedStatusCode': 'IT',
                                                                      'derivedStatus': 'In transit'},
                                                                     {'date': '2014-01-09T04:09:00-05:00',
                                                                      'eventType': 'AR',
                                                                      'eventDescription': 'At local FedEx facility',
                                                                      'exceptionCode': '',
                                                                      'exceptionDescription': '',
                                                                      'scanLocation': {'streetLines': [''],
                                                                                       'city': 'KINGSPORT',
                                                                                       'stateOrProvinceCode': 'TN',
                                                                                       'postalCode': '37663',
                                                                                       'countryCode': 'US',
                                                                                       'residential': False,
                                                                                       'countryName': 'United States'},
                                                                      'locationId': '0376',
                                                                      'locationType': 'DESTINATION_FEDEX_FACILITY',
                                                                      'derivedStatusCode': 'IT',
                                                                      'derivedStatus': 'In transit'},
                                                                     {'date': '2014-01-08T23:26:00-05:00',
                                                                      'eventType': 'IT',
                                                                      'eventDescription': 'In transit',
                                                                      'exceptionCode': '',
                                                                      'exceptionDescription': '',
                                                                      'scanLocation': {'streetLines': [''],
                                                                                       'city': 'KNOXVILLE',
                                                                                       'stateOrProvinceCode': 'TN',
                                                                                       'postalCode': '37921',
                                                                                       'countryCode': 'US',
                                                                                       'residential': False,
                                                                                       'countryName': 'United States'},
                                                                      'locationId': '0379',
                                                                      'locationType': 'FEDEX_FACILITY',
                                                                      'derivedStatusCode': 'IT',
                                                                      'derivedStatus': 'In transit'},
                                                                     {'date': '2014-01-08T18:14:07-06:00',
                                                                      'eventType': 'DP',
                                                                      'eventDescription': 'Departed FedEx location',
                                                                      'exceptionCode': '',
                                                                      'exceptionDescription': '',
                                                                      'scanLocation': {'streetLines': [''],
                                                                                       'city': 'NASHVILLE',
                                                                                       'stateOrProvinceCode': 'TN',
                                                                                       'postalCode': '37207',
                                                                                       'countryCode': 'US',
                                                                                       'residential': False,
                                                                                       'countryName': 'United States'},
                                                                      'locationId': '0371',
                                                                      'locationType': 'FEDEX_FACILITY',
                                                                      'derivedStatusCode': 'IT',
                                                                      'derivedStatus': 'In transit'},
                                                                     {'date': '2014-01-08T15:16:00-06:00',
                                                                      'eventType': 'AR',
                                                                      'eventDescription': 'Arrived at FedEx location',
                                                                      'exceptionCode': '',
                                                                      'exceptionDescription': '',
                                                                      'scanLocation': {'streetLines': [''],
                                                                                       'city': 'NASHVILLE',
                                                                                       'stateOrProvinceCode': 'TN',
                                                                                       'postalCode': '37207',
                                                                                       'countryCode': 'US',
                                                                                       'residential': False,
                                                                                       'countryName': 'United States'},
                                                                      'locationId': '0371',
                                                                      'locationType': 'FEDEX_FACILITY',
                                                                      'derivedStatusCode': 'IT',
                                                                      'derivedStatus': 'In transit'},
                                                                     {'date': '2014-01-07T00:29:00-06:00',
                                                                      'eventType': 'AR',
                                                                      'eventDescription': 'Arrived at FedEx location',
                                                                      'exceptionCode': '',
                                                                      'exceptionDescription': '',
                                                                      'scanLocation': {'streetLines': [''],
                                                                                       'city': 'CHICAGO',
                                                                                       'stateOrProvinceCode': 'IL',
                                                                                       'postalCode': '60638',
                                                                                       'countryCode': 'US',
                                                                                       'residential': False,
                                                                                       'countryName': 'United States'},
                                                                      'locationId': '0604',
                                                                      'locationType': 'FEDEX_FACILITY',
                                                                      'derivedStatusCode': 'IT',
                                                                      'derivedStatus': 'In transit'},
                                                                     {'date': '2014-01-03T19:12:30-08:00',
                                                                      'eventType': 'DP',
                                                                      'eventDescription': 'Left FedEx origin facility',
                                                                      'exceptionCode': '',
                                                                      'exceptionDescription': '',
                                                                      'scanLocation': {'streetLines': [''],
                                                                                       'city': 'SPOKANE',
                                                                                       'stateOrProvinceCode': 'WA',
                                                                                       'postalCode': '99216',
                                                                                       'countryCode': 'US',
                                                                                       'residential': False,
                                                                                       'countryName': 'United States'},
                                                                      'locationId': '0992',
                                                                      'locationType': 'ORIGIN_FEDEX_FACILITY',
                                                                      'derivedStatusCode': 'IT',
                                                                      'derivedStatus': 'In transit'},
                                                                     {'date': '2014-01-03T18:33:00-08:00',
                                                                      'eventType': 'AR',
                                                                      'eventDescription': 'Arrived at FedEx location',
                                                                      'exceptionCode': '',
                                                                      'exceptionDescription': '',
                                                                      'scanLocation': {'streetLines': [''],
                                                                                       'city': 'SPOKANE',
                                                                                       'stateOrProvinceCode': 'WA',
                                                                                       'postalCode': '99216',
                                                                                       'countryCode': 'US',
                                                                                       'residential': False,
                                                                                       'countryName': 'United States'},
                                                                      'locationId': '0992',
                                                                      'locationType': 'FEDEX_FACILITY',
                                                                      'derivedStatusCode': 'IT',
                                                                      'derivedStatus': 'In transit'},
                                                                     {'date': '2014-01-03T15:00:00-08:00',
                                                                      'eventType': 'PU',
                                                                      'eventDescription': 'Picked up',
                                                                      'exceptionCode': '',
                                                                      'exceptionDescription': '',
                                                                      'scanLocation': {'streetLines': [''],
                                                                                       'city': 'SPOKANE',
                                                                                       'stateOrProvinceCode': 'WA',
                                                                                       'postalCode': '99216',
                                                                                       'countryCode': 'US',
                                                                                       'residential': False,
                                                                                       'countryName': 'United States'},
                                                                      'locationId': '0992',
                                                                      'locationType': 'PICKUP_LOCATION',
                                                                      'derivedStatusCode': 'PU',
                                                                      'derivedStatus': 'Picked up'},
                                                                     {'date': '2014-01-03T14:31:00-08:00',
                                                                      'eventType': 'OC',
                                                                      'eventDescription': 'Shipment information sent to FedEx',
                                                                      'exceptionCode': '',
                                                                      'exceptionDescription': '',
                                                                      'scanLocation': {'streetLines': [''],
                                                                                       'postalCode': '83854',
                                                                                       'countryCode': 'US',
                                                                                       'residential': False,
                                                                                       'countryName': 'United States'},
                                                                      'locationType': 'CUSTOMER',
                                                                      'derivedStatusCode': 'IN',
                                                                      'derivedStatus': 'Initiated'}],
                                                      'availableNotifications': ['ON_DELIVERY'],
                                                      'deliveryDetails': {'actualDeliveryAddress': {'city': 'Norton',
                                                                                                    'stateOrProvinceCode': 'VA',
                                                                                                    'countryCode': 'US',
                                                                                                    'residential': False,
                                                                                                    'countryName': 'United States'},
                                                                          'locationType': 'SHIPPING_RECEIVING',
                                                                          'locationDescription': 'Shipping/Receiving',
                                                                          'deliveryAttempts': '0',
                                                                          'receivedByName': 'ROLLINS',
                                                                          'deliveryOptionEligibilityDetails': [
                                                                              {'option': 'INDIRECT_SIGNATURE_RELEASE',
                                                                               'eligibility': 'INELIGIBLE'},
                                                                              {'option': 'REDIRECT_TO_HOLD_AT_LOCATION',
                                                                               'eligibility': 'INELIGIBLE'},
                                                                              {'option': 'REROUTE',
                                                                               'eligibility': 'INELIGIBLE'},
                                                                              {'option': 'RESCHEDULE',
                                                                               'eligibility': 'INELIGIBLE'},
                                                                              {'option': 'RETURN_TO_SHIPPER',
                                                                               'eligibility': 'INELIGIBLE'},
                                                                              {'option': 'DISPUTE_DELIVERY',
                                                                               'eligibility': 'INELIGIBLE'},
                                                                              {'option': 'SUPPLEMENT_ADDRESS',
                                                                               'eligibility': 'INELIGIBLE'}]},
                                                      'originLocation': {
                                                          'locationContactAndAddress': {'address': {'city': 'SPOKANE',
                                                                                                    'stateOrProvinceCode': 'WA',
                                                                                                    'countryCode': 'US',
                                                                                                    'residential': False,
                                                                                                    'countryName': 'United States'}}},
                                                      'lastUpdatedDestinationAddress': {'city': 'Norton',
                                                                                        'stateOrProvinceCode': 'VA',
                                                                                        'countryCode': 'US',
                                                                                        'residential': False,
                                                                                        'countryName': 'United States'},
                                                      'serviceDetail': {'type': 'FEDEX_GROUND',
                                                                        'description': 'FedEx Ground',
                                                                        'shortDescription': 'FG'},
                                                      'standardTransitTimeWindow': {
                                                          'window': {'ends': '2016-08-01T00:00:00-06:00'}},
                                                      'estimatedDeliveryTimeWindow': {'window': {}},
                                                      'goodsClassificationCode': '',
                                                      'returnDetail': {}}]}]}}
