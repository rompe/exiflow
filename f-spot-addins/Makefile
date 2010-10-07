prefix ?= /usr
INSTALL_PATH ?= $(prefix)/lib/f-spot/Extensions

REPOSITORY_PATH ?= repository

all: build

repository:
	mkdir -p $(REPOSITORY_PATH)
	for dir in Exiflow*/; do if [ -f $$dir/Makefile ]; then make -C $$dir mpack; cp $$dir/*.mpack $(REPOSITORY_PATH)/; fi; done
	cd $(REPOSITORY_PATH); mautil rb .

build:
	for dir in Exiflow*/; do if [ -f $$dir/Makefile ]; then make -C $$dir; fi; done

mpack:
	for dir in Exiflow*/; do if [ -f $$dir/Makefile ]; then make -C $$dir mpack; fi; done

install:
	for dir in Exiflow*/; do if [ -f $$dir/Makefile ]; then make -C $$dir install; fi; done

clean:
	for dir in Exiflow*/; do if [ -f $$dir/Makefile ]; then make -C $$dir clean; fi; done

download: 
	ssh rompe,exiflow@shell.sf.net create
	rsync -avuzH rompe,exiflow@shell.sf.net:/home/groups/e/ex/exiflow/htdocs/f-spot-addins/ $(REPOSITORY_PATH)

install-rep: download repository
	ssh rompe,exiflow@shell.sf.net create

	rsync -avuzH --exclude .svn/ --delete --delete-excluded $(REPOSITORY_PATH)/ rompe,exiflow@shell.sf.net:/home/groups/e/ex/exiflow/htdocs/f-spot-addins


.PHONY: install clean all repository download build mpack
