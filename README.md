# wikidata-quicksheets

v0.1 Initial release 

v0.2 Upgraded to Python 3 with 2to3. The sorting functionality is not
working right. The QID Labels are outputting as binary data, hence the
b’stringvalue’ in the CSV. Adding a .decode('UTF-8') throws errors, and
resolving this isn’t critical at this exact moment.