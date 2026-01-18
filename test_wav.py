import asyncio
import os
import wave
from senvoice import SenVoice

async def test_pcm_to_wav_tts():
    # Configuration de l'endpoint direct (sans authentification)
    tts_endpoint = "https://p51hh5ou49h1bk-8000.proxy.runpod.net"
    
    print(f"Connexion à l'endpoint TTS : {tts_endpoint}")
    
    # Initialisation du client SenVoice avec l'endpoint local/direct
    async with SenVoice(tts_endpoint=tts_endpoint) as sdk:
        
        text = "Bonjour, ceci est un test du format PCM converti en WAV."
        voice = "mamito"
        # On sauvegarde d'abord les données brutes
        raw_output_file = "temp_output.pcm"
        wav_output_file = "test_output.wav"
        
        print(f"Synthèse en cours (Format: PCM)...")
        print(f"Texte: '{text}'")
        print(f"Voix: '{voice}'")
        
        try:
            # 1. Récupération du flux PCM brut
            pcm_data = bytearray()
            chunk_count = 0
            
            async for chunk in sdk.tts.synthesize_stream(
                text=text,
                voice=voice
            ):
                pcm_data.extend(chunk)
                chunk_count += 1
                print(f"Reçu chunk #{chunk_count} ({len(chunk)} bytes) | Total: {len(pcm_data)} bytes", end="\r")
            
            print(f"\n✅ Réception terminée !")
            
            # 2. Écriture du fichier WAV avec les en-têtes corrects
            # Spécifications : 24kHz, 16-bit (2 bytes), Mono (1 channel)
            sample_rate = 24000
            num_channels = 1
            sample_width = 2  # 16-bit = 2 bytes
            
            print(f"Conversion en WAV ({sample_rate}Hz, Mono, 16-bit)...")
            
            with wave.open(wav_output_file, 'wb') as wav_file:
                wav_file.setnchannels(num_channels)
                wav_file.setsampwidth(sample_width)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(pcm_data)
                
            print(f"✅ Fichier WAV généré avec succès !")
            print(f"Fichier : {wav_output_file}")
            print(f"Taille : {os.path.getsize(wav_output_file)} bytes")
            print(f"Commande de lecture : afplay {wav_output_file} (sur macOS) ou aplay {wav_output_file} (Linux)")
            
        except Exception as e:
            print(f"\n❌ Erreur lors de la synthèse : {e}")

if __name__ == "__main__":
    asyncio.run(test_pcm_to_wav_tts())
