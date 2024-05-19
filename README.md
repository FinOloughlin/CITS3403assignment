The website we have designed is called Madlib. The purpose of the website is to give users the ability to create and play fun word games called madlibs. Effectively, users write a paragraph of text, but replace some words with blank spots and a description of what is supposed to go in that spot, for example they may fill a blank with the description "adjective".
When a user goes to play they game, they are not shown the text, but simply the placeholder descriptions, where they will answer those placeholders and at the end the text will be read back to them with their decided words in place of the placeholders, which hopefully leads to a funny or silly nonsensical response. We designed our website to work just like that, users can create madlibs, then if they want to play they are provided a random madlib that they can fill in the blanks and get their completed response back at the end.   
For further information on what a madlib is, visit this link: https://en.wikipedia.org/wiki/Mad_Libs   

Group members:  
1. Finlay O'loughlin, 23616047, FinOloughlin.   
2. Yu Weng Choong, 23627242, yuwengchoong.   
3. James Champion, 23866758, kaladin23.    
4. Kaili Zhou, 24057973, KylieZhou.   



How to run:   
pull the files to your computer. Open terminal and navigate to the directory that the project is in. 

in terminal type:
> python3 venv -m tmp-env

> source tmp-env/bin/activate

 -- this will open the temp environment which just allows you to use packages that wont conflict with anything else on your computer --

Then in terminal you type:
> pip install requirements.txt

Now all of the required packages will be installed
if you then run in terminal:
> flask run

it will provide you an address that you can copy into your browser and you can use the website with proper functionality. Hopefully the rest of the functionality on the website should be explained on the page.

How to run tests:
enter environment and type:   
> python -m unittest unit
 
