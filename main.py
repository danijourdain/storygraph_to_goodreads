import os
import pandas as pd
import tkinter
import tkinter.filedialog

# field that the Goodreads import supports 
GOODREADS_IMPORT_FIELDS = ["Title", "Author", "ISBN", "My Rating", "Average Rating", "Publisher", "Binding", "Year Published", "Original Publication Year", "Date Read", "Date Added","Shelves", "Bookshelves", "My Review"]

def main():
    # select which file to use
    # tkinter.Tk().withdraw()
    # filename = tkinter.filedialog.askopenfilename(filetypes=[("CSV files", ".csv")])
    filename="C:/Users/danij/Downloads/690a49c1437fb72d7218d6b4a9d5911d6dbca155e6807eec6ea153613dbf4303.csv"
    print(filename)

    # open the file into a dataframe
    storygraph_df = pd.read_csv(filename)

    # rename columsn that are 1:1 equivalent
    storygraph_df.rename(columns={"Authors": "Author", 
                                  "ISBN/UID": "ISBN", 
                                  "Format":"Binding", 
                                  "Read Status": "Shelves", 
                                  "Last Date Read": "Date Read",
                                  "Star Rating": "My Rating",
                                  "Review": "My Review"
                                  }, inplace=True)
    
    for i, row in storygraph_df.iterrows():
        print(f"On row {i}")

        # add owned to the shelves column
        if row["Owned?"] == "Yes":
            row["Shelves"] =  row["Shelves"] + " owned" if pd.notna(row["Shelves"]) else "owned"

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
        if pd.notna(row["My Review"]):
            review += row["My Review"]
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
        row["My Review"] = review

    
    # remove extra columns
    storygraph_df = storygraph_df.drop(columns=["Owned?", "Moods", "Pace", "Character- or Plot-Driven?", "Strong Character Development?", "Loveable Characters?", "Diverse Characters?", "Flawed Characters?", "Content Warnings", "Content Warning Description", "Contributors", "Dates Read", "Read Count"])

    # save data to a new CSV
    save_path = "/".join(filename.split("/")[:-1])
    save_file = os.path.join(save_path, "goodreads_format.csv")

    storygraph_df.to_csv(save_file, index=False)

if __name__ == "__main__":
    main()