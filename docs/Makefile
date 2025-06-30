# Makefile for building Sphinx documentation

SPHINXBUILD   = sphinx-build
SOURCEDIR     = source
BUILDDIR      = _build

.PHONY: help clean html

help:
	@echo "Makefile for Sphinx documentation"
	@echo ""
	@echo "Usage:"
	@echo "  make html       Build the HTML documentation"
	@echo "  make clean      Clean the built documentation"

html:
	$(SPHINXBUILD) -b html $(SOURCEDIR) $(BUILDDIR)/html
	@echo
	@echo "Build finished. HTML pages are in $(BUILDDIR)/html"

clean:
	rm -rf $(BUILDDIR)

