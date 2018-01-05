# SongAdapter

SongAdapter is a Python CLI application generated from https://github.com/xuanluong/cookiecutter-python-cli.
The purpose of this client tool is to generate a Song payload from command line instructions.

## Basic setup

Install the requirements:
```
$ pip install -r requirements.txt
```

Run the application:
```
$ python -m songadapter --help
```

To run the tests:
```
    $ pytest
```


## Examples

### Initialize a payload
```bash
python SongAdapter.py init payload.json
```

### Set analysis id
```bash
python SongAdapter.py add:analysis_id --input payload.json --id <ANALYSIS_ID>
```

### Set analysis type
```bash
python SongAdapter.py add:analysis_type --input payload.json --type <ANALYSIS_TYPE>
```

### Set experiment
```bash
python SongAdapter.py add:experiment --input payload.json --aligned --library-strategy <LIBRARY_STRATEGY> --reference-genome <REFERENCE_GENOME>
```

### Add file
```bash
python SongAdapter.py add:file --input payload.json --access --md5sum <MD5> --name <FILE_NAME> --size <SIZE> --type <FILE_TYPE>
```

### Add info
```bash
python SongAdapter.py add:info --input payload.json --key <INFO_KEY> --value <INFO_VALUE>
```

### Add sample
```bash
python SongAdapter.py add:sample --input payload.json --donor-gender <GENDER> --donor-submitter-id <SUBMITTER_ID> --sample-submitter-id <S_SUBMITTER_ID> --sample-type <TYPE> --specimen-class <CLASS> --specimen-submitter-id <SUBMITTER_ID> --specimen-type <SPECIMEN_TYPE>
```

### Validate
```bash
python SongAdapter.py validate --input payload.json
```