#!/bin/bash

echo "Running black..."
black --check asyncio_tools.py

echo "Running flake8..."
flake8 asyncio_tools.py
