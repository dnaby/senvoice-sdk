from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="senvoice-sdk",
    version="0.1.0",
    author="Mouhamadou Naby DIA",
    author_email="mouhamadounaby.dia@orange-sonatel.com",
    description="SenVoice SDK - Python SDK for RunPod Serverless APIs (TTS & STT)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/senvoice-sdk",
    packages=find_packages(),
    classifiers=[],
    python_requires=">=3.7",
    install_requires=requirements,
    keywords="senvoice runpod serverless tts stt speech-to-text text-to-speech api sdk wolof french",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/senvoice-sdk/issues",
        "Source": "https://github.com/yourusername/senvoice-sdk",
    },
)
