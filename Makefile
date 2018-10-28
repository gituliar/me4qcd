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

check-3: $(CHECK3)
check-4: $(CHECK4)
check-5: $(CHECK5)
check-all: $(CHECK3) $(CHECK4) $(CHECK5)


help:
	@echo "Usage: make check_<process>"

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

(define (basename2 path)
  (car (string-split (basename path) #\.)))

(define (me4qcd-init-amps path)
  (let* ((process (basename2 path))
         (input (string-split process #\_))
         (arg (lambda (n) (list-ref input n))))
    (list
      (string-join (list "amp/" (arg 1) "_" (arg 2) "_l.h") "")
      (string-join (list "amp/" (arg 1) "_" (arg 3) "_r.h") ""))))


(define (get-args target)
  (let ((n (string-index target #\_)))
    (list
      (substring target 0 n)
      (substring target (+ n 1) (string-length target)))))

(define (command target)
  (car (get-args target)))

(define (process target)
  (cadr (get-args target)))


(define (me4qcd-args target in-suf out-suf)
  (let* ((n (string-index target #\_))
         (command (substring target 0 n))
         (process (substring target (+ n 1) (string-length target))))
    (list
      command
      (string-join (list "me2/" process in-suf) "")
      (string-join (list "me2/" process  out-suf) ""))))
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

# ======================================================= #
#                Main Calculation Steps                   #
# ======================================================= #
all_%: init_% sort_% col_% den_% num_%
	@echo "make '$@'"

me2/%.m: me2/%.h
	@echo "make '$@'"
	@./src/me4qcd.py frm2math $< $@
.PRECIOUS: me2/%.m

me2/%.h: all_% collect_%
	@echo "make '$@'"

init_%: $$(guile (me4qcd-init-amps "$$@")) phony
	@echo "make '$@'"
	@./src/me4qcd.py init $(wordlist 1,2,$^) me2/$(guile (process "$@")).raw

sort_%: phony
	@./src/me4qcd.py $(guile (me4qcd-args "$@" ".raw" ".sort"))

col_%: phony
	@echo "make '$@'"
	@./src/me4qcd.py $(guile (me4qcd-args "$@" ".sort" ""))

num_%: phony
	@echo "make '$@'"
	@./src/me4qcd.py $(guile (me4qcd-args "$@" ".sort" ""))

den_%: phony
	@echo "make '$@'"
	@cp -n me2/$(guile (process "$@")).sort/*.den.h me2/$(guile (process "$@")) 2> /dev/null | true

collect_%: phony
	@echo "make '$@'"
	@./src/me4qcd.py $(guile (me4qcd-args "$@" "" ".h"))

clean_%: phony
	@echo "make '$@'"
	@rm -r me2/$(guile (process "$@"))*

.PRECIOUS: me2/%.m me2/%.m.gz

###########################################################
#                                                         #
#                      III. TESTS                         #
#                                                         #
###########################################################
CHECK := $(CHECK3) $(CHECK4) $(CHECK5)

check_%: me2/%.m test/%.m phony
	@echo "$@"
	@math -script ./src/check.m $* me2/$*.m test/$*.m

test/%.m: src/testgen.m
	@echo "make '$@'"
	@math -script ./src/testgen.m $* $@

.PRECIOUS: test/%.m

phony:;
