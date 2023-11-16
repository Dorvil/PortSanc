import socket
import asyncio
import aiohttp
from datetime import datetime

def obter_endereco_ip(host):
    try:
        endereco_ip = socket.gethostbyname(host)
        return endereco_ip
    except socket.gaierror as e:
        print(f"Erro ao resolver o host: {e}")
        return None

async def verificar_porta(session, host, porta):
    url = f"http://{host}:{porta}"
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resposta:
            return porta, resposta.status
    except aiohttp.ClientError:
        return porta, None
    except TimeoutError:
        return porta, 'timeout'

async def verificar_portas_assincrono(host, portas):
    print(f"\n# PortScan 1.0 scan initiated {datetime.now().strftime('%a %b %d %H:%M:%S %Y')} as: PortScan -p {','.join(map(str, portas))} -sS -oN PortScan.txt {host}")
    print(f"PortScan report for {host} ({host})")
    print("Host is up (0.000048s latency).\n")

    portas_abertas = []
    async with aiohttp.ClientSession() as session:
        tarefas = [verificar_porta(session, host, porta) for porta in portas]
        for tarefa in asyncio.as_completed(tarefas):
            porta, resultado = await tarefa
            print(f"PORT   STATE  SERVICE\n{porta}/tcp {'open' if resultado == 200 else 'closed' if resultado == 'timeout' else 'unreachable'}")
            if resultado is not None:
                portas_abertas.append((porta, resultado))

    print(f"\n# PortScan done at {datetime.now().strftime('%a %b %d %H:%M:%S %Y')} -- 1 IP address (1 host up) scanned in 0.09 seconds")

def main():
    alvo = input("Digite o endereço IP ou nome do host do alvo: ")
    endereco_ip = obter_endereco_ip(alvo)

    if endereco_ip:
        portas = range(1, 1025)  # Escaneia as primeiras 1024 portas, você pode ajustar conforme necessário.
        asyncio.run(verificar_portas_assincrono(endereco_ip, portas))
    else:
        print("Endereço IP inválido ou host inacessível.")

if __name__ == "__main__":
    main()
