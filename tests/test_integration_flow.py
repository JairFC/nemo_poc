import requests
import pytest

# --- URLs de los servicios locales ---
TTS_URL = "http://localhost:5000/synthesize"
STT_URL = "http://localhost:5001/transcribe"

@pytest.mark.integration
def test_full_tts_to_stt_flow():
    """
    Prueba el flujo completo:
    1. Envía texto al servicio TTS para generar audio.
    2. Toma el audio generado y lo envía al servicio STT.
    3. Verifica que el texto transcrito coincide (aproximadamente) con el original.
    """
    # --- 1. Fase de Texto a Voz (TTS) ---
    text_to_synthesize = "Hello world, this is an integration test."
    tts_payload = {"text": text_to_synthesize}
    
    try:
        tts_response = requests.post(TTS_URL, json=tts_payload, timeout=60)
    except requests.ConnectionError:
        pytest.fail(f"No se pudo conectar al servicio TTS en {TTS_URL}. ¿Está el contenedor en ejecución?")

    # Verificar que la síntesis fue exitosa
    assert tts_response.status_code == 200
    assert tts_response.headers['Content-Type'] == 'audio/wav'
    audio_data = tts_response.content
    assert len(audio_data) > 0, "El servicio TTS devolvió audio vacío."

    # --- 2. Fase de Voz a Texto (STT) ---
    stt_files = {'audio_file': ('test_audio.wav', audio_data, 'audio/wav')}
    
    try:
        stt_response = requests.post(STT_URL, files=stt_files, timeout=60)
    except requests.ConnectionError:
        pytest.fail(f"No se pudo conectar al servicio STT en {STT_URL}. ¿Está el contenedor en ejecución?")

    # Verificar que la transcripción fue exitosa
    assert stt_response.status_code == 200
    stt_json = stt_response.json()
    assert "text" in stt_json

    # --- 3. Fase de Verificación ---
    transcribed_text = stt_json["text"].lower().strip().replace(".", "")
    original_text_normalized = text_to_synthesize.lower().strip().replace(",", "").replace(".", "")
    
    # Comparamos que el texto transcrito sea muy similar al original.
    # Los modelos de transcripción no son perfectos, pero debería ser muy cercano.
    assert transcribed_text == original_text_normalized
    print(f"\nPrueba de integración exitosa:")
    print(f"  - Texto Original: '{text_to_synthesize}'")
    print(f"  - Texto Transcrito: '{stt_json['text']}'")

