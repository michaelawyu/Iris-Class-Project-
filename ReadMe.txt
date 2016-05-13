Project Iris Readme File

team ReviewChangesWorld

Ruoqi, Wang (rw2612@columbia.edu)
Yuyang, Liu (yl3319@columbia.edu)
Chen, Yu (cy2415@columbia.edu)

> How to Start/Build Project Iris?

	Project Iris is current available as three parts: a web application, a iOS client and a restfulAPI providing access to the iOS client. The web application and iOS client (w/ the support of restfulAPI) could work separately.

	To start up the web application on the server, run

		python server.py

	and Iris will start on localhost:5000 (by default). Use '--debug' parameter to start Iris in debug mode, in which server would be able to return detailed error message once a failure has occurred.

	To start up the restfulAPI on the server, run

		python restfulAPI.py

	resultAPI works at localhost:5001 (by default). '--debug' option is also available.

	The database structure of Iris is available in database_init.sql. It works current with PostgreSQL, however with SQLAlchemy the program could be migrated to other DBMS easily. The dependency of Iris is listed in the final report; nltk and sqlalchemy have to be installed before running.

	An instance of Iris is now deployed on Microsoft Windows Azure platfrom:

		reviewchangesworld.eastus.cloudapp.azure.com:5000

> What's Included in the Package?

	data: a folder containing training data for the NLP analysis component, including

		Brown_dev.txt, Brown_tagged_dev.txt, Brown_tagged_train.txt, Brown_train.txt: The famous Brown corpus
		AFINN-96.txt (AFINN-111.txt): AFINN weighted word collection

	database_init.sql: A description in SQL about Iris' database structure

	FinalReport.pdf: Final report for the class

	ReadMe.txt: ReadMe file

	iOS Client Source Code.zip: Source code for the iOS client

	IrisNLPCore.py: Core library for NLP functions in Iris

	IrisNLPSentimentAnalysis.py: Library for Sentiment Analysis

	IrisNLPTopicExtractor.py: Library for NLP Topic Extraction Analysis

	output: Outputs of the NLP components

	restfulAPI.py: Source code of the restfulAPI

	server.py: Source code of the web application

	static: Resources referenced in the web application (CSS, images, etc.)

	templates: HTML templates for generating webpages in the web applicaiton

> Tutorials of Iris

	Available in the final report.