.DEFAULT: small_talk

install:
	@pip install -r requirements.txt

small_talk:
	@python littlebrain.py

.PHONY: install small_talk