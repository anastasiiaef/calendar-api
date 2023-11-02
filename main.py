"""Main entrypoint for vault setup"""

from typing import Dict
from datetime import datetime
import json

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event


app = FastAPI()

# Globals
EMAIL_ADDR = "nastkaefff@gmail.com"
CRED_PATH = "./credentials.json"
EVENT_ENV_TYPES = {
    1: "Outdoor On Grass",
    2: "Outdoor On Pavement",
    3: "Indoor In Gym",
}


app = FastAPI(debug=False)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:4200",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class EventData(BaseModel):
    data: Dict


@app.post("/create_event")
async def create_event(data: EventData):
    """Creates event in google calendar"""
    # yo dawg i heard you like data so we put some ....
    data = json.loads(data.json())["data"]

    #  for tessin
    # data = {
    #     # Calendar Event
    #     "eventName": "poopi parti",
    #     "eventStartDate": "2022-12-10T00:00:00.000Z",
    #     "eventEndDate": "2022-12-10T00:00:00.000Z",
    #     "eventStartTime": "12:40",
    #     "eventEndTime": "13:40",
    #     "location": "8319 KENWOOD RD\napt 3, Cincinnati, OH 45236",        
    #     # Description
    #     "eventSetupTime": "21:40",
    #     "customerName": "ANASTASIIA S EFIMOVA",
    #     "environmentTypeID": 2,
    #     "eventType": "Gym",
    #     "eventDescription": "I am a karen! rawrrrr",
    #     "inflatableCount": 0,
    #     "employeesForTheEvent": 10,
    #     "custAddress": "8319 KENWOOD RD\napt 3",
    #     "custCity": "Cincinnati",
    #     "custState": "OH",
    #     "custZip": "45236",
    #     "custEmail": "nastkaefff@gmail.com",
    # }

    # Convert date strings to datetime object
    start_date = data["eventStartDate"]
    end_date = data["eventEndDate"]
    start_date = data["eventStartDate"].split("T")[0]
    start_time = data["eventStartTime"]
    end_date = data["eventEndDate"].split("T")[0]
    end_time = data["eventEndTime"]
    start = datetime.strptime(f"{start_date}@{start_time}", r"%Y-%m-%d@%H:%M")
    end = datetime.strptime(f"{end_date}@{end_time}", r"%Y-%m-%d@%H:%M")

    print(start)
    print(end)
    # Parse out description for misc fields to put in event description
    desc = f"""
{data['customerName']} ({data['custEmail']}) requested the following appointment:
- Environment Type: {EVENT_ENV_TYPES[data['environmentTypeID']]}
- Event Setup Time: {data['eventSetupTime']}
- Requested Employees: {data['employeesForTheEvent']}
- Inflatable Count: {data['inflatableCount']}
- Event Type: {data['eventType']}
- Customer Email: {data['custEmail']}
- Customer Notes: {data['eventDescription']}
"""

    # Call create event method
    calendar = GoogleCalendar(EMAIL_ADDR, credentials_path=CRED_PATH)
    calendar.add_event(
        Event(
            name=data["eventName"],
            location=data["location"],
            summary=data["eventName"],
            start=start,
            end=end,
            description=desc,
            timezone="EST"
        )
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
