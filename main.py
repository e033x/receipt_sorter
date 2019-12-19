from datetime import date
import secrets, os, os.path, csv, tools #probably entirely superflous "tools"-file, which at present contains TWO(!) whole defs. 
import config as cfg

#This program is meant to help me sort and store receipts for tax porposes. It organizes the files with generated filenames,
#and stores their relevant data (extracted mostly using eyeball_mk1()) in a CSV, which can be exported to google sheets et al. later.
#I tried to optimize for the perfect low_click/high_flexibility-ratio.
#Format:
#   "dat" = date,
#   "val" = £$, (with automatic live currency conversion!)
#   "cat" = category, like travel, materials etc.
#   "tag" = for project X, or to vendor Y etc. Possibly useless.
#   "hsh" = four digit hexadecimal hash, because:
#           filename duplications is a pain in the ass. #primePoetry

#1.3 ------------------------------

in_folder = cfg.path["in_folder"]
out_folder = cfg.path["out_folder"]

#----------------------------------

class entry:
    #assigns values to an instance and generates a filename based on them:
    def __init__(self, dat, val, cat, tag, hsh):
        self.filename = f"{cat}{dat.strftime('%d%m%y')}-{hsh}-{tag}.pdf"
        self.data = {"dat": dat.strftime("%d.%m.%Y"),
                     "val": val,
                     "cat": cat,
                     "tag": tag,
                     "hsh": hsh,
                     "filename": self.filename}
         
    #appends instance values (self.data) to a csv, so come Tax Day, I can import to google sheets:
    def append_csv(self, data):
        
        data_csv_exists = os.path.isfile("data.csv")
        
        with open("data.csv", "a", newline="") as csv_file:
            fieldnames = ["dat", "val", "cat", "tag", "hsh", "filename"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            #in case this is the first time the program runs:
            if not data_csv_exists:
                writer.writeheader()
            
            writer.writerow(data)


def file_mover():

    #identifies content in input folder, and processes them each individually:
    inf_content = os.listdir(in_folder)
    for i in inf_content:
        oldname = i #because I tried to make "i" do too many things
        source = f"{in_folder}/{oldname}"
        
        #open file to get values with eyeball_mk1()
        os.startfile(source) 

        #tools.val_input parses an input like "100EURO", and automatically converts it to the
        #   desired currency according to the exchage rate of the date set by i_dat.
        #tools.date_parser parses ambiguous date imputs like 110619 into the CORRECT format.
        i_dat = tools.date_parser(input("Dato: (tom=dd)\n"))
        i_val = tools.val_input(input("Beløp: (num(opt:cur) - no space)\n"), i_dat)
        i_cat = input("Kategori:\n")
        i_tag = input("Tag:\n")
        i_hsh = secrets.token_hex(2)

        i = entry(i_dat, i_val, i_cat, i_tag, i_hsh)

        #trying to move the file while it is still open gives error:
        input("Please close file and press enter") 
        
        dest = f"{out_folder}/{i.filename}"
        #engage!
        os.rename(source, dest)
        i.append_csv(i.data)
        #func()didNothingWrong
        print(f"{oldname} moved to {out_folder} as {i.filename}.")


input("Press enter to start")
file_mover()
        


