from q5_telnet_constants import *
import socket
import subprocess
import argparse


def start_telnet_server(port, verbose=False):
    def prt(s, **kwargs):
        if verbose: print(s, **kwargs)
    prt("_______________________________")
    prt("    INICIANDO TELNET ")
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = ((IP, port))
    s.bind(address)
    s.listen()
    prt(f"[TELNET] Servidor aguardando em: {address[0]}:{address[1]}")

    while True:
        try:
            conection,client = s.accept()
            prt(f"[TELNET] Nova conexão estabelecida. {client[0]}:{client[1]}")
            while True:
                data = conection\
                    .recv(TELNET_DEFAULT_BUFFERSIZE)\
                    .decode(TELNET_DEFAULT_ENCODING)\
                    .strip()
                if not data: 
                    break

                print(f"[TELNET] Comando recebido:")
                print(data)
                print(f"[TELNET] Executando...")
                
                try:
                    result = subprocess.check_output(data, shell=True)
                    print(result)
                    conection.send(result)
                except Exception as e:
                    print(f"[TELNET] Um erro ocorreu ao executar o comando do cliente: {e}")
                    conection.send(f"{e}".encode(TELNET_DEFAULT_ENCODING))

            prt(f"[TELNET] Conexão encerrada com o cliente. {client[0]}:{client[1]}")        
        except Exception as e:
            print(e)
            break

    prt("[TELNET] Encerrando servidor...", end="")
    s.close()
    prt("Sucesso")


if __name__ == "__main__":
    # Sei que não precisa, mas achei legal fazer
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--verbose",
        type=lambda x: x.lower() == "true",
        default=True,
    )

    parser.add_argument(
        "--port",
        type=int,
        default=TELNET_DEFAULT_PORT,
    )

    args = parser.parse_args()
    start_telnet_server(args.port, args.verbose)