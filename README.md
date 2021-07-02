General explanation of the system and its goals

The system is a chatbot created with python on the pycharm ide as I found this was the most suitable ide for the project. The system is a powerlifting chatbot and its goals are to provide a self-service assistance in a user learning about the sport of powerlifting by offering a wealth of information to the user as well as being user-friendly as a chatbot. 

In stage 2 the chatbot now offers the user an image recognition program in which the user selects the image and the chatbot tells the user which powerlifting lift the image is using a keras model.

Stage 3 of the chatbot system introduces a logical knowledgebase which adds user inputs and makes inferences. The aim of stage 3 was to create a first order logic knowledgebase using the NLTK library that can be updated and queried by the user. It will use simple patters to input to the chatbot. Firstly, an initial knowledgebase CSV file will be created with initial facts about powerlifting in NLTK’s FOL syntax. I will also add to the AIML file the patters for the user to enter to input to the CSV file. The goals of the system are to use the patters check that * is * to check a fact is correct in the knowledgebase also, I know that * is * in order to add to the knowledgebase csv.

Stage 4 of the chatbot application introduces azure cognitive services with the textanalyticsclient from the language library and the faceclient from the vision library. The aim of stage 4 was to introduce multi language use of the chatbot meaning any language could be entered to the chatbot and the result be returned in the same language whilst first detecting the user language using the text analytics client.detect_language then using translation to translate first to English then running the command through the chatbot then translating the chatbot output to the language and returning in that language. The additional elements implemented were facial recognition to add more of a user account feel to the chatbot by first entering your name as a username then importing the images for the azure face_client to train with and then using the client to be able to recognize the users face on images of them performing powerlifting movements.

System requirements     

The system has multiple requirements:
-	Include greeting responses for the user
-	Include goodbye responses for the user
-	Include a name response for the user
-	Include general information on the sport of powerlifting
-	Include responses to multiple questions on the sport of powerlifting
-	Include responses to image querying
-	Include indepth information on powerlifting regarding the question
-	Include general chat with the user such as how are you?
-	Include an exit word(bye)
-	Include a title on the ui
-	Include a clause for not understand a question
-	Include a distinguisher between bot input and user input on the ui

Stage 2:
-	Include a gui to use chatbot (feedback from stage 1)
-	Include a file explorer from entering ‘image’
-	Include open file to display the file selected
-	Open file image on new window
-	Display type of lift in chatbot text window using keras model.

Stage 3:
-	Create a CSV knowledgebase file which contains facts.
-	Create at least 10 Knowledgebase facts using NLTK’s First order logic on the topic of powerlifting
-	Extend the current AIML file to include the logical patterns of check that and I know that.
-	Extend the current AIML file to include the logical pattern of I don’t think that which will remove the fact from the knowledgebase.
-	Extend the AIML class to check the knowledgebase integrity.
-	Also add a function to check the user input is not in contradiction with the knowledgebase.
-	Add code in order to check if the query is definitely false to then output ‘incorrect’ or ‘I don’t know’ if it is not found in the knowledgebase.
-	Add code to give the chatbot Text to Speech function using gTTS library.
-	Extend the AIML class to check if query exists then delete said query from the knowledgebase if the user inputs and output an error if it does not exist in the knowledgebase.
-	Extend the AIML class to check if query exists and if not add the query to the knowledgebase CSV and if it contradicts output a contradiction error.
-	Ensure that this runs and outputs to the tkinter gui.

Stage 4:
-	Detecting the user language and storing language code
-	Translating the user language to English using translate_text
-	Find the answer using the chatbot
-	Translate answer back from English to the language code from the user language
-	Store user name using aiml logic into subject
-	Add code to check if group is already exists and print exception
-	Set a group_id for lifters who use chatbot
-	Store username as person_id 
-	Select folder containting images of user
-	Train images using the face_client from the azure faceclient
-	Have the chatbot recognize and identify the user on images of them performing powerlifting movements as they can select images from the previous step using ‘image’ entry.






Explain the employed AI techniques and explanation of your programs

AIML is used in the chatbot, it is an XML based markup language to create artificial intelligence apps. The chatbot will load an XML file that contains all AIML directories and will initialize an infinite loop where it will receive user input. For every input received it will try to match the string with one of the responses available in the AIML file and output an answer. AIML was used for the rule-based components. Various parts of AIML consisting of SRAI, get and set tags, random li tags, think tags.

The Natural Language Toolkit was also used in the development of the chatbot it is a python package for natural language processing, this was used for the similarity based components. This was done using the bag of words model which is a method to extract features from text documents and creates a vocabulary of all the unique words occurring in all the documents in the training set. Also using tfidf which converts a collection of raw documents to a matrix of TFIDF features and is a part of sklearn and also cosine similarity which is also a part of sklearn it computes similarity as the normalized dot product of X and Y. 

Matplotlib was also used which is a plotting library for python it was used to open an image called by the chatbot. 

The program imports all necessary libraries. Then using the kernel trains the xml file containing all aiml files that will be used in the chatbot. The xml file chatbot.xml contains aiml files that use patterns and templates to display answers to users questions. Then using a function to generate bot input using tfidf and cosine similarity to generate an answer from the txt file for the question. Then a while statement to take user input and an if statement for a sys.exit() function and elif to display images using matplotlib if user input matches and finally else statement to print the bot response.


Stage 2

Tkinter which is a library in python is used for the gui of the chatbot to take the user input and display the bot output using the send button. 

Using the .predict function after loading the built model to output the category the model classifies the loaded image into whether that be bench, deadlift or squat and display using the .insert function of tkinter.

Using .listdir as part of the os library to open the input data for the training model and creating the different categories for the dataframe. Then used the keras model to train using category and categorical crossentropy to classify images into categories rather than binary as there is more than 2 categories. It is then trained using 200 epochs with 10 steps per epoch as this was the right amount to attain over 0.85 val accuracy. The data was prepared using image data generator.

The program imports all necessary libraries. Then using the kernel trains the xml file containing all aiml files that will be used in the chatbot. The xml file chatbot.xml contains aiml files that use patterns and templates to display answers to users questions. Then using a function to generate bot input using tfidf and cosine similarity to generate an answer from the txt file for the question. Then a while statement to take user input and an if statement for a sys.exit() function and elif to display images using matplotlib if user input matches and finally else statement to print the bot response.

Using the tkinter library to create the gui for the chatbot using the Tk library by creating each widget and placing on the gui such as the entry text box, the chattext box and also the send button and scroll bar. Using else if statements to output different responses for each user input and if a user inputs image then using .file to open file explorer and using .photoimage to open the file selected. Then using .predict for the keras model to predict which category the image is in and output the category using .insert into the chattext box.


Stage 3
 
A knowledgebase in csv which contains the facts regarding the powerlifting topic the facts will be created in First Order Logic which uses quantified variables over non-logical objects so it allows sentences that contain variables, rather than propositions, this allows expressions to be parsed into expression objects (e.g. British -> European) which means British is European. 

The AIML xml file includes the new logical patterns which will be used by the user in order to query/append the knowledgebase. The pattern is first declared e.g. I KNOW THAT * IS * which allows the input of an object and a symbol into the knowledgebase, then the template declared as #31$ so the program knows which AIML category to use, then the symbol and object are stored as the index. 

Using the ResolutionProver().prove function to prove the fact to be added using the I know that equals the opposite of the current fact in the kb then a contradiction error will occur and if not then the fact will be added and the file will be updated using .append and rewrote using .write to update the file.

The gTTS(google text to speech) library brings a text-to-chat function to the program, which allows the chatbot output to be stored in an mp3 file and outputted to the user as speech.

The libraries imported for the program include the gTTs for the text to chat, the playsound library, pandas in order to read the csv file, nltk.inference for the resolution prover function and nltk.sem to import expression. Firstly the knowledgebase is read using panda into data. The first if statement for the cmd 31 which is the #31$ category of the AIML file which is the pattern I know that firstly stores the object and subject into an expression and is then turned into a string, the opposite of the expression is then created using the !(not) function and is then stored as a contradiction using ResolutionProver. So if the expression equals the contradiction such as Legs is Lift into -Lift(Legs) then the contradiction error will be returned, else the expression will be appended and stored in the csv knowledgebase using the .write and .append and then the ‘ok, I will remember that’ will be returned.

Next is the elif cmd which is the #32$ category from the AIML file so if the user input is check that * is * then the object and subject will be stored as the expression and is then checked against the knowledgebase using the ResolutionProver and if it equals a fact from the kb then ‘correct’ will be returned, again if a contradiction occurs similar to the previous category then ‘incorrect’ is returned and finally else the expression does not meet any facts or contradictions ‘I don’t know’ is returned.

Next I added #33$ category to the AIML and elif cmd 33 which gives the user the feature to remove facts from the knowledgebase file. Firstly storing the object and subject into the expression variable and then checks if it matches against the knowledgebase using Resolution Prover then using.remove and using the .reader function to read the kb file then remove the row which matches the user input then rewrite the file without the fact the user wanted removed and the ‘Okay I will remove that’ is returned, else if the expression the user inputted did not meet any facts in the resolution prover then ‘Neither do I’ is returned. 

Finally using google text to speech in the tkinter class the output from the chatbot is stored and is then saved into an mp3 file in English using myobj = gTTS(text=mytext, lang='en', slow=False) the mp3 is then played on output using the playsound function from the playsound library, the mp3 file is then removed so it can be rewrote to if the chatbot continues output.


Stage 4
 Using an azure cognitive service to obtain a cog key and an endpoint in order to utilize both the azure FaceClient and the Text analytics client as well as using the msrest.authentication to use the cognitive service credentials. The text analytic client will first be used to detect the language using detect language by first storing user input in a txt file then using:
language_analysis = text_analytics_client.detect_language(documents=usertext)
    for usertext_num in range(len(usertext)):
        lang = language_analysis.documents[usertext_num].detected_languages[0]
        print(' - Code: {}\n'.format(lang.iso6391_name))
        usertextlang = lang.iso6391_name
to detect the language then store the language code as usertextlang in order to use for the translation.
The next stage required to translate the text into English so by using the translate_text function which takes the Microsoft translator path and applies the cog key and region and returns the translation as text in English using:
translation = translate_text(cog_region, cog_key, text_to_translate, to_lang='en', from_lang=usertextlang)

this line of code takes the users language code and translates to English and stores in translations.

To return the response from the chatbot into the users language the translate_text function is called again however the to_lang = usertextlang and from_lang = ‘en’.

The Azure faceclient makes facial recognition and facial expression recognition possible this was used in the chatbot application by first using the logic inputs from the aiml file to obtain a person_id and then use user images to train the group_id using: face_client.person_group.train(group_id).
Then using the faceclient.identify to identify the person_id from the trained images from the image the user has selected and then creating a plt.figure around the face and annotate with the person_name from the group_id and person _id using: person_name = face_client.person_group_person.get(group_id, face.candidates[0].person_id).name.





 





