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

### Considerações Finais
Agora você possui um servidor Mosquitto configurado no Raspberry Pi e um conjunto de certificados SSL para garantir uma comunicação segura usando MQTT. Esses certificados podem ser usados no arquivo de configuração do Mosquitto para habilitar SSL/TLS.

