FUNCTIONS_SCHEMA = [
    {
        "name": "get_search_results",
        "description": "Used to get search results when the user asks for it",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The query to search for",
                }
            },
        },
    },
    {
        "name": "get_current_weather",
        "description": "Get the current weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "longitude": {
                    "type": "number",
                    "description": "The approximate longitude of the location",
                },
                "latitude": {
                    "type": "number",
                    "description": "The approximate latitude of the location",
                },
            },
            "required": ["longitude", "latitude"],
        },
    },
    {
        "name": "get_business_hours",
        "description": "Check or set office opening hours before scheduling appointment",
        "parameters": {
            "type": "object",
            "properties": {
                "day": {
                    "type": "string",
                    "enum": ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                    "description": "Day of the week"
                },
                "open": {
                    "type": "string",
                    "description": "Opening time, e.g., 09:00"
                },
                "close": {
                    "type": "string",
                    "description": "Closing time, e.g., 19:00"
                }
            },
            "required": ["day", "open", "close"]
        }
    },
    {
        "name": "is_business_open",
        "description": "Check if business is open or closed",
        "parameters": {
            "type": "object",
            "properties": {
                "current_day": {
                    "type": "string",
                    "description": "Today's day, e.g. Monday"
                },
                "current_time": {
                    "type": "string",
                    "description": "Current time, e.g. 09:30"
                }
            },
            "required": ["current_day", "current_time"]
        }
    }
    # other functions
]
