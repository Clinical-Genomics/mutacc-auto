import pytest
import json
from mock import patch
import os
from pathlib import Path

from mutacc_auto.procedures.export_procedure import (run_mutacc_export_command,
                                                     export_trio,
                                                     bgzip_vcf_file,
                                                     index_vcf_file,
                                                     merge_vcf_files,
                                                     synthesize_dataset,
                                                     synthesize_trio,
                                                     export_dataset)
from mutacc_auto.commands.command import Command

@patch.object(Command, 'check_output')
def test_run_mutacc_export_command(check_output_mock, mutacc_export_output):

    check_output_mock.return_value = mutacc_export_output

    mutacc_out = run_mutacc_export_command(mutacc_config='path/to/config',
                                           mutacc_binary='mutacc_binary',
                                           proband=True,
                                           member='child',
                                           sample_name='child')

    assert mutacc_out == json.loads(mutacc_export_output)


@patch.object(Command, 'check_output')
def test_export_trio(check_output_mock, mutacc_export_output):

    check_output_mock.return_value = mutacc_export_output

    mutacc_files = export_trio(mutacc_config='path/to/config',
                               mutacc_binary='mutacc_binary')
    mutacc_export_output_json = json.loads(mutacc_export_output)
    mutacc_files_expected = {'father': mutacc_export_output_json,
                             'child': mutacc_export_output_json,
                             'mother': mutacc_export_output_json}

    assert mutacc_files == mutacc_files_expected


@patch.object(Command, 'call')
def test_bgzip_vcf_files(call_mock):
    vcf_file = 'vcf_file'
    zipped_vcf = bgzip_vcf_file(vcf_file)
    assert zipped_vcf == vcf_file + '.gz'


@patch.object(Command, 'call')
def test_index_vcf_files(call_mock):
    vcf_file = 'vcf_file.gz'
    index_vcf = index_vcf_file(vcf_file)
    assert index_vcf == vcf_file + '.tbi'


@patch.object(Command, 'call')
def test_merge_vcf_files(call_mock):
    out_vcf = 'vcf_merge.vcf.gz'
    merged_vcf = merge_vcf_files(vcf_files=['vcf1, vcf2, vcf3'],
                                 out_file=out_vcf)
    assert merged_vcf == out_vcf


@patch.object(Command, 'call')
def test_synthesize_dataset(check_output_mock, mutacc_synthesize_output, mutacc_synthesize_input, tmpdir):

    check_output_mock.return_value = mutacc_synthesize_output
    tmp_dir = Path(tmpdir.mkdir('test_run_mutacc_extract'))
    sbatch_path = synthesize_dataset(sample=mutacc_synthesize_input,
                                     mutacc_binary='binary',
                                     mutacc_config='path/to/config',
                                     slurm_options={'log_directory': '/path/to/log/dir'},
                                     tmp_dir=tmp_dir
                                     )

    assert os.path.exists(sbatch_path)


@patch.object(Command, 'call')
def test_synthesize_trio(check_output_mock, mutacc_synthesize_input, tmpdir):

    tmp_dir = Path(tmpdir.mkdir('test_run_mutacc_extract'))
    datasets = synthesize_trio(mutacc_config='path/to/config',
                               samples={'father': mutacc_synthesize_input,
                                        'mother': mutacc_synthesize_input,
                                        'child': mutacc_synthesize_input},
                               mutacc_binary='mutacc_binary',
                               tmp_dir=tmp_dir,
                               slurm_options={'log_directory': '/path/to/log/dir'})

    for member in datasets.keys():
        assert os.path.exists(datasets[member])

@patch('mutacc_auto.procedures.export_procedure.export_trio')
@patch('mutacc_auto.procedures.export_procedure.bgzip_vcf_file')
@patch('mutacc_auto.procedures.export_procedure.index_vcf_file')
@patch('mutacc_auto.procedures.export_procedure.merge_vcf_files')
@patch('mutacc_auto.procedures.export_procedure.synthesize_trio')
@patch('os.remove')
def test_export_dataset(mock_os_remove,
                        mock_synthesize_trio,
                        mock_merge_vcf_files,
                        mock_index_vcf_file,
                        mock_bgzip_vcf_file,
                        mock_export_trio,
                        mutacc_export_output,
                        mutacc_synthesize_output,
                        background_set):

    mutacc_export_output_json = json.loads(mutacc_export_output)
    mock_export_trio.return_value = {'father': mutacc_export_output_json,
                                     'child': mutacc_export_output_json,
                                     'mother': mutacc_export_output_json}
    mock_bgzip_vcf_file.return_value = 'path/to/zipped_vcf'
    mock_index_vcf_file.return_value = 'path/to/vcf_index'
    mock_merge_vcf_files.return_value = 'path/to/merged_vcf'
    synthesize_output = json.loads(mutacc_synthesize_output)['fastq_files']
    mock_synthesize_trio.return_value = ({'father': synthesize_output,
                                          'mother': synthesize_output,
                                          'child': synthesize_output})
    datasets = export_dataset(mutacc_config='path/to/config',
                              background=background_set,
                              mutacc_binary='path/to/binary',
                              merged_vcf_path='path/to/merged_vcf')


    assert datasets == {'father': synthesize_output,
                        'mother': synthesize_output,
                        'child': synthesize_output}
