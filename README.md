# redTor
Proyecto TFM sobre desanonimización de dominios onion. Para poder trabajar con él, es necesario volcar el dump de la base de datos que se encuentra en este repositorio. Hecho esto, en el mismo directorio donde se se vayan a ejecutar los scripts, deberá tener también el fichero txt con la lista de dominios onions que van a ser analizados.

Una vez estos dos requisitos se hayan cumplido, habrá que ejecutar con python3 el fichero onionscanalert.py para que de esta forma, se vayan generando los ficheros json asociados a cada uno de los dominios onion que se vayan a analizar. A partir de ahí, se podrán ejecutar los siguientes scripts:

1.- shodanscan.py (será necesario introducir el API de shodan)
2.- apachescan.py
3.- bitcoinscan.py
4.- smtpscan.py
5.- vncscan.py
6.- tlsDetected.py
7.- ircscan.py

8.- visualization.py nos va a ayudar a visualizar las relaciones entre dominions onion que puedan existir.

Es importante tener en cuenta que se debe tener instalado también para poder ejecutar el script principal el siguiente repositorio: https://github.com/s-rah/onionscan
