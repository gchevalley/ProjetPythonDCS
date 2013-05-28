#Mise en fonction du système

La version de Python utilisée est la 2.7

##Installation des dépendances

* Sous Windows (testé sous 7)
1. Installation de [Python 2.7.5](http://www.python.org/ftp/python/2.7.5/python-2.7.5.msi)
2. [Ajouter le dossier dans lequel est installé python.exe au PATH](http://stackoverflow.com/questions/6318156/adding-python-path-on-windows-7)
3. Installation de [setuptools](https://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11.win32-py2.7.exe#md5=57e1e64f6b7c7f1d2eddfc9746bbaf20) pour Python 2.7 pour faciliter l’installation des librairies annexes
4. Récupérer et installer le package [Python Imaging Library (PIL) 1.1.7 pour Python 2.7](http://effbot.org/downloads/PIL-1.1.7.win32-py2.7.exe)
5. Recupérer le projet [Request](http://docs.python-requests.org/en/latest/user/install.html#install) dans son dépôt [Github](https://github.com/kennethreitz/requests), l’installer depuis un invite de commande avec `python setup.py install`
6. Récupérer la librairie [BeautifulSoup4](http://www.crummy.com/software/BeautifulSoup/bs4/download/4.2/beautifulsoup4-4.2.0.tar.gz), la décompresser et l’installer depuis un invite de commande avec python setup.py install
7. Récupérer et installer le package [pygooglechart](http://pygooglechart.slowchop.com/files/download/pygooglechart-0.2.1.win32.exe)

* Sous Mac OS X (testé avec Mountain Lion 10.8.3)
1. Installer Xcode à partir de l’Apple Store
2. Lancer Xcode, ouvrir le menu Xcode -> Preferences... -> Download et cliquer sur le bouton Install à la hauteur de Command line tools
3. Récupérer le fichier [setuptools-py2.7.egg](https://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11-py2.7.egg#md5=fe1f997bc722265116870bc7919059ea) et le lancer depuis un terminal avec la commande : `sh setuptools-py2.7.egg`
4. Récupérer le fichier [pip-1.3.1.tar.gz](https://pypi.python.org/packages/source/p/pip/pip-1.3.1.tar.gz), le décompresser et l’installer depuis un terminal avec la commande `python setup.py install`
5. Récupérer le code source [Python Imaging Library (PIL) 1.1.7](http://effbot.org/downloads/Imaging-1.1.7.tar.gz), le décompresser et l’installer depuis un terminal avec la commande `python setup.py install`
6. La librairie requests peut être installée depuis un terminal avec la commande `pip install requests`
7. Idem pour beautifulsoup4 : `pip install beautifulsoup4`
8. Et pour pygooglechart on passe par la commande : `easy_install pygooglechart`

* Sous Linux (testé avec la distribution Ubuntu 13.04)
A l’aide d’un terminal avec les droits root, il faut lancer les 4 commandes suivantes :
1. `apt-get install python-tk python-imaging-tk python-pip`
2. `pip install requests`
3. `pip install beautifulsoup4`
4. `easy_install pygooglechart`

##Lancement du système
Depuis n’importe quelle plateforme, le lancement du programme s’effectue grâce au module `Gui.py`
