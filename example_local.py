"""
Example usage of SenVoice SDK with unified endpoints (no authentication)
"""

import asyncio
import os
from senvoice import SenVoice, AuthenticationError, APIError, ValidationError
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

async def main():
    """Example usage of the SenVoice SDK with unified endpoints"""
    
    print("🚀 SenVoice SDK - Unified Endpoints Example")
    print("=" * 50)
    
    # Initialize SDK with unified endpoints (no API key needed)
    try:
        async with SenVoice(
            # Unified endpoints (no authentication, supports French + Wolof)
            tts_endpoint=os.getenv("TTS_LOCAL_ENDPOINT", "http://localhost:8001"),
            asr_endpoint=os.getenv("ASR_LOCAL_ENDPOINT", "http://localhost:8002")
        ) as sdk:
            print("✅ SenVoice SDK initialized successfully (unified mode)")
            
            # Test ping for all services
            print("\n📡 Testing connectivity...")
            try:
                ping_results = await sdk.ping_all()
                for service, result in ping_results.items():
                    if 'error' in result:
                        print(f"❌ {service}: {result['error']}")
                    else:
                        print(f"✅ {service}: OK")
            except Exception as e:
                print(f"⚠️  Ping test failed: {e}")
            
            # Example texts for synthesis (French and Wolof)
            texts = {
                'fr': "Bonjour, comment allez-vous aujourd'hui ?",
                'wo': "Salam naka nga def ?"
            }
            
            print(f"\n🎤 Text-to-Speech Examples (Unified Model)")
            print("-" * 30)
            
            # TTS Examples using unified endpoint
            tts_results = {}
            
            try:
                # French TTS
                print(f"🇫🇷 Synthesizing French: '{texts['fr']}'")
                tts_fr_response = await sdk.tts.synthesize(texts['fr'])
                tts_results['fr'] = tts_fr_response.get('audio', '')
                print(f"✅ French TTS: {len(tts_results['fr'])} characters")
                
                # Wolof TTS
                print(f"🇸🇳 Synthesizing Wolof: '{texts['wo']}'")
                tts_wo_response = await sdk.tts.synthesize(texts['wo'])
                tts_results['wo'] = tts_wo_response.get('audio', '')
                print(f"✅ Wolof TTS: {len(tts_results['wo'])} characters")
                
            except Exception as e:
                print(f"❌ TTS Error: {e}")
                return
            
            print(f"\n🎧 Speech-to-Text Examples (Unified Model)")
            print("-" * 30)
            
            # STT Examples using unified endpoint (using TTS outputs as inputs)
            try:
                if tts_results.get('fr'):
                    print("🇫🇷 Transcribing French audio...")
                    stt_fr_response = await sdk.asr.transcribe(tts_results['fr'])
                    transcription_fr = stt_fr_response.get('transcription', 'No transcription')
                    print(f"✅ French ASR: '{transcription_fr}'")
                
                if tts_results.get('wo'):
                    print("🇸🇳 Transcribing Wolof audio...")
                    stt_wo_response = await sdk.asr.transcribe(tts_results['wo'])
                    transcription_wo = stt_wo_response.get('transcription', 'No transcription')
                    print(f"✅ Wolof ASR: '{transcription_wo}'")
                
            except Exception as e:
                print(f"❌ ASR Error: {e}")
            
            print(f"\n⚡ Concurrent Processing Example")
            print("-" * 30)
            
            # Concurrent TTS + ASR pipeline
            try:
                # Concurrent TTS for both languages
                print("🔄 Running concurrent TTS...")
                tts_tasks = []
                if sdk._tts_base_url:
                    tts_tasks.append(sdk.tts.synthesize("Test français concurrent"))
                    tts_tasks.append(sdk.tts.synthesize("Test wolof concurrent"))
                
                if tts_tasks:
                    concurrent_tts_results = await asyncio.gather(*tts_tasks, return_exceptions=True)
                    
                    # Process results
                    concurrent_audio = []
                    for i, result in enumerate(concurrent_tts_results):
                        if isinstance(result, Exception):
                            print(f"❌ TTS Task {i+1}: {result}")
                        else:
                            audio = result.get('audio', '')
                            concurrent_audio.append(audio)
                            print(f"✅ TTS Task {i+1}: {len(audio)} characters")
                    
                    # Concurrent ASR on the results
                    if concurrent_audio and sdk._asr_base_url:
                        print("🔄 Running concurrent ASR...")
                        asr_tasks = []
                        for audio in concurrent_audio:
                            asr_tasks.append(sdk.asr.transcribe(audio))
                        
                        if asr_tasks:
                            concurrent_asr_results = await asyncio.gather(*asr_tasks, return_exceptions=True)
                            
                            for i, result in enumerate(concurrent_asr_results):
                                if isinstance(result, Exception):
                                    print(f"❌ ASR Task {i+1}: {result}")
                                else:
                                    transcription = result.get('transcription', 'No transcription')
                                    print(f"✅ ASR Task {i+1}: '{transcription}'")
                
            except Exception as e:
                print(f"❌ Concurrent processing error: {e}")
            
            print(f"\n🎯 Mixed Mode Example (RunPod + Local)")
            print("-" * 30)
            
            # Example of mixing RunPod and local endpoints
            try:
                mixed_sdk = SenVoice(
                    # RunPod TTS endpoint (needs API key)
                    api_key=os.getenv("RUNPOD_API_KEY"),
                    tts_endpoint_id=os.getenv("TTS_ENDPOINT"),
                    # Local ASR endpoint (no auth)
                    asr_endpoint="http://localhost:8002"
                )
                
                print("✅ Mixed mode SDK initialized")
                print("  - TTS (French + Wolof): RunPod (with auth)")
                print("  - ASR (French + Wolof): Local (no auth)")
                
                await mixed_sdk.close()
                
            except Exception as e:
                print(f"⚠️  Mixed mode example: {e}")
            
            print(f"\n✨ All examples completed!")
            
    except ValidationError as e:
        print(f"❌ Validation Error: {e}")
    except AuthenticationError as e:
        print(f"❌ Authentication Error: {e}")
    except APIError as e:
        print(f"❌ API Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())