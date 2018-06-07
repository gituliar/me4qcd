ME2 := me2/a2uUg_0_0.m \
       me2/a2uUgg_0_0.m \
       me2/a2uUuU_0_0.m \
       me2/a2uUggg_0_0.m \
       me2/a2uUuUg_0_0.m \
       me2/a2uUuUg_0_0_1_1.m \
       \
       me2/gg2gg_0_0.m \
       me2/g2ggg_0_0.m \
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
      (string-join (list "amp/" (arg 0) (arg 1) ".h") "")
      (string-join (list "amp/" (arg 0) (arg 2) ".h") ""))))

(define (parse-amplitude-id amplitude)
  (let* ((m (string-match "([auUdDg]+)2([auUdDg]+)([0-9]+)" amplitude))
         (in (string->list (match:substring m 1)))
         (out (string->list (match:substring m 2)))
         (loops (string->number (match:substring m 3))))
    (values in out loops)))

(define (format-qgraf.dat amplitude)
  (define (format-momenta tag particles momentum-prefix momentum-1)
    (if (equal? (length particles) 1)
      (format #t "~a= ~c[~a] ;\n\n" tag (list-ref particles 0) momentum-1)
      (format #t "~a= ~a ;\n\n"
        tag
        (string-join
          (map
            (lambda (p i)
              (format #f "~c[~a~d]" p momentum-prefix i))
            particles
            (iota (length particles) 1))
          ", "))))
  (receive (in out loops) (parse-amplitude-id amplitude)
    (format #t "output= 'amp/~a.h' ;\n\n" amplitude)
    (format #t "style= 'src/form.sty' ;\n\n")
    (format #t "model= 'src/qcd.mod' ;\n\n")
    (format-momenta "in" in "p" "q")
    (format-momenta "out" out "k" "k")
    (format #t "loops= ~d ;\n\n" loops)
    (format #t "loop_momentum= l ;\n\n")
    (format #t "options= ;\n\n")))

(define (save-qgraf.dat amplitude filename)
  (with-output-to-file filename
    (lambda () (format-qgraf.dat amplitude))))
endef
$(guile $(AMP_SCM))

amp-clean:
	@rm -fv amp/*.h amp/*.log amp/*.dat

amp/%.dat:
	@echo "make $@"
	@$(guile (mkdir "amp"))
	@$(guile (save-qgraf.dat "$*" "$@"))

AMP=$(sort $(guile (map me2-prerequisite (string-split "$(notdir $(ME2))" \#\space))))

$(AMP): amp/%.h: amp/%.dat src/qcd.mod src/form.sty
	@echo "make $@"
	mkdir -p amp
	@rm -f "$@"
	@ln -s "amp/$*.dat" qgraf.dat
	@qgraf | tee  $(@:.h=.log)
	@rm qgraf.dat

.PRECIOUS: amp/%.dat amp/%.h

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

me2/%.m: src/me2.frm src/me4qcd.h $$(guile (me2-prerequisite "$$(notdir $$@)"))
	@echo "make $@"
	@mkdir -p me2
	$(FORM) $(guile (me2-form-args "$(notdir $@)")) -d ME2=$@ src/me2.frm

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
         check_a2uUuU_0_0 \
         check_g2ggg_0_0 \
         check_gg2gg_0_0 \
         check_gg2ggg_0_0 \
         check_uU2gg_0_0

check: $(CHECK)

$(CHECK): check_%: me2/%.m test/%.m phony
	@echo "$@"
	@math -script ./src/check.m $* me2/$*.m test/$*.m

test/%.m: src/testgen.m
	@echo "make '$@'"
	@math -script ./src/testgen.m $* $@

.PRECIOUS: test/%.m

phony:;
