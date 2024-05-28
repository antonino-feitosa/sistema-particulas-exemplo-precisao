# Exemplo de Colisão Imperfeita

Exemplo de colisão entre esferas com conservação de energia.

Note que a energia não é conservada no sistema devido à representação imperfeita das colisões. A verificação ocorre a cada frame, porém, as colisões não ajustam as distâncias percorridas entre os frames. Uma solução é calcular o instante exato da colisão e mover a partículas de modo proporcional.

### Parâmetros

```
python3 main.py [--seed <seed>] [--size <size>] [--example <example>]
```

Em que:
- seed: Valor utilizado para geração de valores aleatórios.
- size: Quantidade de esferas na simulação.
- example: Executa um dos exemplos configurados: 1 ou 2.


### Dependência
```
python3 -m pip install -U pygame --user
```
