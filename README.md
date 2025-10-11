# ceibwr
Meddalwedd Gynganeddol


### Install from Source (GitHub)

```bash
git clone https://github.com/dimbyd/ceibwr.git
cd ceibwr
pip install .
```

### Install from PyPI (not available)

```bash
pip install ceibwr
```

## Usage

### Datryswr
```bash
$ python3 main.py -d "Wele rith fel ymyl rhod" # demo llinellau
$ python3 main.py -df ./data/cerddi/cerdd.txt
```

### Celfi
```bash
$ python3 main.py -o <query>            # odliadur
$ python3 main.py -o <query>  --llusg   # odlau llusg
$ python3 main.py -c <query>            # cleciadur
$ python3 main.py -p <filename>         # pysgotwr
```

### Demos
```bash
$ python3 main.py -de  # demo llinellau
$ python3 main.py -dc  # demo cwpledi
$ python3 main.py -dp  # demo penillion
```

## TODO Ieithyddol

Y broblem fwyaf yw camacennu. Y rheol cyntaf yw bod geiriau unsill yn acennog, a geiriau lluosill yn ddiacen. Mae'r meddalwedd yn cynnwys nifer o "hacks" i ddarganfod geiriau lluosill acennog (e.e. os oes `h` yn union cyn y sillaf olaf), ond does dim trefn ar rhain eto. Mae modd cofrestru "eithriadau", ond ar hyn y bryd mae angen datblygu set o reolau trefnus.

Mae camacennu yn aml oherwydd yr **w-ansillafog** felltith, a hefyd yr `wy` dalgron a lleddf. Oes rheolau ar gyfer rhain?


## TODO Technegol
The following need a lot of work.

### Docs
Sphinx documentation is included under `/docs` and needs a lot of attention.

### Tests
A `pytest` framework is included, but currently only tests the classifier.
pyp
### Logging
Logging is virtually non-existent, with only token "Hello" and "Goodbye" implemented in the `Peiriant` constructor.

