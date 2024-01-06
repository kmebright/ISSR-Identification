import os
import pandas as pd
import numpy as np

class NOAADataSet():

    def __init__(self, files):
        self.files = files
        self.data = []
        self.read_data()
        self.meta_df = pd.DataFrame()
        self.data_df = pd.DataFrame()
        self.meta_str = '''
                        HEADREC       1-  1  Character
                        SITEID        2- 12  Character
                        YEAR         14- 17  Integer
                        MONTH        19- 20  Integer
                        DAY          22- 23  Integer
                        HOUR         25- 26  Integer
                        RELTIME      28- 31  Integer
                        NUMLEV       32- 36  Integer
                        PW           38- 43  Integer
                        INVPRESS     44- 49  Integer
                        INVHGT       50- 55  Integer
                        INVTEMPDIF   56- 61  Integer
                        MIXPRESS     62- 67  Integer
                        MIXHGT       68- 73  Integer
                        FRZPRESS     74- 79  Integer
                        FRZHGT       80- 85  Integer
                        LCLPRESS     86- 91  Integer
                        LCLHGT       92- 97  Integer
                        LFCPRESS     98- 103  Integer
                        LFCHGT      104- 109  Integer
                        LNBPRESS    110- 115  Integer
                        LNBHGT      116- 121  Integer
                        LI          122- 127  Integer
                        SI          128- 133  Integer
                        KI          134- 139  Integer
                        TTI         140- 145  Integer
                        CAPE        146- 151  Integer
                        CIN         152- 157  Integer
                        '''
        self.data_str = '''
                        PRESS           1-  7   Integer
                        REPGPH          9- 15   Integer
                        CALCGPH        17- 23   Integer
                        TEMP           25- 31   Integer
                        TEMPGRAD       33- 39   Integer
                        PTEMP          41- 47   Integer
                        PTEMPGRAD      49- 55   Integer
                        VTEMP          57- 63   Integer
                        VPTEMP         65- 71   Integer
                        VAPPRESS       73- 79   Integer
                        SATVAP         81- 87   Integer
                        REPRH          89- 95   Integer
                        CALCRH         97- 103   Integer
                        RHGRAD        105- 111   Integer
                        UWND          113- 119   Integer
                        UWDGRAD       121- 127   Integer
                        VWND          129- 135   Integer
                        VWNDGRAD      137- 143   Integer
                        N             145- 151   Integer
                        '''
        self.get_data()
        self.clean_data()

    def read_data(self):
        print('reading data...')
        for file in self.files:
            with open(file, 'r') as f:
                self.data.append(f.readlines())
        return

    def get_data(self):
        print('formatting data...')
        cur_id = 1
        for lines in self.data:
            meta_rows = [lines[0]+' '+str(cur_id)]
            data_rows = []
            for line in lines[1:]:
                if line[0] == '#':
                    cur_id +=1
                    meta_rows.append(line+ ' '+str(cur_id))
                else:
                    data_rows.append(line+' '+str(cur_id))
            text = self.meta_str.split('\n')
            splits = [[t.split()[1].strip('-'), t.split()[2]] for t in text[1:-1]]
            cols = [t.split()[0] for t in text[1:-1]][1:]
            splits = splits[1:]
            splits[0][0] = 1
            splits = [[int(s[0])-1, int(s[1])] for s in splits]
            all_meta = []
            for row in meta_rows:
                temp = []
                for s in splits:
                    temp.append(row[s[0]:s[1]])
                temp.append(row.split()[-1])
                all_meta.append(temp)
            self.meta_df = pd.concat([self.meta_df, pd.DataFrame(all_meta, columns=cols+['uid'])])
            text = self.data_str.split('\n')
            splits = [[t.split()[1].strip('-'), t.split()[2]] for t in text[1:-1]]
            cols = [t.split()[0] for t in text[1:-1]]
            splits = [[int(s[0])-1, int(s[1])] for s in splits]
            all_data = []
            for row in data_rows:
                temp = []
                for s in splits:
                    temp.append(row[s[0]:s[1]])
                temp.append(row.split()[-1])
                all_data.append(temp)
            self.data_df = pd.concat([self.data_df, pd.DataFrame(all_data, columns=cols+['uid_fk'])])
        print('finished formatting')
        return

    def clean_data(self):
        print('cleaning data...')
        for col in self.meta_df.columns[1:]:
            self.meta_df[col] = self.meta_df[col].astype(int)
        for col in self.data_df.columns:
            self.data_df[col] = self.data_df[col].astype(int)
        self.meta_df.replace(-99999, np.nan, inplace=True)
        self.data_df.replace(-99999, np.nan, inplace=True)
        self.meta_df['RELTIME'].replace(9999, np.nan, inplace=True)
        print('done cleaning')
        return


def main(fp):
    data = NOAADataSet([fp+file for file in os.listdir(fp) if '.txt' in file])
    print('saving data...')
    data.meta_df.to_csv(fp+'igra_metadata.csv', index=False)
    data.data_df.to_csv(fp+'igra_measurements.csv', index=False)
    print('done!')
    return data.meta_df, data.data_df
