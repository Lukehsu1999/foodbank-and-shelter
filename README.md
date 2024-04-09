1. Run webserver

To run, run `poetry run python app.py`

2. Get your static Domain. Run this to expose ngrok endpoint.

`ngrok http --domain={static domain} http://127.0.0.1:5000`

3. 

Test with:

```
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"session_id": "Andrew", "input_message": "im hungry"}' \
  https://{your static domain}/chat
```
4. Visit Twilio and find your number, add your endpoint https://{your static domain}/sms in its Messaging Configuration URL