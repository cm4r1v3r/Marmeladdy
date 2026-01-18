import pandas as pd
from fuzzywuzzy import fuzz
from datetime import datetime

class Marmeladdy:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = pd.read_excel(file_path)
        self.df['Timestamp'] = pd.to_datetime(self.df['Timestamp'])
        self.df = self.df.sort_values(by=['Source_IP', 'Timestamp'])

    def run_analysis(self):
        self.df['Similarity'] = self.df.apply(
            lambda x: fuzz.ratio(str(x['Attempted_PW']), str(x['Actual_PW'])), axis=1
        )
        self.df['Time_Gap'] = self.df.groupby('Source_IP')['Timestamp'].diff().dt.total_seconds()
        report = self.df.groupby('Source_IP').agg({
            'Similarity': ['mean', 'count'],
            'Time_Gap': 'median',
            'User_Targeted': 'nunique'
        })
        report.columns = ['Avg_Similarity', 'Total_Attempts', 'Median_Gap_Sec', 'Unique_Users']
        report['Verdict'] = report.apply(self._classify_behavior, axis=1)
        return report

    def _classify_behavior(self, row):
        is_fast = row['Median_Gap_Sec'] < 2.0 if pd.notna(row['Median_Gap_Sec']) else False
        is_high_sim = row['Avg_Similarity'] > 80
        
        if is_fast and not is_high_sim:
            return "Critical: Brute force"
        if is_fast and is_high_sim:
            return "High: Credential stuffing"
        if row['Unique_Users'] > 3:
            return "Medium: Password spraying"
        if is_high_sim:
            return "LOW: Likely user typo"
        return "Normal Activity"

def main():
    print("Hello human person, I'm Marmeladdy!")
    INPUT_FILE = "security_logs.xlsx"
    
    try:
        agent = Marmeladdy(INPUT_FILE)
        results = agent.run_analysis()
        print("\n" + "=" * 80)
        print(f"{'Source IP':<15} | {'Attempts':<8} | {'Fuzzy Avg':<12} | {'Verdict'}")
        print("-" * 80)
        
        for ip, row in results.iterrows():
            print(f"{ip:<15} | {int(row['Total_Attempts']):<8} | {row['Avg_Similarity']:<12.1f} | {row['Verdict']}")  
            
        print("=" * 80)
        results.to_excel("report.xlsx")
        print("Report saved to report.xlsx")
        
    except FileNotFoundError:
        print(f"Error: The file '{INPUT_FILE}' was not found.")

if __name__ == "__main__":
    main()
