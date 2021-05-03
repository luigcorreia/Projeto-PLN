# Assinatura etimológica de textos usada na identificação de autores nativos e não-nativos.

Projeto para a disciplina de Processamento de Linguagem Natural baseado-se no artigo: https://aclweb.org/anthology/D17-1286

No artigo original, os autores tentam verficar a interferência da língua nativa na escolha das palavras em textos escritos por estudantes não-nativos de inglês, ao preferir termos que são cognatos ou relacionados etimologicamente com termos do seu idioma nativo. A partir de um modelo preditivo que leva em consideração a etimologia das palavras, os autores não observaram diferença significante na acurácia quando adicionaram informação etimológica nos dados tratados, mas conseguiram reconstruir uma árvore geneálogica das línguas identificadas nos textos com bastante similaridade com a genealogia real.

Neste projeto reproduzimos a ideia do artigo utilizando um classificador SVM e dois corpus com textos de nativos e não-nativos (The Uppsala Student English Corpus e British Academic Written English Corpus) extraindo uma assinatura etimológica dos textos a partir da busca das palavras em um dicionário etimológico (http://www1.icsi.berkeley.edu/~demelo/etymwn/). 

Apesar de também não observar diferença na acurácia, observamos que o modelo com informações etimológicas é mais resistente a overfiting.

Link para apresentação completa: https://bit.ly/3ui7uRQ
