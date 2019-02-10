from flask import Flask
from flask import request
from flask import redirect
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse

SID = "AC678590516a6bfbc9e471ec3fc9d7bcb8"
TOKEN = "beb12cb52072e2d4756e8074b252515d"

client = Client(SID, TOKEN)

app = Flask(__name__)

index = "node0"
choice = False
choice_result = "0"
data = None


@app.route('/', methods=['Get', 'Post'])
def start():
    global data
    if request.method == "GET":
        return open("index.html").read()
    else:
        data = request.get_json()
        return "+15204418561"


@app.route("/next", methods=['Get', 'Post'])
def next_step():
    global current
    current = get_next()
    get_cur()
    response = VoiceResponse()
    response.redirect('/cur')
    return str(response)


@app.route("/gather", methods=['Get', 'Post'])
def gather():
    global choice_result
    global choice
    response = VoiceResponse()

    if 'Digits' in request.values:
        # Get which digit the caller chose
        c = request.values['Digits']
        choice_result = c
    else:
        response.say("Sorry, I don't understand that choice.")
        response.redirect("/cur")
    response.redirect('/next')

    return str(response)


@app.route("/cur", methods=['Get', 'Post'])
def get_cur():
    global index, choice
    response = VoiceResponse()
    n = current
    if n["option"] == "speak":
        response.say(message=n["message"])
    elif n["option"] == "directory":
        response.say(message="Directory: ")
        for key, value in n.items():
            if key != "option":
                response.say(message=key + " at " + value)
    elif n["option"] == "end":
        response.hangup()
    elif n["option"] == "redirect":
        response.dial(n['redirect'])
    elif n["option"] == "choice":
        choice = True
        choices = n['choices']
        with response.gather(numDigits=1, action="/gather") as gather:
            for i in range(len(choices)):
                gather.say(message="Press" + str(i) + " to " + choices[i])
        response.redirect("/cur")

    response.redirect('/next')
    return str(response)


def get_next():
    global index
    global choice
    if not choice:
        index = index + "0"
    else:
        index = index + choice_result
        choice = False
    return data[index]
