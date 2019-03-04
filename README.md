# mutacc-auto
[![Build Status](https://travis-ci.org/Clinical-Genomics/mutacc-auto.png)](https://travis-ci.org/Clinical-Genomics/mutacc-auto)
[![Coverage Status](https://coveralls.io/repos/github/Clinical-Genomics/mutacc-auto/badge.svg?branch=master)](https://coveralls.io/github/Clinical-Genomics/mutacc-auto?branch=master)

mutacc-auto work as a wrapper for [MutAcc](https://github.com/Clinical-Genomics/mutacc), to automate
the process of uploading new cases to the MutAcc database, export, and upgrade validation sets. mutacc-auto
takes use of other CLI apps in the Clinical-Genomics suite, [hosekeeper](https://github.com/Clinical-Genomics/housekeeper),
and [scout](https://github.com/Clinical-Genomics/scout), to assemble all relevant files, and meta-data about a case as
input to MutAcc.  
