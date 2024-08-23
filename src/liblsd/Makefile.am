AM_CFLAGS = \
	@WARNING_CFLAGS@ \
	-Wno-parentheses \
	-Wno-error=parentheses

AM_CPPFLAGS =

noinst_LTLIBRARIES = liblsd.la

liblsd_la_SOURCES = \
	hostlist.c \
	hostlist.h \
	list.c \
	list.h \
	hash.c \
	hash.h \
	cbuf.c \
	cbuf.h

TESTS = \
	test_hostlist.t

check_PROGRAMS = $(TESTS)

TEST_EXTENSIONS = .t
T_LOG_DRIVER = env AM_TAP_AWK='$(AWK)' $(SHELL) \
	$(top_srcdir)/config/tap-driver.sh

test_hostlist_t_CPPFLAGS = \
        -I$(top_srcdir)/src/libtap
test_hostlist_t_SOURCES = test/hostlist.c
test_hostlist_t_LDADD = \
        $(builddir)/liblsd.la \
        $(top_builddir)/src/libtap/libtap.la
