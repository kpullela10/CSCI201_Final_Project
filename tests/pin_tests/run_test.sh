#!/bin/bash

# USC Squirrel Tracker API Test Runner
# This script helps run the API tests with various options

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}==================================${NC}"
echo -e "${BLUE}USC Squirrel Tracker API Tests${NC}"
echo -e "${BLUE}==================================${NC}"
echo

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo -e "${RED}Error: pytest is not installed${NC}"
    echo "Please run: pip install -r requirements.txt"
    exit 1
fi

# Check if backend is running
echo -e "${BLUE}Checking if backend is running...${NC}"
if ! curl -s http://localhost:8080/api/health > /dev/null 2>&1; then
    echo -e "${RED}Warning: Backend might not be running on http://localhost:8080${NC}"
    echo "Make sure your Spring Boot application is started"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Parse command line arguments
case "$1" in
    "all")
        echo -e "${GREEN}Running all pin tests...${NC}"
        pytest test_pin_operations.py -v
        ;;
    "quick")
        echo -e "${GREEN}Running quick tests (no daily limit test)...${NC}"
        pytest test_pin_operations.py -v -k "not beyond_daily_limit"
        ;;
    "creation")
        echo -e "${GREEN}Running pin creation tests...${NC}"
        pytest test_pin_operations.py -v -k "create"
        ;;
    "retrieval")
        echo -e "${GREEN}Running pin retrieval tests...${NC}"
        pytest test_pin_operations.py -v -k "get"
        ;;
    "validation")
        echo -e "${GREEN}Running validation tests...${NC}"
        pytest test_pin_operations.py -v -k "missing or long"
        ;;
    "report")
        echo -e "${GREEN}Running tests and generating HTML report...${NC}"
        pytest test_pin_operations.py -v --html=report.html --self-contained-html
        echo -e "${GREEN}Report generated: report.html${NC}"
        ;;
    "coverage")
        echo -e "${GREEN}Running tests with coverage...${NC}"
        pytest test_pin_operations.py --cov=. --cov-report=html --cov-report=term
        echo -e "${GREEN}Coverage report generated in htmlcov/ directory${NC}"
        ;;
    "single")
        if [ -z "$2" ]; then
            echo -e "${RED}Error: Please specify test name${NC}"
            echo "Example: ./run_tests.sh single test_create_pin_successfully"
            exit 1
        fi
        echo -e "${GREEN}Running single test: $2${NC}"
        pytest test_pin_operations.py::TestPinCreationRetrieval::$2 -v -s
        ;;
    "help"|"-h"|"--help")
        echo "Usage: ./run_tests.sh [option]"
        echo
        echo "Options:"
        echo "  all         - Run all pin tests (default)"
        echo "  quick       - Run all tests except slow ones (daily limit test)"
        echo "  creation    - Run only pin creation tests"
        echo "  retrieval   - Run only pin retrieval tests"
        echo "  validation  - Run only validation tests"
        echo "  report      - Run tests and generate HTML report"
        echo "  coverage    - Run tests with coverage analysis"
        echo "  single NAME - Run a single test by name"
        echo "  help        - Show this help message"
        echo
        echo "Examples:"
        echo "  ./run_tests.sh all"
        echo "  ./run_tests.sh quick"
        echo "  ./run_tests.sh single test_create_pin_successfully"
        ;;
    *)
        echo -e "${GREEN}Running all pin tests (default)...${NC}"
        pytest test_pin_operations.py -v
        ;;
esac

echo
echo -e "${BLUE}==================================${NC}"
echo -e "${BLUE}Test run complete!${NC}"
echo -e "${BLUE}==================================${NC}"