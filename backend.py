from glob import glob
import numpy as np
import time
import pickle
import nemo.collections.asr as nemo_asr
from statistics import mean, stdev
from sklearn.metrics import accuracy_score
import re
import os
import sys
import re

def speaker_identification(input_file,model_pklfile,ECAPA_TDNN, label):
    embs = ECAPA_TDNN.get_embedding(input_file)
    audio_np = embs.detach().cpu().numpy()
    with open(model_pklfile, 'rb') as file:
        model = pickle.load(file)

    prediction = model.predict(audio_np)
    print("Speaker : label and prediction -", label, prediction[0])
    return label == prediction[0]

def digit_recognition(input_file, VAKYANSH, text_to_digit):
    print(input_file)
    transcription = VAKYANSH.transcribe([input_file])
    label = re.split(r'[\\/]',input_file)[-1].split('.')[0]
    pred =  ""
    for word in transcription[0].split():
        for digit in text_to_digit:
            if word in text_to_digit[digit]:
                pred+=str(digit)
                break
    print("Digit : label and prediction -", label, pred)

    return  label == pred

def authentication(input_file, speaker_label):
    text_to_digit = {}
    text = ["zero","one","two","three","four","five","six","seven","eight","nine"]
    for i in range(10):
        string = text[i]
        text_to_digit[i] = [string[start:start+length] for length in range(2, len(string) + 1) for start in range(len(string) - length + 1)]

    ECAPA_TDNN = nemo_asr.models.EncDecSpeakerLabelModel.from_pretrained(model_name='ecapa_tdnn')
    VAKYANSH = nemo_asr.models.ASRModel.restore_from("English.nemo")
    # input_file = input("Enter the path to the test file : ")
    # speaker_label = input("Enter the speaker ID : ")

    curr_dir = os.getcwd()
    model = curr_dir + "/logreg_models/logreg_local4.pkl"

    label = speaker_label
    s = speaker_identification(input_file,model,ECAPA_TDNN, label)
    d = digit_recognition(input_file, VAKYANSH, text_to_digit)
    print(s, d)
    truth_value = s and d
    return truth_value