FSPOTDIR = ~/local/opt/f-spot
GCONFTOOL = /usr/bin/gconftool-2

all: ExiflowRenameVersion.dll

PACKAGES = \
	-pkg:gtk-sharp-2.0	\
	-pkg:glib-sharp-2.0	\
	-pkg:f-spot \
	-pkg:gnome-vfs-sharp-2.0

ASSEMBLIES = \
	-r:Mono.Posix

RESOURCES = \
	-resource:ExiflowRenameVersion.addin.xml

SOURCES = \
	ExiflowRenameVersion.cs

install: all
	cp *.dll ~/.gnome2/f-spot/addins/

mpack: ExiflowRenameVersion.dll
	mautil p ExiflowRenameVersion.dll

%.dll: $(SOURCES) ExiflowRenameVersion.addin.xml 
	PKG_CONFIG_PATH=$(FSPOTDIR)/lib/pkgconfig gmcs -target:library $(SOURCES) $(PACKAGES) $(ASSEMBLIES) $(RESOURCES)

clean:
	rm -f *.dll *~ *.bak .mpack

PHONY:
	install clean all mpack
