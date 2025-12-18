# Storygraph Export to Goodreads format

Trying to decide which reading tracking app to use? Are you frustrated not being able to swap exports between apps easily? Me too. That's why I created this application to convert the Storygraph exports into the Goodreads format so it can be imported into Goodreads.

The extra information such as publication year is not available from the Storygraph export, so my current solution is to export from Storygraph, run the export through this program, import the data into Goodreads, then export the data from Goodreads into Fable.

## How to use
run `main.py`

## What it does

This program takes the Storygraph CSV export and converts it into the Goodreads format. Because of the difference in format, ***some*** data wil be lost. This includes the number of re-reads and the contributors.

The Storygraph fields such as "Character or plot-driven" will be condensed into a new review field. A typical review from Storygraph will be converted to this format for a Goodreads review:


<b>Moods:</b> funny, lighthearted <br>
<b>Pace:</b> fast <br>
<b>Character or plot driven?</b> Character <br>
<b>Strong character development?</b> Yes <br>
<b>Loveable Characters?</b> Yes <br>
<b>Diverse Characters?</b> Yes <br>
<b>Are character flaws a main focus?</b> Yes <br>

<div>I liked this book</div> <br>

<b>Content Warnings</b> <br>
<i><b>Graphic:</b></i> Sexual content <br>
<i><b>Moderate:</b></i> Death <br>
<i><b>Minor:</b></i> Infidelity <br>