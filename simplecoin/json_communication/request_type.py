from enum import Enum

class RequestType(Enum):
    updateHash = 1
    transactionRequest = 2
    transactionComplite = 3
    checkout = 4
    validateBlockchain = 5
    createCoint = 6