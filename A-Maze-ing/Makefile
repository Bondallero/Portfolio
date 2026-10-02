VENV        = venv
PYTHON      = $(VENV)/bin/python3
PIP         = $(VENV)/bin/pip
FLAKE8      = $(VENV)/bin/flake8
MYPY        = $(VENV)/bin/mypy

SRC_DIR     = src
MAIN        = a_maze_ing.py
CONFIG      = config.txt
REQ_FILE    = requirements.txt
MLX_WHEEL   = mlx-2.2-py3-none-any.whl

export PYTHONPATH := $(SRC_DIR):$(PYTHONPATH)
export MYPYPATH := $(SRC_DIR):$(MYPYPATH)

.PHONY: all install run debug clean fclean re lint lint-strict

all: install run

install:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Creating virtual environment in $(VENV)..."; \
		python3 -m venv $(VENV); \
	fi
	@echo "Upgrading pip and installing tools..."
	@$(PIP) install --upgrade pip
	@$(PIP) install flake8 mypy
	@if [ -n "$(MLX_WHEEL)" ]; then \
		echo "Installing MLX wheel: $(MLX_WHEEL)..."; \
		$(PIP) install $(MLX_WHEEL); \
	fi
	@if [ -f "$(REQ_FILE)" ]; then \
		echo "Installing dependencies from $(REQ_FILE)..."; \
		$(PIP) install -r $(REQ_FILE); \
	fi

run:
	@if [ ! -f "$(PYTHON)" ]; then \
		echo "Error: Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	@if [ ! -f "$(PYTHON)" ]; then \
		echo "Error: Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

lint:
	@if [ ! -f "$(FLAKE8)" ] || [ ! -f "$(MYPY)" ]; then \
		echo "Error: Linters not installed in venv. Run 'make install' first."; \
		exit 1; \
	fi
	$(FLAKE8) .
	$(MYPY) --warn-return-any \
	        --warn-unused-ignores \
	        --ignore-missing-imports \
	        --disallow-untyped-defs \
	        --check-untyped-defs .

lint-strict:
	$(FLAKE8) .
	$(MYPY) --strict .

clean:
	@echo "Removing caches and temporary files..."
	rm -rf __pycache__ */__pycache__ */*/__pycache__
	rm -rf .mypy_cache .pytest_cache
	rm -rf dist build *.egg-info
	rm -f output_maze.txt

fclean: clean
	@echo "Removing virtual environment..."
	rm -rf $(VENV)

re: fclean all