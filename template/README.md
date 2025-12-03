# Nuclear Fallout
Scrivere un programma python che permetta di simulare un mondo post-apocalittico in cui è avvenuta una catastrofe nucleare.

I moduli e le classi vanno sviluppati nel package *fallout*.
Non spostare o rinominare moduli e classi esistenti e non modificare le signature dei metodi.

In *main.py* viene fornito del semplice codice, da voi modificabile, che testa le funzionalità base.
Esso mostra esempi di uso dei metodi principali dei controlli richiesti.

Tutte le eccezioni, se non altrimenti specificato, sono di tipo *VaultException* definito nel modulo *vault*.


## R1: Risorse (6/17)
La classe *Vault* nel modulo *vault* rappresenta un bunker sotterraneo.
Il costruttore accetta come unico parametro il nome che lo identifica univocamente.

La classe astratta *VaultResource* rappresenta una risorsa che possiede delle capacità utili alla sopravvivenza nel bunker.
Una risorsa è identificata univocamente dal suo nome, ottenibile tramite la property:
- ```name(self) -> str```

Inoltre, la classe possiede delle **PROPERTY ASTRATTE** che caratterizzano le capacità della risorsa tramite valori da 0 a 10:
- ```food(self) -> int``` capacità di produrre cibo.
- ```health(self) -> int``` capacità mediche/curative.
- ```maintenance(self) -> int``` capacità di mantenere in funzione gli impianti di sopravvivenza del bunker.

Infine ogni risorsa possiede una dimensione, ottenibile tramite il metodo:
```python
__len__(self) -> int:
```

La classe *Vault* permette di definire due tipi di risorse: ruoli e abitanti.

Il metodo
```python
add_role(self, name: str, food: int, health: int, maintenance: int) -> VaultResource:
```
permette di definire un ruolo che può essere assegnato agli abitanti del bunker.
I metodo accetta come parametri il nome del ruolo, e i valori di capacità da esso richiesti (food, health, maintenance).
Il metodo restituisce il ruolo creato.

Il metodo
```python
add_dweller(self, name: str, vitality: int, *roles: str) -> VaultResource:
```
permette di aggiungere un abitante del bunker.
Il metodo accetta il nome dell'abitante, un numero intero positivo che identifica la sua vitalità, e un numero variabile di nomi di ruoli che deve svolgere.
Il metodo restituisce l'abitante creato.

I valori di capacità di un abitante (food, health, maintenance), sono la somma di quelli richiesti dai ruoli che svolge.
Se la somma dei tre valori di capacità di un abitante supera la sua vitalità, l'abitante non deve essere creato e il metodo deve lanciare un'eccezione.

La dimensione (```__len()__```) di un ruolo è pari al numero di abitanti che lo svolgono, mentre la dimensione (```__len()__```) di un abitante è pari al numero di ruoli che svolge.

Il metodo
```python
get_resource(self, name: str) -> VaultResource
```
della classe *Vault* permette di ottenere una delle risorse create (ruolo o abitante) tramite il nome che le identifica.

**ATTENZIONE**: quando il tipo dell'oggetto restituito da un metodo è **VaultResource**, la notazione include anche le classi figlie (**VaultResource** è astratto).


## R2: Dipartimenti (4/17)
La classe *Vault* permette di definire un terzo tipo di risorsa: i dipartimenti.

Il metodo
```python
add_department(self, name: str, dwellers: List[str], func: Callable[[List[int]], int] = None) -> VaultResource
```
permette di creare un nuovo dipartimento.
Accetta come parametri il nome del dipartimento, la lista dei nomi degli abitanti che ci lavorano (lo stesso abitante può lavorare in più dipartimenti) e una funzione di valutazione che permette di calcolare i valori di capacità di un dipartimento.
Il metodo restituisce il dipartimento creato.

Data una capacità (health, food, o maintenance), la funzione di valutazione accetta come parametro una lista contenente i valori di quella capacità per ciascuno degli abitanti che lavora nel dipartimento, e calcola i valore della capacità per il dipartimento.

La dimensione (```__len()__```) di un dipartimento è pari al numero di abitanti che ci lavorano.

Il metodo
```python
get_most_productive_dweller(self, dept_name) -> Tuple[str, int]:
```
della classe *Vault* accetta come parametro il nome di un dipartimento e restituisce una tupla che identifica l'abitante più produttivo del dipartimento.
La produttività di un abitante è definita come somma dei tre valori di capacità.
La tupla restituita contiene il nome dell'abitante e la sua produttività.

Il metodo
```python
get_resource(self, name: str) -> VaultResource
```
della classe *Vault* deve essere aggiornato di modo da restituire, dato il nome della risorsa, non solo ruoli e abitanti, ma anche dipartimenti.


## R3: Wasteland (3/17)
La classe ```Wasteland``` rappresenta le terre desolate del mondo post-apocalittico, nelle quali sono posizionati i bunker.

Il metodo
```python
add_vaults(self, vaults: List[Vault]) -> None
```
della classe *Wasteland* accetta come parametro una lista di bunker e li aggiunge alla wasteland.

Il metodo
```python
connect_vaults(self, vault_name_1: str, vault_name_2: str, distance: int) -> None
```
della classe *Wasteland* accetta come parametri i nomi di due bunker e la distanza che li separa, definendo un collegamento tra di essi.
Il collegamento definito è **BIDIREZIONALE**.

Il metodo
```python
get_connected(self, vault_name: str) -> Set[str]:
```
della classe *Wasteland* accetta come parametro il nome di un bunker e restituisce un set contenente i nomi dei bunker a esso collegati.
Se non sono presenti collegamenti il metodo deve restituire un **SET VUOTO**.

Il metodo
```python
get_distance(self, vault_name_1: str, vault_name_2: str) -> Optional[int]
```
della classe *Wasteland* accetta come parametro i nomi di due bunker e restituisce la distanza del collegamento tra di essi.
Se i bunker non sono collegati, il metodo deve restituire ```None```.

## R4: Percorsi (4/17)
Il metodo

```python
find_path(self, vault_start_name: str, vault_end_name: str) -> Optional[Tuple[List[str], int]]
```
della classe *Wasteland* accetta come parametri i nomi di un bunker di partenza e di arrivo.
Se presente, il metodo restituisce un percorso che collega i due bunker.
Se non esiste un percorso, il metodo deve restituire ```None```.

Il percorso restituito è rappresentato da una tupla di due elementi.
Il primo elemento contiene la lista di nomi di bunker per cui bisogna transitare per andare dal bunker di partenza a quello di arrivo.
Il secondo elemento rappresenta la distanza del percorso, dato dalla somma della distanza dei collegamenti per cui si transita.

Se più percorsi sono possibili, è sufficiente restituirne uno qualsiasi.
