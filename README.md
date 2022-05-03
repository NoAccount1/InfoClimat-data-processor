# InfoClimat date processor

---
 * `main.py` : used to show graph
 * `request.py` : download data all data from [InfoClimat OpenData](https://www.infoclimat.fr/opendata/)
 * `utils.py` : bundle of all functions and import used in other files

Extensions
---
 * `.raw.json` is the extension for files directly downloaded from the OpenData

    ***Note :*** *it contain only one month data*
 * `.merged.json` is the extension for files without metadata and everything else from the OpenData

    ***Note :*** *here it contain a whole year and* ***can contain `null` values***

 * `.formated.json` is the extension for cleaned and minified data

    ***Note :*** *theses files only contains the dates and temperatures for a year and* ***all `null` values are removed***
    
Example
---
![OpenData Example](https://user-images.githubusercontent.com/74969657/166501403-d7acb4f7-634b-4a64-a369-09ae2d86bdd0.png)
