"""
Example usage of SenVoice SDK with async support
"""

import asyncio
import os
from senvoice import SenVoice, AuthenticationError, APIError, ValidationError


async def main():
    """Example usage of the SenVoice SDK with async/await"""
    
    # Initialize SDK with environment variables
    try:
        async with SenVoice(
            api_key=os.getenv("RUNPOD_API_KEY", "your_api_key_here"),
            tts_fr_endpoint_id=os.getenv("TTS_FR_ENDPOINT", "your-tts-fr-endpoint-id"),
            tts_wo_endpoint_id=os.getenv("TTS_WO_ENDPOINT", "your-tts-wo-endpoint-id"),
            stt_fr_endpoint_id=os.getenv("STT_FR_ENDPOINT", "your-stt-fr-endpoint-id"),
            stt_wo_endpoint_id=os.getenv("STT_WO_ENDPOINT", "your-stt-wo-endpoint-id")
        ) as sdk:
            print("✅ SenVoice SDK initialized successfully")
            
            # Test connectivity (concurrent pings)
            print("\n🔍 Testing connectivity...")
            try:
                ping_results = await sdk.ping_all()
                for service, result in ping_results.items():
                    if 'error' in result:
                        print(f"❌ {service.upper()}: {result['error']}")
                    else:
                        print(f"✅ {service.upper()}: Connected")
            except Exception as e:
                print(f"❌ Connectivity test failed: {e}")
            
            # TTS Tests (concurrent)
            print("\n🗣️  Testing Text-to-Speech (concurrent)...")
            
            try:
                # Run both TTS requests concurrently
                tts_fr_task = sdk.tts_fr.synthesize("Bonjour, comment allez-vous ?")
                tts_wo_task = sdk.tts_wo.synthesize("Salam naka nga deif")
                
                tts_fr_response, tts_wo_response = await asyncio.gather(
                    tts_fr_task, tts_wo_task, return_exceptions=True
                )
                
                # Process TTS French results
                tts_fr_audio = None
                if isinstance(tts_fr_response, Exception):
                    print(f"❌ TTS French error: {tts_fr_response}")
                else:
                    print(f"✅ TTS French Response: {tts_fr_response.get('text', 'Generated successfully')}")
                    if 'audio' in tts_fr_response:
                        tts_fr_audio = tts_fr_response['audio']
                        print(f"📥 TTS French audio extracted (length: {len(tts_fr_audio)} chars)")
                    else:
                        print("⚠️  No audio found in TTS French response")
                
                # Process TTS Wolof results
                tts_wo_audio = None
                if isinstance(tts_wo_response, Exception):
                    print(f"❌ TTS Wolof error: {tts_wo_response}")
                else:
                    print(f"✅ TTS Wolof Response: {tts_wo_response.get('text', 'Generated successfully')}")
                    if 'audio' in tts_wo_response:
                        tts_wo_audio = tts_wo_response['audio']
                        print(f"📥 TTS Wolof audio extracted (length: {len(tts_wo_audio)} chars)")
                    else:
                        print("⚠️  No audio found in TTS Wolof response")
                
            except Exception as e:
                print(f"❌ TTS concurrent test failed: {e}")
                tts_fr_audio = None
                tts_wo_audio = None
            
            # STT Testing with TTS generated audio (concurrent)
            print("\n🎤 Testing Speech-to-Text with TTS generated audio (concurrent)...")
            
            stt_tasks = []
            stt_descriptions = []
            
            # Prepare STT tasks
            if tts_fr_audio:
                stt_tasks.append(sdk.stt_fr.transcribe(audio_base64=tts_fr_audio))
                stt_descriptions.append("STT French")
            
            if tts_wo_audio:
                stt_tasks.append(sdk.stt_wo.transcribe(audio_base64=tts_wo_audio))
                stt_descriptions.append("STT Wolof")
            
            # Execute STT tasks concurrently
            if stt_tasks:
                stt_results = await asyncio.gather(*stt_tasks, return_exceptions=True)
                
                for description, result in zip(stt_descriptions, stt_results):
                    if isinstance(result, Exception):
                        print(f"❌ {description} error: {result}")
                    else:
                        transcribed_text = result.get('transcription', result)
                        print(f"✅ {description} Response: {transcribed_text}")
            else:
                print("⏭️  No audio available for STT testing")
            
            # Cross-language testing (concurrent)
            print("\n🔄 Testing cross-language transcription (concurrent)...")
            
            cross_tasks = []
            cross_descriptions = []
            
            # Prepare cross-language tasks
            if tts_fr_audio:
                cross_tasks.append(sdk.stt_wo.transcribe(audio_base64=tts_fr_audio))
                cross_descriptions.append("🇫🇷→🇸🇳 French TTS → Wolof STT")
            
            if tts_wo_audio:
                cross_tasks.append(sdk.stt_fr.transcribe(audio_base64=tts_wo_audio))
                cross_descriptions.append("🇸🇳→🇫🇷 Wolof TTS → French STT")
            
            # Execute cross-language tasks concurrently
            if cross_tasks:
                cross_results = await asyncio.gather(*cross_tasks, return_exceptions=True)
                
                for description, result in zip(cross_descriptions, cross_results):
                    if isinstance(result, Exception):
                        print(f"❌ {description} error: {result}")
                    else:
                        transcribed_text = result.get('transcription', result)
                        print(f"✅ {description}: {transcribed_text}")
            else:
                print("⏭️  No audio available for cross-language testing")
            
            # Performance test - concurrent vs sequential
            print("\n⚡ Performance comparison...")
            
            if tts_fr_audio and tts_wo_audio:
                import time
                
                # Sequential test
                start_time = time.time()
                await sdk.stt_fr.transcribe(audio_base64=tts_fr_audio)
                await sdk.stt_wo.transcribe(audio_base64=tts_wo_audio)
                sequential_time = time.time() - start_time
                
                # Concurrent test
                start_time = time.time()
                await asyncio.gather(
                    sdk.stt_fr.transcribe(audio_base64=tts_fr_audio),
                    sdk.stt_wo.transcribe(audio_base64=tts_wo_audio)
                )
                concurrent_time = time.time() - start_time
                
                speedup = sequential_time / concurrent_time if concurrent_time > 0 else 0
                print(f"📊 Sequential: {sequential_time:.2f}s")
                print(f"📊 Concurrent: {concurrent_time:.2f}s")
                print(f"🚀 Speedup: {speedup:.2f}x")
            else:
                print("⏭️  Insufficient audio for performance test")
            
            # Summary
            print("\n📊 Test Summary:")
            print(f"TTS French: {'✅' if tts_fr_audio else '❌'}")
            print(f"TTS Wolof: {'✅' if tts_wo_audio else '❌'}")
            print(f"Audio extraction: {'✅' if (tts_fr_audio or tts_wo_audio) else '❌'}")
            print("🎉 SenVoice SDK async test completed!")
            
    except ValidationError as e:
        print(f"❌ Configuration error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
