# TennisCO

In order to use it first extract the zip, then run the command 'python -m pip install -r requirements.txt' in a terminal in the directory of the code.
You can bring up the help as to how to run the code by calling python tennisP.py -h

A couple of examples: For probability of Roger Federer beating Novak Djokovic, run
python tennisP.py men "Roger Federer" "Novak Djokovic"
(tip: adding '-vv' at the end will print on the screen some progress information, as the calculation can take some time (especially if downloading the files for the first time), 
and this way you have an idea of what's going on. So in this case it would be 'python tennisP.py men "Roger Federer" "Novak Djokovic" -vv'

For Serena Williams beating Venus Williams, it would be
python tennisP.py women "Serena Williams" "Venus Williams" -vv

be careful with the case of the text as I haven't implemented any checks. So "serena williams" would not work.