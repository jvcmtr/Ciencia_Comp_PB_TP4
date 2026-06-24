import socket
from q4_constants import *

def send_messages(host, port, messages, decode_format=DEFAULT_DECODE_FORMAT, verbose=False):
    def prt(s, **kwargs):
        if verbose: print(s, **kwargs)

    prt("_____________________________")
    prt("    EXECUTANDO CLIENT UDP")
    prt("[UDP CLIENT] Criando socket... ", end="")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    prt("Sucesso")
    prt("--------------------------------------------------------")


    try:
        for m in messages:
            prt(f"[UDP CLIENT] Enviando mensagem para o servidor em {host}:{port} ... ", end="")
            s.sendto(m.encode(decode_format), (host, port))
            prt(f"Mensagem enviada")
            prt(f' Servidor: {host}:{port}')
            prt(f' Mensagem: "{m}"')
            prt("--------------------------------------------------------")
    finally:
        prt("[UDP CLIENT] Fechando, socket ...", end="")
        s.close()
        prt("Sucesso")


if __name__ == "__main__":
    send_messages(IP, PORT, ["Olá", "UDP"], verbose=True)



    