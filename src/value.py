import json
from dataclasses import dataclass
from copy import deepcopy


@dataclass
class Value:
    inner: dict[str, dict[str, int]]

    def __str__(self):
        return json.dumps(self.inner, indent=4)

    def __eq__(self, other):
        if not isinstance(other, Value):
            return NotImplemented
        return self.inner == other.inner

    def __add__(self, other):
        if not isinstance(other, Value):
            return NotImplemented

        # Use deepcopy to avoid modifying the original instance
        result = deepcopy(self.inner)

        for policy, assets in other.inner.items():
            if policy in result:
                for asset, quantity in assets.items():
                    result[policy][asset] = result[policy].get(asset, 0) + quantity
            else:
                result[policy] = deepcopy(assets)

        output = Value(result)
        output._remove_zero_entries()

        return output

    def __sub__(self, other):
        if not isinstance(other, Value):
            return NotImplemented

        # Use deepcopy to avoid modifying the original instance
        result = deepcopy(self.inner)

        for policy, assets in other.inner.items():
            if policy in result:
                for asset, quantity in assets.items():
                    result[policy][asset] = result[policy].get(asset, 0) - quantity
            else:
                # we are subtracting from zero so it would be negative
                result[policy] = {asset: -quantity for asset, quantity in assets.items()}

        # Create the result Value object and remove zero entries
        output = Value(result)
        output._remove_zero_entries()

        return output

    def __mul__(self, scale):
        if not isinstance(scale, int):
            return NotImplemented
        if scale == 0:
            return Value({})
        new_inner = {}
        for policy, assets in self.inner.items():
            new_assets = {asset: quantity * scale for asset, quantity in assets.items()}
            new_inner[policy] = new_assets
        return Value(new_inner)

    def __rmul__(self, other):
        return self.__mul__(other)

    def quantity_of(self, policy, asset):
        """
        Get the quantity of a policy id and asset name from self.
        """
        if not isinstance(policy, str):
            return NotImplemented
        if not isinstance(asset, str):
            return NotImplemented
        try:
            return self.inner[policy][asset]
        except KeyError:
            return 0

    def negate(self):
        """
        All quantities in self are multiplied by -1.
        """
        for policy, assets in self.inner.items():
            for asset, quantity in assets.items():
                self.inner[policy][asset] = -1 * quantity

    def _remove_zero_entries(self):
        """
        Removes zero entries from self.
        """
        inner_copy = self.inner.copy()  # create a copy so we can delete
        for policy, assets in inner_copy.items():
            assets_to_remove = [asset for asset, amount in assets.items() if amount == 0]
            for asset in assets_to_remove:
                del self.inner[policy][asset]
            if self.inner[policy] == {}:
                del self.inner[policy]
