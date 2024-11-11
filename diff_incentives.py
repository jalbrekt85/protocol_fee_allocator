import pandas as pd
import numpy as np

def diff_incentives(v1_path, v2_path, output_path):
    df_v1 = pd.read_csv(v1_path)
    df_v2 = pd.read_csv(v2_path)
    
    columns_to_diff = [
        'total_incentives', 'bal_incentives', 'earned_fees', 
        'aura_incentives', 'redirected_incentives', 'fees_to_vebal'
    ]
    
    diff_df = pd.DataFrame()
    
    common_columns = list(set(df_v1.columns) & set(df_v2.columns))
    non_numeric_cols = df_v2[common_columns].select_dtypes(exclude=[np.number]).columns
    diff_df[non_numeric_cols] = df_v2[non_numeric_cols]
    
    for col in columns_to_diff:
        if col in df_v1.columns and col in df_v2.columns:
            v1_col = pd.to_numeric(df_v1[col], errors='coerce')
            v2_col = pd.to_numeric(df_v2[col], errors='coerce')
            
            diff_amount = v2_col - v1_col
            diff_pct = np.where(diff_amount == 0, 
                              0, 
                              ((v2_col - v1_col) / v1_col * 100).round(2))
            diff_df[f'{col}_diff'] = diff_amount.astype(str) + ' (' + diff_pct.astype(str) + '%)'

    diff_df.to_csv(output_path, index=False)
    return output_path

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python diff_incentives.py <v1_csv_path> <v2_csv_path> <output_path>")
        sys.exit(1)
    
    diff_incentives(sys.argv[1], sys.argv[2], sys.argv[3])