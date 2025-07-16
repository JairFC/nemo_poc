# ------------------------------------------------------------------
# Servidor API de Transcripción (STT) con Flask y NeMo
# ------------------------------------------------------------------
import os
import torch
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import nemo.collections.asr as nemo_asr

# --- 1. Carga de Modelo ASR (una sola vez al iniciar) ---
print("Cargando modelo ASR en la GPU... (Esto puede tardar varios minutos la primera vez)")
asr_model = None
try:
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    # Cargar el modelo Parakeet TDT 1.1B desde NGC/HuggingFace
    asr_model = nemo_asr.models.ASRModel.from_pretrained(model_name="nvidia/parakeet-tdt-1.1b").to(device)
    print("✅ Modelo ASR cargado y listo para transcribir.")
except Exception as e:
    print(f"❌ Error crítico al cargar el modelo ASR: {e}")

# --- 2. Inicialización de Flask ---
app = Flask(__name__)

# Directorio para guardar archivos temporales dentro del contenedor
TEMP_DIR = "/tmp/stt_uploads"
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    """
    Endpoint para transcribir un archivo de audio.
    Recibe: multipart/form-data con un campo 'audio_file'.
    Devuelve: JSON {"text": "texto transcrito"}.
    """
    if not asr_model:
        return jsonify({"error": "El modelo ASR no está disponible."}), 503

    if 'audio_file' not in request.files:
        return jsonify({"error": "No se encontró el campo 'audio_file' en la petición"}), 400

    file = request.files['audio_file']
    if file.filename == '':
        return jsonify({"error": "No se seleccionó ningún archivo"}), 400

    if file:
        temp_path = None # Inicializar por si falla antes de la asignación
        try:
            # --- 4. Lógica de Transcripción ---
            filename = secure_filename(file.filename)
            temp_path = os.path.join(TEMP_DIR, filename)
            file.save(temp_path)
            
            # Transcribir el archivo de audio
            with torch.no_grad():
                # La llamada correcta a la API, sin el nombre del argumento
                transcriptions = asr_model.transcribe([temp_path])
            
            # CORRECCIÓN: Extraer el atributo .text del objeto Hypothesis
            transcribed_text = transcriptions[0].text if transcriptions and hasattr(transcriptions[0], 'text') else ""

            # --- 5. Devolver Respuesta ---
            return jsonify({"text": transcribed_text})

        except Exception as e:
            print(f"Error durante la transcripción: {e}")
            return jsonify({"error": "Ocurrió un error interno al procesar el audio."}), 500
        finally:
            # Asegurarse de que el archivo temporal se elimine siempre
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)

# --- 6. Ejecución del Servidor ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)