# SenVoice SDK

SDK Python asynchrone pour les APIs serverless RunPod (Text-to-Speech et Speech-to-Text) avec support pour 4 modèles distincts.

## 🚀 Fonctionnalités

- **Asynchrone** : Performances optimisées avec `aiohttp` et `asyncio`
- **4 modèles distincts** : TTS/STT pour Français et Wolof
- **Requêtes concurrentes** : Jusqu'à 2x plus rapide que les appels séquentiels
- **Sample rate automatique** : 16000 Hz par défaut pour le Wolof STT
- **Gestion d'erreurs robuste** : Validation complète et exceptions spécialisées
- **Context manager** : Cleanup automatique des sessions HTTP

## Installation

```bash
pip install -r requirements.txt
```

### Dépendances

```txt
requests>=2.25.0
aiohttp>=3.8.0
```

## Architecture

Le SDK SenVoice supporte 4 modèles distincts, chacun avec son propre endpoint_id :

1. **TTS Français** - Synthèse vocale en français
2. **TTS Wolof** - Synthèse vocale en wolof
3. **STT Français** - Reconnaissance vocale en français
4. **STT Wolof** - Reconnaissance vocale en wolof (sample_rate=16000 auto)

## Utilisation

### Configuration de base

```python
import asyncio
from senvoice import SenVoice

async def main():
    async with SenVoice(
        api_key="votre_api_key_runpod",
        tts_fr_endpoint_id="endpoint-tts-francais",
        tts_wo_endpoint_id="endpoint-tts-wolof",
        stt_fr_endpoint_id="endpoint-stt-francais",
        stt_wo_endpoint_id="endpoint-stt-wolof"
    ) as sdk:
        # Utilisation du SDK
        pass

# Exécution
asyncio.run(main())
```

### Text-to-Speech (TTS)

```python
async with SenVoice(api_key="key", ...) as sdk:
    # Synthèse vocale séquentielle
    response_fr = await sdk.tts_fr.synthesize("Bonjour, comment allez-vous ?")
    response_wo = await sdk.tts_wo.synthesize("Salam naka nga deif")

    # Synthèse vocale concurrente (2x plus rapide)
    response_fr, response_wo = await asyncio.gather(
        sdk.tts_fr.synthesize("Bonjour, comment allez-vous ?"),
        sdk.tts_wo.synthesize("Salam naka nga deif")
    )

    print(f"Audio français: {len(response_fr['audio'])} chars")
    print(f"Audio wolof: {len(response_wo['audio'])} chars")
```

### Speech-to-Text (STT)

```python
import asyncio
import base64

async with SenVoice(api_key="key", ...) as sdk:
    # Préparer l'audio en base64
    with open("audio.wav", "rb") as audio_file:
        audio_data = audio_file.read()
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')

    # Transcription séquentielle
    response_fr = await sdk.stt_fr.transcribe(audio_base64)
    response_wo = await sdk.stt_wo.transcribe(audio_base64)  # sample_rate=16000 auto

    # Transcription concurrente (plus rapide)
    results = await asyncio.gather(
        sdk.stt_fr.transcribe(audio_base64),
        sdk.stt_wo.transcribe(audio_base64)
    )

    print(f"Français: {results[0]['transcription']}")
    print(f"Wolof: {results[1]['transcription']}")
```

### Pipeline TTS → STT complet

```python
async with SenVoice(api_key="key", ...) as sdk:
    # 1. Génération d'audio concurrent
    tts_fr_task = sdk.tts_fr.synthesize("Bonjour")
    tts_wo_task = sdk.tts_wo.synthesize("Salam")

    tts_fr_resp, tts_wo_resp = await asyncio.gather(tts_fr_task, tts_wo_task)

    # 2. Transcription concurrent
    stt_tasks = [
        sdk.stt_fr.transcribe(tts_fr_resp['audio']),
        sdk.stt_wo.transcribe(tts_wo_resp['audio'])
    ]

    stt_results = await asyncio.gather(*stt_tasks)

    print(f"Pipeline FR: {stt_results[0]['transcription']}")
    print(f"Pipeline WO: {stt_results[1]['transcription']}")
```

### Test de connectivité

```python
async with SenVoice(api_key="key", ...) as sdk:
    # Test concurrent de tous les services
    ping_results = await sdk.ping_all()

    for service, result in ping_results.items():
        if 'error' in result:
            print(f"❌ {service}: {result['error']}")
        else:
            print(f"✅ {service}: Connected")
```

### Configuration dynamique

```python
async with SenVoice(api_key="key") as sdk:
    # Configurer les endpoints après initialisation
    sdk.configure_tts_fr("nouveau-endpoint-tts-fr")
    sdk.configure_tts_wo("nouveau-endpoint-tts-wo")
    sdk.configure_stt_fr("nouveau-endpoint-stt-fr")
    sdk.configure_stt_wo("nouveau-endpoint-stt-wo")

    # Tester tous les services
    ping_results = await sdk.ping_all()
```

### Utilisation sans context manager

Le context manager `async with` n'est pas obligatoire. Voici les alternatives :

```python
# Initialisation simple
sdk = SenVoice(
    api_key="your_key",
    tts_fr_endpoint_id="endpoint_id",
    # ... autres endpoints
)

try:
    # Utilisation normale
    response = await sdk.tts_fr.synthesize("Hello")
    print(f"Audio: {len(response['audio'])} chars")

    # Tests concurrents
    results = await asyncio.gather(
        sdk.tts_fr.synthesize("Bonjour"),
        sdk.tts_wo.synthesize("Salam")
    )

finally:
    # ⚠️ OBLIGATOIRE : Fermer les sessions HTTP
    await sdk.close()
```

⚠️ **Important** : Sans context manager, vous **devez** appeler `await sdk.close()` pour éviter les fuites de ressources HTTP.

## Gestion des erreurs

Le SDK inclut une gestion d'erreurs complète avec exceptions spécialisées :

```python
from senvoice import SenVoice, AuthenticationError, APIError, ValidationError

async def safe_usage():
    try:
        async with SenVoice(api_key="key", ...) as sdk:
            response = await sdk.tts_fr.synthesize("Hello")
    except AuthenticationError as e:
        print(f"Erreur d'authentification: {e}")
    except APIError as e:
        print(f"Erreur API: {e}")
    except ValidationError as e:
        print(f"Erreur de validation: {e}")
```

## Exemples d'utilisation avancée

### Traitement concurrent de masse

```python
async def process_texts_concurrent(sdk, texts):
    """Traite plusieurs textes en parallèle"""
    tasks = [sdk.tts_fr.synthesize(text) for text in texts]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Erreur pour '{texts[i]}': {result}")
        else:
            print(f"✅ '{texts[i]}' → {len(result['audio'])} chars")
```

### Monitoring et retry

```python
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def robust_synthesize(sdk, text):
    """Synthèse avec retry automatique"""
    return await sdk.tts_fr.synthesize(text)

async def monitor_performance(sdk):
    """Monitoring des performances en temps réel"""
    import time

    start = time.time()
    results = await asyncio.gather(
        sdk.ping_all(),
        sdk.tts_fr.synthesize("Test"),
        sdk.tts_wo.synthesize("Test")
    )
    duration = time.time() - start

    print(f"3 opérations en {duration:.2f}s")
    return results
```

## Fonctionnalités clés

### ✅ **STT Wolof avec sample_rate automatique**

- `sample_rate=16000` ajouté automatiquement pour le wolof
- Personnalisable si nécessaire : `await sdk.stt_wo.transcribe(audio, sample_rate=22050)`
- Validation automatique des paramètres

### ✅ **Architecture modulaire asynchrone**

- 4 modèles indépendants avec leurs propres endpoints
- Sessions HTTP réutilisées pour les performances
- Context manager pour cleanup automatique

### ✅ **Performance optimisée**

- Requêtes concurrentes avec `asyncio.gather()`
- Sessions aiohttp persistantes
- Benchmark intégré dans les exemples

### ✅ **Interface intuitive**

```python
async with SenVoice(api_key="key", ...) as sdk:
    # Séquentiel
    result1 = await sdk.tts_fr.synthesize("Bonjour")
    result2 = await sdk.tts_wo.synthesize("Salam")

    # Concurrent (plus rapide)
    result1, result2 = await asyncio.gather(
        sdk.tts_fr.synthesize("Bonjour"),
        sdk.tts_wo.synthesize("Salam")
    )
```

---

**SenVoice SDK** - Développé pour les applications vocales sénégalaises avec support natif du français et du wolof. 🇸🇳
