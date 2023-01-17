import time
from datetime import datetime, timezone
from flask import Flask, request, Response

app = Flask(__name__)

messages = [
    # {'name': 'Tester', 'time': time.time(), 'text': 'Hej!'},
]


@app.route("/send", methods=['POST'])
def send():
    name = request.json.get('name')
    text = request.json.get('text')
    if not (name and isinstance(name, str) and
            text and isinstance(text, str)):
        return Response(status=400)

    message = {'name': name, 'time': time.time(), 'text': text}
    messages.append(message)
    return Response(status=200)


def filter_by_key(elements, key, threshold):
    filtered_elements = []

    for element in elements:
        if element[key] > threshold:
            filtered_elements.append(element)

    return filtered_elements


@app.route("/messages")
def messages_view():
    try:
        after = float(request.args['after'])
    except:
        return Response(status=400)

    filtered = filter_by_key(messages, key='time', threshold=after)
    return {'messages': filtered}


@app.route("/")
def hello():
    return "Hello, World! <a href='/status'>Status</a>"


@app.route("/status")
def status():
    return {
        'status': True,
        'name': 'Simple Messenger',
        'time': time.time(),
        'time1': time.asctime(),
        'time2': datetime.now(),
        'time3': datetime.now().isoformat(),
        'time4': datetime.now(tz=timezone.utc).isoformat(),
        'time5': datetime.now().strftime('%H:%M:%S %Y/%m/%d !'),
    }


app.run()
