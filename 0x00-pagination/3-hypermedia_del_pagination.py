#!/usr/bin/env python3
"""Task 3: Deletion-resilient hypermedia pagination
"""

from typing import Dict

class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        dataset = self.dataset()
        total_items = len(dataset)

        if index is None:
            index = 0

        assert index >= 0 and index < total_items, f"Invalid index value: {index}"

        # Calculate next index
        next_index = min(index + page_size, total_items)

        # Get data for current page
        current_page = dataset[index:next_index]

        # Check if any rows were deleted between queries
        current_page_size = len(current_page)
        expected_page_size = min(page_size, total_items - index)

        if current_page_size < expected_page_size:
            # Some rows were deleted, get remaining rows
            remaining_rows = expected_page_size - current_page_size
            next_index = min(next_index + remaining_rows, total_items)
            current_page += dataset[next_index - remaining_rows:next_index]

        # Return page information
        return {
            "index": index,
            "next_index": next_index,
            "page_size": page_size,
            "data": current_page
        }
