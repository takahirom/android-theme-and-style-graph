python parse.py appcompat
dot -Tpdf output/appcompat.dot -o output/appcompat.pdf
dot -Tjpg output/appcompat.dot -o output/appcompat.jpg
convert output/appcompat.jpg -resize 50% output/small_appcompat.jpg

python parse.py iosched
dot -Tpdf output/iosched.dot -o output/iosched.pdf
dot -Tjpg output/iosched.dot -o output/iosched.jpg
convert output/iosched.jpg -resize 50% output/small_iosched.jpg
