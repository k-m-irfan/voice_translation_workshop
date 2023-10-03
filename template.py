"""
WORKSHOP ON NLP FOR VISION AND SPEECH IMPAIRED

INSTRUCTIONS:
    1. Populate the editable sections with required codes (marked by ==)
    2. Instructions are given under each section
    3. Use the functions created during the titorial session to complete the task
    4. Code for the webapp and server has been provided (marked by //), 
        and do not make any changes in them. Otherswise the forntend 
        app will not work as intended.
    5. If you have any queries you can reach out to any of the coordinators
"""

#import necessary packeges here
from flask import Flask, render_template, request, send_file, jsonify
from flask_socketio import SocketIO
import requests
import json
import base64
import ssl
import io

#=======================================ENDPONTS==========================================
"""Populate the below area with the endpoints"""
# asr_endpoint = # add ASR endpoint here
# mt_endpoint = # add MT endpoint here
# tts_endpoint = # add TTS endpoint here



#=========================================================================================

#////////////////////////////////LEAVE THIS SECTION UNTOUCHED/////////////////////////////

# Initialize flask-socketio app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'
socketio = SocketIO(app,async_mode='gevent', monkey_patch=True)

@app.route('/')
def index():
    return render_template('workshop.html')

@socketio.on('new_user')
def handle_new_user(data):
    client_id = data['id']
    print('\n'+f"New user connected with ID: {client_id}")

@app.route('/play_voice', methods=['POST'])
def play_voice():
    # Extract contents from the payload using their respective keys
    input_language = request.form["language"]
    target_language = request.form["target_language"]
    clientID = request.form["clientId"]   
    audio_file = request.files["audio"]

    # Load the audio data into the io 
    # - avoids saving the audio to the disk to pass into next module
    audio_data = io.BytesIO(audio_file.read())

#//////////////////////////////////////////////////////////////////////////////////////////

    # ASR==================================================================================
    """
    Call the ASR function here to transcribe audio:
    eg; stt = speech_to_text(input_language,audio_data)
    """
    stt = # complete the ASR function call


    #======================================================================================

    #////////////////////////////////LEAVE THIS SECTION UNTOUCHED//////////////////////////
    # message to display on the web app
    responseText = f"<b>Input in {input_language.capitalize()}: </b>" + stt 
    socketio.emit("response", responseText,room=clientID) # emit message to the web app
    #//////////////////////////////////////////////////////////////////////////////////////
    
    #TRANSLATION===========================================================================
    """
    Call the MT function here to convert the text to the target language:
    eg; translation = mt(input_language, target_language, stt)
    """
    translation = # complete the ASR function call
    
    
    #======================================================================================

    #////////////////////////////////LEAVE THIS SECTION UNTOUCHED//////////////////////////
    # message to display on the web app
    responseText = f"<b>Response in {target_language.capitalize()}: </b>" + translation 
    socketio.emit("response", responseText,room=clientID) # emit message to the web app
    #//////////////////////////////////////////////////////////////////////////////////////

    #TTS===================================================================================
    """
    Call the TTS function here to convert the target language text to speech:
    eg; tts = text_to_speech(translation, "female", target_language)
    """
    tts = # complete the TTS function call


    #======================================================================================

    #////////////////////////////////LEAVE THIS SECTION UNTOUCHED//////////////////////////
    decode_string = base64.b64decode(tts)
    audio_stream = io.BytesIO(decode_string)

    responseText = "<b>Converted to speech</b>" 
    socketio.emit("response", responseText, room=clientID)
    # send the audio file to the frontend to play it
    return send_file(audio_stream, mimetype='audio/wav', as_attachment=False)
    #//////////////////////////////////////////////////////////////////////////////////////

#============================ASR, MT, and TTS Functions below==============================
# STT
def speech_to_text(input_language,input_file):
    """
    Complete the ASR API code below
    inputs: input language name and audio data
    returns: response.text
    """


# MT (TTT)
def mt(src_language,tgt_language,transcript):
    """
    Complete the MT API code below
    inputs: source language name, target language name, and source language text
    returns: response['mt_out']
    """


# TTS
def text_to_speech(text,gender,lang):
    """
    Complete the TTS API code below
    inputs: target language text, gender, and target language
    returns: response
    """


#===========================================================================================

#////////////////////////////////LEAVE THIS SECTION UNTOUCHED///////////////////////////////

# Aditional listeners to handle client connections
@socketio.on('connect')
def handle_connect():
    print('\nClient connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('\nClient disconnected')

if __name__ == '__main__':
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain('./certificate.pem','./key.pem')
    socketio.run(app,host='0.0.0.0', port=5000, debug=True, ssl_context=ssl_context)
    
#///////////////////////////////////END OF CODE/////////////////////////////////////////////
