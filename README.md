Introducción
============

*“Actualmente, las tareas que realizan estos bots son sumamente
sencillas, sin embargo, se prevé que puedan facilitar la vida de las
personas. De hecho, algunas investigaciones recientes sostienen que a
finales del 2017, sólo una tercera parte de las consultas por internet
requieran la ayuda de seres humanos. @incbots."*\
Los bots conversacionales, también conocidos como *chatbots*, son una
herramienta en auge muy util que nos permite desde realizar un pequeño
agente capaz de interactuar con las personas para proporcionarles
información sobre recetas como veremos en el siguiente documento, cómo
de interactuar mediante distintas plataformas con clientes de grandes
empresas y así hacer los servicios de atención al cliente mucho más
accesibles y rápidos.

Para que la realización de nuestro *bot* sea sencilla y rápida,
emplearemos una herramienta de Google: DialogFlow. Esta nos permite
crear bots que, configurados y entrenados correctamente, son capaces de
mantener conversaciones más o menos complejas utilizando lenguaje
natural, con el usuario con el que interactua o podríamos decir,
diáloga.

Por otra parte controlaremos la lógica de interacción entre el bot y el
usuario mediante Python donde, como veremos más adelante, la entrada
podrá ser mediante un teclado (escrita), o a través de la voz utilizando
por ejemplo un micrófono. Finalmente utilizaremos una herramienta de
Python que nos dará la posibilidad de transformar el texto a audio. Cabe
decir que el lenguaje utilizado para crear el bot ha sido el inglés
debido a que la API utilizada para la búsqueda de recetas así lo
requeria.

ChefBot
=======

Para la realización de nuestro ayudante en la cocina, nuestro búscador
de recetas, podemos separar por una parte la declaración y creación de
nuestro *bot* en la plataforma que DialogFlow nos proporciona, y por
otra, la lógica de nuestra interfaz desarrollada en Python que nos sirve
de pasarela con nuestro *bot* mencionado.

DialogFlow
----------

Previamente a la inserción de los datos en sí en la herramienta de
DialogFlow, hemos realizado un diagrama de como debería ser el flujo de
interacción de los usuarios con nuestro *chatbot*. En
dicho diagrama, cada nodo representa una conexión entre lo que el
usuario dice y que acción debería ser tomada por nuestro *chatbot*,
conocido como *Intents*. Cada *Intent* tiene un *Context* de entrada
(*in*) y otro de sálida (*out*) que nos sirven para guardar la historia
o contexto de la conversación. Además utilizaremos este contexto para
conocer cuales son los ingredientes y/o tipo de recetas que el usuario
esta buscando, así como cuando el *chatbot* emita el contexto *finish*
finalizar la conversación.

Por otra parte contamos con las *Entities* que nos permiten manejar los
“conceptos" proporcionandole ejemplos de estos. En nuestro diagrama
estan representados mediante *@entitie* y nos sirven de enlaces entre
los *Intents*. Por ejemplo la *entitie* @type representa el concepto de
tipo de comida y a DialogFlow le hemos suministrado una serie de
ejemplos cómo pueden ser: pizzas, snacks o salads.

![Diagrama](https://github.com/MarioProjects/ChefBot/blob/master/diagrama.jpg)

Lógica con Python
-----------------

Una vez definido nuestro *chatbot* nos falta crear algún medio por el
que interactuar con él, para ello utilizaremos Python. Gracias a la API
de DialogFlow para Python *apiai*, la comunicación entre nuestro
servicio y la lógica implementada en Python es muy sencilla.\
Hemos definido dos métodos para poder interactuar tanto por voz cómo de
forma escrita con nuestro *chatbot* donde principalmente nos
encargaremos de lo siguiente:

-   ***WELCOME***: Disparamos el primer *Intent* que nos dará la
    bienvenida y nos preguntara que receta estamos buscando.
    Dependiendole de que le pidamos nos conducirá a un sitio u otro. Si
    el usuario contesta alguna cosa que el *chatbot* no tiene
    planificada, se lanzará el “Default Fallback Intent" que tratara de
    ayudar al usuario a encaminar sus respuestas.

-   **process\_response**: Es un método que nos ayudará a tratar el tipo
    de respuestas que provienen de nuestro servicio y extraer los datos
    que nos son de utilidad de las mismas. Nos sirve además para
    identificar los contextos y actuar en consecuencia y a obtener la
    lista de ingredientes y/o tipos que el usuario desea.

Una vez instanciado nuestro *chatbot* y sabiendo procesar las respuestas
que este nos proporciona, realizaremos en bucle una serie de
intercambios de mensajes entre el usuario y el servicio de forma que
cuando tengamos la información necesaria, a través de una tercera API
que nos permite búscar recetas le proporcionaremos al usuario la receta
que estaba búscando, y si esta satisfecho, nuestro servicio terminará.

Mencionar que también hemos utilizado la “Google Cloud Speech API" para
ser capaces de capturar audio online a través de un microfono y pasarlo
a texto para, a su vez, comunicar dicho texto a nuestro servicio y
generar el comportamiento previamente expuesto.

Los resultados obtenidos cuando hemos utilizado la versión en la que se requiere interacturar por micrófono han sido:

![Results Speech](https://github.com/MarioProjects/ChefBot/blob/master/speechBot1.PNG)

Mientras que resultados obtenidos cuando hemos utilizado la versión en la que se requiere interacturar escribiendo han sido:

![Results Text](https://github.com/MarioProjects/ChefBot/blob/master/textBot2.PNG)


#### Author
 
    Mario Parreño 
