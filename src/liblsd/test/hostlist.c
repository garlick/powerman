#if HAVE_CONFIG_H
#include "config.h"
#endif

#include <string.h>

#include "tap.h"
#include "hostlist.h"

void lsd_fatal_error(char *file, int line, char *mesg)
{
    BAIL_OUT ("%s::%d: %s", file, line, mesg);
}

void *lsd_nomem_error(char *file, int line, char *mesg)
{
    BAIL_OUT ("%s: out of memory", mesg);
    return NULL;
}

static void test_issue197 (void)
{
    const char *t1 = "pclstr[201-203]-p";
    const char *hosts[] = { "pclstr201-p", "pclstr202-p", "pclstr203-p" };
    hostlist_t hl;
    hostlist_iterator_t itr;
    char *host;

    hl = hostlist_create (t1);
    itr = hostlist_iterator_create (hl);
    if (!hl || !itr)
        BAIL_OUT ("cannot continue without hostlist and iterator");
    ok (hl != NULL,
        "decoded %s", t1);
    for (int i = 0; i < 3; i++) {
        host = hostlist_next (itr);
        ok (host && !strcmp (host, hosts[i]),
            "host[%d] is %s", i, hosts[i]);
        free (host);
    }
    hostlist_iterator_destroy (itr);
    hostlist_destroy (hl);
}

int main (int argc, char *argv[])
{
    plan (NO_PLAN);
    test_issue197 ();
    done_testing ();
}

// vi: ts=4 sw=4 expandtab
