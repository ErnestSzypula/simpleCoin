from enum import Enum


class RequestType(Enum):
    updateHash = 1
    transactionRequest = 2
    transactionCompleted = 3
    checkout = 4
    validateBlockchain = 5
    createCoin = 6
    proposedBlock = 7
