---

# Instalação do Mosquitto no Raspberry Pi e Configuração de Certificado SSL

## Parte 1: Instalando o Mosquitto no Raspberry Pi

### 1. Atualizar pacotes e repositórios
Antes de instalar o Mosquitto, é recomendável atualizar todos os pacotes no Raspberry Pi:
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Instalar o Mosquitto e seus utilitários
Instale o Mosquitto (servidor MQTT) e o cliente Mosquitto para realizar testes:
```bash
sudo apt install mosquitto mosquitto-clients -y
```

### 3. Habilitar e iniciar o serviço Mosquitto
Após a instalação, habilite o serviço para iniciar automaticamente e inicie o Mosquitto:
```bash
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```

### 4. Editar o arquivo de configuração `mosquitto.conf`
O arquivo de configuração principal do Mosquitto está localizado em `/etc/mosquitto/mosquitto.conf`. A configuração do Mosquitto permite controlar várias funcionalidades, como autenticação e permissões. Para fins de testes, vamos permitir conexões anônimas (não recomendável para ambientes de produção).

Edite o arquivo de configuração:
```bash
sudo nano /etc/mosquitto/mosquitto.conf
```

Adicione ou edite a seguinte linha no arquivo para permitir conexões anônimas:
```bash
allow_anonymous true
```

Isso permitirá que qualquer cliente se conecte ao servidor Mosquitto sem fornecer credenciais. **Lembre-se de desabilitar essa configuração em um ambiente de produção** para garantir segurança.

### 5. Reiniciar o Mosquitto
Depois de salvar as alterações, reinicie o serviço para aplicar a nova configuração:
```bash
sudo systemctl restart mosquitto
```

---

## Parte 2: Criando Certificados SSL com OpenSSL

Abaixo está o passo a passo para criar certificados SSL para proteger a comunicação MQTT com o Mosquitto usando OpenSSL.

### 1. Gerar a chave privada para a Autoridade Certificadora (CA)
Este comando cria uma chave privada de 2048 bits e protege-a com uma senha. Esta chave será usada para assinar o certificado da CA:
```bash
openssl genrsa -des3 -out ca.key 2048
```
- **`genrsa`**: Gera uma chave privada RSA.
- **`-des3`**: Protege a chave com criptografia DES3.
- **`-out ca.key`**: Define o nome do arquivo da chave privada.

### 2. Criar o certificado da Autoridade Certificadora (CA)
Este comando gera um certificado de auto-assinatura para a CA, válido por 5 anos (1826 dias):
```bash
openssl req -new -x509 -days 1826 -key ca.key -out ca.crt
```
- **`req -new`**: Gera um novo pedido de assinatura de certificado.
- **`-x509`**: Cria um certificado autoassinado.
- **`-days 1826`**: Define a validade do certificado para 5 anos.
- **`-key ca.key`**: Usa a chave privada criada anteriormente.
- **`-out ca.crt`**: Especifica o nome do arquivo de saída para o certificado.

### 3. Gerar a chave privada para o servidor MQTT
Agora, gere a chave privada para o servidor Mosquitto:
```bash
openssl genrsa -out server.key 2048
```
- **`genrsa`**: Gera uma chave privada RSA.
- **`-out server.key`**: Define o nome da chave privada do servidor.

### 4. Criar uma Solicitação de Assinatura de Certificado (CSR)
O próximo passo é gerar um pedido de assinatura de certificado (CSR), que será assinado pela CA:
```bash
openssl req -new -out server.csr -key server.key
```
- **`req -new`**: Cria uma nova solicitação de assinatura de certificado.
- **`-out server.csr`**: Define o nome do arquivo CSR gerado.
- **`-key server.key`**: Usa a chave privada do servidor.

### 5. Assinar o certificado do servidor usando a CA
Finalmente, o certificado do servidor é assinado pela CA, tornando-o válido. O certificado será válido por 1 ano (360 dias):
```bash
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 360
```
- **`x509 -req`**: Gera o certificado a partir da solicitação (CSR).
- **`-in server.csr`**: Especifica o CSR gerado anteriormente.
- **`-CA ca.crt`**: Usa o certificado da CA para assinar.
- **`-CAkey ca.key`**: Usa a chave privada da CA para assinar.
- **`-CAcreateserial`**: Cria um número de série para o certificado.
- **`-out server.crt`**: Define o nome do arquivo de saída do certificado do servidor.
- **`-days 360`**: Define a validade do certificado para 1 ano.

---

Aqui está um passo a passo para a instalação e uso básico do **TShark**, a versão de linha de comando do **Wireshark**, que é usado para capturar e analisar pacotes de rede.

---

# Instalação e Uso do TShark

## 1. Instalando o TShark

### 1.1. Atualizar pacotes e repositórios
Primeiro, atualize os repositórios e pacotes no sistema para garantir que o software mais recente seja instalado:
```bash
sudo apt update && sudo apt upgrade -y
```

### 1.2. Instalar o TShark
No Raspberry Pi (ou qualquer sistema baseado em Linux), instale o TShark com o seguinte comando:
```bash
sudo apt install tshark -y
```

Se solicitado, permita que o grupo de usuários sem privilégios execute capturas de pacotes:
```bash
sudo dpkg-reconfigure wireshark-common
```
Escolha "Yes" quando perguntado.

### 1.3. Adicionar o usuário ao grupo `wireshark` (opcional)
Para permitir que o seu usuário execute o TShark sem precisar de permissões de superusuário, adicione o usuário ao grupo `wireshark`:
```bash
sudo usermod -aG wireshark $USER
```
Após isso, reinicie ou faça logout e login novamente para que as mudanças tenham efeito.

---

## 2. Usando o TShark

### 2.1. Verificar as interfaces de rede
Antes de iniciar a captura de pacotes, é importante verificar quais interfaces de rede estão disponíveis no sistema:
```bash
tshark -D
```
Isso listará as interfaces de rede disponíveis (ex: `1. eth0`, `2. wlan0`). Use o número da interface desejada para capturar os pacotes.

### 2.2. Capturando pacotes de rede
Para capturar pacotes em uma interface específica, use o seguinte comando:
```bash
sudo tshark -i 1
```
- **`-i 1`**: Especifica a interface (neste caso, a interface `1`, como `eth0`). Ajuste o número de acordo com a interface que deseja capturar.
- O TShark começará a capturar e exibir os pacotes diretamente na linha de comando.

### 2.3. Salvar captura em um arquivo
Para salvar a captura de pacotes em um arquivo para análise posterior:
```bash
sudo tshark -i 1 -w captura.pcap
```
- **`-w captura.pcap`**: Especifica o arquivo de saída (formato `.pcap`).

### 2.4. Ler um arquivo de captura
Se você já tem um arquivo `.pcap` salvo e quer analisá-lo:
```bash
tshark -r captura.pcap
```
- **`-r captura.pcap`**: Lê o arquivo de captura e exibe o conteúdo.

### 2.5. Filtros básicos no TShark
Você pode aplicar filtros ao capturar pacotes ou analisar arquivos de captura:

- **Captura somente pacotes HTTP:**
  ```bash
  sudo tshark -i 1 -f "tcp port 80"
  ```
  O filtro **`tcp port 80`** captura pacotes que usam a porta 80 (HTTP).

- **Captura somente pacotes de um IP específico:**
  ```bash
  sudo tshark -i 1 -f "host 192.168.1.100"
  ```

- **Exibir apenas pacotes com um filtro Wireshark:**
  Se você já tiver um arquivo `.pcap`, use filtros para exibir somente o que é relevante. Por exemplo, para exibir somente pacotes MQTT:
  ```bash
  tshark -r captura.pcap -Y mqtt
  ```

### 2.6. Exportar informações de pacotes para um arquivo de texto
Se você deseja exportar os dados da captura para um arquivo legível:
```bash
tshark -r captura.pcap > captura.txt
```
Isso exporta os detalhes da captura para um arquivo de texto.

---

## 3. Analisando Pacotes Específicos

### 3.1. Filtrar pacotes por protocolo
Você pode usar filtros para focar em pacotes de protocolos específicos, como MQTT, HTTP, TCP, UDP, etc.

- **Mostrar somente pacotes MQTT:**
  ```bash
  tshark -r captura.pcap -Y mqtt
  ```

- **Mostrar somente pacotes TCP:**
  ```bash
  tshark -r captura.pcap -Y tcp
  ```

### 3.2. Detalhamento de pacotes específicos
Se você quiser ver os detalhes de um pacote específico, use o número da linha (ex: pacote número `5`):
```bash
tshark -r captura.pcap -Y mqtt -V -c 5
```
- **`-V`**: Mostra todos os detalhes do pacote.
- **`-c 5`**: Mostra o pacote de número 5.

---

## 4. Considerações Finais

O TShark é uma ferramenta poderosa para capturar e analisar pacotes de rede diretamente pela linha de comando. Este guia cobre os fundamentos de instalação, captura e análise de pacotes. Para ambientes mais complexos, você pode integrar o TShark com outras ferramentas para uma análise de rede robusta.

---

### Considerações Finais
Agora você possui um servidor Mosquitto configurado no Raspberry Pi e um conjunto de certificados SSL para garantir uma comunicação segura usando MQTT. Esses certificados podem ser usados no arquivo de configuração do Mosquitto para habilitar SSL/TLS.

