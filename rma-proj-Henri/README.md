# Projeto final de RMA
##### Ideia
Fazer um robô que se mova através do circuito no arquivo `src/plano_5x5_com_carrinho.ttt` de forma autônoma.

##### Estrutura (passível de mudança ao longo do projeto)
```
src
├── camp_pot.py
├── plano_5x5_com_carrinho.ttt
├── remoteApi.dll
├── remoteApi.so
├── s1.py
├── simConst.py
└── sim.py
```
##### Guia básico
O arquivo `src/sim.py` controla as funções de simulação do robô, com o arquivo sendo disponibilizado pelo Coppelia (ferramenta da simulação). 
Para executar o projeto, basta ter o python e o coppelia instalados. É possível executar os comandos manualmente, mas também há um makefile que executa diretamente os seguintes comandos:
- s1 (executa o arquivo s1.py)
- camp (executa o arquivo camp_pot.py)
Caso não saiba usar o make, basta digitar no terminal `make run (comando)`
Para o funcionamento dos scripts, é necessário anteriormente iniciar a simulação no coppelia, seguindo o passo a passo:
[Colocar aqui o passo a passo com prints]

##### O que falta
No S1:
1. Fazer o robô evitar paredes
2. Implementação da lógica de seguir caminhos (possivelmente até algum objetivo)

No camp_pot:
1. Corrigir o loop/adicionar outras condições

##### ERROS ATUAIS
- em `src/camp_pot.py`, há um loop incompleto, que dá erro e impede a execução do script
- O robô não se move corretamente em `src/s1.py`, batendo nas paredes e segue sem caminho

##### Membros
- Henrique Silva Barbosa
- Matheus Souza Zanzin
- Rodrigo Guikang Liu
