
all: repository

repository:
	mkdir -p repository
	for dir in */; do if [ -f $$dir/Makefile ]; then make -C $$dir mpack; mv $$dir/*.mpack repository/; fi; done
	cd repository; mautil rb .

clean:
	rm -rf repository/

install: all
	rsync -avuzH repository/ rompe@shell.sf.net:/home/groups/e/ex/exiflow/htdocs/f-spot-addins


.PHONY: install clean all repository
