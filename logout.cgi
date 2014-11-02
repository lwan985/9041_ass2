#!/usr/bin/perl -w

# written by lwan985 2014s2
# as a starting point for COMP2041/9041 assignment 2
# http://cgi.cse.unsw.edu.au/~cs2041/assignments/LOVE2041/

use CGI qw/:all/;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use Data::Dumper;  
use List::Util qw/min max/;
warningsToBrowser(1);

use CGI::Session;

my $cgi = new CGI;
my $session = new CGI::Session("driver:File", $cgi, {Directory=>'/tmp'});
my $username = $session->param("user_name");
my $cookie = $session->id;

# print start of HTML ASAP to assist debugging if there is an error in the script
print page_header();

print "<center>";
print "You will log out in 1 second.<br>\n";
print "Redirecting....\n";
print "</center>";
$session->delete();
$session->flush(); # Recommended practice says use flush() after delete().
print "<META http-equiv=\"Refresh\" content=\"1; url=./love2041.cgi\">";
exit 0;


sub page_header {
	return #header,
	    $session->header(),
   		start_html("-title"=>"LOVE2041", -bgcolor=>"#FEDCBA"),
 		center(h2(i("LOVE2041")));
}
