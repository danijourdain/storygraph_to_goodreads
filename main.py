import os
import pandas as pd
import tkinter
import tkinter.filedialog

from utils.to_goodreads_import import storygraph_export_to_goodreads_import

def save_to_csv(goodreads_df, filename):
    # save data to a new CSV
    save_path = "/".join(filename.split("/")[:-1])
    save_file = os.path.join(save_path, "goodreads_format.csv")
    print(f"Saving to {save_file}")

    goodreads_df.to_csv(save_file, index=False, sep=",", float_format='%.0f')

def main():
    # select which file to use
    tkinter.Tk().withdraw()
    filename = tkinter.filedialog.askopenfilename(filetypes=[("CSV files", ".csv")])
    print(filename)

    # disable scientific notation representation
    pd.set_option("display.float_format", lambda x: "%.f" % x)

    # open the file into a dataframe
    storygraph_df = pd.read_csv(filename)

    # convert to goodreads import format
    goodreads_df = storygraph_export_to_goodreads_import(storygraph_df)
    save_to_csv(goodreads_df, filename)

    # conver to fable import format (same as goodreads export format)

if __name__ == "__main__":
    main()