import os
from tkinter import *
from keras.models import load_model
import aiml
from gtts import gTTS
from playsound import playsound
import nltk
import numpy as np
import sys
import csv
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import string
from PIL import ImageTk, Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from keras.preprocessing import image
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials
from tkinter import filedialog
import requests, uuid, json
import warnings
warnings.filterwarnings('ignore')
from nltk.sem import Expression
from nltk.inference import ResolutionProver
read_expr = Expression.fromstring

import pandas
kb=[]
data = pandas.read_csv('kb.csv', header=None)
[kb.append(read_expr(row)) for row in data[0]]


kernel = aiml.Kernel()
kernel.setTextEncoding(None)
kernel.bootstrap(learnFiles="chatbot.xml")

a = open('chatbottxt.txt', 'r', errors='ignore')#opens txt file
checkpoint = "./chatbot_weights.ckpt"

raw = a.read()
raw = raw.lower()#converts to lowercase
nltk.download('punkt')
nltk.download('wordnet')
sent_tokens = nltk.sent_tokenize(raw)#converts to list of sentences
word_tokens = nltk.word_tokenize(raw)#converts to list of words

cog_key = 'af5cdf102da44ad4b6f73fb8994e5a00'
cog_endpoint = 'https://chatbotcogservice.cognitiveservices.azure.com/'
cog_region = 'uksouth'
face_client = FaceClient(cog_endpoint, CognitiveServicesCredentials(cog_key))

lemmer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

def response(user_input, usertextlang):
    bot_input = ''
    sent_tokens.append(user_input)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    answer = kernel.respond(user_input)
    
    
    if answer[0] == '#':
        params = answer[1:].split('$')
        cmd = int(params[0])
        
        
        if cmd == 0:
            answer = (params[1])
            text_to_translate = answer
            anstranslation = translate_text(cog_region, cog_key, text_to_translate, to_lang=usertextlang, from_lang='en')
            return anstranslation


        elif cmd == 31: 
            object, subject = params[1].split(' is ')
            expr = read_expr(subject + '(' + object + ')')
            strexpr = str(expr)
            opposite_expr = read_expr('!' + subject + '(' + object + ')')

            contradiction = ResolutionProver().prove(opposite_expr, kb, verbose=True)
            if contradiction:
                answer = 'Cannot be added due to a contradiction'
                text_to_translate = answer
                anstranslation = translate_text(cog_region, cog_key, text_to_translate, to_lang=usertextlang, from_lang='en')
                return anstranslation

            else:
                kb.append(expr)
                hs = open("kb.csv", "a")
                hs.write(strexpr + '\n')
                hs.close()
                answer = ('OK, I will remember that ' + object + ' ' + 'is ' + subject)
                text_to_translate = answer
                anstranslation = translate_text(cog_region, cog_key, text_to_translate, to_lang=usertextlang, from_lang='en')
                return anstranslation

        elif cmd == 32: 
            object, subject = params[1].split(' is ')
            expr = read_expr(subject + '(' + object + ')')
            opposit_expr = read_expr('!' + subject + '(' + object + ')')
            answer = ResolutionProver().prove(expr, kb, verbose=True)
            contradic = ResolutionProver().prove(opposit_expr, kb, verbose=True)
            if answer:
                answer = 'Correct.'
                text_to_translate = answer
                anstranslation = translate_text(cog_region, cog_key, text_to_translate, to_lang=usertextlang, from_lang='en')
                return anstranslation
            else:
                if contradic:
                    answer = 'incorrect'
                    text_to_translate = answer
                    anstranslation = translate_text(cog_region, cog_key, text_to_translate, to_lang=usertextlang, from_lang='en')
                    return anstranslation
                else:
                    answer = 'I dont know'
                    text_to_translate = answer
                    anstranslation = translate_text(cog_region, cog_key, text_to_translate, to_lang=usertextlang, from_lang='en')
                    return anstranslation


        elif cmd == 33:
            object, subject = params[1].split(' is ')
            expr = read_expr(subject + '(' + object + ')')
            strexpr = str(expr)
            answer = ResolutionProver().prove(expr, kb, verbose=True)
            if answer:
                kb.remove(expr)
                lines = list()

                with open('kb.csv', 'r') as readFile:

                    reader = csv.reader(readFile)

                    for row in reader:

                        lines.append(row)

                        for field in row:

                            if field == strexpr:
                                lines.remove(row)

                with open('kb.csv', 'w') as writeFile:

                    writer = csv.writer(writeFile)

                    writer.writerows(lines)
                answer = 'Okay I will remove that'
                text_to_translate = answer
                anstranslation = translate_text(cog_region, cog_key, text_to_translate, to_lang=usertextlang, from_lang='en')
                return anstranslation
            else:
                answer = 'Neither do I'
                text_to_translate = answer
                anstranslation = translate_text(cog_region, cog_key, text_to_translate, to_lang=usertextlang, from_lang='en')
                return anstranslation
        
        elif cmd == 34:
             subject = params[1]
             expr = read_expr (subject)
             group_id = 'lifter_group_id'
             try:
         
                face_client.person_group.delete(group_id)
             except Exception as ex:
                print(ex.message)
             finally:
                face_client.person_group.create(group_id, 'lifters')
                print ('Group created!')
             subject = face_client.person_group_person.create(group_id, str(subject))
             folder_selected = filedialog.askdirectory()
             folder = os.path.join(folder_selected)
             subject_pics = os.listdir(folder)
             i = 0
             fig = plt.figure(figsize=(8, 8))
             for pic in subject_pics:
 
                 img_path = os.path.join(folder, pic)
                 img_stream = open(img_path, "rb")
                 face_client.person_group_person.add_face_from_stream(group_id, subject.person_id, img_stream)

             face_client.person_group.train(group_id)
             return 'Member created!'
             
    elif req_tfidf == [0]:
        answer = kernel.respond(user_input)
        text_to_translate = answer
        anstranslation = translate_text(cog_region, cog_key, text_to_translate, to_lang=usertextlang, from_lang='en')
        return anstranslation

    else:
        bot_input = bot_input + sent_tokens[idx]
        text_to_translate = bot_input
        bottranslation = translate_text(cog_region, cog_key, text_to_translate, to_lang=usertextlang, from_lang='en')
        return bottranslation
        
    
    
def translate_text(cog_region, cog_key, text, to_lang='', from_lang=''):

    path = 'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0'
    params = '&from={}&to={}'.format(from_lang, to_lang)
    constructed_url = path + params

    headers = {
        'Ocp-Apim-Subscription-Key': cog_key,
        'Ocp-Apim-Subscription-Region':cog_region,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': text
    }]

    request = requests.post(constructed_url, headers=headers, json=body)
    response = request.json()
    return response[0]["translations"][0]["text"]
   

def send():

    user_input = EntryText.get("1.0",'end-1c').strip()
    EntryText.delete("0.0",END)
    with open("userinputs.txt", "a") as file:
        file.write(user_input)
    usertext = []
    usertext_text = open('userinputs.txt').read()
    usertexts = {"id": 1, "text": usertext_text}
    usertext.append(usertexts)
    text_analytics_client = TextAnalyticsClient(endpoint=cog_endpoint,credentials=CognitiveServicesCredentials(cog_key))
    language_analysis = text_analytics_client.detect_language(documents=usertext)
    for usertext_num in range(len(usertext)):
        lang = language_analysis.documents[usertext_num].detected_languages[0]
        print(' - Code: {}\n'.format(lang.iso6391_name))
        usertextlang = lang.iso6391_name
    with open("userinputs.txt", "a") as file:
        file.truncate(0)
    text_to_translate = usertext_text
    translation = translate_text(cog_region, cog_key, text_to_translate, to_lang='en', from_lang=usertextlang)
    print('{}{}'.format(text_to_translate,translation))
    
    if translation == "Can you show me a squat":
        img = mpimg.imread('squat.png')
        imgplot = plt.imshow(img)
        plt.show()

    elif translation == "Image":
        new_window = Toplevel(root)
        new_window.geometry("950x1000")
        global imageOpen
        global pred_class
        root.filename = filedialog.askopenfilename(initialdir="/Documents", title="Select Image",
                                                   filetypes=(("jpg files", "*.jpg"), ("all files", "*.*")))
        imagePath = Label
        imageOpen = ImageTk.PhotoImage(Image.open(root.filename))
        imageOpen_label = Label(new_window, image=imageOpen).pack()
        model = load_model('imageModel.h5')
        img_width, img_height = 150, 150
        img1 = image.load_img(root.filename, target_size=(img_width, img_height))
        img = image.img_to_array(img1)
        img = np.expand_dims(img, axis=0)
        class_names = ['bench', 'deadlift', 'squat']
        pred = (model.predict(img))
        pred_class = class_names[np.argmax(pred)]
        
        image_path = os.path.join(root.filename)
        image_stream = open(image_path, "rb")
        image_faces = face_client.face.detect_with_stream(image=image_stream)
        image_face_ids = list(map(lambda face: face.face_id, image_faces))

        group_id = 'lifter_group_id'
        face_names = {}
        recognized_faces = face_client.face.identify(image_face_ids, group_id)
        for face in recognized_faces:
            person_name = face_client.person_group_person.get(group_id, face.candidates[0].person_id).name
            face_names[face.face_id] = person_name
            
            img1 = Image.open(image_path)
            fig = plt.figure(figsize=(8, 6))

            if image_faces:

                num_faces = len(face_names)
                caption = ' (' + str(num_faces) + ' faces recognized)'
 
                for face in image_faces:
                    r = face.face_rectangle
                    bounding_box = ((r.left, r.top), (r.left + r.width, r.top + r.height))
                    draw = ImageDraw.Draw(img1)
                    draw.rectangle(bounding_box, outline='magenta', width=5)
                    if face.face_id in face_names:
                        plt.annotate(face_names[face.face_id],
                                     (r.left, r.top + r.height + 15), backgroundcolor='white')
     
                fig.suptitle(caption)

            plt.axis('off')
            plt.imshow(img1)

        ChatText.config(state=NORMAL)
        ChatText.insert(END, "Bot: This lift is " + pred_class + ' and this lifter is ' + face_names[face.face_id] + "\n\n")
        ChatText.config(font=("Arial", 12))
        imagePredict = Label(new_window, text="This lift is: " + pred_class + " and this lifter is " + face_names[face.face_id]).pack()
        mytext = 'This lift is ' + pred_class + " and the lifter is " + face_names[face.face_id]
        myobj = gTTS(text=mytext, lang=usertextlang, slow=False)
        myobj.save("welcome1.mp3")
        playsound(".\welcome1.mp3")
        os.remove("welcome1.mp3")
     

    elif translation == 'Bye':
        sys.exit()

    else:
        ChatText.config(state=NORMAL)
        ChatText.insert(END, "You: " + user_input + '\n\n')
        ChatText.config(font=("Arial", 12))
        res = response(translation, usertextlang)    
        ChatText.insert(END, "Bot: " + res + '\n\n')
        ChatText.config(state=DISABLED)
        ChatText.yview(END)       
        mytext = res
        myobj = gTTS(text=mytext, lang= usertextlang, slow=False)
        myobj.save("welcome2.mp3")
        playsound(".\welcome2.mp3")
        os.remove("welcome2.mp3")

root = Tk()
root.title("Powerlifting Chatbot")
root.geometry("650x700")
root.resizable(width=TRUE, height=TRUE)

ChatText = Text(root, bd=0, bg="white", height="10", width="55", font=("Arial", 12),)
ChatText.insert(END, "Welcome to Powerlifting chatbot feel free to ask me about powerlifting in any language. \n"
                            "You can ask me to identify any images of powerlifting lifts. Just type 'image'. \n\n"
                            "Type 'bye' to close chatbot." + "\n\n")
ChatText.config(state=DISABLED)
mytext = 'Welcome to powerlifting chatbot feel free to ask me about powerlifting in any language'
myobj = gTTS(text=mytext, lang='en', slow=False)
myobj.save("welcome.mp3")
playsound(".\welcome.mp3")
os.remove("welcome.mp3")

EntryText = Text(root, bd=0, bg="white",width="29", height="5", font="Arial")

ScrollBar = Scrollbar(root, command=ChatText.yview, cursor="heart")
ChatText['yscrollcommand'] = ScrollBar.set

SendButton = Button(root, font=("Arial",12,'bold'), text="Send", width="12", height=5,
                    bd=3,
                    command= send)

ScrollBar.place(x=616,y=6, height=475)
ChatText.place(x=6,y=6, height=475, width=623)
EntryText.place(x=190, y=501, height=170, width=440)
SendButton.place(x=6, y=501, height=170, width=165)

root.mainloop()
