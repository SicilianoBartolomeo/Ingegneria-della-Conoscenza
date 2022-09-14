# Ingegneria-della-Conoscenza
Progetto di Ingeneria della Conoscenza - Università degli Studi di Bari

## Realizzato da:
* Siciliano Bartolomeo, 724558 - mail: b.siciliano1@studenti.uniba.it

## Come installare i requisiti:
E' possibile installare le librerie necessarie dal file ```requirements.txt``` con il comando:

```pip install -r requirements.txt```.

Se python su Windows restituisce un errore provare con:
```py -m pip install -r requirements.txt```

In caso si verifichi il seguente errore "_python setup.py egg_info did not run successfully. exit code: 1_" mentre si scarica OSMnx su Windows inserire i seguenti comandi:

* ```pip install pipwin```
* ```pipwin install gdal```
* ```pipwin install fiona```
* ```pip install geopandas```

## Avvio del sistema
Per avviare il sistema utilizzare il comando:
  
  ```python knowladgeBase.py```

Per maggiori informazioni consultare la documentazione nella cartella **doc/**
