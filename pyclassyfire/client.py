"""A client for the ClassyFire API which enables efficient querying with 
chemical database files"""

import requests
import csv

url = "http://classyfire.wishartlab.com"


def structure_query(compound, label='pyclassyfire'):
    """Submit a compound information to the ClassyFire service for evaluation 
    and receive a id which can be used to used to collect results
    
    :param compound: The compound structures as line delimited inchikey or smiles.
    Optionally a tab-separated id may be prepended for each structure.
    
    :type compound: str
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
    print(repr(r.text))
    return r.text


def tabular_query(inpath, structure_key, dialect='excel', outpath=None):
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
    raise NotImplementedError


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