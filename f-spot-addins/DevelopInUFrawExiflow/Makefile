FSPOTDIR = ~/local/opt/f-spot
GCONFTOOL = /usr/bin/gconftool-2

all: DevelopInUFRawExiflow.dll

PACKAGES = \
	-pkg:gtk-sharp-2.0	\
	-pkg:glade-sharp-2.0	\
	-pkg:glib-sharp-2.0	\
	-pkg:f-spot \
	-pkg:gnome-vfs-sharp-2.0

ASSEMBLIES = \
	-r:Mono.Posix

RESOURCES = \
	-resource:DevelopInUFRawExiflow.addin.xml

SOURCES = \
	DevelopInUFRawExiflow.cs

install: all
	cp *.dll ~/.gnome2/f-spot/addins/

mpack: DevelopInUFRawExiflow.dll
	mautil p DevelopInUFRawExiflow.dll

%.dll: $(SOURCES) DevelopInUFRawExiflow.addin.xml
	PKG_CONFIG_PATH=$(FSPOTDIR)/lib/pkgconfig gmcs -target:library $(SOURCES) $(PACKAGES) $(ASSEMBLIES) $(RESOURCES)

clean:
	rm -f *.dll *~ *.bak .mpack

PHONY:
	install clean all mpack
