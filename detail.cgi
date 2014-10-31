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


print browse_screen();
print page_trailer();
exit 0;


sub browse_screen {
    my $index = param('index');
    @temp = split (" ", $index);
	my $id = $temp[0] || 0;
	my $page = $temp[1] || 0;
	my @students = glob("$students_dir/*");
	$id = min(max($id, 0), $#students);
	param('id', $id + 1);
	my $student_to_show  = $students[$id];
	my $profile_filename = "$student_to_show/profile.txt";
	open my $p, "$profile_filename" or die "can not open $profile_filename: $!";
	$profile = join '', <$p>;
	@temp_profile = split '\n', $profile;
	# Remove the private profile.
	my $i = 0;
	$profile = '';
	$private_flag = "false";
	while ($i < @temp_profile) {
	    # If any private content is more than one line.
	    if ($private_flag eq "true" && $temp_profile[$i] =~ /^\s+/) {
	        ++$i;
	        next;
	    }
	    $private_flag = "false";
	    if ($temp_profile[$i] eq "name:" || $temp_profile[$i] eq "email:"
	    || $temp_profile[$i] eq "password:" || $temp_profile[$i] eq "courses:") {
	        $private_flag = "true";
	        # jump the subtitle line.
	        # jump the content line.
	        $i += 2;
	        next;
	    }
	    $profile .= $temp_profile[$i]."\n";
	    ++$i;
	}
	close $p;
	if (-e "$student_to_show/profile.jpg") {
    	print '<img src="'.$student_to_show.'/profile.jpg">';
	}
	
	return p,
		start_form, "\n",
		
		pre($profile),"\n",
		hidden('id', $id + 1),"\n",
		submit('Next student'),"\n",
		"<a href=\"./love2041.cgi?n=$page\">Back to homepage</a><br>\n",
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
















