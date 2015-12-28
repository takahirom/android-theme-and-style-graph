python parse.py appcompat
dot -Tpdf appcompat.dot -o appcompat.pdf
dot -Tjpg appcompat.dot -o appcompat.jpg
convert appcompat.jpg -resize 50% small_appcompat.jpg

python parse.py iosched
dot -Tpdf iosched.dot -o iosched.pdf
dot -Tjpg iosched.dot -o iosched.jpg
convert iosched.jpg -resize 50% small_iosched.jpg
