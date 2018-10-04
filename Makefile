ME2 := me2/a2uUg_0_0.m \
       me2/a2uUg_0_1.m \
       me2/a2uUgg_0_0.m \
       me2/a2uUuU_0_0.m \
       me2/a2uUggg_0_0.m \
       me2/a2uUuUg_0_0.m \
       me2/a2uUuUg_0_0_1_1.m \
       \
       me2/g2ggg_0_0.m \
       me2/g2gg_0_0.m \
       me2/gg2g_0_0.m \
       me2/gg2gg_0_0.m \
       me2/gg2ggg_0_0.m \
       me2/gg2gggg_0_0.m \
       me2/uU2uU_0_0.m \
       me2/uU2uUuU_0_0.m \
       me2/uU2uUgg_0_0.m \
       me2/uU2uUuU_0_0_1_4.m \
       me2/uU2gg_0_0.m

all: $(ME2)

clean: amp-clean me2-clean

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

amp-clean:
	@rm -fv amp/*.h amp/*.log

amp/%_l.h:
	@echo "make $@"
	@./src/drqgraf -v --form -o $@ $*

amp/%_r.h:
	@echo "make $@"
	@./src/drqgraf -v -x --form -o $@ $*

.PRECIOUS: amp/%_l.h amp/%_r.h

###########################################################
#
#              II. SQUARED MATRIX ELEMENTS
#
###########################################################
define ME2_SCM
(define (me2-form-args filename)
  (define (make-arg name val)
	(string-join (list "-d " name "=" val) ""))

  (define (arg-amp name id n)
    (make-arg name (string-join (list "amp/" id n ".h") "")))

  (define (arg-set name str)
    (make-arg name (string-join (string-split str #\+) ",")))

  (define (join . args) (string-join args " "))

  (let* ((input (string-split (string-drop-right filename 2) #\_))
		 (arg (lambda (n) (list-ref input n)))
		 (amp (arg 0))
         (len (length input)))
	(cond ((= len 3)
           (join
             (arg-amp "AMP" amp (arg 1))
             (arg-amp "AMPx" amp (arg 2))
             ""
             ""
             ))
          ((= len 4)
           (join
             (arg-amp "AMP" amp (arg 1))
             (arg-amp "AMPx" amp (arg 2))
             (arg-set "SET" (arg 3))
             (arg-set "SETx" (arg 3))))
          ((= len 5)
           (join
             (arg-amp "AMP" amp (arg 1))
             (arg-amp "AMPx" amp (arg 2))
             (arg-set "SET" (arg 3))
             (arg-set "SETx" (arg 4))))
           (#t 'none))))
endef
$(guile $(ME2_SCM))

TMPDIR ?= /tmp

FORM = tform -w2 -M -t "${TMPDIR}" -ts "${TMPDIR}" -p src -I src -l -f -q

.SECONDEXPANSION:

me2/%.m: $$(guile (me2-prerequisite "$$(notdir $$@)"))
	@echo "make $@"
	@mkdir -p me2
	./src/me4qcd.py $^ $@		

me2-clean:
	@rm -fv me2/*.m

.PRECIOUS: me2/%.m

me2-all: $(ME2)

amp-all: $(AMP)

###########################################################
#
#                      III. TESTS
#
###########################################################
CHECK := check_uU2uU_0_0 \
         check_a2uU_0_0 \
         check_a2dD_0_0 \
         check_a2uUg_0_0 \
         check_uU2uUg_0_0_1 \
         check_a2uUgg_0_0_1 \
         check_a2uUgg_0_0_1+3 \
         check_a2uUgg_0_0_3 \
         check_a2uUuU_0_0_1 \
         check_a2uUuU_0_0_1+2 \
         check_a2uUuU_0_0_1+3 \
         check_a2uUuU_0_0_2 \
         check_a2uUuUg_0_0_1 \
         check_a2uUuUg_0_0_1_9 \
         check_a2uUuUg_0_0_9 \
         check_a2uUgg_0_0 \
         check_a2uUdD_0_0 \
         check_a2uUuU_0_0 \
         check_g2uU_0_0 \
         check_g2gg_0_0 \
         check_g2ggg_0_0 \
         check_gg2g_0_0 \
         check_gg2gg_0_0 \
         check_gg2uU_0_0 \
         check_gg2ggg_0_0 \
         check_uU2gg_0_0 \
         check_uu2uu_0_0 \
         check_uU2dD_0_0

check: $(CHECK)

$(CHECK): check_%: me2/%.m test/%.m phony
	@echo "$@"
	@math -script ./src/check.m $* me2/$*.m test/$*.m

test/%.m: src/testgen.m
	@echo "make '$@'"
	@math -script ./src/testgen.m $* $@

.PRECIOUS: test/%.m

phony:;
