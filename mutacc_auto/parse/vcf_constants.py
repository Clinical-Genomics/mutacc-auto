#Scout fields name: vcf ID
FORMAT_IDS = (
    'GT',
    'AD',
    'DP',
    'GQ'
)
INFO_IDS = (
    'END',
    'RankScore',
    'ANN'
)
COLUMN_NAMES = [
    'CHROM',
    'POS',
    'ID',
    'REF',
    'ALT',
    'QUAL',
    'FILTER',
    'INFO',
    'FORMAT'
]
GENE_INFO = ('hgnc_symbol',
             'region_annotation',
             'functional_annotation',
             'sift_prediction',
             'polyphen_prediction')
HEADER = (
    '##fileformat=VCFv4.2',
    '##INFO=<ID=END,Number=1,Type=Integer,Description="Stop position of the interval">',
    '##INFO=<ID=SVTYPE,Number=1,Type=String,Description="Type of structural variant">',
    '##INFO=<ID=TYPE,Number=A,Type=String,Description="The type of allele, either snp, mnp, ins, del, or complex.">',
    '##INFO=<ID=RankScore,Number=.,Type=String,Description="The rank score for this variant in this family. family_id:rank_score.">',
    f'##INFO=<ID=ANN,Number=.,Type=String,Description="Annotation: {"|".join(GENE_INFO)}">',
    '##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">',
    '##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Approximate read depth (reads with MQ=255 or with bad mates are filtered)">',
    '##FORMAT=<ID=GQ,Number=1,Type=Integer,Description="Genotype Quality">',
    '##FORMAT=<ID=AD,Number=R,Type=Integer,Description="Allelic depths for the ref and alt alleles in the order listed">'
)
NEWLINE = '\n'
TAB = '\t'
HEADER_PREFIX = '#'
