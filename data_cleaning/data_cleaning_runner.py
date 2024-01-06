import os
import pandas as pd
import numpy as np
import igra_clean
import unit_conversions

def main(txt_file_fp, isa_fp):
    print('Starting IGRA Cleaning...')
    meta_df, data_df = igra_clean.main(txt_file_fp)
    print('IGRA Cleaning Done')
    print('Starting Unit Conversions...')
    output = unit_conversions.main(meta_df, data_df)
    print('Unit Converstions Done')
    print('Adding ISA Data...')
    output['DATE'] = pd.to_datetime(output['DATE'])
    output = output.loc[(output['DATE'] >= '2023-01-01') & (output['DATE'] <= '2023-12-31')]
    isa = pd.read_excel(isa_fp)
    for date in np.unique(output['DATE'].values):
        temp = pd.DataFrame()
        temp['ALTITUDE(FT)']= isa['altitude'].values
        temp['TEMP(F)'] = isa['temp F'].values
        temp['uid'] = max(output['uid'].values)+1
        temp['DATE'] = date
        temp['HOUR'] = 'N/A'
        temp['SITE'] = 'ISA'
        output = pd.concat([output, temp])
    print('Done Adding ISA Data')
    output.to_csv(os.path.join(txt_file_fp, 'igra_noaa.csv'), index=False)
    print(f'Done Cleaning Data, Final Output Saved Here: {txt_file_fp}')
    return

main(r'C:\Users\kmebr\Documents\IGRA_project\data/', 
     r'C:\Users\kmebr\Documents\IGRA_project\data\isa_temps.xlsx')