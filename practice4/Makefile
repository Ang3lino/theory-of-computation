
FILE = main

main: $(FILE).py
	python $(FILE).py
git: $(FILE).py
	git add $(FILE).py; git commit -m "v:"; git push
debug: $(FILE).py
	python -m pdb $(FILE).py
