
all: repository

repository:
	mkdir -p repository
	for dir in Exiflow*/; do if [ -f $$dir/Makefile ]; then make -C $$dir clean; make -C $$dir; make -C $$dir mpack; mv $$dir/*.mpack repository/; fi; done
	cd repository; mautil rb .

clean:
	rm -rf repository/

download: 
	ssh rompe,exiflow@shell.sf.net create

	rsync -avuzH rompe,exiflow@shell.sf.net:/home/groups/e/ex/exiflow/htdocs/f-spot-addins/ repository

install: download all
	ssh rompe,exiflow@shell.sf.net create

	rsync -avuzH --exclude .svn/ --delete --delete-excluded repository/ rompe,exiflow@shell.sf.net:/home/groups/e/ex/exiflow/htdocs/f-spot-addins


.PHONY: install clean all repository
