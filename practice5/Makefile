
FILE = main

main: $(FILE).py
	python3 $(FILE).py
git: $(FILE).py
	git add $(FILE).py; git commit -m "v:"; git push
debug: $(FILE).py
	python3 -m pdb $(FILE).py
