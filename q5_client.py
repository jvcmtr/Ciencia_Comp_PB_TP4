from q5_telnet_constants import *
import socket
import argparse


def main(address, verbose=False):
    def prt(s, **kwargs):
        if verbose: print(s, **kwargs)
    prt("_____________________________________")
    prt("    EXECUTANDO CLIENTE TELNET")

    prt("[TELNET] Criando socket...", end="")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    prt("Sucesso")

    prt(f"[TELNET] Estabelecendo conexão com {address[0]}:{address[1]} ... ", end="")
    s.connect(address)
    prt("Sucesso")
    prt("--------------------------------------------------------")
    
    EXIT = ["exit", "close", "quit"]
    try:
        while True:
            cmd = input("$> ")
            if cmd.lower() in EXIT: 
                break
            
            s.send(cmd.encode(TELNET_DEFAULT_ENCODING))
            response = s.recv(4096) # O retorno pode ser de qualquer tamanho
            print(response.decode(TELNET_DEFAULT_ENCODING))

    finally:
        prt("[TELNET] Finalizando sessão ... ", end="")
        s.close()
        prt("Sucesso")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--verbose",
        type=lambda x: x.lower() == "true",
        default=True,
    )

    parser.add_argument(
        "--host",
        type=str,
        default=IP,
    )

    parser.add_argument(
        "--port",
        type=int,
        default=TELNET_DEFAULT_PORT,
    )

    args = parser.parse_args()
    main((args.host, args.port), args.verbose)