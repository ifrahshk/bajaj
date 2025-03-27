import pandas as pd

def run():
    path = "C:/Users/Admin/Desktop/Data Engineering/data - sample.xlsx"
    
    df = pd.read_excel(path)
    df = df.sort_values(by=['student_id', 'attendance_date'])
    df['absent_streak'] = (df['status'] == 'Absent').astype(int)
    df['streak_id'] = (df['absent_streak'].diff() != 0).cumsum()
    
    streaks = df.groupby(['student_id', 'streak_id']).agg(
        absence_start_date=('attendance_date', 'first'),
        absence_end_date=('attendance_date', 'last'),
        total_absent_days=('absent_streak', 'sum')
    ).reset_index()
    
    streaks = streaks[streaks['total_absent_days'] > 3]
    
    latest_streaks = streaks.loc[streaks.groupby('student_id')['absence_end_date'].idxmax(),
                                 ['student_id', 'absence_start_date', 'absence_end_date', 'total_absent_days']]
    
    return latest_streaks
