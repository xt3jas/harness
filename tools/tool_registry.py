BASH_TOOL = {
    "type" : "function" , 
    "function" : {
        "name" : "bash",
        "description" : "Run a shell command and return its output. " ,
        "parameters" : {
            "type" : "object" ,
            "properties" : {
                "command" : {
                    "type" : "string" ,
                    "description" : "The shell command to run. "
                }
            },
            "required" : ["command"],
        }
    }
}

TOOLS = [BASH_TOOL]
