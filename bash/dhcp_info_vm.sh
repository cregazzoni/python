#!/bin/bash

# Prima di eseguire:
# Crea un file List con elenco hostnames da verificare

# Itera su ogni host nel file "List"
for host in $(cat List); do

  # Collega tramite SSH utilizzando sshpass per fornire la password
  ssh -l core -i id_rsa -o StrictHostKeyChecking=no "$host" \
  "ip -o addr show | awk '/inet / && \$2 != \"lo\" {print \$2, \$4}' && ip link show | awk '/link\/ether/ {print \$2}'" > /tmp/info_$host.txt

  if [ $? -eq 0 ]; then
    # Estrai nome interfaccia, IP e MAC address
    INTERFACE=$(awk '{print $1}' /tmp/info_$host.txt | head -n 1)
    IP_ADDRESS=$(awk '{print $2}' /tmp/info_$host.txt | head -n 1 | awk -F"/" '{print $1}')
    MAC_ADDRESS=$(awk '/:/ {print $1}' /tmp/info_$host.txt | head -n 1)

    # Mostra le variabili
    echo "$host|$INTERFACE|$IP_ADDRESS|$MAC_ADDRESS"
	echo "$host|$IP_ADDRESS|$MAC_ADDRESS" >> info.out
  else
    echo "Errore nel collegamento a $host"
  fi
  
  rm -f /tmp/info_$host.txt

done
