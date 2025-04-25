import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # 話す速さを調整
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    speak("こんにちは！今日はどんなお手伝いをしましょうか？")