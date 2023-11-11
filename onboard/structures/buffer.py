from typing import Union
import numpy as np


class Buffer:
    """
    Circular buffer which stores sensor readings in a NumPy structured array.
    """

    def __init__(self, max_size: int):
        """Initialises a circular buffer using a NumPy structured array.

        Args:
            max_size (int): Maximum number of readings to store.
        """
        if max_size <= 0:
            # TODO: Integrate with overall logging system
            raise ValueError('Buffer size must be positive')
        self._buffer = np.zeros(
            max_size,
            dtype=[('value', np.float64), ('sValue', np.float64), ('timestamp', np.float64)]
        )
        self._max_size = max_size
        self._index = 0
        self._size = 0

    def __iadd__(self, other: tuple) -> 'Buffer':
        """Overloads the `+=` operator to add a reading to the buffer.

        Args:
            other (tuple): A reading to add to the buffer.

        Raises:
            ValueError: If `other` is not a compatible type, a ValueError is
                raised.

        Returns:
            Buffer: The buffer itself.
        """
        if not isinstance(other, tuple):
            # TODO: Integrate with overall logging system
            raise ValueError("Invalid argument type.")

        self._buffer[self._index] = other
        self._index = (self._index + 1) % self._max_size
        self._size = min(self._size + 1, self._max_size)
        return self

    def __getitem__(self, key: Union[int, slice], field: str = 'timestamp') -> Union[np.void, np.ndarray]:
        """Returns a reading or a selection of readings from the buffer.

        Args:
            key (Union[int, slice]): 
                int -> Index of the reading to return. 
                    Positive values are interpreted as direct references to
                    the buffer.
                    Negative values are allowed, and are interpreted as the
                    most recent values. E.g., [-1] returns the most recent
                    reading.
                slice -> 
                    Returns a selection of readings from the buffer.  The 
                    slice is interpreted as a range of a particular field, 
                    defaulting to 'timestamp'. The range is inclusive of the 
                    start and end values. E.g., [10:20] returns all readings 
                    with 'timestamp' between 10 and 20, inclusive, and 
                    [10:, 'value'] returns all readings with 'value' between 
                    10 and infinity, inclusive.
            field (str, optional): In case of a slice, determines which field
                to filter for return data by. Defaults to 'timestamp'.

        Raises:
            ValueError:
                key: slice, field -> If the field is not a valid field in the
                    buffer's dtype, a ValueError is raised.
            IndexError: 
                key: int -> Values which are out of range in either direction
                    will raise an IndexError.
            TypeError: An invalid key type will raise a TypeError.

        Returns:
            Union[np.void, np.ndarray]: A single reading or a selection of
                readings from the buffer.
        """
        if isinstance(key, slice):
            if not self._buffer.dtype.names or field not in self._buffer.dtype.names:
                # TODO: Integrate with overall logging system
                raise ValueError(f"Invalid field: {field}")

            start, stop = key.start, key.stop

            # NOTE: This trick depends on all values being numerical.
            if start is None:
                start = float('-inf')
            if stop is None:
                stop = float('inf')

            return self._buffer[(self._buffer[field] >= start) & (self._buffer[field] <= stop)]

        if isinstance(key, int):
            if abs(key) > self._size:
                # TODO: Integrate with overall logging system
                raise IndexError("Index out of range")

            acc_index = (self._index + key) % self._max_size if key < 0 else key
            return self._buffer[acc_index]

        # TODO: Integrate with overall logging system
        raise TypeError("Invalid argument type.")
    