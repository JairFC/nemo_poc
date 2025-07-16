# ------------------------------------------------------------------
# Servidor API de Voz con Flask y NeMo (Versión con Streaming)
# ------------------------------------------------------------------
import io
import torch
import numpy as np
from flask import Flask, request, jsonify, Response # Se importa Response
from scipy.io.wavfile import write as write_wav

# Importación correcta de los módulos específicos de NeMo
from nemo.collections.tts.models import fastpitch, hifigan

# --- 1. Carga de Modelos (sin cambios) ---
print("Cargando modelos en la GPU...")
spectrogram_generator = None
vocoder = None
try:
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    spectrogram_generator = fastpitch.FastPitchModel.from_pretrained("nvidia/tts_en_fastpitch").to(device)
    vocoder = hifigan.HifiGanModel.from_pretrained("nvidia/tts_hifigan").to(device)
    print("✅ Modelos cargados y listos para servir.")
except Exception as e:
    print(f"❌ Error crítico al cargar los modelos: {e}")

# --- 2. Inicialización de Flask (sin cambios) ---
app = Flask(__name__)

@app.route('/synthesize', methods=['POST'])
def synthesize():
    """
    Endpoint para sintetizar texto a audio.
    Recibe: JSON {"text": "texto a sintetizar"}
    Devuelve: Un stream de audio en formato WAV.
    """
    if not spectrogram_generator or not vocoder:
        return jsonify({"error": "Los modelos de IA no están disponibles. Revisa los logs del servidor."}), 503

    if not request.is_json:
        return jsonify({"error": "La petición debe ser de tipo JSON"}), 400

    data = request.get_json()
    text_to_synthesize = data.get('text')

    if not text_to_synthesize:
        return jsonify({"error": "La clave 'text' es requerida en el JSON"}), 400

    try:
        # --- 3. Lógica de Síntesis (sin cambios) ---
        with torch.no_grad():
            parsed_text = spectrogram_generator.parse(text_to_synthesize)
            spectrogram = spectrogram_generator.generate_spectrogram(tokens=parsed_text)
            audio_float32 = vocoder.convert_spectrogram_to_audio(spec=spectrogram)

            sample_rate = vocoder.cfg.preprocessor.sample_rate
            audio_numpy = audio_float32.to('cpu').detach().numpy().squeeze()
            audio_int16 = (audio_numpy * 32767).astype(np.int16)

        # --- 4. Crear buffer de audio en memoria (sin cambios) ---
        buffer = io.BytesIO()
        write_wav(buffer, sample_rate, audio_int16)
        buffer.seek(0)

        # --- 5. Implementación del Streaming ---
        def generate_audio_chunks():
            """
            Función generadora que lee el buffer en fragmentos.
            """
            chunk_size = 4096
            while True:
                chunk = buffer.read(chunk_size)
                if not chunk:
                    break
                yield chunk

        # Devolver una respuesta de streaming
        return Response(generate_audio_chunks(), mimetype='audio/wav')

    except Exception as e:
        print(f"Error durante la síntesis: {e}")
        return jsonify({"error": "Ocurrió un error interno al procesar el audio."}), 500

# --- 6. Ejecución del Servidor (sin cambios) ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
