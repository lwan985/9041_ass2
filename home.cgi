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
&userinfo();
#print "cookie is: ", $cookie, "<br>\n";

# some globals used through the script
$debug = 1;
$students_dir = "./students";
$range = 10;

if (defined param('search_input')){
    my $input = param('search_input');
    print "<META http-equiv=\"Refresh\" content=\"0; url=./search_results.cgi?input=$input\">";
    exit 0;
}

&show_search();
&show_pages();
print page_trailer();
exit 0;

sub show_search {
    print "<center>\n";
    print "Please search for an user name.", "<br>\n";
    print start_form,
        textfield('search_input'), "<br>\n",
        submit('Search'),"<br>\n",
        "<a href=\"./matching.cgi?user=$username\">Try to find your matching\!</a><br><br>\n",
        end_form,
        "</center>";
}

sub show_pages {
    my $n = param('n') || 0;
    opendir(DIR, $students_dir) || die "Can't open directory $students_dir"; 
	my @students = grep (!/^(\.|\.\.)$/, readdir(DIR));
	#print "@students\n";
	$n = min(max($n, 0), $#students);
		
	print "<center>",
	    p,
		start_form, "\n";
		if (defined param('Next '.$range.' users')) {
		    $n = min($n + $range, $#students);
		    param('n', $n);
		}
		elsif(defined param('Previous '.$range.' users')){
		    $n = max($n - $range, 0);
		    param('n', $n);
		}
		print "~~Look Around~~<br>\n";
		foreach $i (0..$range - 1){
		    if ($students[$n + $i]) {
		        my $id = $n + $i;
		        print "<a href=\"./detail.cgi?index=$id $n\">$students[$n + $i]</a><br><br>\n";
	        }
		}
	print hidden('n', $n),"\n",
	    submit('Previous '.$range.' users'),"\n",
		submit('Next '.$range.' users'),"\n",
		end_form, "\n",
		p, "\n",
		"</center>";
}

#
# HTML placed at bottom of every screen
#
sub page_header {
	return header,
	    #$session->header(),
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

sub userinfo {
	if (defined $session->param("user_name")){
	    print "<div align=\"right\">";
        print "Welcome $username\n",
        "<a href=\"./home.cgi\">Back to homepage</a>\n", "or ",
        "<a href=\"./logout.cgi\">log out</a><br>\n";
        #or <a href= "/COMP9321_Assignment2_Movie/?profile_id=<%=id%>">Edit your profile</a>
        print "</div>";
    }
    else {
        print "<center>";
        print "You are not logged in yet.<br>\n";
        print "Redirecting....\n";
        print "<META http-equiv=\"Refresh\" content=\"1; url=./love2041.cgi\">";
        print "</center>";
        exit 0;
    }
}













