from structures.Buffer import Buffer
import numpy as np
from random import randint
from timeit import timeit
from typing import Any
import unittest

class BufferTests(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

        self.buffer = Buffer(
            10, 
            [
                ('value', np.float64), 
                ('corr_value', np.float64), 
                ('timestamp', np.float64)
            ]
        )

        for i in range(15):
            self.buffer += (i, i, 10 * i)
    
    @staticmethod
    def to_tuple(record: Any) -> tuple:
        return tuple(record[field] for field in record.dtype.names)

    def test_add(self):
        """Tests minimum buffer functionality."""
        self.assertEqual(self.buffer._index, 5, "Current index is incorrect.")
        self.assertEqual(self.buffer._size, 10, "Current size is incorrect.")
    
    def test_get_pos_index(self):
        """Tests getting data from the buffer using positive indices."""
        self.assertTrue(
            self.to_tuple(self.buffer[0]) == (5, 5, 50), 
            "Oldest element is incorrect."
        )
        self.assertTrue(
            self.to_tuple(self.buffer[1]) == (6, 6, 60), 
            "Second oldest element is incorrect."
        )
    
    def test_get_neg_index(self):
        """Tests getting data from the buffer using negative indices."""
        self.assertEqual(
            self.to_tuple(self.buffer[-1]), 
            (14, 14, 140), 
            "Most recent element is incorrect."
        )
        self.assertEqual(
            self.to_tuple(self.buffer[-2]), 
            (13, 13, 130),
            "Second most recent element is incorrect."
        )
    
    def test_get_pos_slice(self):
        """Tests getting data from the buffer using positive slices."""
        self.assertEqual(
            [self.to_tuple(record) for record in self.buffer[1:4]], 
            [(6, 6, 60), (7, 7, 70), (8, 8, 80)],
            "Positive slice with endpoints is incorrect."
        )

        self.assertEqual(
            [self.to_tuple(record) for record in self.buffer[:]], 
            [
                (5, 5, 50), (6, 6, 60), (7, 7, 70), (8, 8, 80), (9, 9, 90),
                (10, 10, 100), (11, 11, 110), (12, 12, 120), (13, 13, 130), (14, 14, 140)
            ],
            "Positive slice without endpoints is incorrect."
        )
    
    def test_get_neg_slice(self):
        """Tests getting data from the buffer using negative slices."""
        self.assertEqual(
            [self.to_tuple(record) for record in self.buffer[-3:]], 
            [(12, 12, 120), (13, 13, 130), (14, 14, 140)],
            "Negative slice withonly LHS endpoint is incorrect."
        )

        self.assertEqual(
            [self.to_tuple(record) for record in self.buffer[:-3]],
            [
                (5, 5, 50), (6, 6, 60), (7, 7, 70), (8, 8, 80),
                (9, 9, 90), (10, 10, 100), (11, 11, 110)
            ],
            "Negative slice with only RHS endpoint is incorrect."
        )
    
    def test_get_field(self):
        """Tests getting data from the buffer using a field."""
        self.assertEqual(
            self.buffer["value"].tolist(), 
            list(range(5, 15)),
            "Get by field is incorrect."
        )
    
    def test_get_filtered_slice(self):
        """Tests getting data from the buffer using a field-filtered slice."""
        self.assertEqual(
            self.buffer[6:8, "value"].tolist(),
            [(6, 6, 60), (7, 7, 70)],
            "Get by field-filtered slice is incorrect."
        )
    
    def test_get_nonint_filtered_slice(self):
        """Tests getting data from the buffer using a non-integer field-filtered slice."""
        self.assertEqual(
            self.buffer[6.5:8.5, "value"].tolist(),
            [(7, 7, 70), (8, 8, 80)],
            "Get by non-integer field-filtered slice is incorrect."
        )

class BufferPerfTests(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

        self._size = 1000
        self._num_ops = 500 * 12 * 2
        self._max_time = 1

        self.buffer = Buffer(
            self._size, 
            [
                ('value', np.float64), 
                ('corr_value', np.float64), 
                ('timestamp', np.float64)
            ]
        )

        for i in range(self._num_ops):
            self.buffer += (i, i, 10 * i)

    @staticmethod 
    def fill_buffer(buffer: Buffer, num_ops: int):
        for i in range(num_ops):
            buffer += (i, i, 10 * i)

    def test_add_perf(self):
        time_taken = timeit(lambda: self.fill_buffer(self.buffer, self._num_ops), number=1)
        print(f"Adding {self._num_ops} elements: {time_taken}")
        # self.assertLess(time_taken, self._max_time, "Adding elements is too slow")

    def test_read_single_perf(self):
        self.fill_buffer(self.buffer, self._num_ops)

        def read_single_elements():
            for i in range(self._num_ops):
                _ = self.buffer[randint(0, self._size - 1)]

        time_taken = timeit(read_single_elements, number=1)
        print(f"Reading {self._num_ops} random elements: {time_taken}")
        # self.assertLess(time_taken, self._max_time, "Reading single elements is too slow")
    
    def test_read_slice_perf(self):
        self.fill_buffer(self.buffer, self._num_ops)

        def read_slice_elements():
            for _ in range(self._num_ops // 12):
                _ = self.buffer[:randint(0, self._size - 1)]
        
        time_taken = timeit(read_slice_elements, number=1)
        print(f"Reading {self._num_ops} random slices: {time_taken}")
        # self.assertLess(time_taken, self._max_time, "Reading slices is too slow")
    
    def test_read_field_perf(self):
        self.fill_buffer(self.buffer, self._num_ops)

        def read_field_elements():
            for _ in range(self._num_ops):
                _ = self.buffer["value"]

        time_taken = timeit(read_field_elements, number=1)
        print(f"Reading {self._num_ops} single elements: {time_taken}")
        # self.assertLess(time_taken, self._max_time, "Reading fields is too slow")
