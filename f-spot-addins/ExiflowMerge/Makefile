ADDIN = ExiflowMerge
#FSPOTDIR = ~/local/opt/f-spot
FSPOTDIR = /usr

all: $(ADDIN).dll

PACKAGES = \
	-pkg:gtk-sharp-2.0	\
	-pkg:f-spot 		\
 	-r:$(FSPOTDIR)/lib/f-spot/Hyena.Gui.dll 

ASSEMBLIES =

RESOURCES = \
	-resource:$(ADDIN).addin.xml

SOURCES = \
	$(ADDIN).cs

$(ADDIN).dll: $(SOURCES) $(ADDIN).addin.xml
	PKG_CONFIG_PATH=$(FSPOTDIR)/lib/pkgconfig gmcs -target:library -o:$@ $(SOURCES) $(PACKAGES) $(ASSEMBLIES) $(RESOURCES)

clean:
	rm -f *.dll *~ *.bak *.mpack

install: all
	cp $(ADDIN).dll ~/.config/f-spot/addins/

mpack: $(ADDIN).dll
	mautil p $(ADDIN).dll

PHONY:
	install clean all mpack
