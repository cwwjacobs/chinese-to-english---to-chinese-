PYTHON ?= python3
PACKAGE_VERSION ?= v0.3.0-rc1-terminus
PACKAGE_NAME := cli-translation-overlay
PACKAGE_ZIP := dist/$(PACKAGE_NAME)-$(PACKAGE_VERSION).zip

.PHONY: clean validate test package receipt smudge

clean:
	rm -rf dist build __pycache__ scripts/__pycache__ tests/__pycache__ .pytest_cache
	rm -f /tmp/trans_fifo /tmp/op_trans_fifo

validate:
	$(PYTHON) -m py_compile translator.py
	$(PYTHON) -m py_compile overlay.py
	$(PYTHON) -m py_compile replay.py
	$(PYTHON) -m py_compile scripts/export_training_trace.py
	$(PYTHON) -m py_compile scripts/validate_package.py
	$(PYTHON) -m py_compile tests/test_bundle.py

test:
	cd tests && $(PYTHON) -m pytest test_bundle.py -v 2>&1 || $(PYTHON) -m unittest test_bundle -v

package:
	mkdir -p dist
	cd .. && zip -r cli-translation-overlay/$(PACKAGE_ZIP) cli-translation-overlay/ \
		-x "cli-translation-overlay/dist/*" \
		-x "cli-translation-overlay/__pycache__/*" \
		-x "cli-translation-overlay/.pytest_cache/*" \
		-x "cli-translation-overlay/.git/*" \
		-x "cli-translation-overlay/*.pyc" \
		-x "cli-translation-overlay/.*"
	@echo "Package: $(PACKAGE_ZIP)"

receipt:
	$(PYTHON) scripts/build_final_receipt.py --version $(PACKAGE_VERSION)

# Quick end-to-end smoke test: start overlay, pipe a test message
smudge:
	@echo "Starting overlay in background..."
	$(PYTHON) overlay.py &
	sleep 2
	echo '{"role":"operator","original":"你好","translation":"Hello"}' > /tmp/trans_fifo
	sleep 1
	@echo "Overlay should show 'Hello'. Press Ctrl+C to stop."
	wait
