# PortScan - Ferramenta de varredura de portas
# Desenvolvida por Davidson Dorvil   
# GitHub: https://github.com/Dorvil

import socket

def realizar_port_scan(host, portas):
    resultados = {}
    for porta in portas:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((host, porta))
            resultados[porta] = "Aberta"
            sock.close()
        except (socket.timeout, socket.error):
            resultados[porta] = "Fechada"
    
    return resultados

def main():
    print("******************************************************")
    print("*                  PortScan - v1.0                    *")
    print("*               Desenvolvido por Davidson Dorvi       *")
    print("*                  GitHub: https://github.com/Dorvil  *")
    print("******************************************************")

    host = input("Digite o endereço IP para realizar a varredura: ")
    portas_str = input("Digite as portas a serem verificadas (separadas por vírgula): ")

    try:
        portas = [int(p) for p in portas_str.split(",")]
    except ValueError:
        print("Por favor, insira portas válidas.")
        return

    resultados = realizar_port_scan(host, portas)

    print("\nResultado da Varredura:")
    print("------------------------")
    
    for porta, status in resultados.items():
        print(f"Porta {porta}: {status}")

if __name__ == "__main__":
    main()
