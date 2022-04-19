from concurrent.futures import thread
from pynput.keyboard import Key, Listener
import threading
from datetime import datetime
import cv2
import time
import speech_recognition as sr # pip package: 'SpeechRecogn
import pyttsx3 # pip package: same as import
# dependent on the package 'PyAudio'


####
#
# How to run:
#   - install dependencies above
#       - I'm gunna try to find a way to make them all located in this repo
#           - that way Sean won't have to jump through hoops to run ours
#   - change 'face_cascade' to the windows one if necessary
#
####

# windows
# face_cascade = cv2.CascadeClassifier(r'C:/Users/rcanv/Documents/web/Assisted-Selfie/haarcascade_frontalface_default.xml') 
# mac
face_cascade = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')

# for audio processing
r = sr.Recognizer()
engine = pyttsx3.init()
dir_max = 3 # amount of times it will say a response
dir_count = [dir_max, dir_max, dir_max, dir_max] # used to help if no face is recognized
responses = ["top left", "top right", "bottom left", "bottom right"]
responses_str = " ".join(responses)
finished = False
capture = False
# thread_lock = threading.Lock()


# class ttsThread(threading.Thread):
#     def __init__(self, text):
#         threading.Thread.__init__(self)
#         self.text = text

#     def setText(self, text):
#         self.text = text

#     def run(self):
#         thread_lock.acquire()

#         # print("saying...")
#         # engine.say(self.text)
#         # engine.runAndWait()
#         # print("finished.")
        
#         thread_lock.release()

# tts_thread = ttsThread(" ")

def main():
    textToSpeech("welcome to the selfie assistant")
    #print("welcome to the selfie assistant")
    textToSpeech("unfortunately this version of the selfie assistant can not direct you during the selfie process")
    #print("unfortunately this version of the selfie assistant can not direct you during the selfie process")
    textToSpeech("something about freezing the program to talk breaks the video capture and multithreading does not fix it")
    #print("something about freezing the program to talk breaks the video capture and multithreading does not fix it")
    textToSpeech("please wait two seconds after a question is asked to respond thank you")
    #print("please wait two seconds after a question is asked to respond thank you")
    textToSpeech("where would you like your face to be located")
    #print("where would you like your face to be located")
    res = recordAudio()
    #res = "top right"
    print(res)

    while res not in responses:
        textToSpeech("i am sorry " + res + " is not recognized as a location")
        #print("i am sorry " + res + " is not recognized as a location")
        textToSpeech("please choose either " + responses_str)
        #print("please choose either " + responses_str)
        res = None
        res = recordAudio()
        print(res)

    listener = Listener(on_press=on_press, on_release=on_release)
    
    
    listener.start()
    #while not finished:
    captureVideo(res)
    
    #print("out of while loop. finished: " + str(finished))
    listener.stop()


def captureVideo(place):
    global responses, responses_str, finished, capture, dir_count
    face_found = False
    cap = cv2.VideoCapture(0)

    textToSpeech("please click on the window. press space to capture the photo or escape to cancel")
    print("please click on the window. press space to capture the photo or escape to cancel")

    while not finished:
        ret, img = cap.read()

        if not ret:
            print("invalid frame?")
            break

        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        faces = face_cascade.detectMultiScale(gray_img, 1.25, 4) 
        window_w = img.shape[1]
        window_h = img.shape[0]
    
        if len(faces) > 0:
            face_found = True
        else:
            face_found = False

        for (x,y,w,h) in faces: 
            face_loc = (x+w/2, y+h/2)
    
        cv2.imshow('Face Recognition',img) 
        cv2.waitKey(1)

        if capture: # Space
            if not face_found:
                # try to 'randomly' guess where they should move their face
                #textToSpeech("no face was recognized")
                print("no face was recognized")

                if dir_count[0] != 0:
                    #textToSpeech("please move your head to the left")
                    print("please move your head to the left")
                    dir_count[0] -= 1

                elif dir_count[1] != 0:
                    if dir_count[1] == dir_max:
                        #textToSpeech("please move your head back to its original position then move it to the right")
                        print("please move your head back to its original position then move it to the right")
                    else:
                        #textToSpeech("please move your head to the right")
                        print("please move your head to the right")
                    dir_count[1] -= 1

                elif dir_count[2] != 0:
                    if dir_count[2] == dir_max:
                        #textToSpeech("please move your head back to its original position then move it up")
                        print("please move your head back to its original position then move it up")
                    else:
                        #textToSpeech("please move your head up")
                        print("please move your head up")
                    dir_count[2] -= 1

                elif dir_count[3] != 0:
                    if dir_count[3] == dir_max:
                        #textToSpeech("please move your head back to its original position then move it down")
                        print("please move your head back to its original position then move it down")
                    else:
                        #textToSpeech("please move your head down")
                        print("please move your head down")
                    dir_count[3] -= 1
                
                else:
                    for i in range(len(dir_count)):
                        dir_count[i] = dir_max
                    dir_count[0] -= 1
                    #textToSpeech("please move your head back to its original position then to the left")
                    print("please move your head back to its original position then to the left")

                capture = False

            else: # face has been found
                # find the location of the center of their face
                if face_loc[0] < window_w/2 and face_loc[1] < window_h/2:
                    face_quad = "top left"
                elif face_loc[0] > window_w/2 and face_loc[1] < window_h/2:
                    face_quad = "top right"
                elif face_loc[0] < window_w/2 and face_loc[1] > window_h/2:
                    face_quad = "bottom left"
                elif face_loc[0] > window_w/2 and face_loc[1] > window_h/2:
                    face_quad = "bottom right"

                # if face is correctly placed
                if face_quad == place:
                    date_time = datetime.now()
                    file_name = date_time.strftime("selfie_%m%d_%H%M%S.jpg")
                    print(file_name)
                    cv2.imwrite(file_name, img)
                    correct_place = True
                    textToSpeech("photo saved")
                    print("photo saved")
                    textToSpeech("exiting")
                    finished = True
                    break
                
                # if face is incorrectly placed; give helpful instructions
                else:
                    if face_quad == "top left":
                        if place == "top right":        
                            #textToSpeech("please move your head to the left")
                            print("please move your head to the left")
                        elif place == "bottom left":    
                            #textToSpeech("please move your head down")
                            print("please move your head down")
                        elif place == "bottom right":   
                            #textToSpeech("please move your head down and to the left")
                            print("please move your head down and to the left")

                    elif face_quad == "top right":
                        if place == "top left":         
                            #textToSpeech("please move your head to the right")
                            print("please move your head to the right")
                        elif place == "bottom left":    
                            #textToSpeech("please move your head down and to the right")
                            print("please move your head down and to the right")
                        elif place == "bottom right":   
                            #textToSpeech("please move your head down")
                            print("please move your head down")

                    elif face_quad == "bottom left":
                        if place == "top left":         
                            #textToSpeech("please move your head up")
                            print("please move your head up")
                        elif place == "top right":      
                            #textToSpeech("please move your head up and to the left")
                            print("please move your head up and to the left")
                        elif place == "bottom right":   
                            #textToSpeech("please move your head to the left ")
                            print("please move your head to the left ")

                    elif face_quad == "bottom right":
                        if place == "top left":         
                            #textToSpeech("please move your head up and to the right")
                            print("please move your head up and to the right")
                        elif place == "top right":      
                            #textToSpeech("please move your head up")
                            print("please move your head up")
                        elif place == "bottom left":    
                            #textToSpeech("please move your head to the right") 
                            print("please move your head to the right") 

                    capture = False              
    
    cap.release() 
    cv2.destroyAllWindows()
    time.sleep(1)
    


def recordAudio(): # returns lowercase text of audio recorded
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.2)

        print("listening...")
        audio = r.listen(source)

        my_text = r.recognize_google(audio)
        my_text.lower()

        print("recorded: " + my_text)
        return(my_text)


def textToSpeech(command):
    #thread_lock.acquire()

    #tts_thread = ttsThread(command)
    #print("in lock")
    #tts_thread.start()

    #thread_lock.release()
    #print("made it out of lock")
    print("saying: " + command)
    engine.say(command)
    engine.runAndWait()
    print("finished.")


def on_press(key):
    global capture
    print('{0} pressed'.format( key))
    if key == Key.space:
        capture = True

def on_release(key):
    print('{0} release'.format(key))
    if key == Key.esc:
        # Stop listener
        return False


if __name__ == "__main__":
    main()