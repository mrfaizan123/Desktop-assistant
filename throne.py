import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
import pyjokes
import os
import psutil
import socket
import uuid
import wikipedia
import platform
import subprocess
import speedtest
import logging
import cv2
from datetime import datetime
from PIL import ImageGrab

logging.basicConfig(filename="voice_assistant.log", level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
import requests
import webbrowser
import math

def calculate_expression(expr):
    try:
        # Only allow safe built-in functions and math module
        allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
        result = eval(expr, {"__builtins__": {}}, allowed_names)
        return result
    except Exception as e:
        return "Sorry, I couldn't compute that."

def show_location_on_map():
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()

        location = data.get("loc")  # Format: "latitude,longitude"
        if location:
            maps_url = f"https://www.google.com/maps?q={location}"
            webbrowser.open(maps_url)
            return f"Opening your location on Google Maps."
        else:
            return "Location data not available."
    except Exception as e:
        return "Unable to get your location."

# Example use


camera = None
def sptext():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...!")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            data = recognizer.recognize_google(audio)
            logging.info(f"User said: {data}")
            return data.lower()
        except sr.UnknownValueError:
            
            print("Could not understand audio")
            return None
import cv2

def detect_face():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        # Draw rectangles around faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Show the output
        cv2.imshow("Face Detection", frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Call the function to test

def detect_motion():
    cam = cv2.VideoCapture(0)
    _, frame1 = cam.read()
    _, frame2 = cam.read()
    while True:
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            if cv2.contourArea(c) < 900:
                continue
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.imshow("Motion Detector", frame1)
        frame1 = frame2
        ret, frame2 = cam.read()
        if cv2.waitKey(1) == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()
 
def click_photo():
    # Open camera
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        return "Failed to open camera."

    ret, frame = cap.read()
    cap.release()

    if not ret:
        return "Failed to capture photo."

    # Create folder if it doesn't exist
    save_dir = "Gallery"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Filename with timestamp
    filename = datetime.now().strftime("photo_%Y%m%d_%H%M%S.jpg")
    path = os.path.join(save_dir, filename)

    # Save photo
    cv2.imwrite(path, frame)

    return f"Photo clicked and saved "

def speechtx(x):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    engine.setProperty("rate", 140)
    engine.say(x)
    engine.runAndWait()

def get_ip_address():
    return socket.gethostbyname(socket.gethostname())

def get_mac_address():
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2 * 6, 8)][::-1])
    return mac

def get_disk_space():
    disk = psutil.disk_usage('/')
    return f"Total: {disk.total // (1024 ** 3)} GB, Used: {disk.used // (1024 ** 3)} GB, Free: {disk.free // (1024 ** 3)} GB"

def get_battery_status():
    battery = psutil.sensors_battery()
    if battery:
        return f"Battery is at {battery.percent}% and is {'charging' if battery.power_plugged else 'not charging'}."
    else:
        return "Battery information not available."

def get_cpu_temperature():
    try:
        temps = psutil.sensors_temperatures()
        if temps:
            for name, entries in temps.items():
                for entry in entries:
                    if entry.current:
                        return f"Current CPU temperature is {entry.current}°C."
        return "CPU temperature information not available."
    except:
        return "Unable to fetch CPU temperature."

def take_screenshot():
    screenshot = ImageGrab.grab()
    screenshot.save("screenshot.png")
    return "Screenshot take ."

def lock_system():
    if platform.system() == "Windows":
        os.system("rundll32.exe user32.dll,LockWorkStation")
    elif platform.system() == "Linux":
        os.system("gnome-screensaver-command -l")
    else:
        return "Locking system is not supported on this OS."
    return "System locked."

def test_internet_speed():
    st = speedtest.Speedtest()
    download_speed = st.download() / 1_000_000  # Convert to Mbps
    upload_speed = st.upload() / 1_000_000      # Convert to Mbps
    return f"Download speed: {download_speed:.2f} Mbps, Upload speed: {upload_speed:.2f} Mbps."

def ping_website(website="google.com"):
    try:
        output = subprocess.check_output(f"ping -n 4 {website}", shell=True, universal_newlines=True)
        return output
    except subprocess.CalledProcessError:
        return f"Failed to ping {website}."

def close_application(app_name):
    os.system(f"taskkill /IM {app_name} /F")

def search_and_speak(query):
    if "search on the browser" in query:
        query = query.replace("search on the browser", "").strip()
        speechtx(f"Searching for {query} on the browser.")
        webbrowser.open(f"https://www.google.com/search?q={query}")
    else:
        try:
            # Get Wikipedia summary - first sentence only
            summary = wikipedia.summary(query, sentences=1)
            # Optionally truncate to 300 characters max for speech brevity
            summary = summary.split('.')[0] + '.'  # first sentence only
            if len(summary) > 300:
                summary = summary[:297] + '...'
            speechtx(summary)
        except wikipedia.exceptions.DisambiguationError:
            speechtx(f"There are multiple results for {query}. Try being more specific.")
        except wikipedia.exceptions.PageError:
            speechtx(f"I couldn't find information on {query}. Opening browser for you.")
            webbrowser.open(f"https://www.google.com/search?q={query}")

            
if __name__ == '__main__':
    while True:
        data1 = sptext()
        if data1 is None:
            continue
        if "k" in data1:
            speechtx("System activated. Welcome! You may now ask me any questions or request assistance.")
            speechtx("Say help me if you want help")
        
            while True:
                command = sptext()
                if command is None:
                    continue
                
                if "help" in command:
                    speechtx("Hello! I am your smart assistant, designed by Mohd Faizan.")
                    speechtx("I can help you with many tasks—like checking your system status, opening applications, browsing the internet, and even telling jokes.")
                    speechtx("Just tell me what you need, like 'what is computer', 'open browser',internet speed,disk,cpu,memor usage, or 'what's the time',current location,photo capture. and more")
                    speechtx("Please note, while I strive to assist you accurately, sometimes I might fail or misunderstand. Your patience is appreciated as I keep learning and improving.")
                elif "hello" in command or 'hi' in command:
                    speechtx("Hello! How may I assist you today?")
                elif "your name" in command:
                    speechtx("I am a voice assistant")
                elif "how old are you" in command:
                    speechtx("Not applicable")
                elif "purpose" in command:
                    speechtx("My purpose is to assist you!")
                elif "show my location" in command or "open map" in command or 'current location' in command or 'location' in command:
                    speechtx(show_location_on_map())
   
                elif "thank you" in command or 'good' in command or 'nice' in command or 'thanks' in command or 'thankyou' in command:
                    speechtx("You're welcome!")
                elif "how are you" in command:
                    speechtx("I am fine. How can I assist you?")
                elif "time" in command:
                    current_time = datetime.datetime.now().strftime("%I:%M %p")
                    speechtx(f"The current time is {current_time}")
                elif "date" in command:
                    today_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
                    speechtx(f"Today's date is {today_date}")
                elif "tell me a joke" in command:
                    joke = pyjokes.get_joke()
                    speechtx(joke)
                elif "open google" in command:
                    speechtx("Opening Google")
                    os.system('start chrome "https://www.google.com"')
                elif "close google" in command:
                    speechtx("Closing Google")
                    close_application("chrome.exe")
                elif "search for" in command:
                    query = command.replace("search for", "").strip()
                    speechtx(f"Searching for {query}")
                    webbrowser.open(f"https://www.google.com/search?q={query}")
                elif "open youtube" in command:
                    speechtx("Opening YouTube")
                    os.system('start chrome "https://www.youtube.com"')
                elif "close youtube" in command:
                    speechtx("Closing YouTube")
                    close_application("chrome.exe")
                elif "open whatsapp" in command:
                    speechtx("Opening WhatsApp")
                    os.system("start WhatsApp:")
                elif "close whatsapp" in command:
                    speechtx("Closing WhatsApp")
                    close_application("WhatsApp.exe")
                elif "open notepad" in command:
                    speechtx("Opening Notepad")
                    os.system("notepad")
                elif "close notepad" in command:
                    speechtx("Closing Notepad")
                    close_application("notepad.exe")
                elif "open camera" in command:
                    speechtx("Opening Camera")
                    os.system("start microsoft.windows.camera:")
                elif "close camera" in command:
                    speechtx("Closing Camera")
                    os.system("taskkill /f /im WindowsCamera.exe")
                elif "open calculator" in command:
                    speechtx("Opening Calculator")
                    os.system("calc")
                elif "close calculator" in command:
                    speechtx("Closing Calculator")
                    close_application("calc.exe")
                elif "open command prompt" in command or "open cmd" in command:
                    speechtx("Opening Command Prompt")
                    os.system("cmd.exe")
                elif "cpu usage" in command:
                    usage = psutil.cpu_percent()
                    speechtx(f"CPU usage is at {usage} percent")
                elif "memory status" in command or 'memory' in command:
                    memory = psutil.virtual_memory()
                    speechtx(f"Memory usage is at {memory.percent} percent")
                elif "disk space" in command:
                    speechtx(get_disk_space())
                elif "ip address" in command:
                    speechtx(f"Your IP address is {get_ip_address()}")
                elif "mac address" in command:
                    speechtx(f"Your MAC address is {get_mac_address()}")
                elif "battery status" in command or "battery" in command:
                    speechtx(get_battery_status())
                elif "cpu temperature" in command:
                    speechtx(get_cpu_temperature())
                elif "take screenshot" in command or 'screenshot' in command:
                    speechtx(take_screenshot())
            
                elif "lock system" in command or "sleep" in command:
                    speechtx(lock_system())
                elif "internet speed" in command:
                    speechtx(test_internet_speed())
                elif "ping" in command:
                    
                    speechtx(ping_website())
                elif "calculate" in command or "what is" in command:
                    expression = command.replace("calculate", "").replace("what is", "").strip()
                    result = calculate_expression(expression)
                    speechtx(f"The result is {result}")
    
                elif "shutdown" in command:
                    speechtx("Are you sure you want to shutdown? Say cancel to abort.")
                    confirmation = sptext()
                    if confirmation and "cancel" in confirmation:
                        speechtx("Shutdown cancelled.")
                    else:
                        speechtx("Shutting down in 3 seconds.")
                        os.system("shutdown /s /t 3")
                elif "restart" in command:
                    speechtx("Restart")
                elif "detect face" in command or 'face' in command:
                    speechtx("Starting face detection")
                    detect_face()    
                elif "click photo" in command:
                    result = click_photo()
                    speechtx(result)

                elif "help" in command or 'help me' in command:
                    speechtx("Hello! I am your smart assistant, designed by Mohd Faizan.")
                    speechtx("I can help you with many tasks—like checking your system status, opening applications, browsing the internet, and even telling jokes.")
                    speechtx("Just tell me what you need, like 'what is computer',current location,photo capturing 'open browser', or 'what's the time'.")
                    speechtx("Please note, while I strive to assist you accurately, sometimes I might fail or misunderstand. Your patience is appreciated as I keep learning and improving.")   
                else:
                    
                    speechtx("Let me browse it.")
                    search_and_speak(command)
                 # Start camera once (open camera command)
                

                
 
