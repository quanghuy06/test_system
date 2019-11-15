*phocroffice* is a Python library for creating Microsoft Word (.docx),
Excel (.xlsx) and PowerPoint (.pptx) files.

--------------
How to install
--------------

* Prepare *lxml* and *PIL* libraries to copy them into ``3rdparty`` folder

----------
How to use
----------

* Run docx_creator.py, xlsx_creator.py or pptx_creator.py coressponding to output format you want to export and pass valid parameters::
	python docx_creator.py -x <xml_file> -l <language> -o <output_file> [-d <debug>] [--remove-xml]


---------
Structure
---------

^^^^^^^^^^^
phocroffice
^^^^^^^^^^^

  ==================== =======================================================================
  Sub-directory            Contents
  ==================== =======================================================================
  ``docx``             Contain docx library
  ``xlsx``             Contain xlsx library
  ``pptx``             Contain pptx library
  ``phocr_elements``   Contain elements which are porting from PHOcr like OCRPage, ...
  ``tests``            Contain testing source code
  ``phocr_shared``     Contain sharing objects
  ``docx_creator.py``  Executable of creating .docx file
  ``xlsx_creator.py``  Executable of creating .xlsx file
  ``pptx_creator.py``  Executable of creating .pptx file
  ``README.rst``       Overview about module
  ``requirements.txt`` Installed requirements for supported packages
  ``LICENSE``          PHOcr license
  ``.gitignore``       Ignore python like \*.pyc
  ==================== =======================================================================