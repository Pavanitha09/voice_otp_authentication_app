from flask import Flask, render_template, request, redirect, url_for
from backend import authentication
import os

app = Flask(__name__)

if not os.path.exists('temp'):
    os.makedirs('temp')

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('main.html')

@app.route('/start_verification', methods=['POST'])
def start_verification():
    return redirect(url_for('verification'))

@app.route('/verification', methods=['POST'])
def verification():
    if request.method == 'POST':
        input_file = request.files['input_file']
        speaker_label = request.form['speaker_label']

        temp_path = os.path.join('temp', input_file.filename)
        input_file.save(temp_path)

        result = backend_process(temp_path, speaker_label)
        os.remove(temp_path)

        return result  

    return render_template('verification.html')
 

def backend_process(input_file, speaker_label):
    result = authentication(input_file, speaker_label)
    return "Authentication successful" if result else "Authentication failed"

if __name__ == '__main__':
    app.run(debug=True)
