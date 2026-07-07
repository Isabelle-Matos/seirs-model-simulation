# Simulação de Propagação de Malware: SEIRS e Correção Humana

Este repositório contém a implementação do modelo epidemiológico SEIRS baseada em autômatos celulares, utilizada para a análise da propagação de *malware* em redes de dispositivos móveis. O projeto utiliza *branches* distintas para diferenciar o modelo base da extensão proposta.

## Estrutura das Branches

O código está organizado da seguinte forma:

* `master`: Contém a implementação original da propagação conforme a metodologia de [1, 2]. Esta *branch* simula a dinâmica de infecção sem intervenção externa, servindo como referência para validação.
* `feature/human-factor`: Contém a versão estendida que introduz o fator humano ($p$) como variável de mitigação. Esta implementação permite analisar como a tomada de decisão individual atua na contenção do surto infeccioso em diferentes topologias de vizinhança.

## Como Executar

Para acessar as diferentes versões do projeto, utilize os comandos do Git para alternar entre as *branches*:

1. Para acessar o modelo base:
   ```bash
   git checkout master

## Referências 
[1] Peng, S., Wang, G., & Yu, S. (2013). Modeling the dynamics of worm propagation using two-dimensional cellular automata in smartphones. Journal of Computer and System Sciences, 79(4), 586-595.
[2] Signes-Pont, M. T., Cortés-Castillo, A., Mora-Mora, H., & Szymanski, J. (2018). Modelling the malware propagation in mobile computer devices. Computers & Security, 79, 80-93