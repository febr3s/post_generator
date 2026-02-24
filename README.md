This script is meant to be ran every 91 days, after curating 39 books. Curating can mean adding an excerpt and the missing metadata from the Google Books database, or adding the correct library information. Also, in both cases, the editor has to choose a < 350 characters fragment from the excerpt (counting from the beginning), and mark it with <!-- post -->.

The script must have a beggining date and an end date, counting 91 days.

The action the script must perform is:

1. Create a grid with 13 weeks, starting the beggining date; the posts created by this grid will be published on Mondays, Fridays and Saturdays, in times to be defined. 
2. Go to ´../../morel-no-code-generator/books_zotero.csv´ (alternatively use the Zotero API)
3. Choose the lastly modified items that:
	1. Have a note
	2. Are not already in the posts database 
4. Pick one item
5. Store a post in a csv
	- Caption: Draft it with a standard syntax, using placeholders and metadata + tags
	- Images: Generate them by picking the excerpt until the <!--post--> mark, and running the command. Create a folder for each book, and place the images inside them. Source them on the csv. Repeat until finishing the elegible posts. 
6. Set up the cron job, to send a message every time a post is due via Telegram. Let the user know how many weeks left before running out of content.