# mutacc-auto
[![Build Status](https://travis-ci.org/Clinical-Genomics/mutacc-auto.png)](https://travis-ci.org/Clinical-Genomics/mutacc-auto)
[![Coverage Status](https://coveralls.io/repos/github/Clinical-Genomics/mutacc-auto/badge.svg?branch=master)](https://coveralls.io/github/Clinical-Genomics/mutacc-auto?branch=master)

mutacc-auto work as a wrapper for [MutAcc](https://github.com/Clinical-Genomics/mutacc), to automate
the process of uploading new cases to the MutAcc database, export, and upgrade validation sets. mutacc-auto
takes use of other CLI apps in the Clinical-Genomics suite, [hosekeeper](https://github.com/Clinical-Genomics/housekeeper),
and [scout](https://github.com/Clinical-Genomics/scout), to assemble all relevant files, and meta-data about a case as
input to MutAcc.  

## Dependencies

mutacc-auto depends on housekeeper >= 2.2 and scout >= 4.2. These tools must be installed first. mutacc-auto also uses the slurm workload manager to submit jobs.  

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

To extract the clinically relevant reads from a case used

```console
mutacc-auto extract \
--config-file <mutacc_configuration> \
--case-id <case_id> \
--environment <conda_env> \
```

slurm specific options can be given with options --log-directory, --email.

full list of options

```console
Usage: mutacc-auto extract [OPTIONS]

Options:
  -c, --case-id TEXT        case id used in scout and housekeeper
  -d, --days-ago INTEGER    days since last update of case
  -e, --environment TEXT    conda environment used for mutacc
  -C, --config-file PATH    configuration file used for mutacc
  -L, --log-directory PATH  Directory for slurm logs
  -E, --email TEXT          email to notify
  -p, --padding INTEGER     padding for genomic regions. this defaults to 0
                            for WES cases
  -D, --dry                 dry run
  -V, --verbose             verbose
  -k, --conda               Use 'conda activate' to source environment
  --help                    Show this message and exit.

```

### Import

To import the extracted cases into the database (specified in the mutacc configuration file) the
'import' subcommand is used.

```console
mutacc-auto import \
--config-file <mutacc_configuration> 
```

This will import all extracted cases.

```console
Usage: mutacc-auto import [OPTIONS]

Options:
  -C, --config-file PATH  configuration file used for mutacc
  -D, --dry               dry run
  -V, --verbose           verbose
  --help                  Show this message and exit.
```
