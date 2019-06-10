#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from emoji import emojize
import telebot
from telebot import types
import mysql.connector
from random import randint

#Establecemos conexión con la base de datos
cnx = mysql.connector.connect(user='root', password='bottodobypca',
                              host='127.0.0.1',
                              database='bottododata')
cursor = cnx.cursor()

#Conectamos con el bot de telegram
TOKEN = ................................... #PASTE BOT TOKEN HERE
bot = telebot.TeleBot(TOKEN)

# Funcion que envia el sticker en la bienvenida
def send_sti(message):
    chatid = message.chat.id
    sti = open('imagenbot.webp', 'rb')
    bot.send_sticker(chatid, sti)

# Funcion que envia el sticker de congratulations
def send_congrat(message):
    chatid = message.chat.id
    sti = open('homerofeliz.webp', 'rb')
    bot.send_sticker(chatid, sti)

def send_bossimg(chatid,rutaimg):
    sti = open(rutaimg+'.webp', 'rb')
    bot.send_sticker(chatid, sti)


# Funcion que da la bienvenida
@bot.message_handler(commands = ["start"])
def send_welcome(message):
    #global userid
    #global chatid
    #global name
    #global mensaje
    #global commands
    #global bosselect
    commands="default"
    mensaje = message
    chatid = message.chat.id
    userid = message.from_user.id
    grupo="no"
    if message.chat.type == "group":
        grupo="si"
        bosselect=0
        name = str(message.chat.title)
        #Parámetros del boss
        cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                  host='127.0.0.1',
                                  database='bottododata')
        cursor = cnx.cursor()
        query=("SELECT DISTINCT bossid FROM saves WHERE chatid=%(emp_no)s")
        cursor.execute(query,{"emp_no":chatid})
        resultado=cursor.fetchone()
        if resultado!=None:
            bosselect=resultado[0]
        cursor.close()
        cnx.close()
        #se selecciona un boss por su id aleatoriamente
        
        if bosselect==0:
            cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                  host='127.0.0.1',
                                  database='bottododata')
            cursor = cnx.cursor()
            query=("SELECT COUNT(*) FROM jefes")
            cursor.execute(query)
            count=cursor.fetchone()[0]
            cursor.close()
            cnx.close()
            #se selecciona un boss por su id aleatoriamente
            bosselect=randint(1,count)
            
            cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                    host='127.0.0.1',
                                    database='bottododata')
            cursor = cnx.cursor()             
            query=("SELECT vida FROM jefes WHERE id=%(bossid)s")
            cursor.execute(query, {"bossid":bosselect})
            restante=cursor.fetchone()[0]
            cursor.close()
            cnx.close()
            
            cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                host='127.0.0.1',
                                database='bottododata')
            cursor = cnx.cursor()             
            query=("SELECT vida FROM jefes WHERE id = %(emp_no)s")
            cursor.execute(query, {"emp_no":bosselect})
            vida=cursor.fetchone()[0]
            cursor.close()
            cnx.close()
            
            cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                  host='127.0.0.1',
                                  database='bottododata')
            cursor = cnx.cursor()
        
            query=("INSERT INTO saves(chatid,bossid,userid,restante) VALUES (%(chatid)s,%(bosselect)s,%(userid)s,%(restante)s) ON DUPLICATE KEY UPDATE bossid=%(bosselect)s")
            cursor.execute(query,{"chatid":chatid,"userid":userid,"bosselect":bosselect,"restante":vida})
            cnx.commit()
            cursor.close()
            cnx.close()
        else:
            cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                    host='127.0.0.1',
                                    database='bottododata')
            cursor = cnx.cursor()             
            query=("SELECT DISTINCT restante FROM saves WHERE chatid = %(emp_no)s AND bossid=%(bossid)s")
            cursor.execute(query, {"emp_no":chatid,"bossid":bosselect})
            restante=cursor.fetchone()[0]
            cursor.close()
            cnx.close()
                
        cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                host='127.0.0.1',
                                database='bottododata')
        cursor = cnx.cursor()             
        query=("SELECT nombre,vida,imagen FROM jefes WHERE id = %(emp_no)s")
        cursor.execute(query, {"emp_no":bosselect})
        datosboss=cursor.fetchone()
        cursor.close()
        cnx.close()
        
        bossimg=datosboss[2]             
        saludo = emojize("Hola, gente de {nombre}! \nSoy BotToDo, un bot creado para ayudaros con la organización de vuestras tareas. :calendar:"+
                         "\n"+ ":question:" + "Si necesitas ayuda, escribe /help\n\n:warning: :warning: :warning: :warning: :warning: :warning: :warning: :warning:", use_aliases=True)
        bot.send_message(chatid, saludo.format(nombre=name))
        send_bossimg(chatid,bossimg)
        saludo = emojize("\n¡Vaya, parece que tenéis un visitante inesperado! Se trata, ni más ni menos, de :smiling_imp:*{bossname}*:smiling_imp:, con "+str(datosboss[1])+" puntos de vida."+
                         "\n¡Completad muchas tareas entre todos para derrotar al jefe intruso!\n¡Ánimo!:muscle:"+
                         "\n*Para participar en la batalla, pulsa el primer botón y envíame por privado el mensaje /start*", use_aliases=True)
        markup = types.InlineKeyboardMarkup(2)
        txt_enviar = emojize(":star: ¡Quiero participar! :star:", use_aliases=True)
        txt_vida = emojize(":imp: Comprobar vida del jefe :imp:", use_aliases=True)
        btn1=types.InlineKeyboardButton(txt_enviar,callback_data="participar")
        btn2=types.InlineKeyboardButton(txt_vida,callback_data="vervidaboss")
        markup.add(btn1)
        markup.add(btn2)

        bot.send_message(chatid, saludo.format(bossname=datosboss[0]), parse_mode= 'Markdown',reply_markup=markup)
    
    else:
        bosselect=0
        cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                  host='127.0.0.1',
                                  database='bottododata')
        cursor = cnx.cursor()
        query=("SELECT bossid FROM saves WHERE userid=%(emp_no)s")
        cursor.execute(query,{"emp_no":userid})
        resultado=cursor.fetchone()
        if resultado!=None:
            bosselect=resultado[0]
        cursor.close()
        cnx.close()
        
        name = str(message.from_user.first_name)
        if bosselect==0:
            saludo = emojize("Hola, {nombre}! \nSoy BotToDo, un bot creado para ayudarte a organizar tus tareas. :calendar: \n¡Parece que no estás jugando con más gente! Para disfrutar de la experiencia completa, usa BotToDo en algún grupo y combate junto a tus compañeros para vencer a los malos. :smiling_imp:"+ "\n:question:" + "Si necesitas ayuda, escribe /help", use_aliases=True)
        else:
            saludo = emojize("Hola, {nombre}! \nSoy BotToDo, un bot creado para ayudarte a organizar tus tareas. :calendar: \n"+ ":question:" + "Si necesitas ayuda, escribe /help", use_aliases=True)
        send_sti(message)
        markup = types.InlineKeyboardMarkup(2)
        txt_addtarea = emojize(":pencil2: Añadir una tarea", use_aliases=True)
        txt_fintarea = emojize(":star: Completar una tarea", use_aliases=True)
        txt_deltarea = emojize(":x: Eliminar una tarea :x:", use_aliases=True)
        txt_vertareas = emojize(":clipboard: Ver mis tareas :clipboard:", use_aliases=True)
        btn1=types.InlineKeyboardButton(txt_addtarea,callback_data="addtarea")
        btn2=types.InlineKeyboardButton(txt_fintarea,callback_data="fintarea")
        btn3=types.InlineKeyboardButton(txt_deltarea,callback_data="deltarea")
        btn4=types.InlineKeyboardButton(txt_vertareas,callback_data="vertareas")
        markup.row(btn1,btn2)
        markup.add(btn3)
        markup.add(btn4)

        bot.send_message(chatid, saludo.format(nombre=name),reply_markup=markup)
    #Guardamos estado
    cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                  host='127.0.0.1',
                                  database='bottododata')
    cursor = cnx.cursor()
    query=("INSERT INTO savestate(chatid,userid,bosselect,name,commands,grupo) VALUES (%(chatid)s,%(userid)s,%(bosselect)s,%(name)s,%(commands)s,%(grupo)s) ON DUPLICATE KEY UPDATE bosselect=%(bosselect)s,name=%(name)s,commands=%(commands)s")
    cursor.execute(query,{"chatid":chatid,"userid":userid,"bosselect":bosselect,"name":name,"commands":commands,"grupo":grupo})
    cnx.commit()
    cursor.close()
    cnx.close()

@bot.callback_query_handler(func=lambda call: True)
def callbacker(inline_query):
    name=inline_query.from_user.first_name
    userid=inline_query.from_user.id
    chatid=inline_query.message.chat.id
    #cnx = mysql.connector.connect(user='root', password='bottodobypca',
    #                                  host='127.0.0.1',
    #                                  database='bottododata')
    #cursor = cnx.cursor()
    #query=("SELECT chatid,bosselect,name FROM savestate WHERE userid=%(userid)s AND")
    #cursor.execute(query,{"userid":userid})
    #resultado=cursor.fetchone()
    #chatid=resultado[0]
    #bosselect=resultado[1]
    #name=resultado[2]
    #cursor.close()
    #cnx.close()
    
    if inline_query.data == "addtarea":
        
        #Guardamos estado
        cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                      host='127.0.0.1',
                                      database='bottododata')
        cursor = cnx.cursor()
        query=("UPDATE savestate SET commands = 'task' WHERE chatid=%(chatid)s")
        cursor.execute(query,{"chatid":chatid})
        cnx.commit()
        cursor.close()
        cnx.close()
        
        bot.send_message(chatid, "Introduce tu tarea:")
        bot.answer_callback_query(callback_query_id=inline_query.id)
    elif inline_query.data == "vervidaboss":
        cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                          host='127.0.0.1',
                                          database='bottododata')
        cursor = cnx.cursor()
        query=("SELECT DISTINCT restante,bossid FROM saves WHERE chatid=%(chatid)s")
        cursor.execute(query,{"chatid":chatid})
        resultado=cursor.fetchone()
        cursor.close()
        cnx.close()

            
        if resultado!=None:
            restante=resultado[0]
            bosselect=resultado[1]

            cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                          host='127.0.0.1',
                                          database='bottododata')
            cursor = cnx.cursor()
            query=("UPDATE savestate SET commands = 'default' WHERE chatid=%(chatid)s")
            cursor.execute(query,{"chatid":chatid})
            cnx.commit()
            cursor.close()
            cnx.close()
        
            
            cnx = mysql.connector.connect(user='root', password='bottodobypca',
                host='127.0.0.1',
                database='bottododata')
            cursor = cnx.cursor()             
            query=("SELECT nombre,vida,imagen FROM jefes WHERE id = %(emp_no)s")
            cursor.execute(query, {"emp_no":bosselect})
            datosboss=cursor.fetchone()

            saludo = emojize("Estáis combatiendo a :smiling_imp:*{bossname}*:smiling_imp:.\nVida restante: "+str(restante)+"/"+str(datosboss[1])+
                             "\n¡No os rindáis y seguid completando tareas!:muscle:", use_aliases=True)
            send_bossimg(chatid,datosboss[2])
            bot.send_message(chatid, saludo.format(bossname=datosboss[0]), parse_mode= 'Markdown')
            bot.answer_callback_query(callback_query_id=inline_query.id)

        else:
            saludo = "¡Vaya, parece que no hay ningún visitante 'inesperado' en estos momentos!"
            bot.send_message(chatid, saludo)
            bot.answer_callback_query(callback_query_id=inline_query.id)
    
    elif inline_query.data == "participar":
        cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                          host='127.0.0.1',
                                          database='bottododata')
        cursor = cnx.cursor()
        query=("SELECT bossid FROM saves WHERE userid=%(userid)s AND chatid=%(chatid)s")
        cursor.execute(query,{"userid":userid,"chatid":inline_query.message.chat.id})
        resultado=cursor.fetchone()
        cursor.close()
        cnx.close()
        if resultado!=None:
            text="¡Hola, "+ name +", parece que ya estás apuntad@ al combate! ¿Quieres iniciar una conversación conmigo para organizar tus tareas?"
            markup = types.InlineKeyboardMarkup(2)
            btn1=types.InlineKeyboardButton(emojize(":smile: ¡Sí! :smile:",use_aliases=True),url="https://web.telegram.org/#/im?p=@bottodo_bot")
            markup.add(btn1)
            bot.send_message(inline_query.message.chat.id, emojize(text,use_aliases=True),reply_markup=markup)
        else:
                
            cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                              host='127.0.0.1',
                                              database='bottododata')
            cursor = cnx.cursor()
            query=("SELECT DISTINCT bossid FROM saves WHERE chatid=%(chatid)s")
            cursor.execute(query,{"chatid":chatid})
            resultado=cursor.fetchone()
            
            if resultado!=None:
                bosselect=resultado[0]
                cursor.close()
                cnx.close()

                cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                              host='127.0.0.1',
                                              database='bottododata')
                cursor = cnx.cursor()
                #query=("UPDATE savestate SET commands = 'default', bosselect = %(bosselect) WHERE chatid=%(chatid)s")
                
                
                query=("INSERT INTO savestate(chatid,userid,bosselect,name,commands,grupo) VALUES (%(chatid)s,%(userid)s,%(bosselect)s,%(name)s,%(commands)s,%(grupo)s) ON DUPLICATE KEY UPDATE bosselect=%(bosselect)s,name=%(name)s,commands=%(commands)s")
                cursor.execute(query,{"bosselect":bosselect,"userid":userid,"chatid":chatid,"commands":'default',"grupo":"si","name":name})
                
                cnx.commit()
                cursor.close()
                cnx.close()
                
                cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                    host='127.0.0.1',
                                    database='bottododata')
                cursor = cnx.cursor()             
                query=("SELECT restante FROM jefes WHERE id=%(bossid)s")
                cursor.execute(query, {"bossid":bosselect})
                restante=cursor.fetchone()[0]
                cursor.close()
                cnx.close()
            
                cnx = mysql.connector.connect(user='root', password='bottodobypca',
                    host='127.0.0.1',
                    database='bottododata')
                cursor = cnx.cursor()             
                query=("INSERT INTO saves(chatid,bossid,userid,restante) VALUES (%s,%s,%s,%s)")
                cursor.execute(query,(chatid,bosselect,inline_query.from_user.id,restante))
                cnx.commit()
                cursor.close()
                cnx.close()

                text="¡Hola, "+ inline_query.from_user.first_name+"! Te has apuntado al combate, ¿quieres iniciar una conversación conmigo?"
                markup = types.InlineKeyboardMarkup(2)
                btn1=types.InlineKeyboardButton(emojize(":smile: ¡Sí! :smile:",use_aliases=True),url="https://web.telegram.org/#/im?p=@bottodo_bot")
                markup.add(btn1)
                bot.send_message(chatid, emojize(text,use_aliases=True),reply_markup=markup)

                bot.answer_callback_query(callback_query_id=inline_query.id)
            else:
                saludo = "¡Vaya, parece que no hay ningún visitante 'inesperado' en estos momentos!"
                bot.send_message(chatid, saludo)
                bot.answer_callback_query(callback_query_id=inline_query.id)
        
    elif inline_query.data == "deltarea":

        #commands="delete"
        cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                      host='127.0.0.1',
                                      database='bottododata')
        cursor = cnx.cursor()
        query=("UPDATE savestate SET commands = 'delete' WHERE chatid=%(chatid)s")
        cursor.execute(query,{"chatid":chatid})
        cnx.commit()
        cursor.close()
        cnx.close()
        
        cnx = mysql.connector.connect(user='root', password='bottodobypca',
                              host='127.0.0.1',
                              database='bottododata')
        cursor = cnx.cursor()
        query=("SELECT tarea FROM tareas WHERE usuario = %(emp_no)s")
        cursor.execute(query,{ 'emp_no': userid })
        a=cursor.fetchall()
        cursor.close()
        cnx.close()
        printlist=str("")
        for i,item in enumerate(a):
            a[i]=item[0]
            printlist=printlist+"\n"+":black_small_square: "+a[i]
        if len(a)>0:
            text="Estas son tus tareas:"+"\n"+printlist+"\n"+"¿Cuál quieres eliminar?:"
            bot.send_message(chatid,emojize(text))
            bot.answer_callback_query(callback_query_id=inline_query.id)
        else:
            text="¡No tienes ninguna tarea! ¿Por qué no añades alguna que tengas pendiente? :grin:"
            
            markup = types.InlineKeyboardMarkup(2)
            btn1=types.InlineKeyboardButton("Añadir una tarea",callback_data="addtarea")
            btn2=types.InlineKeyboardButton("Volver al menú",callback_data="return")  
            markup.add(btn1)
            markup.add(btn2)
            bot.send_message(chatid, emojize(text,use_aliases=True),reply_markup=markup)
            bot.answer_callback_query(callback_query_id=inline_query.id)
            
            
    elif inline_query.data == "fintarea":

        #commands="complete"
        cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                      host='127.0.0.1',
                                      database='bottododata')
        cursor = cnx.cursor()
        query=("UPDATE savestate SET commands = 'complete' WHERE chatid=%(chatid)s")
        cursor.execute(query,{"chatid":chatid})
        cnx.commit()
        cursor.close()
        cnx.close()
        
        cnx = mysql.connector.connect(user='root', password='bottodobypca',
                              host='127.0.0.1',
                              database='bottododata')
        cursor = cnx.cursor()
        query=("SELECT tarea FROM tareas WHERE usuario = %(emp_no)s")
        cursor.execute(query,{ 'emp_no': userid })
        a=cursor.fetchall()
        cursor.close()
        cnx.close()
        printlist=str("")
        for i,item in enumerate(a):
            a[i]=item[0]
            printlist=printlist+"\n"+":black_small_square: "+a[i]
        if len(a)>0:
            text="Estas son tus tareas:"+"\n"+printlist+"\n"+"¿Cuál has completado?:"
            bot.send_message(chatid,emojize(text))
            bot.answer_callback_query(callback_query_id=inline_query.id)
        else:
            text="¡No tienes ninguna tarea! ¿Por qué no añades alguna que tengas pendiente? :grin:"
            
            markup = types.InlineKeyboardMarkup(2)
            btn1=types.InlineKeyboardButton("Añadir una tarea",callback_data="addtarea")
            btn2=types.InlineKeyboardButton("Volver al menú",callback_data="return")  
            markup.add(btn1)
            markup.add(btn2)
            bot.send_message(chatid, emojize(text,use_aliases=True),reply_markup=markup)
            bot.answer_callback_query(callback_query_id=inline_query.id)
        
    elif inline_query.data == "return":

        
        cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                      host='127.0.0.1',
                                      database='bottododata')
        cursor = cnx.cursor()
        query=("UPDATE savestate SET commands = 'default' WHERE chatid=%(chatid)s")
        cursor.execute(query,{"chatid":chatid})
        cnx.commit()
        cursor.close()
        cnx.close()
        #commands="default"
        saludo = emojize("Hola, {nombre}! \nSoy BotToDo, un bot creado para ayudarte a organizar tus tareas. :calendar: \n"+ ":question:" + "Si necesitas ayuda, escribe /help", use_aliases=True)
        markup = types.InlineKeyboardMarkup(2)
        txt_addtarea = emojize(":pencil2: Añadir una tarea", use_aliases=True)
        txt_fintarea = emojize(":star: Completar una tarea", use_aliases=True)
        txt_deltarea = emojize(":x: Eliminar una tarea :x:", use_aliases=True)
        txt_vertareas = emojize(":clipboard: Ver mis tareas :clipboard:", use_aliases=True)
        btn1=types.InlineKeyboardButton(txt_addtarea,callback_data="addtarea")
        btn2=types.InlineKeyboardButton(txt_fintarea,callback_data="fintarea")
        btn3=types.InlineKeyboardButton(txt_deltarea,callback_data="deltarea")
        btn4=types.InlineKeyboardButton(txt_vertareas,callback_data="vertareas")
        markup.row(btn1,btn2)
        markup.add(btn3)
        markup.add(btn4)
        bot.send_message(chatid, saludo.format(nombre=name),reply_markup=markup)
        
        bot.answer_callback_query(callback_query_id=inline_query.id)
    elif inline_query.data == "facil":
        
        #commands="default"
        cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                      host='127.0.0.1',
                                      database='bottododata')
        cursor = cnx.cursor()
        query=("UPDATE savestate SET commands = 'default' WHERE chatid=%(chatid)s")
        cursor.execute(query,{"chatid":chatid})
        cnx.commit()
        cursor.close()
        cnx.close()
        #Obtenemos el texto de la tarea
        cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                      host='127.0.0.1',
                                      database='bottododata')
        cursor = cnx.cursor()
        query=("SELECT texto FROM savestate WHERE chatid=%(chatid)s AND userid=%(userid)s")
        cursor.execute(query,{"chatid":chatid,"userid":userid})
        textinput=cursor.fetchone()[0]
        cursor.close()
        cnx.close()
        
        cnx = mysql.connector.connect(user='root', password='bottodobypca',
                              host='127.0.0.1',
                              database='bottododata')
        cursor = cnx.cursor()
        query=("INSERT INTO tareas(usuario,tarea,dificultad) VALUES (%s,%s,%s)")
        cursor.execute(query, (userid, textinput,1))
        cnx.commit()
        cursor.close()
        cnx.close()
        
        markup = types.InlineKeyboardMarkup(2)
        btn1=types.InlineKeyboardButton("Añadir otra tarea",callback_data="addtarea")
        btn2=types.InlineKeyboardButton("Volver al menú",callback_data="return")  
        markup.add(btn1)
        markup.add(btn2)
    
        bot.send_message(chatid, "¿Qué más quieres hacer?",reply_markup=markup)
        
    elif inline_query.data == "intermedia":

        
        #commands="default"
        cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                      host='127.0.0.1',
                                      database='bottododata')
        cursor = cnx.cursor()
        query=("UPDATE savestate SET commands = 'default' WHERE chatid=%(chatid)s")
        cursor.execute(query,{"chatid":chatid})
        cnx.commit()
        cursor.close()
        cnx.close()
        #Obtenemos el texto de la tarea
        cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                      host='127.0.0.1',
                                      database='bottododata')
        cursor = cnx.cursor()
        query=("SELECT texto FROM savestate WHERE chatid=%(chatid)s AND userid=%(userid)s")
        cursor.execute(query,{"chatid":chatid,"userid":userid})
        textinput=cursor.fetchone()[0]
        cursor.close()
        cnx.close()
        
        cnx = mysql.connector.connect(user='root', password='bottodobypca',
                              host='127.0.0.1',
                              database='bottododata')
        cursor = cnx.cursor()
        query=("INSERT INTO tareas(usuario,tarea,dificultad) VALUES (%s,%s,%s)")
        cursor.execute(query, (userid, textinput,2))
        cnx.commit()
        cursor.close()
        cnx.close()
        
        markup = types.InlineKeyboardMarkup(2)
        btn1=types.InlineKeyboardButton("Añadir otra tarea",callback_data="addtarea")
        btn2=types.InlineKeyboardButton("Volver al menú",callback_data="return")  
        markup.add(btn1)
        markup.add(btn2)
    
        bot.send_message(chatid, "¿Qué más quieres hacer?",reply_markup=markup)
        
    elif inline_query.data == "dificil":

        #commands="default"
        cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                      host='127.0.0.1',
                                      database='bottododata')
        cursor = cnx.cursor()
        query=("UPDATE savestate SET commands = 'default' WHERE chatid=%(chatid)s")
        cursor.execute(query,{"chatid":chatid})
        cnx.commit()
        cursor.close()
        cnx.close()
        #Obtenemos el texto de la tarea
        cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                      host='127.0.0.1',
                                      database='bottododata')
        cursor = cnx.cursor()
        query=("SELECT texto FROM savestate WHERE chatid=%(chatid)s AND userid=%(userid)s")
        cursor.execute(query,{"chatid":chatid,"userid":userid})
        textinput=cursor.fetchone()[0]
        cursor.close()
        cnx.close()
        
        cnx = mysql.connector.connect(user='root', password='bottodobypca',
                              host='127.0.0.1',
                              database='bottododata')
        cursor = cnx.cursor()
        query=("INSERT INTO tareas(usuario,tarea,dificultad) VALUES (%s,%s,%s)")
        cursor.execute(query, (userid, textinput,3))
        cnx.commit()
        cursor.close()
        cnx.close()
        
        markup = types.InlineKeyboardMarkup(2)
        btn1=types.InlineKeyboardButton("Añadir otra tarea",callback_data="addtarea")
        btn2=types.InlineKeyboardButton("Volver al menú",callback_data="return")  
        markup.add(btn1)
        markup.add(btn2)
    
        bot.send_message(chatid, "¿Qué más quieres hacer?",reply_markup=markup)
        
    elif inline_query.data == "vertareas":

        #commands="default"
        cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                      host='127.0.0.1',
                                      database='bottododata')
        cursor = cnx.cursor()
        query=("UPDATE savestate SET commands = 'default' WHERE chatid=%(chatid)s")
        cursor.execute(query,{"chatid":chatid})
        cnx.commit()
        cursor.close()
        cnx.close()
        
        cnx = mysql.connector.connect(user='root', password='bottodobypca',
                              host='127.0.0.1',
                              database='bottododata')
        cursor = cnx.cursor()
        query=("SELECT tarea FROM tareas WHERE usuario = %(emp_no)s")
        cursor.execute(query,{ 'emp_no': userid })
        a=cursor.fetchall()
        cursor.close()
        cnx.close()
        printlist=str("")
        for i,item in enumerate(a):
            a[i]=item[0]
            printlist=printlist+"\n"+":black_small_square: "+a[i]
        if len(a)>0:
            text="Estas son tus tareas:"+"\n"+printlist+"\n¿Qué quieres hacer?"
            
            markup = types.InlineKeyboardMarkup(2)
            btn1=types.InlineKeyboardButton("Completar una tarea",callback_data="fintarea")
            btn2=types.InlineKeyboardButton("Eliminar una tarea",callback_data="deltarea")
            btn3=types.InlineKeyboardButton("Volver al menú",callback_data="return")  
            markup.add(btn1)
            markup.add(btn2)
            markup.add(btn3)
            bot.send_message(chatid, emojize(text),reply_markup=markup)
            bot.answer_callback_query(callback_query_id=inline_query.id)
        else:
            text="¡No tienes ninguna tarea! ¿Por qué no añades alguna que tengas pendiente? :grin:"
            
            markup = types.InlineKeyboardMarkup(2)
            btn1=types.InlineKeyboardButton("Añadir una tarea",callback_data="addtarea")
            btn2=types.InlineKeyboardButton("Volver al menú",callback_data="return")  
            markup.add(btn1)
            markup.add(btn2)
            bot.send_message(chatid, emojize(text,use_aliases=True),reply_markup=markup)
            bot.answer_callback_query(callback_query_id=inline_query.id)
        
    else:
        cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                          host='127.0.0.1',
                                          database='bottododata')
        cursor = cnx.cursor()
        query=("SELECT chatid,bosselect,name FROM savestate WHERE userid=%(userid)s AND grupo='no'")
        cursor.execute(query,{"userid":userid})
        resultado=cursor.fetchone()
        chatid=resultado[0]
        bosselect=resultado[1]
        name=resultado[2]
        cursor.close()
        cnx.close()
        bot.send_message(chatid, emojize("Ha habido algún problema :worried:. Prueba otra vez o contacta con el grupo desarrollador.",use_aliases=True))
        bot.answer_callback_query(callback_query_id=inline_query.id)
    
@bot.message_handler(commands=["help"])
def new_task(message):
    #global commands
    #commands = "return"
    chatid=message.chat.id
    cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                  host='127.0.0.1',
                                  database='bottododata')
    cursor = cnx.cursor()
    query=("UPDATE savestate SET commands = 'return' WHERE chatid=%(chatid)s AND userid=%(userid)s")
    cursor.execute(query,{"chatid":message.chat.id,"userid":message.from_user.id})
    cnx.commit()
    cursor.close()
    cnx.close()
    
    text="Pulsa los botones que se te presentan para interactuar. ¡No es necesario el uso de comandos!"+" Hay algunos datos extra que deberías conocer: \n :black_small_square: Aunque las tareas no se guardan asociadas a ningún nombre reconocible, sí son guardadas explicitamente en una base de datos. ¡Por si acaso, no escribas nada comprometido o información personal!"+" \n :black_small_square: BotToDo se disfruta mejor en compañía. Inicia BotToDo en un grupo para invocar a un monstruo al azar y participad todos juntos para derrotarlo. Para causarle daño al monstruo, bastará con completar tus tareas. ¡Las tareas más difíciles causarán más daño!"+" \n :black_small_square: Este bot ha sido desarrollado por el grupo PCA (de Pedro, Carol y Ana)"
    if message.chat.type == "group":
        bot.send_message(chatid, emojize(text,use_aliases=True))
    else:
        markup = types.InlineKeyboardMarkup(2)
        btn1=types.InlineKeyboardButton("Volver al menú",callback_data="return")  
        markup.add(btn1)
        bot.send_message(chatid, emojize(text,use_aliases=True),reply_markup=markup)
    
# Funcion que escucha tareas todo el rato
@bot.message_handler(func=lambda message: True)
def list_tasks(message):
    #global a
    #global commands
    chatid=message.chat.id
    userid=message.from_user.id
    textinput=message.text
    cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                  host='127.0.0.1',
                                  database='bottododata')
    cursor = cnx.cursor()
    query=("SELECT commands,bosselect,name FROM savestate WHERE chatid=%(chatid)s AND userid=%(userid)s")
    cursor.execute(query,{"chatid":chatid,"userid":userid})
    results=cursor.fetchone()
    commands=results[0]
    bosselect=results[1]
    name=results[2]
    cursor.close()
    cnx.close()
        
    if commands == "task":
        #global mensaje
        #mensaje=message
        markup = types.InlineKeyboardMarkup(2)
        dif1 = emojize(":smiley: (Fácil)", use_aliases=True)
        dif2 = emojize(":neutral_face: (Media)", use_aliases=True)
        dif3 = emojize(":astonished: (Difícil)", use_aliases=True)
        btn1=types.InlineKeyboardButton(dif1,callback_data="facil")
        btn2=types.InlineKeyboardButton(dif2,callback_data="intermedia")
        btn3=types.InlineKeyboardButton(dif3,callback_data="dificil") 
        markup.row(btn1,btn2,btn3)
        
            #Guardamos estado
        cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                      host='127.0.0.1',
                                      database='bottododata')
        cursor = cnx.cursor()
        query=("UPDATE savestate SET texto=%(texto)s WHERE chatid=%(chatid)s AND userid=%(userid)s")
        cursor.execute(query,{"chatid":chatid,"userid":userid,"texto":textinput})
        cnx.commit()
        cursor.close()
        cnx.close()
    
        bot.send_message(message.chat.id, "¿Cómo de difícil es la tarea?",reply_markup=markup)
        
    elif commands == "complete":
        cnx = mysql.connector.connect(user='root', password='bottodobypca',
                              host='127.0.0.1',
                              database='bottododata')
        cursor = cnx.cursor()
        query=("SELECT tarea FROM tareas WHERE usuario = %(emp_no)s")
        cursor.execute(query,{ 'emp_no': userid })
        a=cursor.fetchall()
        cursor.close()
        cnx.close()
        for i,item in enumerate(a):
            a[i]=item[0]
        if message.text in a:
            #Determinar cuántos puntos ha ganado el usuario:
            cnx = mysql.connector.connect(user='root', password='bottodobypca',
                              host='127.0.0.1',
                              database='bottododata')
            cursor = cnx.cursor()
            query=("SELECT DISTINCT dificultad FROM tareas WHERE usuario = %s AND tarea = %s")
            cursor.execute(query,(userid,message.text))
            
            result=cursor.fetchone()
            cursor.close()
            cnx.close()
            dif=result[0]
            puntos=dif*10

            cursor.close()
            cnx.close()
            
            cnx = mysql.connector.connect(user='root', password='bottodobypca',
                              host='127.0.0.1',
                              database='bottododata')
            cursor = cnx.cursor()
            query=("SELECT id_usuario FROM usuarios")
            cursor.execute(query)
            a=cursor.fetchall()   
            cursor.close()
            cnx.close()
            cnx = mysql.connector.connect(user='root', password='bottodobypca',
                              host='127.0.0.1',
                              database='bottododata')
            #Comprobamos si el usuario existe ya en la base de datos (editar/incluir)
            for i,item in enumerate(a):
                a[i]=item[0]
            if message.from_user.id in a:
                #Si ya existe miramos a ver qué puntuación tiene y calculamos la nueva puntuación
                cursor = cnx.cursor()
                query=("SELECT puntuacion FROM usuarios WHERE id_usuario = %(emp_no)s")
                cursor.execute(query,{ 'emp_no': message.from_user.id })
                puntuacion=cursor.fetchone()[0]+puntos
                cursor.close()
                #Actualizamos la puntuación en la BBDD
                cursor = cnx.cursor()
                query=("UPDATE usuarios SET puntuacion = %s WHERE id_usuario = %s")
                cursor.execute(query,(puntuacion,message.from_user.id))          
            
            else:
                cursor = cnx.cursor()
                puntuacion=puntos
                query=("INSERT INTO usuarios(id_usuario,puntuacion,nombre) VALUES (%s,%s,%s)")
                cursor.execute(query,(message.from_user.id,puntuacion,name))  
            cnx.commit()
            cursor.close()
            cnx.close()
            #Se elimina la tarea de la base de datos
            cnx = mysql.connector.connect(user='root', password='bottodobypca',
                              host='127.0.0.1',
                              database='bottododata')
            cursor = cnx.cursor()
            query=("DELETE FROM tareas WHERE usuario = %s AND tarea = %s")
            cursor.execute(query,(message.from_user.id,message.text))
            cnx.commit()
            cursor.close()
            cnx.close()
            bot.send_message(message.chat.id, emojize("¡Yujuuu! :confetti_ball: :confetti_ball: \n ¡Has ganado "+str(puntos)+" puntos!"+"\n Tienes un total de "+str(puntuacion)+" puntos."))
            send_congrat(message)
            #Actualizar vida del boss (si hay)
            
            cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                      host='127.0.0.1',
                                      database='bottododata')
            cursor = cnx.cursor()
            query=("SELECT bossid FROM saves WHERE userid = %(emp_no)s")
            cursor.execute(query,{ 'emp_no': message.from_user.id })
            resultado=cursor.fetchone()
            if resultado!=None:
                bosselect=resultado[0]
                cursor.close()
                cnx.close()

                if bosselect != 0:
                    cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                          host='127.0.0.1',
                                          database='bottododata')
                    cursor = cnx.cursor()
                    query=("SELECT vida FROM jefes WHERE id = %(emp_no)s")
                    cursor.execute(query,{ 'emp_no': bosselect })
                    vida=cursor.fetchone()[0]
                    cursor.close()
                    cnx.close()

                    cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                          host='127.0.0.1',
                                          database='bottododata')
                    cursor = cnx.cursor()
                    query=("SELECT restante,chatid FROM saves WHERE userid = %(emp_no)s")
                    cursor.execute(query,{ 'emp_no': message.from_user.id })
                    resultado=cursor.fetchone()
                    restante=resultado[0]
                    groupid=resultado[1]
                    cursor.close()
                    cnx.close()

                    restante=restante-puntos

                    cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                          host='127.0.0.1',
                                          database='bottododata')

                    if restante>0:
                        #Actualizamos la vida en la BBDD
                        cursor = cnx.cursor()
                        query=("UPDATE saves SET restante = %s WHERE chatid = %s")
                        cursor.execute(query,(restante,groupid))
                        cnx.commit()
                        cursor.close()
                        cnx.close()
                    else:
                        commands="default"

                        cursor = cnx.cursor()
                        query=("UPDATE saves SET restante = %s WHERE chatid = %s")
                        cursor.execute(query,(vida,groupid))
                        cnx.commit()
                        cursor.close()
                        cnx.close()

                        cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                          host='127.0.0.1',
                                          database='bottododata')
                        cursor = cnx.cursor()
                        query=("DELETE FROM saves WHERE chatid = %(emp_no)s")
                        cursor.execute(query,{ 'emp_no': groupid })
                        cnx.commit()
                        cursor.close()
                        cnx.close()

                        cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                          host='127.0.0.1',
                                          database='bottododata')
                        cursor = cnx.cursor()
                        query=("SELECT nombre FROM jefes WHERE id = %(emp_no)s")
                        cursor.execute(query,{ 'emp_no': bosselect })
                        bossname=cursor.fetchone()[0]
                        cursor.close()
                        cnx.close()
                        #Obtenemos la lista de participantes ordenados por puntuacion    
                        cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                          host='127.0.0.1',
                                          database='bottododata')
                        cursor = cnx.cursor()
                        query=("SELECT nombre,puntuacion FROM usuarios WHERE puntuacion>0 ORDER BY puntuacion DESC")
                        cursor.execute(query)
                        a=cursor.fetchall()
                        cursor.close()
                        cnx.close()

                        printlist=str("")
                        for i,item in enumerate(a):
                            a[i]=item[0]
                            if i==0:
                                printlist=printlist+"\n"+":white_small_square: "+a[i]+" ("+str(item[1])+") :trophy:"
                            else:
                                printlist=printlist+"\n"+":white_small_square: "+a[i]+" ("+str(item[1])+")"

                        cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                          host='127.0.0.1',
                                          database='bottododata')

                        #Ponemos de nuevo todas las puntuaciones a 0
                        cnx = mysql.connector.connect(user='root', password='bottodobypca',
                                          host='127.0.0.1',
                                          database='bottododata')
                        cursor = cnx.cursor()
                        query=("UPDATE usuarios SET puntuacion = 0")
                        cursor.execute(query)
                        cnx.commit()
                        cursor.close()
                        cnx.close()

                        congrats=emojize("¡Yujuuu! :confetti_ball: :confetti_ball:"+"\n¡Habéis derrotado a *{bossname}*! :smiley: \n\n Aquí están los resultados:\n"+printlist+"\n\n",use_aliases=True)
                        bot.send_message(groupid, congrats.format(bossname=bossname), parse_mode= 'Markdown')
                        sti = open('buentrabajo.webp', 'rb')
                        bot.send_sticker(groupid, sti)

                        congrats=emojize("\nSi queréis recibir otro visitante 'inesperado', volved a escribir el comando */start*",use_aliases=True)
                        bot.send_message(groupid, congrats, parse_mode= 'Markdown')
        
            markup = types.InlineKeyboardMarkup(2)
            btn1=types.InlineKeyboardButton("Completar otra tarea",callback_data="fintarea")
            btn2=types.InlineKeyboardButton("Volver al menú",callback_data="return")  
            markup.add(btn1)
            markup.add(btn2)
            bot.send_message(message.chat.id, "¿Qué más quieres hacer?",reply_markup=markup)
        else:
            markup = types.InlineKeyboardMarkup(2)
            btn1=types.InlineKeyboardButton("Intentarlo de nuevo",callback_data="fintarea")
            btn2=types.InlineKeyboardButton("Volver al menú",callback_data="return")  
            markup.add(btn1)
            markup.add(btn2)
    
            bot.send_message(message.chat.id, "Esta tarea no está en la lista... \n ¿Qué quieres hacer?",reply_markup=markup)

            
    elif commands == "delete":
        cnx = mysql.connector.connect(user='root', password='bottodobypca',
                              host='127.0.0.1',
                              database='bottododata')
        cursor = cnx.cursor()
        query=("SELECT tarea FROM tareas WHERE usuario = %(emp_no)s")
        cursor.execute(query,{ 'emp_no': message.from_user.id })
        a=cursor.fetchall()
        cursor.close()
        cnx.close()
        for i,item in enumerate(a):
            a[i]=item[0]
        if message.text in a:
            cnx = mysql.connector.connect(user='root', password='bottodobypca',
                              host='127.0.0.1',
                              database='bottododata')
            cursor = cnx.cursor()
            query=("DELETE FROM tareas WHERE usuario = %s AND tarea = %s")
            cursor.execute(query,(message.from_user.id,message.text))
            cnx.commit()
            cursor.close()
            cnx.close()

            markup = types.InlineKeyboardMarkup(2)
            btn1=types.InlineKeyboardButton("Eliminar otra tarea",callback_data="fintarea")
            btn2=types.InlineKeyboardButton("Volver al menú",callback_data="return")  
            markup.add(btn1)
            markup.add(btn2)

            bot.send_message(message.chat.id, "La tarea se ha eliminado correctamente. \n ¿Qué más quieres hacer?",reply_markup=markup)
        else:
            markup = types.InlineKeyboardMarkup(2)
            btn1=types.InlineKeyboardButton("Intentarlo de nuevo",callback_data="deltarea")
            btn2=types.InlineKeyboardButton("Volver al menú",callback_data="return")  
            markup.add(btn1)
            markup.add(btn2)

            bot.send_message(message.chat.id, "Esta tarea no está en la lista... \n ¿Qué quieres hacer?",reply_markup=markup)

    elif commands == "return":
        saludo = emojize("Hola, {nombre}! \nSoy BotToDo, un bot creado para ayudarte a organizar tus tareas. :calendar: \n"+ ":question:" + "Si necesitas ayuda, escribe /help", use_aliases=True)
        markup = types.InlineKeyboardMarkup(2)
        txt_addtarea = emojize(":pencil2: Añadir una tarea", use_aliases=True)
        txt_fintarea = emojize(":star: Completar una tarea", use_aliases=True)
        txt_deltarea = emojize(":x: Eliminar una tarea :x:", use_aliases=True)
        txt_vertareas = emojize(":clipboard: Ver mis tareas :clipboard:", use_aliases=True)
        btn1=types.InlineKeyboardButton(txt_addtarea,callback_data="addtarea")
        btn2=types.InlineKeyboardButton(txt_fintarea,callback_data="fintarea")
        btn3=types.InlineKeyboardButton(txt_deltarea,callback_data="deltarea")
        btn4=types.InlineKeyboardButton(txt_vertareas,callback_data="vertareas")
        markup.row(btn1,btn2)
        markup.add(btn3)
        markup.add(btn4)
        bot.send_message(message.chat.id, saludo.format(nombre=name),reply_markup=markup)
        
    elif commands == "default":
        if message.chat.type == "group":
            pass
        else:
            saludo = emojize("Perdona, {nombre}, pero no entiendo tu orden :persevere:. Por favor, utiliza los botones bajo mis mensajes.\n:question:" + "Si necesitas ayuda, escribe /help", use_aliases=True)
            markup = types.InlineKeyboardMarkup(2)
            txt_addtarea = emojize(":pencil2: Añadir una tarea", use_aliases=True)
            txt_fintarea = emojize(":star: Completar una tarea", use_aliases=True)
            txt_deltarea = emojize(":x: Eliminar una tarea :x:", use_aliases=True)
            txt_vertareas = emojize(":clipboard: Ver mis tareas :clipboard:", use_aliases=True)
            btn1=types.InlineKeyboardButton(txt_addtarea,callback_data="addtarea")
            btn2=types.InlineKeyboardButton(txt_fintarea,callback_data="fintarea")
            btn3=types.InlineKeyboardButton(txt_deltarea,callback_data="deltarea")
            btn4=types.InlineKeyboardButton(txt_vertareas,callback_data="vertareas")
            markup.row(btn1,btn2)
            markup.add(btn3)
            markup.add(btn4)
            bot.send_message(message.chat.id, saludo.format(nombre=message.from_user.first_name),reply_markup=markup)


    else:
        bot.send_message(message.chat.id, emojize("Esta tarea no está en tu lista..."))
            
    
print("El bot se está ejecutando")
while True:
    try:
        bot.polling()
    except:
        "Error en el bot"

