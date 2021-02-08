# hirni-tools

## compare_specs

A small tool to compare two datalad-hirni studyspec files.

### Usage

#### library

```python
>>> from compare_specs import compare_specs
>>> compare_specs("/path/to/dataset1/studyspec.json",
                  "/path/to/dataset2/studyspec.json")
```

#### command line

```
$ python compare_specs.py /path/to/dataset1/studyspec.json /path/to/dataset2/studyspec.json
```