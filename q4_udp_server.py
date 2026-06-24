import socket
from q4_constants import *

def _on_message_recieved(client, message):
    print("_______________________________")
    print(f" Mensagem recebida do cliente: {client}")
    print(f" Mensagem:  \t  \t  \t({len(message)} caracteres)")
    print('"' + message + '"')
    return message


def start_udp_server(buffer_size=DEFAULT_BUFFER_SIZE, decode_format=DEFAULT_DECODE_FORMAT, verbose=False, handler=_on_message_recieved):
    def prt(s, **kwargs):
        if verbose: print(s, **kwargs)

    prt("_______________________________")
    prt("    INICIANDO SOCKET UDP ")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(ADDR)
    prt(f"[UDP SERVER] Socket ativo em: {ADDR}")
    prt("--------------------------------------------------------")
            
    while True:
        try:
            data, client = s.recvfrom(buffer_size)
            msg = handler(client, data.decode(decode_format))
            s.sendto(msg.encode(decode_format), client)
        except Exception as e:
            print(f"\t[ERRO] Uma falha ocorreu ao processar uma mensagem: {e}")

    prt("--------------------------------------------------------")        
    prt("[UDP SERVER] Fechando socket...", end="")
    s.close()
    prt("Sucesso")

if __name__ == "__main__":
    start_udp_server(verbose=True)


    