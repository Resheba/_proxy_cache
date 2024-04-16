import pytest

from src.core.paginator import PaginatorPage


def test_paginator_page():
    paginator_page = PaginatorPage(page_size=10, page_num=1)
    assert paginator_page.page_size == 10
    assert paginator_page.page_num == 1