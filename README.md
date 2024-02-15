
# State Processing Flask Application
This Flask application provides an endpoint to retrieve the processed state based on the provided file name and block number.

## Running the Application
To run the application, execute the following command in the terminal:

```
python3 blocks_assignment.py
```
## API Endpoint
### GET /state

* Parameters:
    * fileName: The name of the file containing blocks data.
    * blockNumber: The block number until which to process the state.

### Example Usage

```
GET /state?fileName=data.json&blockNumber=2
```
### Description
The application reads JSON data from the provided file, processes the state until the specified block number, and returns the processed state as a JSON response.

The processed state contains two main components:

* 'validators': A list of validators, each with an ID, address, and a list of associated operators.
* 'operators': A list of operators, each with an ID and a list of associated validator IDs.


### State Processing Logic
The state processing logic is as follows:

* Iterate through the blocks data until the specified block number.
* For each block, iterate through the transactions.
* If a transaction has a register with at least 3 operators, create a validator and add it to the validators list.
* For each operator in the register, update the operators list by adding the validator ID to the operator's list of associated validators.
  
### Note
The code assumes that the blocks data is stored in a JSON file with the following structure:

```
{
    "blocks": [
        {
            "id": 1,
            "transactions": [
                {
                    "id": 1,
                    "register": ["operator1", "operator2", "operator3"],
                    "address": "validator1_address"
                },
                ...
            ]
        },
        ...
    ]
}
```
Make sure to replace the file path in the code with the actual path to your blocks data file.

## Dockerfile
Alternatively, you can run the application using Docker.

To build and run the Docker container, execute the following commands in the terminal:
```
docker build -t your_image_name .
docker run -p 5005:5005 your_image_name
```
Replace "your_image_name" with the desired name for your Docker image.
