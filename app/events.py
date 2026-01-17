import vobject
from app.db import get_connection
from datetime import datetime, timezone


def get_all_events(start, end):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT calendarid, CONVERT(principaluri USING utf8) AS principal_uri
        FROM calendarinstances
    """)
    calendars = cursor.fetchall()

    events = []

    if start.tzinfo is None:
        start = start.replace(tzinfo=timezone.utc)
    if end.tzinfo is None:
        end = end.replace(tzinfo=timezone.utc)

    for cal in calendars:
        calendarid = cal["calendarid"]
        principal = cal["principal_uri"]

        cursor.execute("""
            SELECT calendardata
            FROM calendarobjects
            WHERE calendarid = %s
        """, (calendarid,))

        rows = cursor.fetchall()

        for row in rows:
            ical_text = row["calendardata"].decode("utf-8")
            cal_obj = vobject.readOne(ical_text)

            for component in cal_obj.components():
                if component.name == "VEVENT":
                    vevent = component
                    dtstart = vevent.dtstart.value
                    dtend = vevent.dtend.value if hasattr(vevent, "dtend") else None

     
                    if dtstart.tzinfo is None:
                        dtstart = dtstart.replace(tzinfo=timezone.utc)
                    if dtend and dtend.tzinfo is None:
                        dtend = dtend.replace(tzinfo=timezone.utc)

                    if start <= dtstart <= end:
                        events.append({
                            "calendar": principal.split("/")[-1], 
                            "summary": vevent.summary.value if hasattr(vevent, "summary") else "",
                            "start": dtstart.strftime("%H:%M %d-%m-%Y"),
                            "end": dtend.strftime("%H:%M %d-%m-%Y") if dtend else "",
                            "description": vevent.description.value if hasattr(vevent, "description") else ""
                        })

    cursor.close()
    conn.close()
    return events
