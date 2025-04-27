#!/usr/bin/env python
# -*- coding: utf-8 -*-
# chat-robot.AuzreTTS
# @Calendar: 2025-04-24 21:44
# @Time: 21:44
# @Author: mammon, kiramario
import datetime
import json, os, base64, requests
from os.path import expanduser, expandvars
import azure.cognitiveservices.speech as speechsdk

def get_secrets():
    with open(expanduser('~/chat-robot.env')) as f:
        secrets = json.load(f)
    return secrets["azure"]

azure_secrets = get_secrets()


def recognize_from_microphone():
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription=azure_secrets["voice_demo"]["secret_key_1"],
                                           region=azure_secrets["voice_demo"]["region"])
    speech_config.speech_recognition_language="zh-CN"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Speak into your microphone.")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(speech_recognition_result.text))
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")

def speech_recognize_continuous_async_from_microphone():
    """performs continuous speech recognition asynchronously with input from microphone"""
    speech_config = speechsdk.SpeechConfig(subscription=azure_secrets["voice_demo"]["secret_key_1"],
                                           region=azure_secrets["voice_demo"]["region"])
    # The default language is "en-us".
    speech_config.speech_recognition_language = "zh-CN"
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    done = False

    def recognizing_cb(evt: speechsdk.SpeechRecognitionEventArgs):
        print('RECOGNIZING: {}'.format(evt))

    def recognized_cb(evt: speechsdk.SpeechRecognitionEventArgs):
        print('RECOGNIZED: {}'.format(evt))

    def stop_cb(evt: speechsdk.SessionEventArgs):
        """callback that signals to stop continuous recognition"""
        print('CLOSING on {}'.format(evt))
        nonlocal done
        done = True

    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognizing.connect(recognizing_cb)
    speech_recognizer.recognized.connect(recognized_cb)
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Perform recognition. `start_continuous_recognition_async asynchronously initiates continuous recognition operation,
    # Other tasks can be performed on this thread while recognition starts...
    # wait on result_future.get() to know when initialization is done.
    # Call stop_continuous_recognition_async() to stop recognition.
    result_future = speech_recognizer.start_continuous_recognition_async()

    result_future.get()  # wait for voidfuture, so we know engine initialization is done.
    print('Continuous Recognition is now running, say something.')

    while not done:
        # No real sample parallel work to do on this thread, so just wait for user to type stop.
        # Can't exit function or speech_recognizer will go out of scope and be destroyed while running.
        print('type "stop" then enter when done')
        stop = input()
        if (stop.lower() == "stop"):
            print('Stopping async recognition.')
            speech_recognizer.stop_continuous_recognition_async()
            break

    print("recognition stopped, main thread can exit now.")


def reconginze_from_file():

    # 配置
    speech_key = "你的Azure语音Key"
    service_region = "你的Azure区域"

    # 创建语音识别器
    speech_config = speechsdk.SpeechConfig(subscription=azure_secrets["voice_demo"]["secret_key_1"],
                                           region=azure_secrets["voice_demo"]["region"])

    speech_config.speech_recognition_language = "ja-JP"
    audio_config = speechsdk.AudioConfig(filename="C:\\Users\\mammon\\Desktop\\video_audio\\a1.wav")

    # 开始识别
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # 获取识别结果
    result = speech_recognizer.recognize_once()

    # 打印结果
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("识别到的文本:", result.text)
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("没有识别到语音。")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation = result.cancellation_details
        print("识别取消:", cancellation.reason)
        if cancellation.reason == speechsdk.CancellationReason.Error:
            print("错误详情:", cancellation.error_details)


def run():
    # recognize_from_microphone()
    # speech_recognize_continuous_async_from_microphone()
    reconginze_from_file()

if __name__ == "__main__":
    start = datetime.datetime.now()
    run()
    exec_time = (datetime.datetime.now() - start).total_seconds()
    print(f"run total spend: {exec_time:.3f}s\n")
