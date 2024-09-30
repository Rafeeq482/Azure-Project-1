import os
import azure.cognitiveservices.speech as speechsdk
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Azure credentials and region
SPEECH_KEY = "b32f134094a2432fa1293380952bfa61"
SPEECH_REGION = "eastus"
TEXT_ANALYTICS_KEY = "d59c070ceefa417687e0b85ddf37a7c8"
TEXT_ANALYTICS_ENDPOINT = "https://lang097867575.cognitiveservices.azure.com/"

# Function to convert speech to text
def speech_to_text():
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Say something...")
    result = recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"Recognized: {result.text}")
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech Recognition canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")

    return ""

# Function to analyze sentiment using Azure Text Analytics
def analyze_sentiment(text):
    credential = AzureKeyCredential(TEXT_ANALYTICS_KEY)
    client = TextAnalyticsClient(endpoint=TEXT_ANALYTICS_ENDPOINT, credential=credential)

    documents = [text]
    response = client.analyze_sentiment(documents=documents)[0]

    print(f"Sentiment: {response.sentiment}")
    print(f"Scores: Positive={response.confidence_scores.positive}; Neutral={response.confidence_scores.neutral}; Negative={response.confidence_scores.negative}")
    
    return response.sentiment, response.confidence_scores

# Function to convert text to speech
def text_to_speech(text):
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized to speaker for text [{}]".format(text))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

# Main function
if __name__ == "__main__":
    text = speech_to_text()
    if text:
        sentiment, scores = analyze_sentiment(text)
        sentiment_text = f"The sentiment of the text is {sentiment} with positive score {scores.positive}, neutral score {scores.neutral}, and negative score {scores.negative}."
        print(f"Sentiment Text: {sentiment_text}")
        text_to_speech(sentiment_text)
    else:
        print("No valid speech input was detected. Please try again.")
