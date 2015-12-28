python parse.py
dot -Tpdf style.dot -o output.pdf
dot -Tjpg style.dot -o output.jpg
convert output.jpg -resize 50% small_output.jpg
