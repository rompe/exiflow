#FSPOTDIR = ~/local/opt/f-spot
FSPOTDIR = /usr
GCONFTOOL = /usr/bin/gconftool-2

all: ExiflowRenameVersion.dll

PACKAGES = \
	-pkg:gtk-sharp-2.0	\
	-pkg:glib-sharp-2.0	\
	-pkg:f-spot \
	-pkg:gnome-vfs-sharp-2.0

ASSEMBLIES = \
	-r:Mono.Posix 	\
        -r:$(FSPOTDIR)/lib/f-spot/Hyena.dll \
        -r:$(FSPOTDIR)/lib/f-spot/gio-sharp.dll \
        -r:$(FSPOTDIR)/lib/f-spot/gtk-sharp-beans.dll

RESOURCES = \
	-resource:ExiflowRenameVersion.addin.xml

SOURCES = \
	ExiflowRenameVersion.cs

install: all
	cp *.dll ~/.config/f-spot/addins/

mpack: ExiflowRenameVersion.dll
	mautil p ExiflowRenameVersion.dll

%.dll: $(SOURCES) ExiflowRenameVersion.addin.xml 
	PKG_CONFIG_PATH=$(FSPOTDIR)/lib/pkgconfig gmcs -target:library $(SOURCES) $(PACKAGES) $(ASSEMBLIES) $(RESOURCES)

clean:
	rm -f *.dll *~ *.bak .mpack

PHONY:
	install clean all mpack
