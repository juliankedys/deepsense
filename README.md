# deepsense

Aim of the project: Parsing .csv files; finding their underlying statistics

Tools used: Flask, Flask Restful, Pandas, JSON library

* Programme's setup and workings: The programme is fairly simple to use; Having started the .py file one needs to pass the path to their .csv file twice (in the terminal) - would the file be renamed to default app.py it could be run via terminal with "flask run" and then entering the path once would suffice. 

* An URL link should appear which, when clicked, will open the browser. The default address (http://127.0.0.1:5000) then has to be extended with any of the endpoints (as defined in the .py file as well as the starting page accessed through the aforementioned URL; the endpoints are explained in more detail there) or an integer standing for the ID of a specific object from the .csv file. 

* Having opened the URL, the user navigates through the programme using endpoints and objects' IDs where suitable (i.e. when a particular collection resource contains more than one object)

* It is possible to upload a csv file via Postman service:
    - add new collection in Postman
    - add new request
    -  paste the URL
    -  change the action to POST
    -  below, switch from   "Params" to "Body"
    -  choose form-data
    -  specify file's name, set the type type from text to file and choose appropriate csv file
    -  click on send

* For the purpose of testing percent() function (meant for calculating the ratio of missing values in a column) I simulate filling some cells of the table with None values.

* Example csv file is attached to the repository (MOCK-DATA.csv)

* Every function has its output allocated to a seperate endpoint (collections or singular where applicable)

