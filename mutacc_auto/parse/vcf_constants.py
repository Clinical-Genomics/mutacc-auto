#Scout fields name: vcf ID
SCOUT_TO_FORMAT = {

    'genotype_call': 'GT',
    'allele_depths': 'AD',
    'read_depth': 'DP',
    'genotype_quality': 'GQ'

}

SCOUT_TO_INFO = {

    'end': 'END',
    'rank_score': 'RankScore'
}

HEADER = (

    '##fileformat=VCFv4.2',

    '##INFO=<ID=END,Number=1,Type=Integer,Description="Stop position of the interval">',
    '##INFO=<ID=SVTYPE,Number=1,Type=String,Description="Type of structural variant">',
    '##INFO=<ID=TYPE,Number=A,Type=String,Description="The type of allele, either snp, mnp, ins, del, or complex.">',
    '##INFO=<ID=RankScore,Number=.,Type=String,Description="The rank score for this variant in this family. family_id:rank_score.">',


    '##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">',
    '##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Approximate read depth (reads with MQ=255 or with bad mates are filtered)">',
    '##FORMAT=<ID=GQ,Number=1,Type=Integer,Description="Genotype Quality">',
    '##FORMAT=<ID=AD,Number=R,Type=Integer,Description="Allelic depths for the ref and alt alleles in the order listed">'

)
