import datetime



def minutes_to_seconds( minutes: str ) -> int:
      """ Converts minutes to seconds """
      return int(minutes)*60


def hours_to_minutes( hours: str ) -> int:
      """ Converts hours to minutes """
      return int(hours)*60


def hhmm_to_seconds( hhmm: str ) -> int:
      """ Converts time to seconds """

      if len(hhmm.split(':')) != 2:
          print('Incorrect format. Argument must be formatted as HH:MM')
          return None
      return minutes_to_seconds(hours_to_minutes(hhmm.split(':')[0])) + \
          minutes_to_seconds(hhmm.split(':')[1])


def hhmmss_to_seconds( hhmmss: str ) -> int:
      """ Converts time to seconds """
      if len(hhmmss.split(':')) != 3:
          print('Incorrect format. Argument must be formatted as HH:MM:SS')
          return None
      return minutes_to_seconds(hours_to_minutes(hhmmss.split(':')[0])) + \
          minutes_to_seconds(hhmmss.split(':')[1]) + int(hhmmss.split(':')[2])


def present_time():
    """ Function to retrieve current time """
    now = datetime.datetime.now().strftime('%H:%M')
    return now


def time_difference(update_time):
    """ Function to calculate time difference between requested update time and current time """
    update_seconds = hhmm_to_seconds(update_time)
    present_seconds = hhmm_to_seconds(present_time())
    time_diff = update_seconds - present_seconds
    return time_diff

