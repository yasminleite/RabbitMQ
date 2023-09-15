import pika
from threading import Thread
from tkinter import *

rabbitmq_username = "ads"
rabbitmq_password = "ads"

def receber():
    def chamada(ch, method, propreties, body):
        msg_list.insert(END, "Receptor -- " + body.decode())

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost',
            port=5672,
            virtual_host='/',
            credentials=pika.PlainCredentials(rabbitmq_username, rabbitmq_password)))

        canal = connection.channel()
        canal.queue_declare(queue='chat1')

        if (canal.basic_consume(queue='chat1', on_message_callback=chamada, auto_ack=True)):
            msg_list.insert(END)

        canal.start_consuming()
        connection.close()
    except Exception as e:
        print("Erro ao se conectar ao RabbitMQ:", e)

def enviar():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost',
            port=5672,
            virtual_host='/',
            credentials=pika.PlainCredentials(rabbitmq_username, rabbitmq_password)))

        canal = connection.channel()
        canal.queue_declare(queue='chat2')

        mensagem = campo_entrada.get()                                                     
        msg_list.insert(END, "Emissor -- " + mensagem)                                     

        canal.basic_publish(exchange='', routing_key='chat2', body=mensagem)               
        connection.close()
        
    #Limpar o campo de entrada após o envio
        campo_entrada.delete(0, END)
    except Exception as e:
        print("Erro ao se conectar ao RabbitMQ:", e)

janela = Tk()
janela.title("Chat 1")

msg_list = Listbox(janela, height=10, width=50)
msg_list.pack()

campo_entrada = Entry(janela, textvariable='') 
campo_entrada.pack()

Botao_enviar = Button(janela, text="Enviar", command=enviar)
Botao_enviar.pack()

receive_thread = Thread(target=receber)
sender_thread = Thread(target=enviar)
receive_thread.start()
sender_thread.start()

janela.mainloop()