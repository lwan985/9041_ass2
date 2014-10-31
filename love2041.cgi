#!/usr/bin/perl -w

# written by lwan985 2014s2
# as a starting point for COMP2041/9041 assignment 2
# http://cgi.cse.unsw.edu.au/~cs2041/assignments/LOVE2041/

use CGI qw/:all/;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use Data::Dumper;  
use List::Util qw/min max/;
warningsToBrowser(1);

# print start of HTML ASAP to assist debugging if there is an error in the script
print page_header();

# some globals used through the script
$debug = 1;
$students_dir = "./students";
$range = 10;


&show_pages();
print page_trailer();
exit 0;

sub show_pages {
    my $n = param('n') || 0;
    opendir(DIR, $students_dir) || die "Can't open directory $students_dir"; 
	my @students = grep (!/^(\.|\.\.)$/, readdir(DIR));
	print "@students\n";
	$n = min(max($n, 0), $#students);
		
	print p,
		start_form, "\n";
		if (defined param('Next '.$range.' users')) {
		    $n = min($n + $range, $#students);
		    param('n', $n);
		}
		elsif(defined param('Previous '.$range.' users')){
		    $n = max($n - $range, 0);
		    param('n', $n);
		}
		print "n = $n<br><br><br><br>\n";
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
		p, "\n";
}

#
# HTML placed at bottom of every screen
#
sub page_header {
	return header,
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
















