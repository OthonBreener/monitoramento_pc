from dashing import HSplit, VSplit, VGauge, HGauge
from time import sleep
from psutil import virtual_memory, swap_memory, cpu_percent, cpu_count
from utils import converter_bytes_para_gb


# Nucleos do CPU
nucleos = cpu_count()
interfaces_por_nucleo = [
    HGauge(title=f'CPU_{index} %') for index in range(1, int(nucleos) + 1)
]

# Interface de dashing

interface = HSplit(
    HSplit(
        VGauge(title="RAM"),
        VGauge(title="SWAP"),
        title='Memória',
        border_color=1
    ),
    VSplit(
        HGauge(title='CPU %'),
        *interfaces_por_nucleo,
        title='CPU',
        border_color=2,
    )
)

while True:

    # Memória
    interface_memoria = interface.items[0]

    ## RAM
    interface_ram = interface_memoria.items[0]
    interface_ram.value = virtual_memory().percent
    interface_ram.title = f'RAM {interface_ram.value} %'

    ## SWAP
    interface_swap = interface_memoria.items[1]
    interface_swap.value = swap_memory().percent
    interface_swap.title = f'SWAP {interface_swap.value} %'

    # CPU
    interface_cpu = interface.items[1]
    
    ## Porcetagem de CPU em uso
    interface_porcentagem_cpu = interface_cpu.items[0]
    interface_porcentagem_cpu.value = cpu_percent()
    interface_porcentagem_cpu.title = f'CPU {interface_porcentagem_cpu.value} %'

    ## Porcentagem de cada core
    interface_porcentagem_por_core = interface_cpu.items[1:nucleos+1]

    nucleos_e_frequencias = enumerate(
        zip(interface_porcentagem_por_core, cpu_percent(percpu=True))
    )
    for i, (nucleo, frequencia) in nucleos_e_frequencias:
        nucleo.value = frequencia
        nucleo.title = f'CPU_{i+1} {frequencia}%'

    try:
        interface.display()
        sleep(0.5)
    except KeyboardInterrupt:
        break