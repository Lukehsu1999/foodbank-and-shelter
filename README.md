1. Run webserver

To run, run `poetry run python app.py`

2. Run this to expose ngrok endpoint.

`ngrok http --domain=steady-panda-noted.ngrok-free.app http://127.0.0.1:5000`

3. 

Test with:

```
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"session_id": "Andrew", "input_message": "im hungry"}' \
  https://steady-panda-noted.ngrok-free.app/chat
  ```