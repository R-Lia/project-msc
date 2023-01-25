#!/usr/bin/perl

use strict;
use warnings;

use CGI;

# Create a CGI object
my $cgi = CGI->new;
#my $postdata = $cgi->query_string;
# The param method from CGI parses the query string (the portion of a URL after ?) into key value pairs.
my $postdata = $cgi->param("POSTDATA");

#print $cgi->header('application/json','200 OK');
#print $cgi->header('application/json','201 CREATED');
#print $cgi->header('application/json','400 BAD REQUEST');
#print $cgi->header('application/json','404 NOT FOUND');
print $cgi->header('application/json','409 CONFLICT');

print qq([ "postdata": $postdata ]\n);
