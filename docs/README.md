# README

## Environment

Python 3 must be installed in `/usr/bin/python3`.

## Running

The code can be run with the command `make build f=language` where the file `language.sem` exists in the current directory and contains a set of semantics. I have provided `arith.sem`, `lambda_cbv.sem`, and `lambda_cbn.sem` for testing. This should generate an executable `language` file which can be used to interpret code writen in `language` and a directory `_language/` containing the source code for the interpreter. The usage of the `language` interpreter is `./language <file>` where file contains a program written in `language`. The source directory can safely be deleted once the interpreter is generated; it only persists so the user can satisfy their curiosity (or debug their semantics).

The interpreter and the directory created by `make build f=language` can be removed by `make clean f=language`.

