# ProCM

- [[#Sestavení a spuštění aplikace|Sestavení a spuštění aplikace]]
	- [[#Sestavení aplikace#Požadavky|Požadavky]]
		- [[#Požadavky#Požadované moduly|Požadované moduly]]
		- [[#Požadavky#Docker|Docker]]
	- [[#Sestavení aplikace#Spuštění aplikace a její nastavení|Spuštění aplikace a její nastavení]]
		- [[#Spuštění aplikace a její nastavení#Příprava|Příprava]]
		- [[#Spuštění aplikace a její nastavení#Nastavení|Nastavení]]
		- [[#Spuštění aplikace a její nastavení#Development server|Development server]]
		- [[#Spuštění aplikace a její nastavení#Production server|Production server]]
- [[#Dokumentace projektu|Dokumentace projektu]]
	- [[#Dokumentace projektu#Souborový systém|Souborový systém]]
	- [[#Dokumentace projektu#Moduly|Moduly]]
	- [[#Dokumentace projektu#Modely|Modely]]
		- [[#Modely#User|User]]
		- [[#Modely#Group|Group]]
		- [[#Modely#Post|Post]]
		- [[#Modely#Project|Project]]
		- [[#Modely#Comment|Comment]]

ProCM je blog a galerie projektů napsaná v Flask frameworku.  
Flask je light-weight framework pro web aplikace v pythonu.

## Sestavení a spuštění aplikace

### Požadavky

Pro sestavení, resp. spuštění aplikace jsou zapotřebí následující závislosti.

- Python >=3.10
- pip
- [Požadované moduly](#Požadované moduly)

#### Požadované moduly

Závislosti v requirements.txt jsou zapotřebí pro spuštění web serveru, protože jsou to moduly, které jsou importované v pod modulech aplikace.  
Lze je nainstalovat po splnění požadavků Python a pip pomocí příkazu `pip install -r ./requirements.txt`, popř. `python -m pip install -r ./requirements.txt`.  
Pokud obdržíte chybovou hlášku ve formě `Python is not a recognised or executable program`, ujistěte se že jste python i pip nainstalovaly, a přidaly jej do systémové proměné `PATH`.

- [Jak upravit PATH proměnou ve Windows 10](https://windowsloop.com/how-to-add-to-windows-path/)
- Pokud jste na Linuxu, měli by jste znát jak upravit PATH proměnou

Pokud i po úpravě PATH proměné budete dostávat chybu, zkuste se odhlásit a přihlásit, dále restartovat zařízení pokud se problém nevyřešil.

#### Docker

Alternativně je dostupný `dockerfile` pro sestavení obrazu pro [Docker](https://www.docker.com/).  
Proměné prostředí najdete pod nadpisem [[#Nastavení|Nastavení]].

##### Docker Compose

```yaml

```

### Spuštění aplikace a její nastavení

#### Příprava

Pro spuštění a správnou funkčnost aplikace je zapotřebí databáze [MongoDB](https://www.mongodb.com/) za účelem ukládání postů, komentářů a účtů uživatelů.

#### Nastavení

Všechny nastavení lze provést v `.env` souboru, který je popsán v tabulce níže.

| Vlastnost               | Výchozí hodnota | Popis                                                                                   |
| ----------------------- | --------------- | --------------------------------------------------------------------------------------- |
| PASSWORD_SECRET         | CHANGE_ME       | Tato hodnota je použita pro hash salting                                                |
| FLASK_SECRET            | CHANGE_ME       | Tato hodnota je použita pro šifrování session cookie                                    |
| FLASK_SESSION_LIFETIME  | 1400            | Tato hodnota určuje jak dlouho může být session cookie uložena                          |
| MONGO_HOST              | localhost       | Tato hodnota určuje hosta s MongoDB databází                                            |
| MONGO_PORT              | 27017           | Tato hodnota určuje port na hostovy MongoDB databáze                                    |
| MONGO_USER              | root            | Tato hodnota určuje přihlašovací jméno pro databázy                                     |
| MONGO_PASS              | root            | Tato hodnota určuje přihlašovací heslo pro databázy                                     |
| MONGO_SRV               | false           | Tato hodnota je použita za účelem správného sestavení MongoDB URI pro SRV Mongo servery |
| PCM_DATABASE            | ProCM           | Jméno databáze, kde se budou ukládat data                                               |
| PCM_COLLECTION_USERS    | Users           | Jméno kolekce, kde jsou ukládany dokumenty reprezentující uživatele                     |
| PCM_COLLECTION_GROUPS   | Groups          | Jméno kolekce, kde jsou ukládany dokumenty reprezentující skupiny oprávnění             |
| PCM_COLLECTION_PROJECTS | Projects        | Jméno kolekce, kde jsou ukládany dokumenty reprezentující projekty                      |
| PCM_COLLECTION_POSTS    | Posts           | Jméno kolekce, kde jsou ukládany dokumenty reprezentující blog posty                    |
| PCM_COLLECTION_COMMENTS | Comments        | Jméno kolekce, kde jsou ukládany dokumenty reprezentující komentáře                     |
| REGISTRATION            | true            | Tato hodnota určuje, zda je povolena registrace nebo ne                                 |
| BRAND                   | ProCM           | Tato hodnota určuje jméno stránky - brand                                               |

Je důležité dát pozor, aby `.env` soubor nikdy neskončil na VCS nebo veřejně přístupném místě.

#### Development server

Tento server je určen pro vývoj nebo troubleshooting. Je nebezpečné ho používat v production nebo veřejně dostupném prostředí, protože povoluje přístup k nefiltrovanému interpretru pythonu.

Spustí se následujícími kroky:
1) Vstupte do složky app
2) Spusťte příkaz `python main.py`, popř. `python3 main.py`

#### Production server

Tento server je určen pro production environment. Ve většine případech budete chtít používat tento server.

1) Vstupte do složky app
2) Spusťte příkaz `gunicorn main:app -b 0.0.0.0`

## Dokumentace projektu

### Souborový systém

V této kategorii bude popsáno jak jsou rozděleny soubory do složek a podsložek.

| Cesta                    | Obsahuje                                               |
| ------------------------ | ------------------------------------------------------ |
| app/                     | Hlavní adresář - Zde začíná aplikace                   |
| app/common/              | Adresář modulu common (viz. níže)                      |
| app/models/              | Adresář modulu models (viz. níže)                      |
| app/routes/              | Adresář obsahující definice routů                      |
| app/routes/api/          | Routy pro API                                          |
| app/routes/www/          | Routy pro Frontend stránky                             |
| app/static/              | Adresář pro statický obsah                             |
| app/static/css/          | CSS Soubory a adresář pro JIT zkompilovaný SASS        |
| app/static/img/          | Obrázky                                                |
| app/static/js/           | Javascript soubory                                     |
| app/static/sass/         | SASS a Bootstrap                                       |
| app/templates/           | Adresář pro templaty (šablony) a HTML soubory          |
| app/templates/admin      | Šablony pro Admin panel                                |
| app/templates/components | Sdílené komponenty                                     |
| app/templates/home       | Šablony pro domovskou stránku a přihlašovací obrazovku |

### Moduly

V této kategori jsou zadokumentovány moduly a třídy.

| Jméno modulu | Adresář      | Popis                                                                           |
| ------------ | ------------ | ------------------------------------------------------------------------------- |
| common       | /app/common/ | Tento modul obsahuje proměné a třídy, často importované v mnoha souborech       |
| models       | /app/models/ | Tento modul obsahuje modely (reprezentace objektů v databázy) a client databáze |
| routes       | /app/routes/ | Tento modul obsahuje definice všech routů                                       |

> `routes` modul obsahuje podmoduly, které existují pro orgranizační účely.

### Modely

#### User

...

#### Group

...

#### Post

...

#### Project

...

#### Comment

...

### API
