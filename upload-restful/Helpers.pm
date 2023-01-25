use strict;
use warnings;
use JSON;


#
# json_out( $cgi, $httpresponsecode, $jsondata );
#	Produce a json response and exit.
#	$httpresponsecode is the Http response code (eg. "200 OK"
#	"201 CREATED" etc), and $jsondata is
#	- EITHER an existing valid json string,
#	- OR an array ref or hashref to be json encoded,
#	the json produced (or passed in) is the body...
#
sub json_out
{
	my( $cgi, $httpresponsecode, $jsondata ) = @_;
	$jsondata = encode_json( $jsondata ) if ref $jsondata;
	print $cgi->header(
		-type => 'application/json',
		-status => $httpresponsecode,
		"-Access-Control-Allow-Origin" => '*' );
	print "$jsondata\n";
	exit 0;
}


#
# h_ok( $cgi, $json ); Generate a 200 OK response, with $json as the body
#
sub h_ok
{
	my( $cgi, $json ) = @_;
	json_out( $cgi, '200 OK', $json );
}


#
# h_internal_error( $cgi, $msg ); Generate a 500 internal error..
#
sub h_internal_error
{
	my( $cgi, $msg ) = @_;
	json_out( $cgi, '500 INTERNAL ERROR', ["Internal Error: $msg"] );
}


#
# h_bad_request( $cgi, $msg ); Print a bad request and exit..
#
sub h_bad_request
{
	my( $cgi, $msg ) = @_;
	json_out( $cgi, '400 BAD REQUEST', ["Bad request: $msg"] );
}


#
# h_conflict( $cgi, $msg ); Print a conflict request and exit..
#
sub h_conflict
{
	my( $cgi, $msg ) = @_;
	json_out( $cgi, '409 CONFLICT', ["Conflict: $msg"] );
}


#
# h_notfound( $cgi, $msg ); Print a notfound request and exit..
#
sub h_notfound
{
	my( $cgi, $msg ) = @_;
	json_out( $cgi, '404 NOT FOUND', [$msg] );
}


#
# h_created( $cgi, $msg ); Print a created request and exit..
#
sub h_created
{
	my( $cgi, $msg ) = @_;
	json_out( $cgi, '201 CREATED', [$msg] );
}


#
# h_teapot( $cgi, $msg ); Print a teapot request and exit..
#
sub h_teapot
{
	my( $cgi, $msg ) = @_;
	json_out( $cgi, "418 I'M A TEAPOT", [$msg] );
}


1;
