import asyncio
import os
from senvoice import SenVoice

async def test_opus_tts():
    # Configuration de l'endpoint direct (sans authentification)
    tts_endpoint = "https://p51hh5ou49h1bk-8000.proxy.runpod.net"
    
    print(f"Connexion à l'endpoint TTS : {tts_endpoint}")
    
    # Initialisation du client SenVoice avec l'endpoint local/direct
    # On passe None pour asr_endpoint_id/tts_endpoint_id car on utilise l'URL directe
    async with SenVoice(tts_endpoint=tts_endpoint) as sdk:
        
        text = "Bonjour, ceci est un test du format Opus avec le SDK SenVoice."
        voice = "mamito"
        output_file = "test_output.ogg"
        
        print(f"Synthèse en cours (Format: OPUS)...")
        print(f"Texte: '{text}'")
        print(f"Voix: '{voice}'")
        
        try:
            # Utilisation du mode streaming pour récupérer les chunks audio directement
            # Le format 'opus' est le défaut, mais on le spécifie explicitement pour le test
            with open(output_file, "wb") as f:
                chunk_count = 0
                total_bytes = 0
                
                async for chunk in sdk.tts.synthesize_stream(
                    text=text,
                    voice=voice,
                    format="opus"
                ):
                    f.write(chunk)
                    chunk_count += 1
                    total_bytes += len(chunk)
                    print(f"Reçu chunk #{chunk_count} ({len(chunk)} bytes)", end="\r")
            
            print(f"\n✅ Synthèse terminée avec succès !")
            print(f"Fichier sauvegardé : {output_file}")
            print(f"Taille totale : {total_bytes} bytes")
            print(f"Nombre de chunks : {chunk_count}")
            
        except Exception as e:
            print(f"\n❌ Erreur lors de la synthèse : {e}")

if __name__ == "__main__":
    asyncio.run(test_opus_tts())
