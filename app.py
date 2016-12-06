import os
from flask import Flask, jsonify, request
from faker import Factory
from twilio.access_token import AccessToken, IpMessagingGrant

app = Flask(__name__)
fake = Factory.create()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/token')
def token():
    # get credentials for environment variables
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    api_key = os.environ['TWILIO_API_KEY']
    api_secret = os.environ['TWILIO_API_SECRET']
    service_sid = os.environ['TWILIO_IPM_SERVICE_SID']
    push_credential_sid = os.environ['TWILIO_PUSH_CREDENTIAL_SID']

    identity = request.args.get('identity')
    
    # create a randomly generated username for the client if no query string passed in
    if identity == None:
        identity = fake.user_name()

    # Create a unique endpoint ID for the 
    device_id = request.args.get('device')
    endpoint = "TwilioChatDemo:{0}:{1}".format(identity, device_id)

    # Create access token with credentials
    token = AccessToken(account_sid, api_key, api_secret, identity)

    # Create an IP Messaging grant and add to token
    ipm_grant = IpMessagingGrant(endpoint_id=endpoint, service_sid=service_sid, push_credential_sid=push_credential_sid)
    token.add_grant(ipm_grant)

    # Return token info as JSON
    return jsonify(identity=identity, token=token.to_jwt())

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    # app.run(debug=True)
