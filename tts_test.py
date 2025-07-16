# ------------------------------------------------------------------
# Script de Inferencia TTS para NeMo (Con Corrección de Dimensión)
# ------------------------------------------------------------------
import torch
import numpy as np
from scipy.io import wavfile
from nemo.collections.tts.models import fastpitch, hifigan

# --- Configuración y Carga de Modelos ---
if torch.cuda.is_available():
    device = torch.device("cuda:0")
    print(f"✅ GPU encontrada: {torch.cuda.get_device_name(0)}")
else:
    print("❌ No se encontró GPU. NeMo requiere una GPU para funcionar.")
    exit()

print("Cargando modelos en la GPU...")
spectrogram_generator = fastpitch.FastPitchModel.from_pretrained("nvidia/tts_en_fastpitch").to(device)
vocoder = hifigan.HifiGanModel.from_pretrained("nvidia/tts_hifigan").to(device)
print("Modelos cargados. Iniciando síntesis de voz...")

# --- Generación de Audio ---
text_to_synthesize = "Hello world! I am alive, and this time, it works."
parsed_text = spectrogram_generator.parse(text_to_synthesize)
spectrogram = spectrogram_generator.generate_spectrogram(tokens=parsed_text)
audio_float32 = vocoder.convert_spectrogram_to_audio(spec=spectrogram)

# --- Guardado de Archivo ---
output_file = "voz_generada.wav"
sample_rate = vocoder.cfg.preprocessor.sample_rate

# --- LA CORRECCIÓN ESTRUCTURAL ---
# 1. Pasamos a NumPy y usamos .squeeze() para convertir el array de (1, N) a (N,)
audio_numpy = audio_float32.to('cpu').detach().numpy().squeeze()

# 2. Hacemos la conversión de tipo a int16, que sigue siendo una buena práctica
audio_int16 = (audio_numpy * 32767).astype(np.int16)

# 3. Escribimos el array 1D de enteros al archivo .wav
wavfile.write(filename=output_file, rate=sample_rate, data=audio_int16)

print(f"🎉 ¡ÉXITO! El audio se ha guardado como '{output_file}'")