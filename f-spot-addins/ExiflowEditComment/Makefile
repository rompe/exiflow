ADDIN = ExiflowEditComment

prefix ?= /usr
INSTALL_PATH ?= $(prefix)/lib/f-spot/Extensions

all: $(ADDIN).dll

PACKAGES = \
	-pkg:gtk-sharp-2.0      \
	-pkg:glade-sharp-2.0    \
	-pkg:glib-sharp-2.0     \
	-pkg:f-spot \
	-pkg:gnome-vfs-sharp-2.0

ASSEMBLIES = \
	-r:Mono.Posix \
        -r:$(prefix)/lib/f-spot/gtk-sharp-beans.dll \
        -r:$(prefix)/lib/f-spot/gio-sharp.dll \
        -r:$(prefix)/lib/f-spot/Hyena.dll \
        -r:$(prefix)/lib/f-spot/Hyena.Gui.dll 

RESOURCES = \
	-resource:$(ADDIN).glade \
	-resource:$(ADDIN).addin.xml

SOURCES = \
	$(ADDIN).cs

$(ADDIN).dll: $(SOURCES) $(ADDIN).addin.xml
	PKG_CONFIG_PATH=$(prefix)/lib/pkgconfig gmcs -target:library $(SOURCES) $(PACKAGES) $(ASSEMBLIES) $(RESOURCES)

install: all
	cp *.dll $(INSTALL_PATH)/

mpack: $(ADDIN).dll
	mautil p $(ADDIN).dll && touch mpack

clean:
	rm -f *.dll *~ *.bak *.mpack mpack

PHONY:
	install clean all 
