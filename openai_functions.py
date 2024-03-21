from langchain.agents import initialize_agent, AgentType, Tool
from langchain import SerpAPIWrapper
from langchain.chat_models import ChatOpenAI
import requests
import json
import os
from datetime import datetime

class OpenAIFunctions:
    @staticmethod
    def get_current_weather(longitude, latitude):
        """Get the current weather for a location"""
        try:
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current_weather": "true",
                "timezone": "Europe/London",
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return json.dumps(data["current_weather"])
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"Other error occurred: {err}")
        return json.dumps({"error": "Failed to get weather"})

    @staticmethod
    def get_search_results(query):
        """Get search results for a query"""
        try:
            llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
            search = SerpAPIWrapper(
                serpapi_api_key=os.getenv("SERPAPI_API_KEY"),
            )
            tools = [
                Tool(
                    name="Search",
                    func=search.run,
                    description="useful for when you need to answer questions about current events. You should ask targeted questions",
                )
            ]
            agent = initialize_agent(
                tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True
            )
            res = agent.run(query)
            return json.dumps(res)
        except Exception as e:
            print(f"Error getting search results: {e}")
            return json.dumps({"error": "Failed to get search results"})
    
    # @staticmethod
    # def get_business_hours(day=None, open_time=None, close_time=None):
    #     # Define office hours for each day of the week
    #     office_hours = {
    #         "Monday": {"open": "8:00", "close": "19:00"},
    #         "Tuesday": {"open": "8:00", "close": "19:00"},
    #         "Wednesday": {"open": "8:00", "close": "19:00"},
    #         "Thursday": {"open": "8:00", "close": "19:00"},
    #         "Friday": {"open": "8:00", "close": "19:00"},
    #         "Saturday": {"open": "9:00", "close": "16:00"},
    #         "Sunday": {"open": "10:00", "close": "15:00"},
    #     }

    #     # If no day is specified, but open and close are, consider this as a validation scenario
    #     if day and open and close:
    #         # Logic to validate or use open and close times
    #         # For example, checking if the provided times fall within the opening hours for the given day
    #         if day in office_hours:
    #             hours = office_hours[day]
    #             # Here you might compare 'open' and 'close' with 'hours' to perform your validation or other logic
    #             # For simplicity, here we just return the default hours for the day
    #             return json.dumps(hours)
    #         else:
    #             return "Invalid day" 
    
    # @staticmethod
    # def is_business_open(current_day=None, current_time=None):
    #     # If current_day and current_time are not provided, fetch them
    #     if current_day is None or current_time is None:
    #         now = datetime.now()
    #         current_day = now.strftime("%A")
    #         current_time = now.strftime("%H:%M")
            
            
    #     office_hours_json = OpenAIFunctions.get_business_hours(current_day)
    #     office_hours = json.loads(office_hours_json)
        
    #     if current_day in office_hours:
    #         opening_time_str, closing_time_str = office_hours[current_day]["open"], office_hours[current_day]["close"]
    #         opening_time = datetime.strptime(opening_time_str, "%H:%M").time()
    #         closing_time = datetime.strptime(closing_time_str, "%H:%M").time()
            
            
    #         # Convert current_time from string to a datetime.time object
    #         current_time_obj = datetime.strptime(current_time, "%H:%M").time()

    #         # Check if the current time is within the office hours
    #         if opening_time <= current_time_obj <= closing_time:
    #             return "The office is open."
    #         else:
    #             return "The office is closed."
    #     else:
    #         return "Invalid day."
        
    @staticmethod
    def get_business_hours(day=None, open=None, close=None):
        """Get the office/business hours to enable scheduling calls"""
        # Define office hours for each day of the week
        office_hours = {
            "Monday": {"open": "8:00", "close": "19:00"},
            "Tuesday": {"open": "8:00", "close": "19:00"},
            "Wednesday": {"open": "8:00", "close": "19:00"},
            "Thursday": {"open": "8:00", "close": "19:00"},
            "Friday": {"open": "8:00", "close": "19:00"},
            "Saturday": {"open": "9:00", "close": "16:00"},
            "Sunday": {"open": "10:00", "close": "15:00"},
        }

        # If no day is specified, return all hours
        if day is None:
            return json.dumps(office_hours)

        # If day is specified, but open and close are not, return the hours for that day
        if day and open is None and close is None:
            return json.dumps({day: office_hours.get(day, "Invalid day")})

        # If day, open, and close are specified, perform your validation or logic here
        # This example will just return the default hours for simplicity
        if day in office_hours:
            hours = office_hours[day]
            # Implement your logic for using 'open' and 'close' here
            return json.dumps(hours)
        else:
            return "Invalid day"

    @staticmethod
    def is_business_open(current_day=None, current_time=None):
        """Get the current time and day so that you can schedule calls"""
        # If current_day and current_time are not provided, fetch them
        if current_day is None or current_time is None:
            now = datetime.now()
            current_day = now.strftime("%A")  # Get the full weekday name
            current_time = now.strftime("%H:%M")  # Format the time as HH:MM

        office_hours_json = OpenAIFunctions.get_business_hours(current_day)
        office_hours = json.loads(office_hours_json)
        
        if current_day in office_hours:
            opening_time_str, closing_time_str = office_hours[current_day]["open"], office_hours[current_day]["close"]
            opening_time = datetime.strptime(opening_time_str, "%H:%M").time()
            closing_time = datetime.strptime(closing_time_str, "%H:%M").time()

            # Convert current_time from string to a datetime.time object
            current_time_obj = datetime.strptime(current_time, "%H:%M").time()

            # Check if the current time is within the office hours
            if opening_time <= current_time_obj <= closing_time:
                return "The office is open."
            else:
                return "The office is closed."
        else:
            return "Invalid day."

FUNCTIONS_MAPPING = {
    "get_search_results": OpenAIFunctions.get_search_results,
    "get_current_weather": OpenAIFunctions.get_current_weather,
    "get_business_hours": OpenAIFunctions.get_business_hours,
    "is_business_open": OpenAIFunctions.is_business_open,
}
