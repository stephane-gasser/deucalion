theme=$1
cd bootswatch
grunt swatch:$theme --force
cp build/$theme/bootstrap*.css ../../main/static/css/
