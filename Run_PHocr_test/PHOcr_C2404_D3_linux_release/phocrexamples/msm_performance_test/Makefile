# Current working directory is phocrexamples
PHOCR_LIBRARY_PATH = $(shell pwd)/../../

CXXFLAGS= -m32 -g -Wall -std=c++11 -I$(PHOCR_LIBRARY_PATH)/include/phocr/ -I$(PHOCR_LIBRARY_PATH)/include/leptonica/  -D_GLIBCXX_USE_CXX11_ABI=0
PHOCRLIBS= $(PHOCR_LIBRARY_PATH)/lib/libPHOcr.so
LDFLAGS=   $(PHOCRLIBS) $(BOOSTLIBS) -Wl,-rpath=$(PHOCR_LIBRARY_PATH)/lib/

all: PHOcrSample

PHOcrSample: PHOcrSample.o
	$(CXX) -o $(PHOCR_LIBRARY_PATH)/bin/MSMPerformanceTestExecutable $(CXXFLAGS) $^ $(LDFLAGS)

PHOcrSample.o: PHOcrSample.cpp
	$(CXX) $(CXXFLAGS) -c $<

clean:
	rm -f $(PHOCR_LIBRARY_PATH)/bin/MSMPerformanceTestExecutable *.o
