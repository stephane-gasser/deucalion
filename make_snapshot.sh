## create an archive to ease (proto) deployment
DATE=`date +%y%m%d`
#python manage.py dumpdata --indent 2 cms text picture >content-$DATE.json #file snippet googlemap form_designer 
python manage.py dumpdata --natural --indent 2 Content >content-content-$DATE.json
FILES="media/ content-content-$DATE.json"
tar cvfz snapshot-$DATE.tgz $FILES
