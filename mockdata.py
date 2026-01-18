import pandas as pd
from datetime import datetime, timedelta

def create_mock_excel():
    base_time=datetime.now()
    data=[]
    
    for i in range(2):
        data.append({"Source_IP":"192.168.1.10","Timestamp": base_time + timedelta(seconds=i*30),
        "Attempted_PW": "wiona2026!", "Actual_PW": "wiosna2026!",
        "User_Targeted": "Eddie"})
    for i, pw in enumerate(["root","admin","password123","shadow"]):
        data.append({"Source_IP":"103.44.12.5","Timestamp": base_time + timedelta(milliseconds=i*300),
        "Attempted_PW": pw, "Actual_PW": "Gr33nl4nd_i5_3vr0p34n!",
        "User_Targeted": "admin"})
    for i, user in enumerate(["exec1","exec2","exec3","exec4"]):
        data.append({"Source_IP": "1721.16.0.44","timestamp": base_time + timedelta(minutes=i*5),
        "Attempted_PW": "Company_name_2026!", "Actual_PW": "Unknown_PW",
        "User_Targeted": user})
    pd.DataFrame(data).to_excel("security_logs.xlsx", index=False)
    print("test generted successfully 'security_logs.xlsx'")
 
if __name__ == "__main__":
     create_mock_excel()