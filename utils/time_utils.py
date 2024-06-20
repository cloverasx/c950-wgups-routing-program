from datetime import datetime

class TimeUtils:
    @staticmethod
    def convert_to_minutes(time_str):
        time = datetime.strptime(time_str, '%H:%M')
        return time.hour * 60 + time.minute

    @staticmethod
    def convert_to_time_string(minutes):
        return f'{minutes // 60:02d}:{minutes % 60:02d}'