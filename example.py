"""
Example usage of SenVoice SDK with unified endpoints and async support
"""

import asyncio
import os
from senvoice import SenVoice, AuthenticationError, APIError, ValidationError


async def main():
    """Example usage of the SenVoice SDK with unified endpoints and async/await"""
    
    # Initialize SDK with unified endpoints
    try:
        async with SenVoice(
            api_key=os.getenv("RUNPOD_API_KEY", "your_api_key_here"),
            tts_endpoint_id=os.getenv("TTS_ENDPOINT", "your-unified-tts-endpoint-id"),
            asr_endpoint_id=os.getenv("ASR_ENDPOINT", "your-unified-asr-endpoint-id")
        ) as sdk:
            print("✅ SenVoice SDK initialized successfully (unified mode)")
            
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
            
            # TTS Tests (concurrent with unified model)
            print("\n🗣️  Testing Text-to-Speech (unified model, concurrent)...")
            
            try:
                # Run both TTS requests concurrently using unified model
                tts_fr_task = sdk.tts.synthesize("Bonjour, comment allez-vous ?")
                tts_wo_task = sdk.tts.synthesize("Salam naka nga deif")
                
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
            
            # ASR Testing with TTS generated audio (concurrent with unified model)
            print("\n🎤 Testing Speech-to-Text with TTS generated audio (unified model, concurrent)...")
            
            asr_tasks = []
            asr_descriptions = []
            
            # Prepare ASR tasks using unified model
            if tts_fr_audio:
                asr_tasks.append(sdk.asr.transcribe(audio_base64=tts_fr_audio))
                asr_descriptions.append("ASR French")
            
            if tts_wo_audio:
                asr_tasks.append(sdk.asr.transcribe(audio_base64=tts_wo_audio))
                asr_descriptions.append("ASR Wolof")
            
            # Execute ASR tasks concurrently
            if asr_tasks:
                asr_results = await asyncio.gather(*asr_tasks, return_exceptions=True)
                
                for description, result in zip(asr_descriptions, asr_results):
                    if isinstance(result, Exception):
                        print(f"❌ {description} error: {result}")
                    else:
                        transcribed_text = result.get('transcription', result)
                        print(f"✅ {description} Response: {transcribed_text}")
            else:
                print("⏭️  No audio available for ASR testing")
            
            # Language detection testing (unified model automatically detects language)
            print("\n🔄 Testing automatic language detection (unified ASR model)...")
            
            detection_tasks = []
            detection_descriptions = []
            
            # Test unified model's language detection capability
            if tts_fr_audio:
                detection_tasks.append(sdk.asr.transcribe(audio_base64=tts_fr_audio))
                detection_descriptions.append("🇫🇷 French TTS → Unified ASR (auto-detect)")
            
            if tts_wo_audio:
                detection_tasks.append(sdk.asr.transcribe(audio_base64=tts_wo_audio))
                detection_descriptions.append("🇸🇳 Wolof TTS → Unified ASR (auto-detect)")
            
            # Execute language detection tasks concurrently
            if detection_tasks:
                detection_results = await asyncio.gather(*detection_tasks, return_exceptions=True)
                
                for description, result in zip(detection_descriptions, detection_results):
                    if isinstance(result, Exception):
                        print(f"❌ {description} error: {result}")
                    else:
                        transcribed_text = result.get('transcription', result)
                        print(f"✅ {description}: {transcribed_text}")
            else:
                print("⏭️  No audio available for language detection testing")
            
            # Performance test - concurrent vs sequential (unified model)
            print("\n⚡ Performance comparison (unified ASR model)...")
            
            if tts_fr_audio and tts_wo_audio:
                import time
                
                # Sequential test
                start_time = time.time()
                await sdk.asr.transcribe(audio_base64=tts_fr_audio)
                await sdk.asr.transcribe(audio_base64=tts_wo_audio)
                sequential_time = time.time() - start_time
                
                # Concurrent test
                start_time = time.time()
                await asyncio.gather(
                    sdk.asr.transcribe(audio_base64=tts_fr_audio),
                    sdk.asr.transcribe(audio_base64=tts_wo_audio)
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
            print(f"Unified TTS French: {'✅' if tts_fr_audio else '❌'}")
            print(f"Unified TTS Wolof: {'✅' if tts_wo_audio else '❌'}")
            print(f"Audio extraction: {'✅' if (tts_fr_audio or tts_wo_audio) else '❌'}")
            print(f"Unified ASR: {'✅' if (tts_fr_audio or tts_wo_audio) else '❌'}")
            print("🎉 SenVoice SDK unified models test completed!")
            
    except ValidationError as e:
        print(f"❌ Configuration error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
