FSPOTDIR = ~/local/opt/f-spot
GCONFTOOL = /usr/bin/gconftool-2

all: ExiflowDevelopInUFRaw.dll

PACKAGES = \
	-pkg:gtk-sharp-2.0	\
	-pkg:glade-sharp-2.0	\
	-pkg:glib-sharp-2.0	\
	-pkg:f-spot \
	-pkg:gnome-vfs-sharp-2.0

ASSEMBLIES = \
	-r:Mono.Posix

RESOURCES = \
	-resource:ExiflowDevelopInUFRaw.addin.xml

SOURCES = \
	ExiflowDevelopInUFRaw.cs

install: all
	cp *.dll ~/.gnome2/f-spot/addins/

mpack: ExiflowDevelopInUFRaw.dll
	mautil p ExiflowDevelopInUFRaw.dll

%.dll: $(SOURCES) ExiflowDevelopInUFRaw.addin.xml
	PKG_CONFIG_PATH=$(FSPOTDIR)/lib/pkgconfig gmcs -target:library $(SOURCES) $(PACKAGES) $(ASSEMBLIES) $(RESOURCES)

clean:
	rm -f *.dll *~ *.bak .mpack

PHONY:
	install clean all mpack
