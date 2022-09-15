# Ingegneria-della-Conoscenza
Progetto di Ingeneria della Conoscenza - Università degli Studi di Bari

## Realizzato da:
* Siciliano Bartolomeo, 724558 - mail: b.siciliano1@studenti.uniba.it

## Come installare i requisiti:
Progetto realizzato in Python 3.10.2 .

E' possibile installare le librerie necessarie dal file ```requirements.txt``` con il comando:

```pip install -r requirements.txt```.

Se Python su Windows restituisce un errore provare con:
```py -m pip install -r requirements.txt```

In caso si verifichi il seguente errore "_python setup.py egg_info did not run successfully. exit code: 1_" mentre si scarica OSMnx su Windows esegui i seguenti comandi:

* ```pip install pipwin```
* ```pipwin install gdal```
* ```pipwin install fiona```
* ```pip install geopandas```

Se avviando per la prima volta _"knowladgeBase.py"_ restituisce il seguente errore: "_AttributeError: module 'collections' has no attribute 'Mapping'_", modificare la linea 16 del file *frozendict_init_.py* della libreria Experta contenuto nella cartella di Python *\Python\Python310\lib\site-packages\frozendict\__init__.py*, sostituendo:

```class frozendict(collections.Mapping):``` con

 ```class frozendict(collections.abc.Mapping):``` 

## Avvio del sistema
Si consiglia di avviare il sistema tramite VS Code.

Per avviare il sistema utilizzare il comando da console:
  
  ```python knowladgeBase.py```

Per maggiori informazioni consultare la documentazione nella cartella **doc/**
