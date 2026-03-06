# Use guide

0. In its current version this scripts (in progress) requires a MOREL site built with a Zotero library.
1. Select a fragment no shorter than 280 characters and no longer than 320 characters from your book excerpt or description and add it to the "abstract" field of the correspondent item of the Zotero library
2. Repeat until completing 39 fragments
3. Edit the ´config.py´ file to link your Zotero site's ´books_zotero.csv´ file, and ´SM_posts´ folder
4. Run the simple_test.py script to concatenate all the scripts

# Next steps

X Add a BibAV identification 

# Founding prompt

This script is meant to be ran every 91 days, after curating 39 books. Curating can mean adding an excerpt and the missing metadata from the Google Books database, or adding the correct library information. Also, in both cases, the editor has to choose a < 350 characters fragment from the excerpt (counting from the beginning), and mark it with <!-- post -->.

The script must have a beggining date and an end date, counting 91 days.

The action the script must perform is:

1. Create a grid with 13 weeks, starting the beggining date; the posts created by this grid will be published on Mondays, Fridays and Saturdays, at 11 am. 
2. Go to ´../../morel-no-code-generator/books_zotero.csv´
3. Choose the lastly modified items that:
	1. Have a note
	2. Are not already in the posts database 
4. Pick one item
5. Generate a video quote by picking the excerpt until the <!--post--> mark, and running the commands:
-  ´echo "{{ excerpt }}" | fold -sw70 | while read line; do n=$((n+1)); convert -size 1080x1080 -background "#C6C8C4" -fill "#2a3425" -font "AvantGarde-Book" -weight Black -pointsize 115 -gravity west -size 980x1080 caption:"$(echo "$line" | tr '[:lower:]' '[:upper:]')" -gravity center -extent 1080x1080 "fragment_$n.png"; echo "Generated fragment_$n.png"; done´
- ´ffmpeg -loop 1 -t 3 -i fragment_1.png -loop 1 -t 3 -i fragment_2.png -loop 1 -t 3 -i fragment_3.png -loop 1 -t 3 -i fragment_4.png -loop 1 -t 3 -i fragment_5.png -filter_complex "[0][1]xfade=transition=fade:duration=1:offset=2[ab];[ab][2]xfade=transition=fade:duration=1:offset=4[abc];[abc][3]xfade=transition=fade:duration=1:offset=6[abcd];[abcd][4]xfade=transition=fade:duration=1:offset=8" -c:v libx264 -r 30 -pix_fmt yuv420p output.mp4´
Create a folder for each book named with the Zotero key, and place the images and the video inside them.
6. Pick the full caption from the Jekyll project, based on the Zotero key ´# this needs to be coded in the jekyll project´
7. Store everything as a post in a csv
	- Instagram caption (one column)
    - Twitter caption (several columns)
	- Source to de video
8. Repeat until finishing the elegible posts. 
9. Set up the cron job, to send a message every time a post is due via Telegram, with the correspondent content. Also set up a separate message to let the user know every monday how many weeks left before running out of content.