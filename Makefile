TESTS = $(wildcard tests/test-*.txt)
RESULTS = $(patsubst %.txt,%.result,$(TESTS))
DIFFS = $(patsubst %.txt,%.diff,$(TESTS))
TIMES = times3.log
DIFF_SUMMARY = diffs_summary.log

all: $(RESULTS) $(DIFFS) $(TIMES) $(DIFF_SUMMARY)

%.result: %.txt
	@echo "Running test $<"
	@/bin/bash -c "TIMEFORMAT='%R'; { time python3 pipe.py < $< > $@; } 2>> $(TIMES)"

%.diff: %.result %.out
	@echo "Creating diff for $<"
	@diff $*.result $*.out > $@ || true

$(TIMES): $(TESTS)
	@rm -f $(TIMES)
	@touch $(TIMES)
	@for test in $(TESTS); do \
		echo -n "$$test: " >> $(TIMES); \
		/bin/bash -c "TIMEFORMAT='%R'; { time python3 pipe.py < $$test > $$(patsubst %.txt,%.result,$$test); } 2>> $(TIMES)"; \
	done

$(DIFF_SUMMARY): $(DIFFS)
	@rm -f $(DIFF_SUMMARY)
	@touch $(DIFF_SUMMARY)
	@for diff in $(DIFFS); do \
		if [ -s $$diff ]; then \
			echo "$$diff has differences" >> $(DIFF_SUMMARY); \
		fi \
	done

clean:
	rm -f $(RESULTS) $(DIFFS) $(TIMES) $(DIFF_SUMMARY)