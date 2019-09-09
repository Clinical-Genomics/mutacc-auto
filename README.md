# mutacc-auto
[![Build Status](https://travis-ci.org/Clinical-Genomics/mutacc-auto.png)](https://travis-ci.org/Clinical-Genomics/mutacc-auto)
[![Coverage Status](https://coveralls.io/repos/github/Clinical-Genomics/mutacc-auto/badge.svg?branch=master)](https://coveralls.io/github/Clinical-Genomics/mutacc-auto?branch=master)

mutacc-auto work as a wrapper for [MutAcc](https://github.com/Clinical-Genomics/mutacc), to automate
the process of uploading new cases to the MutAcc database, export, and upgrade validation sets. mutacc-auto
takes use of other CLI apps in the Clinical-Genomics suite, [hosekeeper](https://github.com/Clinical-Genomics/housekeeper),
and [scout](https://github.com/Clinical-Genomics/scout), to assemble all relevant files, and meta-data about a case as
input to MutAcc. ```mutacc-auto``` is designed to be run from [cg](https://github.com/Clinical-Genomics/cg).  

## Dependencies


## Install

mutacc-auto can be installed using pip,

```console
git clone https://github.com/Clinical-Genomics/mutacc-auto.git
cd mutacc-auto
pip install -e .
```
## Usage

### Extract

To use mutacc extract feature on a given case the 'extract' subcommand is used

To extract the clinically relevant reads from a case use

```console
mutacc-auto --config-file <config_file> extract \
--case <case_json> \
--variants <variants_json> \
```

To search for recently finished cases in scout, and extract reads from the cases
finished since the past few days, the --days-ago option can be used

This would find all cases finished the past week and extract the reads from those

full list of options

```console
Usage: mutacc-auto extract [OPTIONS]

Options:
  -c, --case TEXT         JSON formated string containing case data (passed to
                          mutacc-auto via cg)
  -v, --variants TEXT     JSON formated string containing variant data (passed
                          to mutacc-auto via cg)
  -e, --environment TEXT  conda environment used for mutacc
  -p, --padding INTEGER   padding for genomic regions. this defaults to 0 for
                          WES cases
  -D, --dry               dry run
  -V, --verbose           verbose
  -k, --conda             Use 'conda activate' to source environment
  --help                  Show this message and exit.

```

The configuration file, passed with option --config-file allows the user to predefine
some important parameters. Here the user can specify the path to the binaries for
mutacc, scout, and housekeeper, as well as passing the configuration files for the
respective tools.

The user should also add slurm specific parameters to the configuration file. This is
added to a yaml formated file, as the example below:

```yaml
#Configuration and binary paths placed here
mutacc_config: /path/to/mutacc/config
mutacc_binary: /path/to/mutacc/binary

#Slurm specific parameters placed here after the 'slurm' key
slurm:
  log_directory: /path/to/log/dir #The log (stdout + stderr) files will be created here
  email: 'clark.kent@mail.com' #Mail to notify when slurm completes, or fails
  time: '1:00:00' #Time limit for slurm jobs
  account: 'account_name' #account name
  priority: 'low' #priority
```

### Import

To import the extracted cases into the database (specified in the mutacc configuration file) the 'import' subcommand is used.

```console
mutacc-auto --config-file <config> import
```

This will import all extracted cases.

```console
Usage: mutacc-auto import [OPTIONS]

Options:
  -D, --dry               dry run
  --help                  Show this message and exit.
```

### export

To export a synthetic trio, i.e. three pairs of paired fastq-files, and one
vcf-file with the queried variants the export subcommand is used

```console
mutacc-auto --config-file <config.yaml> export \
--vcf-out <vcf_path> \
--dataset-dir <dir_path> \
--background <backgrounds.yaml>
```

This would include all variants in the mutacc database, and enrich the background
genomic sets specified in the background file. The background yaml file should
specify three pairs of paired fastq-files and a bam-file for each sample in a trio
as the example below

```yaml
child:
  fastq1: /path/to/child/fastq1
  fastq2: /path/to/child/fastq2
  bam: /path/to/child/bam

father:
  fastq1: /path/to/father/fastq1
  fastq2: /path/to/father/fastq2
  bam: /path/to/father/bam

mother:
  fastq1: /path/to/mother/fastq1
  fastq2: /path/to/mother/fastq2
  bam: /path/to/mother/bam
```

The full list of options are

```console
Usage: mutacc-auto export [OPTIONS]

Options:
  -o, --vcf-out PATH      Path to created vcf-file
  -b, --background PATH   yaml file with genomic backgrounds for each sample
                          in trio
  -d, --dataset-dir PATH  Directory where fastq files are placed
  -k, --conda             Use 'conda activate' to source environment
  -e, --environment TEXT  conda environment used for mutacc
  -D, --dry               dry run
  -V, --verbose           verbose
  --help                  Show this message and exit.

```
