register_schema = {
    "type": "object",
    "properties": {
        "action": {
            "type": "string",
            "enum": ["register"]
        },
        "data": {
            "type": "object",
            "properties": {
                "username": {
                    "type": "string",
                    "minLength": 1
                },
                "password": {
                    "type": "string",
                    "minLength": 1
                }
            },
            "required": ["username", "password"]
        }
    },
    "required": ["action", "data"]
}


loginschema = {
    "type" : "object",
    "properties":
        {
        "action" : {"type": "string"},
        "data" : {
            "type" : "object",
            "properties":{
                "username": {"type": "string"},
                "password": {"type": "string"}
                },
            "required": ["username", "password"]
        }
        },
    "required": ["action", "data"]
}


room_action_schema = {
    "type": "object",
    "properties": {
        "action": {
            "type": "string",
            "enum": ["room"]
        },
        "data": {
            "type": "object",
            "properties": {
                "room_action": {
                    "type": "string",
                    "enum": ["enter_room", "leave_room"]
                },
                "room_name": {
                    "type": "string",
                    "minLength": 1
                }
            },
            "required": ["room_action", "room_name"]
        }
    },
    "required": ["action", "data"]
}

chat_message_schema = {
    "type": "object",
    "properties": {
        "action": {
            "type": "string",
            "enum": ["chat"]
        },
        "data": {
            "type": "object",
            "properties": {
                "to": {
                    "type": "string",
                    "minLength": 1
                },
                "message": {
                    "type": "string",
                    "minLength": 1
                }
            },
            "required": ["to", "message"]
        }
    },
    "required": ["action", "data"]
}
