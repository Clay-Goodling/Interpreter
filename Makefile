build:
	mkdir -p _$f
	# cp templates/template.mli _$f/$f.mli
	cp templates/builtin.ml _$f
	cp templates/.merlin _$f
	sed 's/fname/$f/g;s/Fname/$(shell f=$(f); echo $${f^})/g' templates/main.ml > _$f/main.ml
	sed 's/fname/$f/g;s/Fname/$(shell f=$(f); echo $${f^})/g' templates/Makefile > _$f/Makefile
	./module_gen.py $f
	make -C _$f $f
	mv _$f/$f .

clean:
	rm -r $f _$f