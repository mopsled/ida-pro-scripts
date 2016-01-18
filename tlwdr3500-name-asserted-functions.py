ea = BeginEA()
functions_with_assert = set()
function_renames = {}

for function_start in Functions(SegStart(ea), SegEnd(ea)):
	function_name = GetFunctionName(function_start)
	if not function_name.startswith('sub_'):
		continue

	function_end = FindFuncEnd(function_start)
	current_address = function_start
	while current_address != BADADDR:
		code_refs = list(CodeRefsFrom(current_address, 1))
		for ref in code_refs:
			if GetFunctionName(ref) == "__assert":
				functions_with_assert.add(function_name)

				# Step back from current_address, find what was loaded into a2
				instruction_address_for_argument = current_address
				for x in range(10):
					instruction_address_for_argument = PrevHead(instruction_address_for_argument)
					mnem = GetMnem(instruction_address_for_argument)
					if mnem == "la":
						register = GetOpnd(instruction_address_for_argument, 0)
						if register == "$a3":
							string_location = GetOperandValue(instruction_address_for_argument, 1)
							string_value = GetString(string_location, -1, ASCSTR_C)
							function_renames[function_name] = string_value

		current_address = NextHead(current_address, function_end)

functions_with_renames = [f for f in functions_with_assert if f in function_renames]
unidentified_funtions = [f for f in functions_with_assert if f not in function_renames]

for f in functions_with_renames:
	print "Found %s using __assert with function name %s" % (f, function_renames[f])
for f in unidentified_funtions:
	print "Found unidentified function %s using assert" % f
