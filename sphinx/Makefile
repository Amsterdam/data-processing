.PHONY: docs server clean invclean gh-pages

RM            := rm -rf
SPHINXOPTS    := -d .doctrees
SPHINXBUILD   := sphinx-build
AUTOBUILD     := sphinx-autobuild
SOURCEDIR     := source
BUILDDIR      := ../docs
GITORIGIN     = "$$(git config --get remote.origin.url)"
GITBRANCH     = "$$(git symbolic-ref HEAD | sed -e "s/^refs\/heads\///")"


docs:
	$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)
	touch $(BUILDDIR)/.nojekyll


server:
	@$(AUTOBUILD) "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) --watch ../src --watch ./

clean:
	@$(RM) $(BUILDDIR) .doctrees


invclean:
	@$(RM) *.inv *.inv.txt

gh-pages: docs
	[ -d gh-pages ] || git clone --branch gh-pages --single-branch $(GITORIGIN) gh-pages
	cd gh-pages && { [ "`echo *`" = '*' ] || git rm -rf *; }
	cd ../docs && cp -a * ../sphinx/gh-pages
	cd gh-pages && \
	  git add * && \
	  git commit -m 'Update from branch $(GITBRANCH)' && \
	  git push