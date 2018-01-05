#!/usr/bin/env python

import click
import os
import argparse
import json
import jsonschema
from icgconnect.icgc import song
from icgconnect.utils.file_utils import get_file_md5
from icgconnect.utils.file_utils import get_file_size

@click.group()
def songadapter():
    pass

@songadapter.command()
@click.option('--filename','-f', required=True, help='Filename to initialize the payload')
@click.option('--force', default=False, is_flag=True, help="Overwrite the file if already exists")
def init(filename,force):
    """Initialize a song payload with empty values"""
    if os.path.isfile(filename):
        if force:
            os.remove(filename)
        else:
            click.echo('Error: File '+filename+' already exists')
            exit(1)

    with open(filename, 'w') as f:
        _json = {'analysisId': None,'analysisType': None,
            'experiment': {'aligned': True,'libraryStrategy':  None,'referenceGenome': None},
            'file': [],
            'info':{},
            'sample': []
        }
        f.writelines(json.dumps(_json, indent=4, sort_keys=True))
    #try:
    #    validate(_json,song.get_schema())
    #except Exception, err:
    #    print str(err)


@songadapter.command('add:analysis_id')
@click.option('--input','-i', type=click.Path(exists=True),help="An existing song payload")
@click.option('--id','-id', required=True, help="Analysis ID")
def add_analysis_id(input, id):
    """Add analysisId to the payload"""
    json_load = json.load(open(input))
    json_load['analysisId'] = id
    save_json(json_load, input)

@songadapter.command('add:analysis_type')
@click.option('--input','-i', type=click.Path(exists=True),help="An existing song payload")
@click.option('--type','-t', required=True, help="Analysis Type")
def add_analysis_type(input, type):
    """Add analysisType to the payload"""
    json_load = json.load(open(input))
    json_load['analysisType'] = type
    save_json(json_load, input)

@songadapter.command('add:experiment')
@click.option('--input','-i', type=click.Path(exists=True),help="An existing song payload")
@click.option('--aligned/--unaligned',required=True, help="Aligned or unaligned experiment")
@click.option('--library-strategy','-l', required=True, help="Library strategy")
@click.option('--reference-genome','-r', required=True, help="Reference genome")
def add_experiment(input, aligned, library_strategy, reference_genome):
    """Add experiment to the payload"""
    json_load = json.load(open(input))

    if aligned: json_load['experiment']['aligned'] = True
    else: json_load['experiment']['aligned'] = False

    json_load['experiment']['libraryStrategy'] = library_strategy
    json_load['experiment']['referenceGenome'] = reference_genome

    save_json(json_load, input)

@songadapter.command('add:file')
@click.option('--input','-i', type=click.Path(exists=True),help="An existing song payload")
@click.option('--access/--controlled', required=True, help="Access or Controlled")
@click.option('--md5sum','-m', help="MD5 Checksum of the file")
@click.option('--name','-n', type=click.Path(exists=True),required=True, help="Name of the file")
@click.option('--size','-s', help="Size of the file")
@click.option('--type','-t', required=True, help="Type of the file")
def add_file(input, access, md5sum, name,size, type):
    """Add file to the payload"""
    if access: _access = 'open'
    else: _access = 'controlled'

    if not md5sum == None:
        _md5_sum = md5sum
    else:
        _md5_sum = get_file_md5(name)

    if not name == None:
        _name = os.path.basename(name)
    else:
        _name = name

    if not size == None:
        _size = size
    else:
        _size = get_file_size(name)

    json_load = json.load(open(input))
    _file = {'fileAccess':_access,'fileMd5sum':_md5_sum,'fileName':_name,'fileSize':int(_size),'fileType':type}
    json_load['file'].append(_file)
    save_json(json_load, input)

@songadapter.command('add:info')
@click.option('--input','-i', type=click.Path(exists=True),help="An existing song payload")
@click.option('--key','-k', required=True, help="Json key to add")
@click.option('--value','-v',required=True, help="Value of the json key")
def add_info(input, key, value):
    """Add info to the payload"""
    json_load = json.load(open(input))
    json_load['info'][key] = value
    save_json(json_load, input)


@songadapter.command('add:sample')
@click.option('--input','-i', type=click.Path(exists=True),help="An existing song payload")
@click.option('--donor-gender',required=True, help="Gender of the donor")
@click.option('--donor-submitter-id',required=True, help="Submitter ID of the donor")
@click.option('--sample-submitter-id',required=True, help="Submitter sample ID")
@click.option('--sample-type',required=True, help="Sample type")
@click.option('--specimen-class',required=True, help="Specimen class (Normal, Tumour or Adjacent normal)")
@click.option('--specimen-submitter-id',required=True, help='Specimen submitter ID')
@click.option('--specimen-type',required=True, help='Specimen type')
def add_sample(input, donor_gender, donor_submitter_id, sample_submitter_id,sample_type,specimen_class,specimen_submitter_id,specimen_type):
    """Add sample to the payload"""
    json_load = json.load(open(input))
    _donor = {'donorGender':donor_gender,'donorSubmitterId':donor_submitter_id}
    _specimen = {'specimenClass':specimen_class,'specimenSubmitterId':specimen_submitter_id,'specimenType':specimen_type}
    json_load['sample'].append({
        'donor':_donor,
        'sampleSubmitterId': sample_submitter_id,
        'sampleType': sample_type,
        'specimen': _specimen
    })

    save_json(json_load, input)

@songadapter.command('validate')
@click.option('--input','-i', type=click.Path(exists=True),help="An existing song payload")
def validate(input):
    """Validate the json payload"""
    json_load = json.load(open(input))
    try:
        jsonschema.validate(json_load,song.get_schema())
    except Exception, err:
        print str(err)
        exit(1)

def save_json(json_string, output_file):
    with open(output_file, 'w') as f:
        f.writelines(json.dumps(json_string, indent=4, sort_keys=True))

if __name__ == '__main__':
    songadapter()

