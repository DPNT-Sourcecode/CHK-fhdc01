import json

class CheckoutSolution:

    # skus = unicode string
    def checkout(self, skus):
        prices = None
        with open("lib/solutions/CHK/prices.json") as f:
            prices = json.load(f)
        raise NotImplementedError()
