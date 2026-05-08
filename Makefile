MAIN ?= main.tex
OUTDIR ?= out

LATEXMK ?= latexmk
LATEXMK_FLAGS ?= -f -pdf -interaction=nonstopmode -file-line-error

PDF := $(OUTDIR)/$(basename $(notdir $(MAIN))).pdf

.PHONY: all pdf watch clean

all: pdf

pdf:
	mkdir -p "$(OUTDIR)"
	$(LATEXMK) $(LATEXMK_FLAGS) -outdir="$(OUTDIR)" "$(MAIN)" || true
	test -s "$(PDF)"

watch:
	mkdir -p "$(OUTDIR)"
	$(LATEXMK) $(LATEXMK_FLAGS) -pvc -outdir="$(OUTDIR)" "$(MAIN)"

clean:
	$(LATEXMK) -C -outdir="$(OUTDIR)" "$(MAIN)"
