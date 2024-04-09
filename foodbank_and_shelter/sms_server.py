# This is just for testing
# Steps to reproduce: https://www.twilio.com/docs/sms/tutorials/how-to-receive-and-reply/python
# 1. Run the server
# 2. Open a new terminal, expose the port through ngrok
# 3. Visit the virtual number's setting, edit "A Message Comes in", set the webhook url to ngrok url + "/sms"

from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    request_dict = dict(request.values)
    print("Request dictionary: ", request_dict)
    userId = request_dict['From']
    message = request_dict['Body']
    print("From: "+str(userId)+" Message: "+str(message))

    resp = MessagingResponse()
    
    # need to send Andrew incoming_message and number
    # Add a message
    resp.message("The Robots are coming! Head for the hills!")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True, port=8080)
