# SenVoice SDK

SDK Python asynchrone pour les APIs serverless RunPod (Text-to-Speech et Speech-to-Text) avec modèles unifiés supportant le français et le wolof.

## 🚀 Fonctionnalités

- **Asynchrone** : Performances optimisées avec `aiohttp` et `asyncio`
- **Modèles unifiés** : TTS et ASR supportant français et wolof automatiquement
- **Détection automatique de langue** : Plus besoin de spécifier la langue
- **Requêtes concurrentes** : Jusqu'à 2x plus rapide que les appels séquentiels
- **Endpoints flexibles** : Support RunPod (cloud) et endpoints locaux
- **Gestion d'erreurs robuste** : Validation complète et exceptions spécialisées
- **Context manager** : Cleanup automatique des sessions HTTP

## Installation

```bash
pip install git+https://TOKEN@github.com/dnaby/senvoice-sdk.git
```

### Requirements.txt

Pour intégrer SenVoice dans vos projets, ajoutez cette ligne à votre `requirements.txt` :

```txt
senvoice-sdk @ git+https://TOKEN@github.com/dnaby/senvoice-sdk.git
```

## Architecture

Le SDK SenVoice utilise 2 modèles unifiés, chacun supportant automatiquement le français et le wolof :

1. **TTS Unifié** - Synthèse vocale multilingue (français + wolof)
2. **ASR Unifié** - Reconnaissance vocale multilingue (français + wolof)

## Utilisation

### Configuration de base

```python
import asyncio
from senvoice import SenVoice

async def main():
    # Mode RunPod (cloud avec authentification)
    async with SenVoice(
        api_key="votre_api_key_runpod",
        tts_endpoint_id="endpoint-tts-unifie",
        asr_endpoint_id="endpoint-asr-unifie"
    ) as sdk:
        # Utilisation du SDK
        pass

    # Mode local (sans authentification)
    async with SenVoice(
        tts_endpoint="http://localhost:8001",
        asr_endpoint="http://localhost:8002"
    ) as sdk:
        # Utilisation du SDK
        pass

    # Mode mixte (RunPod + Local)
    async with SenVoice(
        api_key="votre_api_key_runpod",
        tts_endpoint_id="runpod-tts-unifie-id",  # RunPod
        asr_endpoint="http://localhost:8002"     # Local
    ) as sdk:
        # Utilisation du SDK
        pass

# Exécution
asyncio.run(main())
```

### Text-to-Speech (TTS)

```python
async with SenVoice(api_key="key", ...) as sdk:
    # Synthèse vocale séquentielle (détection automatique de langue)
    response_fr = await sdk.tts.synthesize("Bonjour, comment allez-vous ?")
    response_wo = await sdk.tts.synthesize("Salam naka nga deif")

    # Synthèse vocale concurrente (2x plus rapide)
    response_fr, response_wo = await asyncio.gather(
        sdk.tts.synthesize("Bonjour, comment allez-vous ?"),
        sdk.tts.synthesize("Salam naka nga deif")
    )

    print(f"Audio français: {len(response_fr['audio'])} chars")
    print(f"Audio wolof: {len(response_wo['audio'])} chars")
```

### Speech-to-Text (ASR)

```python
import asyncio
import base64

async with SenVoice(api_key="key", ...) as sdk:
    # Préparer l'audio en base64
    with open("audio.wav", "rb") as audio_file:
        audio_data = audio_file.read()
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')

    # Transcription avec détection automatique de langue
    response_fr = await sdk.asr.transcribe(audio_base64)  # Détecte automatiquement le français
    response_wo = await sdk.asr.transcribe(audio_base64)  # Détecte automatiquement le wolof

    # Transcription concurrente de plusieurs fichiers
    results = await asyncio.gather(
        sdk.asr.transcribe(audio_base64_fr),
        sdk.asr.transcribe(audio_base64_wo)
    )

    print(f"Transcription 1: {results[0]['transcription']}")
    print(f"Transcription 2: {results[1]['transcription']}")
```

### Pipeline TTS → ASR complet

```python
async with SenVoice(api_key="key", ...) as sdk:
    # 1. Génération d'audio concurrent (détection automatique de langue)
    tts_fr_task = sdk.tts.synthesize("Bonjour")
    tts_wo_task = sdk.tts.synthesize("Salam")

    tts_fr_resp, tts_wo_resp = await asyncio.gather(tts_fr_task, tts_wo_task)

    # 2. Transcription concurrent (détection automatique de langue)
    asr_tasks = [
        sdk.asr.transcribe(tts_fr_resp['audio']),
        sdk.asr.transcribe(tts_wo_resp['audio'])
    ]

    asr_results = await asyncio.gather(*asr_tasks)

    print(f"Pipeline FR: {asr_results[0]['transcription']}")
    print(f"Pipeline WO: {asr_results[1]['transcription']}")
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
    sdk.configure_tts("nouveau-endpoint-tts-unifie")
    sdk.configure_asr("nouveau-endpoint-asr-unifie")

    # Tester tous les services
    ping_results = await sdk.ping_all()
```

### Utilisation sans context manager

Le context manager `async with` n'est pas obligatoire. Voici les alternatives :

```python
# Initialisation simple
sdk = SenVoice(
    api_key="your_key",
    tts_endpoint_id="endpoint_id",
    asr_endpoint_id="asr_endpoint_id"
)

try:
    # Utilisation normale (détection automatique de langue)
    response = await sdk.tts.synthesize("Hello")
    print(f"Audio: {len(response['audio'])} chars")

    # Tests concurrents
    results = await asyncio.gather(
        sdk.tts.synthesize("Bonjour"),
        sdk.tts.synthesize("Salam")
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
            response = await sdk.tts.synthesize("Hello")
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
    """Traite plusieurs textes en parallèle (détection automatique de langue)"""
    tasks = [sdk.tts.synthesize(text) for text in texts]
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
    """Synthèse avec retry automatique (détection automatique de langue)"""
    return await sdk.tts.synthesize(text)

async def monitor_performance(sdk):
    """Monitoring des performances en temps réel"""
    import time

    start = time.time()
    results = await asyncio.gather(
        sdk.ping_all(),
        sdk.tts.synthesize("Test français"),
        sdk.tts.synthesize("Test wolof")
    )
    duration = time.time() - start

    print(f"3 opérations en {duration:.2f}s")
    return results
```

## Fonctionnalités clés

### ✅ **Endpoints flexibles**

- **RunPod (cloud)** : Authentification Bearer token, URLs automatiques
- **Local** : Aucune authentification, URLs directes
- **Mode mixte** : Combinaison RunPod + Local selon vos besoins

### ✅ **Modèles unifiés multilingues**

- Détection automatique de langue (français/wolof)
- Plus besoin de spécifier la langue
- Validation automatique des paramètres

### ✅ **Architecture modulaire asynchrone**

- 2 modèles unifiés avec leurs propres endpoints
- Sessions HTTP réutilisées pour les performances
- Context manager pour cleanup automatique

### ✅ **Performance optimisée**

- Requêtes concurrentes avec `asyncio.gather()`
- Sessions aiohttp persistantes
- Benchmark intégré dans les exemples

### ✅ **Interface intuitive**

```python
async with SenVoice(api_key="key", ...) as sdk:
    # Séquentiel (détection automatique de langue)
    result1 = await sdk.tts.synthesize("Bonjour")
    result2 = await sdk.tts.synthesize("Salam")

    # Concurrent (plus rapide)
    result1, result2 = await asyncio.gather(
        sdk.tts.synthesize("Bonjour"),
        sdk.tts.synthesize("Salam")
    )
```

---

**SenVoice SDK** - Développé pour les applications vocales sénégalaises avec support natif du français et du wolof. 🇸🇳
