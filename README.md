# HW a SW nároky

## Hardware nároky

- 1 MB volného úložistě
- 1 GB RAM
- základní vstupní/výstupní zařízení
    - klávensice, myš, monitor
---
- *+ hardware nároky pro [software](#software-nároky)*

## Software nároky

- Python 3.10+
- python `tkinter` modul
---
- software pro iniciální rozbalení `.zip` archivu


# Popis instalačního balíku

Jde o prostý `.zip` archiv, který obsahuje vše, co **mSweeper** potřebuje.<br>
Dále je potřeba už jen `python` interpreter zmíněný výše.

Nejde o instalaci, ale o stand-alone, který je závislý pouze na `pythonu`.<br>
Tudíž je adresář s **mSweeper**-em přenostitelný.


# Popis instalace/konfigurace

- rozbalení `.zip` archivu v daném adresáři


# Spuštění aplikace

Z příkazové řádky *(`cmd`, `PowerShell`, `bash`, atd.)* v daném adresáři příkazem:

- pro klasické spuštění
    ```
    python3 main.py
    ```

- pro spuštění jako super-uživatel
    ```
    python3 main.py custom
    ```

    oproti klasickému spuštění poskytuje správu nejlepších skóre
    a úpravu počtu min na hracím poli pro dané spuštění
