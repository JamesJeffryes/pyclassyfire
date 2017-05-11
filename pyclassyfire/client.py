"""A client for the ClassyFire API which enables efficient querying with 
chemical database files"""

import requests

url = "http://classyfire.wishartlab.com"


def structure_query(label, input):
    """Submit a compound information to the ClassyFire service for evaluation 
    and receive a id which can be used to used to collect results
    
    :param label: 
    :type label: str
    :param input: The compound structures as a tab-separated list of id and 
    inchikey or smiles
    :type input: str
    :return: query_id
    :rtype: str
    """
    raise NotImplementedError


def get_results(query_id, format="json"):
    """Given a query_id, fetch the classification results.
    
    :param query_id: A numeric query id returned at time of query submission
    :type query_id: str
    :param format: desired return format. valid types are json, csv or sdf
    :type format: str
    :return: query information
    :rtype: str
    """
    raise NotImplementedError


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