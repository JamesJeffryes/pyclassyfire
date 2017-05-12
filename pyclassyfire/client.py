"""A client for the ClassyFire API which enables efficient querying with 
chemical database files"""

import requests
import csv
import time
import os
import json

url = "http://classyfire.wishartlab.com"
chunk_size = 1000
sleep_interval = 60


def structure_query(compound, label='pyclassyfire'):
    """Submit a compound information to the ClassyFire service for evaluation 
    and receive a id which can be used to used to collect results
    
    :param compound: The compound structures as line delimited inchikey or smiles.
    Optionally a tab-separated id may be prepended for each structure.
    :type compound: str
    :param label: A label for 
    :type label:
    :return: A query ID number
    :rtype: int
    """
    r = requests.post(url + '/queries.json', data='{"label": "%s", '
                      '"query_input": "%s", "query_type": "STRUCTURE"}'
                                                  % (label, compound),
                      headers={"Content-Type": "application/json"})
    r.raise_for_status()
    return r.json()['id']


def get_results(query_id, return_format="json"):
    """Given a query_id, fetch the classification results.
    
    :param query_id: A numeric query id returned at time of query submission
    :type query_id: str
    :param return_format: desired return format. valid types are json, csv or sdf
    :type return_format: str
    :return: query information
    :rtype: str
    """
    r = requests.get('%s/queries/%s.%s' % (url, query_id, return_format),
                     headers={"Content-Type": "application/%s" % return_format})
    r.raise_for_status()
    return r.text


def get_entity(inchikey, return_format="json"):
    """Given a InChIKey for a previously queried structure, fetch the 
    classification results.

    :param inchikey: An InChIKey for a previously calculated chemical structure
    :type inchikey: str
    :param return_format: desired return format. valid types are json, csv or sdf
    :type return_format: str
    :return: query information
    :rtype: str
    """
    r = requests.get('%s/entities/%s.%s' % (url, inchikey, return_format),
                     headers={
                         "Content-Type": "application/%s" % return_format})
    r.raise_for_status()
    print(repr(r.text))
    return r.text


def tabular_query(inpath, structure_key, dialect='excel', outpath=None,
                  outfields=('taxonomy', 'description', 'substituents')):
    """Given a path to a compound set in tabular form (comma or tab delimited)
    annotate all compounds and write results to an expanded table.
    
    :param inpath: path to compound file to be annotated
    :type inpath: str
    :param structure_key: column heading which contains the compounds InChIKey 
    or SMILES
    :type structure_key: str
    :param dialect: dialect for parsing table (generally 'excel' for csv, 
    'excel-tab' for tsv)
    :type dialect: str
    :param outpath: Path to desired output location
    :type outpath: str
    :return: 
    :rtype: 
    """
    tax_fields = ('kingdom', 'superclass', 'class', 'subclass')
    query_ids = []
    infile = open(inpath)
    if not outpath:
        outpath = _prevent_overwrite(inpath)
    comps = []
    for line in csv.DictReader(infile, dialect=dialect):
        comps.append(line[structure_key])
        if not len(comps) % chunk_size:
            query_ids.append(structure_query('/n'.join(comps)))
            comps = []
    if comps:
        query_ids.append(structure_query('\\n'.join(comps)))
    print('%s queries submitted to ClassyFire API' % len(query_ids))
    i = 0
    infile.seek(0)
    with open(outpath, 'w') as outfile:
        reader = csv.DictReader(infile, dialect=dialect)
        writer = csv.DictWriter(outfile, reader.fieldnames+list(outfields),
                                dialect=dialect)
        writer.writeheader()
        while i < len(query_ids):
            result = json.loads(get_results(query_ids[i]))
            if result["classification_status"] == "Done":
                for hit, line in zip(result['entities'], reader):
                    if 'taxonomy' in outfields:
                        hit['taxonomy'] = ";".join(
                            ['%s:%s' % (hit[x]['name'], hit[x]['chemont_id'])
                             for x in tax_fields if hit[x]])
                    for field in outfields:
                        if isinstance(hit[field], list):
                            line[field] = ';'.join(hit[field])
                        else:
                            line[field] = hit[field]
                    writer.writerow(line)
                i += 1
            else:
                print("%s percent complete" % round(i/len(query_ids)*100))
                time.sleep(sleep_interval)
    infile.close()


def sdf_query(inpath, outpath=None):
    """Given a path to a compound set in a sdf file, annotate all compounds 
    and write results as attributes in a sdf file.
    
    :param inpath: path to compound file to be annotated
    :type inpath: str
    :param outpath: Path to desired output location
    :type outpath: str
    :return: 
    :rtype: 
    """
    raise NotImplementedError


def _prevent_overwrite(write_path, suffix='_annotated'):
    """Prevents overwrite of existing output files by appending a suffix when needed

    :param write_path: potential write path
    :type write_path: string
    :return:
    :rtype:
    """
    while os.path.exists(write_path):
        sp = write_path.split('.')
        if len(sp) > 1:
            sp[-2] += suffix
            write_path = '.'.join(sp)
        else:
            write_path += suffix
    return write_path
