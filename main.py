import cv2
import speech_recognition as sr # pip package: 'SpeechRecogn
import pyttsx3 # pip package: same as import
# dependent on the package 'PyAudio'


####
#
# How to run:
#   - install dependencies above
#       - I'm gunna try to find a way to make them all located in this repo
#           - that way Sean won't have to jump through hoops to run ours
#   - change 'face_cascade' to the windows one
#
#
# Current functions:
#   - main()
#       - main driver of the program
#   - captureVideo()
#       - where I put the code you had before
#       - opens a video window that puts a square over faces it detects
#   - recordAudio()
#       - records audio, returns a lowercase string 
#   - textToSpeech()
#       - takes in a string, audibly says it
#
####


# windows
# face_cascade = cv2.CascadeClassifier(r'C:/Users/rcanv/Documents/web/Assisted-Selfie/haarcascade_frontalface_default.xml') 
# mac
face_cascade = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')

# for audio processing
r = sr.Recognizer()


def main():
    # is there a quicker way to get this across? feels jumbled
    textToSpeech("where would you like your face be located")

    res = recordAudio()
    textToSpeech("you said " + res)


def captureVideo():
    cap = cv2.VideoCapture(0)

    while True:  
        ret, img = cap.read()  
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        faces = face_cascade.detectMultiScale(gray_img, 1.25, 4) 
    
        for (x,y,w,h) in faces: 
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
            rec_gray = gray_img[y:y+h, x:x+w] 
            rec_color = img[y:y+h, x:x+w]   
    
        cv2.imshow('Face Recognition',img) 
    
        k = cv2.waitKey(30) & 0xff
        if k == 27: 
            break
    
    cap.release() 
    cv2.destroyAllWindows()


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
    engine = pyttsx3.init()
    engine.say(command)

    print("saying...")
    engine.runAndWait()
    print("finished.")


if __name__ == "__main__":
    main()