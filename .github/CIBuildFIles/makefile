# Makefile for pyRogue

# Variables
SRC_DIR := ../../src
UTILITIES_DIR := $(SRC_DIR)/utilities
MODULES_DIR := $(SRC_DIR)/modules
MAIN_FILE := $(SRC_DIR)/main.py
BUILD_DIR := build
DIST_DIR := dist

# List of added files with their respective directories
ADDED_FILES := $(UTILITIES_DIR)/*.py:utilities $(MODULES_DIR)/*.py:modules

# Build target
build:
    @echo "Building pyRogue..."
    @kivy_pyinstaller -F --name pyRogue --windowed --icon icon.ico --add-data "$(ADDED_FILES)" $(MAIN_FILE)
    @echo "Build completed. Find the executable in $(DIST_DIR)"
    @echo "Modifying permissions..."
    @echo "{\"app_name\": \"pyRogue\", \"permissions\": [\"INTERNET\", \"KEYBOARD\"]}" > $(DIST_DIR)/kivy_permissions.json
    @echo "Permissions set."

# Clean target
clean:
    @echo "Cleaning up..."
    @rm -rf $(BUILD_DIR) $(DIST_DIR)
    @echo "Cleanup completed."
