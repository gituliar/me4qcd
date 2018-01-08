ME2 := me2/a2qqg_0_0.m \
       me2/a2qqgg_0_0.m \
       me2/a2qqqq_0_0.m \
       me2/a2qqggg_0_0.m \
       me2/a2qqqqg_0_0.m \
       me2/a2qqqqg_0_0_1_1.m

all: $(ME2)

clean: amp-clean me2-clean

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

(define (parse-amplitude-id amplitude)
  (let* ((m (string-match "([aqg]+)2([aqg]+)([0-9]+)" amplitude))
         (in (string->list (match:substring m 1)))
         (out (string->list (match:substring m 2)))
         (loops (string->number (match:substring m 3))))
    (values in out loops)))

(define (format-qgraf.dat amplitude)
  (define (format-momenta tag particles momentum-base)
    (if (equal? (length particles) 1)
      (format #t "~a= ~c[~a] ;\n\n" tag (list-ref particles 0) momentum-base)
      (let ((nq 0))
        (format #t "~a= ~a ;\n\n"
          tag
          (string-join
            (map
              (lambda (p i)
                (format #f "~c[~a~d]"
                  (case p
                    ((#\q)
                      (set! nq (+ nq 1))
                      (if (odd? nq) #\q #\Q))
                    (else p))
                  momentum-base
                  i))
              particles
              (iota (length particles) 1))
            ", ")))))
  (receive (in out loops) (parse-amplitude-id amplitude)
    (format #t "output= 'amp/~a.h' ;\n\n" amplitude)
    (format #t "style= 'amp/form.sty' ;\n\n")
    (format #t "model= 'amp/qcd.mod' ;\n\n")
    (format-momenta "in" in "q")
    (format-momenta "out" out "k")
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
	@$(guile (save-qgraf.dat "$(basename $(notdir $@))" "$@"))

amp/%.h: amp/%.dat
	@echo "make $@"
	@ln -s "$^" qgraf.dat
	@qgraf | tee  $(@:.h=.log)
	@rm qgraf.dat

.PRECIOUS: amp/%.dat amp/%.h

###########################################################
#
#              II. SQUARED MATRIX ELEMENTS
#
###########################################################
define ME2_SCM
(define (me2-prerequisite filename)
  (let* ((input (string-split (string-drop-right filename 2) #\_))
         (arg (lambda (n) (list-ref input n))))
    (list
      (string-join (list "amp/" (arg 0) (arg 1) ".h") "")
      (string-join (list "amp/" (arg 0) (arg 2) ".h") ""))))

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

FORM = tform -w2 -p ${PWD}/src -I ${PWD}/src -l -f -q

.SECONDEXPANSION:

me2/%.m: $$(guile (me2-prerequisite "$$(notdir $$@)"))
	@echo "make $@"
	$(FORM) $(guile (me2-form-args "$(notdir $@)")) -d ME2=$@ src/me2.frm

me2-clean:
	@rm -fv me2/*.m

AMP=$(sort $(guile (map me2-prerequisite (string-split "$(notdir $(ME2))" \#\space))))

me2-all: $(ME2)

amp-all: $(AMP)

###########################################################
#
#                      III. TESTS
#
###########################################################
define CHECK_SCM
  (define (check-args name)
    (let* ((basename (string-drop name 6))
           (n (map string-length (string-split (car (string-split basename #\_)) #\2))))
      (list
        (string-join (list "me2/" basename ".m") "")
        (string-join (list "test/" basename ".m") "")
        (string-join (list "test/ps"
                           (number->string (car n)) "to"
                           (number->string (cadr n)) ".m") "")
       )))
endef
$(guile $(CHECK_SCM))

CHECK := check_a2qqg_0_0 \
         check_a2qqgg_0_0 \
         check_a2qqgg_0_0_1 \
         check_a2qqgg_0_0_3 \
         check_a2qqgg_0_0_1+3 \
         check_a2qqqq_0_0 \
         check_a2qqqq_0_0_1 \
         check_a2qqqq_0_0_2 \
         check_a2qqqq_0_0_1+2 \
         check_a2qqqqg_0_0_1 \
         check_a2qqqqg_0_0_9 \
         check_a2qqqqg_0_0_1_9

check: $(CHECK)

check_%: me2/%.m test/%.m phony
	@echo "$@"
	@math -script ./src/check.m $(guile (check-args "$@"))

test/%.m: src/testgen.m
	@echo "make '$@'"
	@math -script ./src/testgen.m $(basename $(notdir $@)) $@ # > /dev/null

phony:;
