# ceibwr
Meddalwedd Gynganeddol

### Install from PyPI

```bash
pip install ceibwr
```

### Install from Source (GitHub)

```bash
git clone https://github.com/dimbyd/ceibwr.git
cd ceibwr
pip install .
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
methods. 

### Logging
Logging is virtually non-existent, with only token "Hello" and "Goodbye" implemented in the `Peiriant` constructor.

