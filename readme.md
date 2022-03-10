# Forest Fire By Tree
## Aluno
    Allann Gois Hoffmann
    180029789
 
# Sobre a simulação
## Modelo
O modelo base para a simulação foi o `Forest Fire`, que tem como objetivo mostrar como o fogo se propaga em uma floresta
 
## Hipótese
Existem diferentes tipos de árvores e com diferentes características, sendo uma delas a resistência ao fogo. Com isso temos árvores que tem uma facilidade maior para propagar o fogo e árvores mais resistentes dependendo da força do fogo.
 
## Mudanças realizadas
### Agent
Foi adicionada espécies de árvores baseado em um [estudo](https://www.fs.fed.us/rm/pubs/rmrs_gtr292/1934_starker.pdf) realizado na América do Norte. Com essas espécies existem uma diferença na chance da árvore mais resistente pegar fogo
Adição da característica `log_strength`, que tem como objetivo aumentar a resistência ao fogo em geral. Essa resistência pode ser "traduzida" como cascas mais grossas, raízes mais profundas e outros.
 
### Model
Adição da característica de `fire_power` que se relaciona com a força do fogo na floresta.
Contador de clusters (ilhas) de árvores que permaneceram inteiras durante a queimada.
 
## Como utilizar
Instale todos os requisitos do sistema com `pip install -r requirements.txt`.
Ao instalar, realiza a execução do sistema com o comando: `mesa runserver`
 
## Aplicação
Com a aplicação rodando, temos três sliders:
- `Tree density`
- `Log strength`
- `Fire power`
 
O primeiro influencia na quantidade de árvores no grid.
O segundo influencia na força das árvores contra o fogo.
O terceiro influencia na força do fogo.
 
Abaixo do grid, temos alguns gráficos:
- Número de árvores vivas, queimadas ou em chamas.
- Número de cada espécie viva na floresta.
- Número de clusters (ilhas) na floresta.
 
## Arquivos CSV
- `Model_data`: Contém os dados de árvores vivas, árvores mortas, árvores em chamas e número de clusters
- `Agent_data`: Possui a quantidade de cada árvore na florestas, sendo elas:
(Ordem das menos resistente para as mais resistentes)
    - "Abies_lasiocarpa"
    - "Tsuga_heterophylla"
    - "Tsuga_mertensiana"
    - "Picea_engelmannii"
    - "Thuja_plicata"
    - "Pinus_monticola"
    - "Pinus_contorta"
    - "Abies_grandis"
    - "Pseudotsuga_menziesii"
    - "Pinus_ponderosa"
    - "Larix_occidentalis"
           
 
# Readme Original
# Forest Fire Model
 
## Summary
 
The [forest fire model](http://en.wikipedia.org/wiki/Forest-fire_model) is a simple, cellular automaton simulation of a fire spreading through a forest. The forest is a grid of cells, each of which can either be empty or contain a tree. Trees can be unburned, on fire, or burned. The fire spreads from every on-fire tree to unburned neighbors; the on-fire tree then becomes burned. This continues until the fire dies out.
 
## How to Run
 
To run the model interactively, run ``mesa runserver`` in this directory. e.g.
 
```
    $ mesa runserver
```
 
Then open your browser to [http://127.0.0.1:8521/](http://127.0.0.1:8521/) and press Reset, then Run.
 
To view and run the model analyses, use the ``Forest Fire Model`` Notebook.
 
## Files
 
### ``forest_fire/model.py``
 
This defines the model. There is one agent class, **TreeCell**. Each TreeCell object which has (x, y) coordinates on the grid, and its condition is *Fine* by default. Every step, if the tree's condition is *On Fire*, it spreads the fire to any *Fine* trees in its [Von Neumann neighborhood](http://en.wikipedia.org/wiki/Von_Neumann_neighborhood) before changing its own condition to *Burned Out*.
 
The **ForestFire** class is the model container. It is instantiated with width and height parameters which define the grid size, and density, which is the probability of any given cell having a tree in it. When a new model is instantiated, cells are randomly filled with trees with probability equal to density. All the trees in the left-hand column (x=0) are set to *On Fire*.
 
Each step of the model, trees are activated in random order, spreading the fire and burning out. This continues until there are no more trees on fire -- the fire has completely burned out.
 
 
### ``forest_fire/server.py``
 
This code defines and launches the in-browser visualization for the ForestFire model. It includes the **forest_fire_draw** method, which takes a TreeCell object as an argument and turns it into a portrayal to be drawn in the browser. Each tree is drawn as a rectangle filling the entire cell, with a color based on its condition. *Fine* trees are green, *On Fire* trees red, and *Burned Out* trees are black.
 
## Further Reading
 
Read about the Forest Fire model on Wikipedia: http://en.wikipedia.org/wiki/Forest-fire_model
 
This is directly based on the comparable NetLogo model:
 
Wilensky, U. (1997). NetLogo Fire model. http://ccl.northwestern.edu/netlogo/models/Fire. Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.
 
 

