
# coding: utf-8

# ## Pruebas toma audio

# In[1]:


# Para el reconocimiento de voz
import speech_recognition as sr


# In[2]:


def record_to_text(debug=False):
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        #if debug:
        #    print("Say something!")
        audio = r.listen(source)
    # Speech recognition using Google Speech Recognition
    recognized = False
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        recognized = r.recognize_google(audio)
        if debug:
            print("You said: " + str(recognized))
    except sr.UnknownValueError:
        if debug:
            print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        if debug:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
    if not recognized or None:
        record_to_text(debug)
    else:
        return recognized


# In[4]:


#record_to_text(True)


# ## ChefBot DialogFlow

# In[5]:


# Importamos el archivo con las funciones que nos permitiran realizar búsquedas de cocina
import recipe_searcher as rs


# In[6]:


import apiai
import json
import sys
# Con win32com.client podremos sacar texto a audio por los altavoces
import win32com.client as wincl
chef = wincl.Dispatch("SAPI.SpVoice")


# ### Procesador de las respuestas del Bot

# In[7]:


def process_response(response, debug=False):
    
    # Le pasamos un diccionario que es la respuesta de DialogFlow
    rSearch = ""
    confirmed = False
    
    if debug:
        print(json.dumps(response, indent=4))
        print(response.keys())
        
    contexts = response['result']['contexts']
    
    if len(contexts) > 0 and debug:
        print (list(c['name'] for c in contexts))
    
    # Si entre los contextos esta 'confirm' es por que el usuario ha confirmado 
    # los ingredientes y/o tipos de recetas que desea
    if any(c['name'] == 'confirm' for c in contexts):
        for c in contexts:
            if c['name'] == 'recipe_config':
                # Los parametros pueden llegar como listas o string
                rtype = c['parameters']['type']
                ringredients = c['parameters']['type']
                if type(rtype) is not str:
                    rtype = ' '.join(c['parameters']['type'])
                if type(ringredients) is not str:
                    ringredients = ' '.join(c['parameters']['ingredients'])
                rSearch = (rtype + ' ' + ringredients).strip()
        if debug:
            print (json.dumps(response['result'], indent=4))
            
    # Si entre los contextos esta 'confirmed' es que ya hemos acabado
    if any(c['name'] == 'finish' for c in contexts):
        confirmed = True
        if debug:
            print (json.dumps(response['result'], indent=4))
    
    # Almacenamos la respuesta que proporciona el bot de DialogFlow para devolverla
    answer = response['result']['fulfillment']['speech']
    
    return answer, rSearch, confirmed


# ### Logica ejecución

# In[25]:


def ChefBotSpeech():
    """
        Para esta versión necesitarás un microfono y unos altavoces
        Cuando el sistema (chef) realice sus preguntas deberás responder con la voz
    """
    CLIENT_ACCESS_TOKEN = "30309bed62544139abc0718a65a9f97f"
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    #peticion de inicio del dialogo
    request = ai.event_request(apiai.events.Event("WELCOME")) #Disparamos el evento WELCOME
    request.lang = 'en'  #(Opcional: Decimos que idioma es ingles (en))

    response = request.getresponse() # Obtenemos la respuesta para nuestra peticion

    #La respuesta viene en binario y hay que transformarla para JSON
    json_res = json.loads(response.read().decode('utf8'))

    # Disponemos de funciones para obtener el texto de la respuesta JSON
    utterance, _, _ = process_response(json_res)
    print("System:", utterance)
    
    # Realizamos un bucle hasta que finalizamos (contexto finish)
    end = False
    recipe_found = False
    while not end:
        user_turn = record_to_text(True)
        request = ai.text_request() # Disponemos de un speech request tambien para enviar el audio
        request.query = user_turn
        response = request.getresponse()
        json_res = json.loads(response.read().decode('utf8'))
        utterance, rSearch, end = process_response(json_res)
        if rSearch and not recipe_found:
            recipe_found = rSearch
        print("\nSystem:", utterance)
        if recipe_found and not end:
            rs.get_popular_recipes(recipe_found)
            print("\nAre you okey with this recipe or you want another one?")


# In[9]:


def ChefBot():
    """
        Versión del chef que funciona mediante la entrada de texto por teclado
    """
    CLIENT_ACCESS_TOKEN = "30309bed62544139abc0718a65a9f97f"
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    #peticion de inicio del dialogo
    request = ai.event_request(apiai.events.Event("WELCOME")) #Disparamos el evento WELCOME
    request.lang = 'en'  #(Opcional: Decimos que idioma es ingles (en))

    response = request.getresponse() # Obtenemos la respuesta para nuestra peticion

    #La respuesta viene en binario y hay que transformarla para JSON
    json_res = json.loads(response.read().decode('utf8'))

    # Disponemos de funciones para obtener el texto de la respuesta JSON
    utterance, _, _ = process_response(json_res)
    print("System:", utterance)
    
    # Realizamos un bucle hasta que finalizamos (contexto finish)
    print()
    end = False
    recipe_found = False
    while not end:
        user_turn = input('-->:')
        request = ai.text_request() # Disponemos de un speech request tambien para enviar el audio
        request.query = user_turn
        response = request.getresponse()
        json_res = json.loads(response.read().decode('utf8'))
        utterance, rSearch, end = process_response(json_res)
        if rSearch and not recipe_found:
            recipe_found = rSearch
        print("\nSystem:", utterance)
        if recipe_found and not end:
            rs.get_popular_recipes(recipe_found)
            print("\nAre you okey with this recipe or you want another one?")


