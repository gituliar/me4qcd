# Three-point functions
CHECK3 = check_a2uU_0_0 \
         check_a2dD_0_0 \
         check_g2gg_0_0 \
         check_g2uU_0_0

# Four-point functions
CHECK4 = check_a2uUg_0_0 \
         check_g2ggg_0_0 \
         check_g2uUg_0_0 \
         check_gg2gg_0_0 \
         check_gg2uU_0_0 \
         check_gu2ug_0_0 \
         check_gU2gU_0_0 \
         check_ug2ug_0_0 \
         check_uu2uu_0_0 \
         check_uU2gg_0_0 \
         check_uU2uU_0_0 \
         check_uU2dD_0_0 \
         check_ud2ud_0_0

# Five-point functions
CHECK5 = check_a2uUgg_0_0 \
         check_a2uUuU_0_0 \
         check_a2uUdD_0_0 \
         check_g2uUgg_0_0 \
         check_gg2ggg_0_0 \
         check_ug2ugg_0_0 \
         check_uu2uug_0_0 \
         check_uU2uUg_0_0

CHECK6 = check_a2uUuUg_0_0 \
         check_a2uUggg_0_0 \
         check_a2uUdDg_0_0


help:
	@echo "Usage: make check_<process>"

clean: clean-me2

ifneq "$(filter guile,$(.FEATURES))" "guile"
    $(error This Makefile requires GNU make with Guile support)
endif

###########################################################
#
#                    I. AMPLITUDES
#
###########################################################
define AMP_SCM
(use-modules (ice-9 format))
(use-modules (ice-9 receive))
(use-modules (ice-9 regex))
(use-modules (srfi srfi-1))
(define (me2-prerequisite filename)

  (let* ((input (string-split (string-drop-right filename 2) #\_))
         (arg (lambda (n) (list-ref input n))))
    (list
      (string-join (list "amp/" (arg 0) "_" (arg 1) "_l.h") "")
      (string-join (list "amp/" (arg 0) "_" (arg 2) "_r.h") ""))))
endef
$(guile $(AMP_SCM))

amp/%_l.h:
	@echo "make $@"
	@./src/qgraf.py -v --form -o $@ $*

amp/%_r.h:
	@echo "make $@"
	@./src/qgraf.py -v -x --form -o $@ $*

clean-amp:
	@rm -fv amp/*.h amp/*.log

.PRECIOUS: amp/%_l.h amp/%_r.h

###########################################################
#                                                         #
#              II. SQUARED MATRIX ELEMENTS                #
#                                                         #
###########################################################
.SECONDEXPANSION:

me2/%.m: me2/%.m.gz
	@echo "make $@"
	@gunzip -k $<

me2/%.m.gz: $$(guile (me2-prerequisite "$$(notdir $$(subst .gz,,$$@))"))
	@echo "make $@"
	@mkdir -p me2
	@./src/me4qcd.py $^ $(subst .gz,,$@)
	@gzip $(subst .gz,,$@)

.PRECIOUS: me2/%.m me2/%.m.gz

###########################################################
#                                                         #
#                      III. TESTS                         #
#                                                         #
###########################################################
CHECK := $(CHECK3) $(CHECK4) $(CHECK5) $(CHECK6)

check-3: $(CHECK3)
check-4: $(CHECK4)
check-5: $(CHECK5)
check-6: $(CHECK6)
check-all: $(CHECK)

check_%: me2/%.m test/%.m phony
	@echo "$@"
	@math -script ./src/check.m $* me2/$*.m test/$*.m

test/%.m: src/testgen.m
	@echo "make '$@'"
	@math -script ./src/testgen.m $* $@

KEEP_M  := $(patsubst check_%,me2/%.m,$(CHECK3) $(CHECK4))
KEEP_GZ := $(patsubst check_%,me2/%.m.gz,$(CHECK5) $(CHECK6))

clean-me2:
	@rm -vf $(filter-out $(KEEP_M) $(KEEP_GZ),$(wildcard me2/*))

.PRECIOUS: test/%.m $(KEEP_M) $(KEEP_GZ)

phony:;
