roi
===

ReOrientedIndexer
-----------------

The ReOrientedIndexer needs a small amount of configuration. To start with, you need to create the Translation and Word Index directories and set up the Pack size.
We will use the example of /optimise/index for the Word Index and /optimise/indexmeta for the Translation Index.

Set up the configuration file like so, leaving the PackSize at its default:

	[Main]
	WordIndex = /optimise/index/
	TransIndex = /optimise/indexmeta/
	PackSize = 100
	
Next, create a source directory wherever you want. In the example, we are going to use /optimise/source. We have added three folders in here which contain the .po files.

	source
	------> Evolution
	-------------> en_GB.po
	-------------> de.po
	-------------> ...
	------> Evolution2
	-------------> en_GB.po
	-------------> de.po
	-------------> ...
	------> Evolution3
	-------------> en_GB.po
	-------------> de.po
	-------------> ...
	
Looking at the help option, we get this

	pete@test:~/workspace/roi$ python ./roi.py --help
	Usage: roi.py <CFG_FILE>

	Indexer

	Options:
	  --version             show program's version number and exit
	  -h, --help            show this help message and exit
	  --cfg=<cfg_file>      Configuration file.

	  Search options:
		--search            Activates the search context.
		-q QUERY, --query=QUERY
							The term to use in your query.
		-o ORIGIN, --origin=ORIGIN
							The original language file to use in your query.
		-t TARGET, --target=TARGET
							The target language file to perform your search.

	  Full indexing options:
		--full-index        Activates the full index context. (Will not run unless
							indexing directories are empty.)
		-s SOURCEDIR, --source-dir=SOURCEDIR
							The source directory for all projects

	  Single project indexing options:
		--project-index     Activates the single project context. (This will
							destroy a projects existing index)
		-p PROJECTDIR, --project-dir=PROJECTDIR
							The project directory for a specific project

	Constructive comments and feedback gladly accepted.
	pete@cagalli:~/workspace/roi$ 
	
	
Now we index the data, using the Full Index option.

	pete@test:~/workspace/roi$ python ./roi.py --cfg=roi.cfg --full-index --source-dir=/optimise/source
	en_GB.po
	/optimise/source/Evolution3/en_GB.po
	pt.po
	/optimise/source/Evolution3/pt.po
	eo.po
	/optimise/source/Evolution3/eo.po
	th.po
	/optimise/source/Evolution3/th.po
	....
	....
	....
	
Now we can search, using the search option

	pete@test:~/workspace/roi$ python ./roi.py --cfg=roi.cfg --search -q "you" -o en_GB.po -t de.po
	Creating Search Object
	=================
	Evolution2-3001
	-----------------
	You are replying to a message which arrived via a mailing list, but you are replying privately to the sender; not to the list. Are you sure you want to proceed?
	-----------------
	Sie antworten auf eine Nachricht, die über eine Mailingliste gesendet wurde, aber Sie antworten an den privaten Absender, nicht an die Liste. Wollen Sie wirklich fortsetzen?
	=================
	Evolution3-3001
	-----------------
	You are replying to a message which arrived via a mailing list, but you are replying privately to the sender; not to the list. Are you sure you want to proceed?
	-----------------
	Sie antworten auf eine Nachricht, die über eine Mailingliste gesendet wurde, aber Sie antworten an den privaten Absender, nicht an die Liste. Wollen Sie wirklich fortsetzen?
	=================
	pete@cagalli:~/workspace/roi$ 

At the moment only two entries have been returned, this is not the only entires in the index, but due to the way the system works at present.
