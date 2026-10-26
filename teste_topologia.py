#!/usr/bin/env python3
import sys
from time import sleep
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel

def start_network(edge_list_file):
    # Inicializa o Mininet com controlador remoto e switches Open vSwitch
    net = Mininet(controller=RemoteController, switch=OVSKernelSwitch)
    c0 = net.addController('c0', ip='127.0.0.1', port=6633)

    edges = []
    switch_names = set()

    # 1. Parsing do ficheiro de topologia
    with open(edge_list_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) == 2:
                u, v = parts[0], parts[1]
                edges.append((u, v))
                switch_names.add(u)
                switch_names.add(v)

    # Ordena os nomes dos switches (ex: s1, s2, s3...)
    sorted_switches = sorted(
        list(switch_names), 
        key=lambda x: int(x.replace('s', '')) if x.replace('s', '').isdigit() else x
    )

    switches = {}
    hosts = {}

    # 2. Instanciação dos switches e criação de um host por switch
    for s_name in sorted_switches:
        # Configura o switch para operar com o protocolo OpenFlow 1.3
        sw = net.addSwitch(s_name, protocols='OpenFlow13')
        switches[s_name] = sw

        # Cria um host associado ao switch (ex: h1 para s1) com IP correspondente (10.0.0.X)
        host_id = s_name.replace('s', '')
        h_name = f"h{host_id}"
        ip_addr = f"10.0.0.{host_id}" if host_id.isdigit() else None

        if ip_addr:
            host = net.addHost(h_name, ip=ip_addr)
        else:
            host = net.addHost(h_name)

        hosts[h_name] = host

        # Conecta o host ao seu respetivo switch
        net.addLink(host, sw)

    # 3. Adiciona os enlaces entre os switches com base na lista de arestas
    for u, v in edges:
        net.addLink(switches[u], switches[v])

    # Inicializa a rede
    net.start()
    print("Aguardando inicialização do controlador...")
    sleep(3)

    # 4. Envio de Gratuitous ARP de todos os hosts para descoberta pelo Ryu
    print("Enviando Gratuitous ARP de todos os hosts para descoberta pelo Ryu...")
    for h in net.hosts:
        h.cmd('arping -U -c 1 ' + h.IP())
        sleep(0.1)

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    if len(sys.argv) > 1:
        start_network(sys.argv[1])
    else:
        print("Uso: sudo python3 teste_topologia.py <arquivo_topologia.txt>")
