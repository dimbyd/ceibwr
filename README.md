# ceibwr

### Meddalwedd Gynganeddol

#### Install from source 

```bash
git clone https://github.com/dimbyd/ceibwr.git
cd ceibwr
pip install .
```

#### Install from PyPI (not available)

```bash
pip install ceibwr
```

## Usage

### Cymorth
```bash
$ ceibwr -h
```

### Datryswr
```bash
$ ceibwr -d "Wele rith fel ymyl rhod"
$ ceibwr -df ./data/cerddi/cerdd.txt
```

### Celfi
```bash
$ ceibwr -o <query>            # odliadur
$ ceibwr -o <query>  --llusg   # odlau llusg
$ ceibwr -c <query>            # cleciadur
$ ceibwr -p <filename>         # pysgotwr
```

### Demos
```bash
$ ceibwr -de  # demo llinellau
$ ceibwr -dc  # demo cwpledi
$ ceibwr -dp  # demo penillion
```

## TODO Ieithyddol

Y broblem fwyaf yw camacennu. Y rheol cyntaf yw bod geiriau unsill yn acennog, a geiriau lluosill yn ddiacen. Mae'r meddalwedd yn cynnwys nifer o "hacks" i ddarganfod geiriau lluosill acennog (e.e. os oes 'h' yn union cyn y sillaf olaf), ond does dim trefn ar rhain eto. Mae modd cofrestru "eithriadau", ond ar hyn y bryd mae angen am set o reolau trefnus.

Mae camacennu yn aml oherwydd yr **w-ansillafog** felltith, a hefyd yr `wy` esgynedig a disgynedig. Oes rheolau ar gyfer rhain?


## TODO Technegol
Mae angen llawer o waith ar y cydrannau canlynol.

### Docs
Sphinx documentation is included under `/docs` and needs a lot of work.

### Tests
A `pytest` framework is included, but currently only tests the classifier.

### Logging
Logging is virtually non-existent, with only token "Hello" and "Goodbye" implemented in the `Peiriant` constructor.

