from django_hosts import patterns, host

host_patterns = patterns(
    '',
    # Domain: mediap.org
    host(r'www|', 'Mediap.root_urls', name='home'), 

    # Subdomain: cflows.mediap.org
    host(r'cflows', 'cflows.urls', name='cflows'),
)