ADDIN = ExiflowEditComment
FSPOTDIR = ~/local/opt/f-spot

all: $(ADDIN).dll

PACKAGES = \
	-pkg:gtk-sharp-2.0      \
	-pkg:glade-sharp-2.0    \
	-pkg:glib-sharp-2.0     \
	-pkg:f-spot \
	-pkg:gnome-vfs-sharp-2.0

ASSEMBLIES = \
	-r:Mono.Posix

RESOURCES = \
	-resource:$(ADDIN).glade \
	-resource:$(ADDIN).addin.xml

SOURCES = \
	$(ADDIN).cs

$(ADDIN).dll: $(SOURCES) $(ADDIN).addin.xml
	PKG_CONFIG_PATH=$(FSPOTDIR)/lib/pkgconfig gmcs -target:library $(SOURCES) $(PACKAGES) $(ASSEMBLIES) $(RESOURCES)

clean:
	rm -f *.dll *~ *.bak *.mpack

install: all
	cp $(ADDIN).dll ~/.config/f-spot/addins/

mpack: $(ADDIN).dll
	mautil p $(ADDIN).dll

PHONY:
	install clean all mpack
