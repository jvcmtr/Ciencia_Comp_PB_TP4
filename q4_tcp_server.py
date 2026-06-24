import socket
from q4_constants import *

def _on_message_recieved(client, message):
    print(f" Mensagem recebida do cliente: {client}")
    print(f" Mensagem: \t({len(message)} caracteres)")
    print('"' + message + '"')
    return message

def start_tcp_server(buffer_size=DEFAULT_BUFFER_SIZE, decode_format=DEFAULT_DECODE_FORMAT, verbose=False, handler=_on_message_recieved):
    def prt(s, **kwargs):
        if verbose: print(s, **kwargs)

    prt("_______________________________")
    prt("    INICIANDO SOCKET TCP ")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(ADDR)
    s.listen()
    prt(f"[TCP SEVER] Socket ativo em: {ADDR}")

    while True:
        try:
            conection,client = s.accept()
            prt(f"[TCP SEVER] Nova conexão estabelecida. {client[0]}:{client[1]}")
            prt("--------------------------------------------------------")
            while True:
                data = conection.recv(buffer_size)
                if not data: break
                msg = data.decode(decode_format)
                response = handler(client, msg)
                if response:
                    conection.sendto(msg.encode(decode_format), client)
                prt("--------------------------------------------------------")
            prt(f"[TCP SEVER] Conexão encerrada com o cliente. {client[0]}:{client[1]}")
        
        except Exception as e:
            raise e
            print(f"\t[ERRO] [TCP SEVER] Uma falha ocorreu ao processar uma mensagem: {e}")

    prt("[TCP SEVER] Fechando socket...", end="")
    s.close()
    prt("Sucesso")

if __name__ == "__main__":
    start_tcp_server(verbose=True)



    