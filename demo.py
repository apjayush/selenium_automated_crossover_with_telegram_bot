import schedule
import time
from datetime import datetime, time as dt_time


# def greet():
#     print("Hello Aryan")

# def schedule_task():
#     now = datetime.now().time()
#     start_time = dt_time(17, 55)
#     end_time = dt_time(18, 00)
    
#     if start_time <= now <= end_time:
#         greet()

# # Schedule the task every 3 seconds
# schedule.every(10).seconds.do(schedule_task)

# # Run the scheduler
# while True:
#     schedule.run_pending()
#     time.sleep(1)  # Adjust sleep time as

now =  datetime.now()
print(now.hour)