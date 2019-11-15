# Path to PHOcr library path which contain include and lib folder
PHOCR_LIBRARY_PATH = $(shell pwd)/../../

CXXFLAGS= -m32 -g -Wall -std=c++11 -pthread -I$(PHOCR_LIBRARY_PATH)/include/phocr/ -I$(PHOCR_LIBRARY_PATH)/include/leptonica/  -D_GLIBCXX_USE_CXX11_ABI=0
PHOCRLIBS= $(PHOCR_LIBRARY_PATH)/lib/libPHOcr.so
LDFLAGS=   $(PHOCRLIBS) $(BOOSTLIBS) -Wl,-rpath=$(PHOCR_LIBRARY_PATH)/lib/

all: CancelPHOcr

CancelPHOcr: CancelPHOcr.o
	$(CXX) -o $(PHOCR_LIBRARY_PATH)/bin/CancelPHOcr $(CXXFLAGS) $^ $(LDFLAGS)

CancelPHOcr.o: CancelPHOcr.cpp
	$(CXX) $(CXXFLAGS) -c $<

clean:
	rm -f $(PHOCR_LIBRARY_PATH)/bin/CancelPHOcr *.o
