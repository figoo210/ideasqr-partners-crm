import datetime
import pytz


def get_user_timezone_info():
    # Get the local timezone of the system
    local_timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo

    # Get the current offset from UTC
    offset_seconds = datetime.datetime.now(local_timezone).utcoffset().total_seconds()
    offset_hours = int(offset_seconds // 3600)
    offset_minutes = int((offset_seconds % 3600) // 60)

    # Format the offset string
    offset_str = "{:+03}:{:02}".format(offset_hours, abs(offset_minutes))

    # Create the timezone string
    timezone_string = "Timezone: ({}) {}".format(offset_str, local_timezone)

    return timezone_string
