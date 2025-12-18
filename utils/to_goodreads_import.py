import os
import pandas as pd

# field that the Goodreads import supports 
GOODREADS_IMPORT_FIELDS = ["Title", "Author", "ISBN", "My Rating", "Average Rating", "Publisher", "Binding", "Year Published", "Original Publication Year", "Date Read", "Date Added","Shelves", "Bookshelves", "My Review"]

def storygraph_export_to_goodreads_import(storygraph_df: pd.DataFrame):
    print("Converting books...", end="\r")

    # rename columsn that are 1:1 equivalent
    goodreads_df = storygraph_df.copy().infer_objects()
    goodreads_df.rename(columns={"Authors": "Author", 
                                  "ISBN/UID": "ISBN", 
                                  "Format":"Binding", 
                                  "Read Status": "Shelves", 
                                  "Last Date Read": "Date Read",
                                  "Star Rating": "My Rating",
                                  "Review": "My Review"
                                  }, inplace=True)
    
    # convert column data types
    goodreads_df['ISBN'] = pd.to_numeric(goodreads_df['ISBN'], errors='coerce').astype('Int64')
    goodreads_df['Date Read'] = pd.to_datetime(goodreads_df['Date Read'], errors='coerce').dt.strftime('%Y-%m-%d')
    goodreads_df['Date Added'] = pd.to_datetime(goodreads_df['Date Added'], errors='coerce').dt.strftime('%Y-%m-%d')

    for i, row in storygraph_df.iterrows():
        # add owned to the shelves column
        if row["Owned?"] == "Yes":
            goodreads_df.loc[i, "Shelves"] =  row["Read Status"] + " owned" if pd.notna(row["Read Status"]) else "to-read, owned"

        # condense the review into one field
        review = ""

        # convert the Storygraph categories into HTML text fields
        if pd.notna(row["Moods"]):
            review += f"<b>Moods:</b> {row["Moods"]} <br>"
        if pd.notna(row["Pace"]):
            review += f"<b>Pace:</b> {row["Pace"]} <br>"
        if pd.notna(row["Character- or Plot-Driven?"]):
            review += f"<b>Character or plot driven?</b> {row["Character- or Plot-Driven?"]} <br>"
        if pd.notna(row["Strong Character Development?"]):
            review += f"<b>Strong character development?</b> {row["Strong Character Development?"]} <br>"
        if pd.notna(row["Loveable Characters?"]):
            review += f"<b>Loveable Characters?</b> {row["Loveable Characters?"]} <br>"
        if pd.notna(row["Diverse Characters?"]):
            review += f"<b>Diverse Characters?</b> {row["Diverse Characters?"]} <br>"
        if pd.notna(row["Flawed Characters?"]):
            review += f"<b>Are character flaws a main focus?</b> {row["Flawed Characters?"]} <br>"

        # add the actual review
        if pd.notna(row["Review"]):
            review += row["Review"]
            review += "<br>"

        # add any content warnings
        if pd.notna(row["Content Warnings"]):
            content_warnings = row["Content Warnings"].split(";")[:-1]
            
            # print(f"CONTENT WARNINGS: {content_warnings}")

            # address by severity (Graphic, Moderate, and Minor)
            for severity_level in content_warnings:
                severity = severity_level.split(":")[0]
                warnings = severity_level.split(":")[1].split(",")

                review += f"<i><b>{severity}:</b></i>{warnings}<br>"

        # add content warning descriptions
        if pd.notna(row["Content Warning Description"]):
            review += row["Content Warning Description"]

        # add the review back to the column
        goodreads_df.loc[i, "My Review"] = review
        
    
    # remove extra columns
    goodreads_df = goodreads_df.drop(columns=["Owned?", "Moods", "Pace", "Character- or Plot-Driven?", "Strong Character Development?", "Loveable Characters?", "Diverse Characters?", "Flawed Characters?", "Content Warnings", "Content Warning Description", "Contributors", "Dates Read", "Read Count", "Tags"])

    # add columns required for Fable?
    goodreads_df["Average Rating"] = pd.Series()
    goodreads_df["Publisher"] = pd.Series()
    goodreads_df["Year Published"] = pd.Series()
    goodreads_df["Original Publication Year"] = pd.Series()
    goodreads_df["Bookshelves"] = pd.Series()

    print("Conversion complete!")

    return goodreads_df