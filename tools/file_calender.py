import csv
from datetime import datetime
from icalendar import Calendar, Event

def remove_contacts_without_birthday(input_file, output_file):
    """Removes contacts with missing birthday details and writes to a new CSV file."""
    with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        headers = next(reader)  # Read header row
        writer.writerow(headers)  # Write header to new file

        for row in reader:
            subject, start_date, start_time, end_date, end_time, description, location, all_day_event = row

            # Check if Start Date (birthday) is present
            if start_date.strip():
                writer.writerow(row)

    print(f"Filtered CSV file created: {output_file}")

def convert_to_google_calendar_csv(input_file, output_file):
    # Define Google Calendar CSV headers
    headers = ["Subject", "Start Date", "Start Time", "End Date", "End Time", "Description", "Location", "All Day Event"]

    # Read input CSV file
    with open(input_file, mode='r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        next(reader)  # Skip header row

        events = []
        for row in reader:
            name, year, month, day, profile_link = row

            # If year is missing, leave Start Date blank
            if year.strip():
                start_date = f"{month}/{day}/{year}"  # MM/DD/YYYY format
            else:
                start_date = ""

            # Define event details
            event = [
                name,        # Subject
                start_date,  # Start Date
                "",         # Start Time (Blank)
                start_date,  # End Date (Same as Start Date)
                "",         # End Time (Blank)
                profile_link,# Description (Using Profile Link)
                "",         # Location (Blank)
                "True"       # All Day Event
            ]
            events.append(event)

    # Write to Google Calendar formatted CSV file
    with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(headers)  # Write header row
        writer.writerows(events)  # Write event data

    print(f"CSV file successfully converted and saved as {output_file}")


def convert_to_google_calendar_ical(input_file, output_file):
    cal = Calendar()
    cal.add('X-WR-CALNAME', 'My Birthday List')  # Set calendar name

    with open(input_file, mode='r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        next(reader)  # Skip header row

        for row in reader:
            subject, start_date, start_time, end_date, end_time, description, location, all_day_event = row

            if not start_date.strip():
                continue

            try:
                event_date = datetime.strptime(start_date, "%m/%d/%Y")
            except ValueError:
                continue  # Skip invalid dates

            event = Event()
            event.add('summary', f"{subject} BD 🎂")  # Modify event title
            event.add('dtstart', event_date)
            event.add('dtend', event_date)
            event.add('description', description)  # Add profile link as description
            #event.add('allDay', 'TRUE')
            event.add('rrule', {'freq': 'yearly'})  # Set recurrence yearly
            event.add('X-APPLE-CALENDAR-COLOR', 'tomato')  # Set event color to red (Tomato)
            event.add('transp', 'TRANSPARENT')  # Ensure it's marked as an all-day event

            cal.add_component(event)

    # Write .ics file
    with open(output_file, 'wb') as icsfile:
        icsfile.write(cal.to_ical())

    print(f"ICS file successfully created: {output_file}")


# Example usage
remove_contacts_without_birthday("google_calendar_events.csv", "google_calendar_events_filtered.csv")
convert_to_google_calendar_ical("google_calendar_events_filtered.csv", "google_calendar_events.ics")
#convert_to_google_calendar_csv("facebook-dates-of-birth.csv", "google_calendar_events.csv")
