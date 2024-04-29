# Makefile para compilar e executar um programa Python

PYTHON = python3
TESTDIR = tests
TESTFILES = $(wildcard $(TESTDIR)/*.txt)
OUTFILES = $(TESTFILES:.txt=.out)

all: test

test: $(TESTFILES)
    @for testfile in $^ ; do \
        echo "Testando $$testfile" ; \
        $(PYTHON) codigo_feito.py < $$testfile > $$testfile.actual ; \
        if diff -u $$testfile.out $$testfile.actual ; then \
            echo "Teste $$testfile passou!" ; \
        else \
            echo "Teste $$testfile falhou!" ; \
            exit 1 ; \
        fi ; \
    done

clean:
    rm -f $(TESTDIR)/*.out $(TESTDIR)/*.actual
