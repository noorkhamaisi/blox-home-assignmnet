import json
from flask import Flask, request, jsonify

app = Flask(__name__)

REQUIRED_VALIDATORS_NUMBER = 3

@app.route('/state', methods=['GET'])
def get_state():
    """
    Endpoint to retrieve the processed state based on the provided file name and block number.

    Returns:
        tuple: A tuple containing JSON response containing the processed state and HTTP status code.
    """
    file_name = request.args.get('fileName')
    block_number = int(request.args.get('blockNumber'))
    blocks_data = read_file(file_name)
    processed_state = process_state(blocks_data, block_number)
    return jsonify(processed_state), 200

def process_state(blocks_data: dict, block_number: int) -> dict:
    """
    Processes the state from blocks data until the specified block number.

    Args:
        blocks_data (dict): The data containing blocks information.
        block_number (int): The block number until which to process the state.

    Returns:
        dict: The processed state containing validators and operators.
    """
    existing_operators_positions = {}
    validators = []
    operators = []
    validator_id = 0
    blocks_data = blocks_data['blocks']
    sorted_blocks_data = sort_blocks_and_transactions(blocks_data)
    
    for i in range(block_number + 1):
        block = sorted_blocks_data[i]
        for transaction in block['transactions']:
            register = transaction.get('register')
            address = transaction.get('address')
            if len(register) >= REQUIRED_VALIDATORS_NUMBER:
                validator = create_validator(validator_id, address, register)
                validators.append(validator)
                for operator in register:
                    operators = update_operators(operator, operators, existing_operators_positions, validator_id)
                validator_id += 1
                
    state = {"validators": validators, "operators": operators}
    return state

def update_operators(operator: str, operators: list, existing_operators_positions: dict, validator_id: int) -> list:
    """
    Updates the operators list based on the provided operator, its position, and the validator ID.

    Args:
        operator (str): The operator to update.
        operators (list): The list of operators.
        existing_operators_positions (dict): Dictionary mapping operator IDs to their positions in the operators list.
        validator_id (int): The ID of the validator associated with the operator.

    Returns:
        list: The updated list of operators.
    """
    if operator not in existing_operators_positions:
        existing_operators_positions[operator] = len(operators)
        operators.append({'id': operator, 'validators': [validator_id]})
    else:
        operator_position = existing_operators_positions[operator]
        operators[operator_position]['validators'].append(validator_id)
    return operators

def create_validator(validator_id: int, address: str, register: list) -> dict:
    """
    Creates a validator dictionary.

    Args:
        validator_id (int): The ID of the validator.
        address (str): The address of the validator.
        register (list): The list of operators associated with the validator.

    Returns:
        dict: The validator dictionary.
    """
    return {'id': validator_id, 'address': address, 'operators': register}

def sort_blocks_and_transactions(blocks_data: list) -> list:
    """
    Sorts the blocks and transactions based on their IDs.

    Args:
        blocks_data (list): The list of blocks.

    Returns:
        list: The sorted list of blocks.
    """
    sorted_blocks_data = sorted(blocks_data, key=lambda x: x['id'])
    for block in sorted_blocks_data:
        block['transactions'] = sorted(block['transactions'], key=lambda x: x['id'])
    return sorted_blocks_data

def read_file(file_name: str) -> dict:
    """
    Reads JSON data from the provided file.

    Args:
        file_name (str): The name of the file to read.

    Returns:
        dict: The loaded JSON data.
    """
    with open(file_name, 'r') as file:
        data = json.load(file)
    return data

if __name__ == '__main__':
    app.run(debug=True, port=5005)
    
