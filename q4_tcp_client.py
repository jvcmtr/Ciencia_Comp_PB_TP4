import socket
from q4_constants import *

def send_messages(host, port, messages, decode_format=DEFAULT_DECODE_FORMAT, buffer_size=DEFAULT_BUFFER_SIZE, verbose=False):
    def prt(s, **kwargs):
        if verbose: print(s, **kwargs)
    addr = (host, port)

    prt("_____________________________________")
    prt("    EXECUTANDO CLIENT TCP")

    prt("[TCP CLIENT] Criando socket...", end="")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    prt("Sucesso")

    prt(f"[TCP CLIENT] Estabelecendo conexão com {host}:{port} ... ", end="")
    s.connect(addr)
    prt("Sucesso")
    prt("--------------------------------------------------------")

    responses = []

    try:
        for m in messages:
            try:
                prt(f" Enviando mensagem para o servidor em {host}:{port} ... ", end="")
                s.sendall(m.encode(decode_format))
                prt(f"Mensagem enviada")

                prt(f" Recebendo resposta do servidor ...", end="")
                resp = s.recv(buffer_size)
                if not resp:
                    prt("SEM RESPOSTA")
                    continue
                else:
                    r = resp.decode(decode_format)
                    prt("Sucesso")
                    prt(f' Resposta: "{r}"')

            except Exception as e:
                prt("!! FALHA !!")
                prt(e)
                responses.append(f"{e}")
            finally:
                prt("--------------------------------------------------------")
    finally:
        prt("[TCP CLIENT] Fechando, socket ... ", end="")
        s.close()
        prt("Sucesso")
        return messages

if __name__ == "__main__":
    send_messages(IP, PORT, ["Olá", "TCP"], verbose=True)




    