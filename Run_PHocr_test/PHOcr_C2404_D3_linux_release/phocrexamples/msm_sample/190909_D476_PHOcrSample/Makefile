# Current working directory is phocrexamples
PHOCR_LIBRARY_PATH = $(shell pwd)/../../../

CXXFLAGS= -m32 -g -Wall -std=c++11 -I$(PHOCR_LIBRARY_PATH)/include/phocr/ -I$(PHOCR_LIBRARY_PATH)/include/leptonica/ -D_GLIBCXX_USE_CXX11_ABI=0
PHOCRLIBS= $(PHOCR_LIBRARY_PATH)/lib/libPHOcr.so \
	$(PHOCR_LIBRARY_PATH)/lib/libleptonica.so \
	$(PHOCR_LIBRARY_PATH)/lib/libmacroregion.so \
	$(PHOCR_LIBRARY_PATH)/lib/libocrengine.so \
	$(PHOCR_LIBRARY_PATH)/lib/libutility.so \
	$(PHOCR_LIBRARY_PATH)/lib/libbarcode.so \
	$(PHOCR_LIBRARY_PATH)/lib/libpreprocess.so

LDFLAGS=   $(PHOCRLIBS) $(BOOSTLIBS) -Wl,-rpath=$(PHOCR_LIBRARY_PATH)/lib/

all: PHOcrSample

PHOcrSample: PHOcrSample.o
	$(CXX) -o $(PHOCR_LIBRARY_PATH)/bin/190909_D476_PHOcrSample $(CXXFLAGS) $^ $(LDFLAGS)

PHOcrSample.o: PHOcrSample.cpp
	$(CXX) $(CXXFLAGS) -c $<

clean:
	rm -f $(PHOCR_LIBRARY_PATH)/bin/190909_D476_PHOcrSample *.o
