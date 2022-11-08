def validate_input(input, expectedType, field):
            
    if input is None:
        raise Exception(f"Cannot create user with no valid {field}")
    
    if isinstance(input, expectedType):
        return input
    raise AssertionError("[validate_input] Invalid input for type", field)