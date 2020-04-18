git clone https://github.com/thomaspark/bootswatch.git
cd bootswatch
git checkout v2.3.2
npm install
bower install
ln -s bower_components/ components
mv readable ..
ln -s ../readable
