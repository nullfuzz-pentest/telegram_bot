import telebot
import mysql.connector
import re

# Expresiones regulares para validar dominios e IPs
dominio_regex = re.compile(r'^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$')
ip_regex = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')

# Conexión a la base de datos
mydb = mysql.connector.connect(
  host="localhost",
  user="telebot",
  password="yourpassword",
  database="telebot"
)

#Define ID admin telegram user 
telegram_id=yourid

#Api key godfather 
telegram_bot_api_key="YourAPI"

# Inicialización del bot 
bot = telebot.TeleBot(telegram_bot_api_key)

#Definimos comando /info
@bot.message_handler(commands=['info'])
def send_welcome(message):

    # Verificar que el usuario sea "nullzpwd"
    if message.from_user.id != telegram_id:
        bot.reply_to(message, "Lo siento, solo puedo recibir comandos de administrador. 😕")
        return
    #setea nombre de usuario en telegram    
    name = str(message.from_user.first_name)
    #Comentario INFO
    bot.reply_to(message, f'''¡Hola {name}! Soy un bot de BugBounty que puede ayudarte a almacenar IPs, dominios y subdominios en una base de datos.
 
Puedes agregarlos utilizando los comandos: 

    /addip [IP] 
    /adddominio [dominio]  
    /addsubdominio [subdominio]

Asegúrate de seguir las instrucciones para asegurarte de que tus entradas son válidas. ¡Gracias por usar este bot! 😊
''')

# Definimos Comando para agregar IPs /addip
@bot.message_handler(commands=['addip'])
def add_ip(message):

    #debug username
    #print (message.from_user.username)
    
    # Verificar que el usuario sea "nullzpwd"
    if message.from_user.id != telegram_id:
        bot.reply_to(message, "Lo siento, solo puedo recibir comandos de administrador. 😕")
        return
    if len(message.text.split()) < 2:
        bot.reply_to(message, "Debes proporcionar una ip. Ejemplo: /addip 192.168.0.1")
        return 

    ip = message.text.split()[1]

    # Validar que la IP sea válida
    if not ip_regex.match(ip):
        bot.reply_to(message, "La IP no es válida. 😕")
        return

    # Verificar que la IP no esté ya almacenada en la base de datos
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM dominios_ips WHERE valor = %s", (ip,))
    result = cursor.fetchone()
   
    if result:
        bot.reply_to(message, "Esta IP ya ha sido almacenada. 😊 ")
    else:

        # Insertar la IP en la base de datos
        cursor.execute("INSERT INTO dominios_ips (valor, tipo) VALUES (%s, 'IP')", (ip,))
        mydb.commit()
        bot.reply_to(message, "IP almacenada correctamente. 😊")

# Definimos Comando para agregar dominios /adddominio
@bot.message_handler(commands=['adddominio'])
def add_dominio(message):

    #debug username
    print (message.from_user.id)
    
    # Verificar que el usuario sea "nullzpwd"   
    if message.from_user.id != telegram_id:
        bot.reply_to(message, "Lo siento, solo puedo recibir comandos de administrador. 😕")
        return
    if len(message.text.split()) < 2:
        bot.reply_to(message, "Debes proporcionar un dominio. Ejemplo: /adddominio dominio.com")
        return 
    dominio = message.text.split()[1]

    # Validar que el dominio sea válido
    if not dominio_regex.match(dominio):
        bot.reply_to(message, "El dominio no es válido. 😕")
        return
    # Verificar que el dominio no esté ya almacenado en la base de datos
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM dominios_ips WHERE valor = %s", (dominio,))
    result = cursor.fetchone()
    if result:
        bot.reply_to(message, "Este dominio ya ha sido almacenado. 😊 ")
    else:
        # Insertar el dominio en la base de datos
        cursor.execute("INSERT INTO dominios_ips (valor, tipo) VALUES (%s, 'dominio')", (dominio,))
        mydb.commit()
        bot.reply_to(message, "Dominio almacenado correctamente. 😊")

# Comando para agregar subdominios /addsubdominio
@bot.message_handler(commands=['addsubdominio'])
def add_subdominio(message):

    #debug username
    #id_user=str(message.from_user.id)
    #print (id_user)
    if message.from_user.id != telegram_id:
        bot.reply_to(message, "Lo siento, solo puedo recibir comandos del administrador. 😕")
        return
    if len(message.text.split()) < 2:
        bot.reply_to(message, "Debes proporcionar un subdominio. Ejemplo: /addsubdominio ejemplo.misitio.com")
        return
    subdominio = message.text.split()[1]

    # Validar que el subdominio sea válido
    if not dominio_regex.match(subdominio):
        bot.reply_to(message, "El subdominio no es válido. 😕")
        return
    # Verificar que el subdominio no esté ya almacenado en la base de datos
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM dominios_ips WHERE valor = %s", (subdominio,))
    result = cursor.fetchone()
    if result:
        bot.reply_to(message, "Este subdominio ya ha sido almacenado. 😊 ")
    else:
        # Insertar el subdominio en la base de datos
        cursor.execute("INSERT INTO dominios_ips (valor, tipo) VALUES (%s, 'subdominio')", (subdominio,))
        mydb.commit()
        bot.reply_to(message, "Subdominio almacenado correctamente. 😊")

# Iniciar el bot
bot.polling()
