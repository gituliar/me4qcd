###########################################################
#
#                    I. AMPLITUDES
#
###########################################################
AMPDIR = amp
AMP := amp/a2qqg0.h \
       amp/a2qqgg0.h \
       amp/a2qqqq0.h \
       amp/a2qqggg0.h \
       amp/a2qqqqg0.h

all: me2-all

amp-all: $(AMP)

amp-clean:
	@rm -fv  $(AMPDIR)/*.h $(AMPDIR)/*.log

$(AMP): %.h: %.dat
	@echo "make $@"
	cd amp/; \
	ln -s $(notdir $<) qgraf.dat ; \
	qgraf | tee  $($(notdir $@):.h=.log); \
	rm qgraf.dat; \
	mv amp.h $(notdir $@)

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

(define (test-dep name)
  (let* ((input (string-split name #\_))
		 (arg (lambda (n) (list-ref input n))))
    (list
      (string-join (list (arg 1) (arg 2) ".h") "")
      (string-join (list (arg 1) (arg 3) ".h") ""))))

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

ME2 := me2/a2qqg_0_0.m \
       me2/a2qqgg_0_0.m \
       me2/a2qqqq_0_0.m \
       me2/a2qqggg_0_0.m \
       me2/a2qqqqg_0_0.m \
       me2/a2qqqqg_0_0_1_1.m

me2-all: $(ME2)

define me2-rule
$(1): $(guile (me2-prerequisite "$(notdir $(1))"))
	$(FORM) $$(guile (me2-form-args "$$(notdir $$@)")) -d ME2=$$@ src/me2.frm
endef
$(foreach me2,$(ME2),$(eval $(eval $(call me2-rule,$(me2)))))

###########################################################
#
#                      III. TESTS
#
###########################################################
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
TEST = $(patsubst check_%,test/%.m,$(CHECK))

check: $(CHECK)

.PHONY: $(CHECK)
$(CHECK): check_%: me2/%.m test/%.m
	@echo "$@"
	@math -script ./src/check.m $(guile (check-args "$@"))

$(TEST): src/testgen.m
	@echo "make '$@'"
	@math -script ./src/testgen.m $(basename $(notdir $@)) $@ # > /dev/null

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
