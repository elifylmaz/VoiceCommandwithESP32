import numpy as np
import librosa
import json
import sounddevice as sd
import requests  # HTTP isteği için
from joblib import load
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest

# Etiket haritasını yükle
with open('label_mapping.json', 'r', encoding='utf-8') as f:
    label_mapping = json.load(f)

# Model ve ön işleme nesnelerini yükle
svm_model = load('svm_model_karma_with_probabilities.joblib')
scaler = load('svm_karma_scaler.joblib')
selector = load('svm_selector.joblib')

# ESP32'nin URL bilgisi
ESP_URL = "http://10.42.0.217/command"  # ESP32'nin IP adresi ve komut URL'si

# Özellik çıkarma fonksiyonu
def extract_rich_audio_features_from_audio(audio, sr, n_mfcc=30, max_pad_len=100):
    try:
        mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc)
        pad_width = max_pad_len - mfccs.shape[1]
        if pad_width > 0:
            mfccs = np.pad(mfccs, pad_width=((0, 0), (0, pad_width)), mode='constant')
        else:
            mfccs = mfccs[:, :max_pad_len]

        delta_mfcc = librosa.feature.delta(mfccs)
        delta2_mfcc = librosa.feature.delta(mfccs, order=2)
        spectral_contrast = librosa.feature.spectral_contrast(y=audio, sr=sr)

        features = np.concatenate([
            np.mean(mfccs, axis=1), np.std(mfccs, axis=1),
            np.mean(delta_mfcc, axis=1), np.std(delta_mfcc, axis=1),
            np.mean(delta2_mfcc, axis=1), np.std(delta2_mfcc, axis=1),
            np.mean(spectral_contrast, axis=1), np.std(spectral_contrast, axis=1)
        ])

        return features
    except Exception as e:
        print(f"Error processing audio: {e}")
        return None

# Ses kaydı alma
def record_audio(duration=3, fs=16000):
    print("Ses kaydı başlıyor...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()
    print("Ses kaydı tamamlandı.")
    return audio.flatten(), fs

# ESP32'ye sonuç gönderme
def send_to_esp32(command):
    try:
        data = {"command": command}
        response = requests.post(ESP_URL, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        if response.status_code == 200:
            print(f"Komut {command} başarıyla gönderildi.")
        else:
            print(f"ESP32'ye gönderim sırasında hata oluştu: {response.status_code}")
    except Exception as e:
        print(f"ESP32 bağlantı hatası: {e}")

# Yeni ses kaydında tahmin yapma
def predict_class_from_audio(audio, sr):
    feature = extract_rich_audio_features_from_audio(audio, sr, n_mfcc=30, max_pad_len=100)
    if feature is not None:
        feature = scaler.transform([feature])
        feature = selector.transform(feature)
        decision_scores = svm_model.decision_function(feature)
        predicted_class_index = np.argmax(decision_scores)

        predicted_class = list(label_mapping.keys())[list(label_mapping.values()).index(predicted_class_index)]
        predicted_score = decision_scores[0][predicted_class_index]

        prediction_probability = 100 * (1 / (1 + np.exp(-predicted_score)))
        print(f"Gerçek Zamanlı Tahmin: {predicted_class} sınıfına % {prediction_probability:.2f} olasılıkla aittir.")

        if predicted_class == 'close':
            send_to_esp32("turn_off")
        elif predicted_class == 'open':
            send_to_esp32("turn_on")
        elif predicted_class == 'red':
            send_to_esp32("red")
        elif predicted_class == 'green':
            send_to_esp32("green")
        elif predicted_class == 'blue':
            send_to_esp32("blue")

        return predicted_class, prediction_probability
    else:
        print(f"Özellik çıkarılamadı.")
        return None

print("Real-time ses tanıma başlıyor. Çıkmak için CTRL+C.")
try:
    while True:
        audio, sr = record_audio(duration=3)
        predict_class_from_audio(audio, sr)
except KeyboardInterrupt:
    print("Çıkış yapılıyor.")

