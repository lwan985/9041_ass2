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

my $cgi= new CGI;
my $session = new CGI::Session("driver:File", $cgi, {Directory=>'/tmp'});
$session->expire(9000);
my $cookie = $cgi->cookie(CGISESSID => $session->id);


# print start of HTML ASAP to assist debugging if there is an error in the script
print page_header(), "\n";
#print $cookie, "<br>\n";

# some globals used through the script
$debug = 1;
$students_dir = "./students";

if (!defined $session->param("user_name")){
    &validation();
}
else{
    print "<center>";
    print "You have already authenticated.<br>\n",
    "Redirecting....\n";
    print "<META http-equiv=\"Refresh\" content=\"2; url=./home.cgi\">";
    print "</center>";
}
print page_trailer();
exit 0;


sub validation() {
    $username = param('username');
    $password = param('password');
    if (!defined $username && !defined $password) {
        print "<center>",
            start_form,
            'Username: ',
            textfield('username'), "<br>\n",
            'Password: ',
            password_field('password'), "<br>\n",
            submit('Go'),"\n",
            end_form,
            end_html,
            "</center>";
        exit(0);
    }
    else {
        # sanitize username
        $username = substr $username, 0, 256;
        $username =~ s/\W//g;

        my $profile_path = "$students_dir/$username/profile.txt";
        if (!open F, '<', $profile_path) {
            print "<center>";
            print "Unknown username!\n";
            print "</center>";
        }
        else {
            my @profile = <F>;
            foreach $i (0..$#profile) {
                if ($profile[$i] =~ /^password:/) {
                    $correct_password = $profile[$i + 1];
                }
            }
            $correct_password =~ s/(\s*)//g;
            if ($password eq $correct_password) {
                print "<center>";
                print "You are authenticated.<br>\n";
                print "Redirecting....\n";
                $session->param('user_name', $username);
                print "<META http-equiv=\"Refresh\" content=\"1; url=./home.cgi\">";
                print "</center>";
            }
            else {
                print "<center>";
                print "Incorrect password!\n";
                print "</center>";
            }
        }
        print end_html;
        exit(0);
    }
}

#
# HTML placed at bottom of every screen
#
sub page_header {
	return #header,
	    $session->header(),
   		start_html("-title"=>"LOVE2041", -bgcolor=>"#FEDCBA"),
 		center(h2(i("LOVE2041")));
}

#
# HTML placed at bottom of every screen
# It includes all supplied parameter values as a HTML comment
# if global variable $debug is set
#
sub page_trailer {
	my $html = "";
	$html .= join("", map("<!-- $_=".param($_)." -->\n", param())) if $debug;
	$html .= end_html;
	return $html;
}
















