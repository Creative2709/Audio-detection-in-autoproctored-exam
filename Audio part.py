import pyaudio
import wave
import audioop
import math
from collections import deque
import speech_recognition as sr  
import wave
import os          
import speech_recognition as sr


def record_on_detect(file_name, silence_limit=4, silence_threshold=1000, chunk=1024, rate=44100, prev_audio=1):
  CHANNELS = 2
  FORMAT = pyaudio.paInt16

  p = pyaudio.PyAudio()
  stream = p.open(format=p.get_format_from_width(2),
                  channels=CHANNELS,
                  rate=rate,
                  input=True,
                  output=False,
                  frames_per_buffer=chunk)

  listen = True
  started = False
  rel = rate/chunk
  frames = []

  prev_audio = deque(maxlen=int(prev_audio * rel))
  slid_window = deque(maxlen=int(silence_limit * rel))

  while listen:
    data = stream.read(chunk)
    slid_window.append(math.sqrt(abs(audioop.avg(data, 4))))

    if(sum([x > silence_threshold for x in slid_window]) > 0):
      if(not started):
        print("Starting record of phrase")
        started = True
    elif (started is True):
      started = False
      listen = False
      prev_audio = deque(maxlen=int(0.5 * rel))

    if (started is True):
      frames.append(data)
    else:
      prev_audio.append(data)

  stream.stop_stream()
  stream.close()

  p.terminate()


  wf = wave.open(f'{file_name}.wav', 'wb')
  wf.setnchannels(CHANNELS)
  wf.setsampwidth(p.get_sample_size(FORMAT))
  wf.setframerate(rate)

  wf.writeframes(b''.join(list(prev_audio)))
  wf.writeframes(b''.join(frames))
  wf.close()
  
def convert():
        
        sound = 'example.wav'
        r = sr.Recognizer()
            
        with sr.AudioFile(sound) as source:
            r.adjust_for_ambient_noise(source)
            print("Converting Audio To Text and saving to file.. . ") 
            audio = r.listen(source)
            
        try:
            value = r.recognize_google(audio)            # API call to google for speech recognition
            #os.remove(sound)      Deletes the audio file
            print(value)
            if str is bytes: 
                result = u"{}".format(value).encode("utf-8")
            else: 
                result = "{}".format(value)

                
            with open("test.txt","w") as f:
                f.write(result)
                f.write(" ")
                f.close()
                    
        except sr.UnknownValueError:
            print("")
        except sr.RequestError as e:
            print("{0}".format(e))
        except KeyboardInterrupt:
            pass
            
        from nltk.corpus import stopwords 
        from nltk.tokenize import word_tokenize 

        file = open("test.txt") ## Student speech file
        data = file.read()
        file.close()
        stop_words = set(stopwords.words('english'))   
        word_tokens = word_tokenize(data) ######### tokenizing sentence
        filtered_sentence = [w for w in word_tokens if not w in stop_words]  
        filtered_sentence = [] 
    
        for w in word_tokens:   ####### Removing stop words
            print(w)
            if w not in stop_words: 
                filtered_sentence.append(w) 
                               
    ##### checking whether proctor needs to be alerted or not
        file = open("question_paper.txt") ## Question file
        data = file.read()
        file.close()
        stop_words = set(stopwords.words('english'))   
        word_tokens = word_tokenize(data) ######### tokenizing sentence
        filtered_questions = [w for w in word_tokens if not w in stop_words]  
        filtered_questions = [] 
    
        for w in word_tokens:   ####### Removing stop words
            if w not in stop_words: 
                filtered_questions.append(w) 
            
        def common_member(a, b):     
            a_set = set(a) 
            b_set = set(b) 
        
            # check length  
            if len(a_set.intersection(b_set)) > 0: 
                return(a_set.intersection(b_set))   
            else: 
                return([]) 

        comm = common_member(filtered_questions, filtered_sentence)
        print('Number of common words spoken by test taker:', len(comm))
        print(comm)
        
        print("Done")
        if(len(comm)):
            print("Stop cheating...")
            
        else:
            os.remove('example.wav')
            print("You are making noise..")
                
            
record_on_detect('example')
convert()