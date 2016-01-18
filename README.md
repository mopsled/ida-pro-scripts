# ida-pro-scripts

All scripts are written in IDAPython.

## Script Descriptions

- **tlwdr3500-name-asserted-functions.py**

  In the TLWDR3500 firmware, the `__assert` function uses the function name as a parameter whenever an assert is triggered, e.g.
  
      int parser_parse_entity(request_id *reqId) {
        if (reqId->sProtocol < 2) {
           __assert("reqId->sProtocol < 2", "httpOutput.c", 0x48, "httpStatusLine");
        }
        // ...
      }
  This script locates the fourth argument (`$a3`) in `__assert` function calls from unnamed functions (`sub_*`) and prints the results.
