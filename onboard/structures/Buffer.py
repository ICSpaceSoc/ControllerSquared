from datetime import datetime
from typing import Union
import numpy as np
from sys import maxsize

_DEF_DTYPE = [('value', np.float64), ('corr_value', np.float64), ('timestamp', datetime)]

class Buffer:
    """
    Circular buffer which stores sensor readings in a NumPy structured array.
    """

    def __init__(self, max_size: int, dtype: list[tuple[str, type]] = _DEF_DTYPE):
        """Initialises a circular buffer using a NumPy structured array.

        Args:
            max_size (int): Maximum number of readings to store.
            dtype: (list[tuple[str, type]], optional): Data type of the readings. Defaults to _DEF_DTYPE.
        """
        if max_size <= 0:
            raise ValueError('Buffer size must be positive')
        
        self._dtype = dtype
        self._fields = list(map(lambda type: type[0], self._dtype))
        self._types = tuple(map(lambda type: type[1], self._dtype))
        self._buffer = np.zeros(max_size, dtype = self._dtype)
        self._max_size = max_size
        self._index = 0
        self._size = 0

    def __iadd__(self, other: tuple) -> 'Buffer':
        """Overloads the `+=` operator to add a reading to the buffer.

        Args:
            other (tuple): A reading to add to the buffer.

        Returns:
            Buffer: The buffer itself.
        """
        self._buffer[self._index] = other
        self._index = (self._index + 1) % self._max_size
        self._size = min(self._size + 1, self._max_size)
        return self

    def __getitem__(
            self, 
            key: Union[int, slice, str, tuple[slice, str]], 
        ) -> Union[np.void, np.ndarray]:
        """Returns a reading or a selection of readings from the buffer based on the given key.

        Args:
            key (Union[int, slice, str, tuple[slice, str]]):
                int -> Returns the index offset from the current index.
                slice -> Returns a selection based on the slice, offset from the current index.
                str -> Returns the field from the buffer, oldest to newest.
                tuple[slice, str] -> Returns a selection based on the slice, filtered by the field.

        Raises:
            IndexError: The index or slice range is out of bounds, or invalid.
            ValueError: The field provided is not valid.

        Returns:
            Union[np.void, np.ndarray]: A single reading or a selection of readings.
        """
        
        if isinstance(key, int):
            if (key >= self._size) or (key < -self._size):
                raise IndexError("Index out of bounds.")

            return self._buffer[(self._index + key) % self._max_size]
        
        if isinstance(key, tuple) and len(key) == 2 and isinstance(key[1], str):
            field = key[1]
            if field not in self._fields:
                    raise ValueError(f"Field '{field}' does not exist in the buffer.")

            if isinstance(key[0], slice):
                start, stop = key[0].start, key[0].stop
                return self._buffer[
                    (start is None or self._buffer[field] >= start) &\
                    (stop is None or self._buffer[field] < stop)
                ]
            
            if isinstance(key[0], self._types):
                return self._buffer[self._buffer[field] == key[0]]
            
            raise ValueError(f"Invalid slice type '{type(key[0])}' for field '{field}'.")
        
        if isinstance(key, slice):
            start, stop, step = key.indices(self._max_size)
            return np.array([self._buffer[(self._index + i) % self._max_size] for i in range(start, stop, step)])
        
        if isinstance(key, str):
            if key not in self._fields:
                raise ValueError(f"Field '{key}' does not exist in the buffer.")
            return np.roll(self._buffer[key], -self._index)

        raise IndexError("Key must be an int, slice, string, or a field-filtered slice.")
    
    def __str__(self) -> str:
        """
        Returns a string representation of the data in the buffer, formatted in a table-like style.

        Returns:
            str: A string representation of the buffer data.
        """

        column_widths = {name: max(len(name), max(len(str(row[name])) for row in self._buffer)) for name in self._fields}
        header = " | ".join(name.ljust(column_widths[name]) for name in self._fields)
        separator = "-+-".join("-" * column_widths[name] for name in self._fields)

        rows = []
        for row in self._buffer:
            formatted_row = " | ".join(str(row[name]).ljust(column_widths[name]) for name in self._fields)
            rows.append(formatted_row)

        data_str = "\n".join([header, separator] + rows)
        return data_str + f"\nIndex: {self._index}\nSize: {self._size}\nMax Size: {self._max_size}"
