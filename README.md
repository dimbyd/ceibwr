# ceibwr
Meddalwedd Gynganeddol

## Install
Pan fydd y pecyn ar PyPi ...
```
$ python3 -m pip install ceibwr
```

## TODO Ieithyddol

Y broblem fwyaf yw camacennu. Y rheol cyntaf yw bod geiriau unsill yn acennog, a geiriau lluosill yn ddiacen. Mae'r meddalwedd yn cynnwys nifer o "hacks" i ddarganfod geiriau
lluosill acennog (e.e. os oes `h` yn union cyn y sillaf olaf), ond does dim trefn ar rhain eto. Mae modd cofrestru "eithriadau", ond ar hyn y bryd dylai'r ffocws fod ar ddatblygu set o reolau trefnus.

### W ansillafog
Mae'r rhaglen yn camacennu rhai geiriau.
- Yn aml mae hyn oherwydd yr *w-ansillafog* felltith.
- Oes rheolau ar gael am rhain?
- Mae hefyd angen ystyried yr `wy` dalgron a'r `wy` leddf mewn ffordd drefnus.


## TODO Technegol
The following aspects need a lot of work.

### Docs
Sphinx documentation is included under `/docs` and needs a lot of work, mostly by the package author in the first instance.

### Tests
A `pytest` framework is included, but currently only tests the classification 
methods. 

### Logging
Logging is virtually non-existent, with only "Hello" and "Goodbye" implemented in the constructor for `Peiriant`.

