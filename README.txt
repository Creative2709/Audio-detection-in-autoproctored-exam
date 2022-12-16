The basic idea behind this audio part of the auto proctoring project is capturing 
sound from the microphone when it detects sound and converting it into text using Google’s speech 
recognition API.
   
The stopwords from this text are removed. 

Then a question paper whose stopwords are also removed is compared with this text. 

If the words of text from the candidate's voice and question paper matches. The audio and text files both are 
saved for the reference and we give warning to him.
