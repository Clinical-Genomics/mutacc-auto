
import json

from mutacc_auto.parse.vcf_constants import (SCOUT_TO_FORMAT,
                                             SCOUT_TO_INFO,
                                             HEADER,
                                             NEWLINE,
                                             TAB,
                                             COLUMN_NAMES,
                                             SCOUT_TO_COLUMNS,
                                             SCOUT_GENE,
                                             GENE_INFO,
                                             ANNOTATION)



def get_vcf_from_json(scout_vcf_output):

    """
        Reconstructs vcf from scout variant object

        Args:
            scout_vcf_output (str): string returned by command 'scout export variants --json'

        Returns:
            vcf_string (str): string with vcf content
    """

    scout_vcf_output = json.loads(scout_vcf_output)

    vcf_string = ""

    #Write header of vcf
    for header_line in HEADER:
        vcf_string += header_line + NEWLINE

    #Get samples
    samples = [sample['sample_id'] for sample in scout_vcf_output[0]['samples']]

    #Append sample names to the COLUMN_NAMES list
    column_names = COLUMN_NAMES + samples
    column_names = TAB.join(column_names)

    vcf_string += column_names + NEWLINE

    #Write variants
    for variant in scout_vcf_output:

        #Write column values
        record = get_columns(variant)

        #write INFO
        info = get_info(variant)
        record.append(info)

        #Write the format a
        vcf_format = ':'.join([SCOUT_TO_FORMAT[ID] for ID in SCOUT_TO_FORMAT.keys()])
        record.append(vcf_format)

        #write genotypes for each sample
        samples = get_genotypes(variant)
        record.append(samples)

        record = TAB.join(record) + NEWLINE

        #Add variant record to vcf_string
        vcf_string += record

    return vcf_string

def get_columns(variant):
    """
        Given a variant object from scout, write the columns CHR - FILTER
        as a string with values separated by tab

        Args:
            variant (dict): dictionary of scout variant object
        Returns:
            record (str): values CHR-FILTER as a string
    """
    record = []

    for column in SCOUT_TO_COLUMNS:

        if type(variant[column]) == list:
            column_value = ','.join([str(element) for element in variant[column]])

        else:
            column_value = str(variant[column])

        record.append(column_value)

    return record

def get_info(variant):
    """
        Given a variant object from scout, write the INFO column
        for a variant.

        Args:
            variant (dict): dictionary of scout variant object
        Returns:
            info (str): INFO string
    """
    info = []
    for ID in SCOUT_TO_INFO.keys():

        info_string = f"{SCOUT_TO_INFO[ID]}={int(variant[ID])}"
        info.append(info_string)

    if variant['category'].lower() == 'snv':
        info_string = f"TYPE={variant['sub_category']}"

    else:
        info_string = f"SVTYPE={variant['sub_category']}"

    info.append(info_string)

    #Get annotations
    genes = variant[SCOUT_GENE]
    ann_info = []

    for gene in genes:
        gene_info = '|'.join([gene[ann_id] if gene.get(ann_id) else '' for ann_id in GENE_INFO])
        ann_info.append(gene_info)
    ann_info = f"{ANNOTATION}=" + ','.join(ann_info)

    info.append(ann_info)

    # Join info string

    info = ';'.join(info)

    return info

def get_genotypes(variant):
    """
        Given a variant object from scout, write the genotypes column for each
        sample.

        Args:
            variant (dict): dictionary of scout variant object
        Returns:
            samples (str): genotypes for each sample
    """
    samples = []
    for sample in variant['samples']:

        gt_calls = []
        for ID in SCOUT_TO_FORMAT.keys():

            if type(sample[ID]) == list:

                ID_value = ','.join([str(element) for element in sample[ID]])

            else:
                ID_value = str(sample[ID])

            gt_calls.append(ID_value)

        gt_calls = ':'.join(gt_calls)
        samples.append(gt_calls)

    samples = TAB.join(samples)

    return samples
