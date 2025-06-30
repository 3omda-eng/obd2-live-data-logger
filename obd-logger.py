import obd
import pandas as pd
import time
from datetime import datetime

print("Connecting to OBD2 device...")
connection = obd.OBD()

commands = {
    "RPM": obd.commands.RPM,
    "Speed": obd.commands.SPEED,
    "CoolantTemp": obd.commands.COOLANT_TEMP
}

data_log = []

print("Starting data logging... Press Ctrl+C to stop.\n")
try:
    while True:
        row = {"Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        for label, cmd in commands.items():
            response = connection.query(cmd)
            row[label] = response.value.magnitude if not response.is_null() else None
        data_log.append(row)
        print(row)
        time.sleep(1)
except KeyboardInterrupt:
    print("\nLogging stopped. Saving file...")
    df = pd.DataFrame(data_log)
    df.to_csv("obd2_log.csv", index=False)
    print("✅ Data saved to obd2_log.csv")
