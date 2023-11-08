import json
import numpy


def load_chemicals_genes():
    chemicals = []
    genes = []
    with open("entity/CPR.json") as json_file:
        entity_data = json.load(json_file)

    for item in entity_data:
        if item["type"] == "CHEMICAL":
            chemicals.append(item["name"])

        if item["type"] == "GENE":
            genes.append(item["name"])

    chemicals = numpy.unique(chemicals)
    genes = numpy.unique(genes)

    return (chemicals, genes)