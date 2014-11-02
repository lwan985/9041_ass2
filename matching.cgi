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
$match_para = 1.5;
%self_data = ();
%prefer = ();

&do_matching();
print page_trailer();
exit 0;

sub do_matching() {
	my $n = param('n') || 0;
    opendir(DIR, $students_dir) || die "Can't open directory $students_dir";
    my @original_students = glob("$students_dir/*");
    
	&load_preferences();
	%self_data = &load_self_data($username);
	&load_self_interests();
    my @score;
    #$score[@original_students][2];
    foreach $i (0..$#original_students){
        $score[$i][0] = $i;
        #$score[$i][1] = &rating($original_students[$i]);
        $score[$i][1] = &rating($original_students[$i], $i);
        #print "$score[$i][0]\n";
        #print "$score[$i][1]<br>\n";
    }
=pod    
    foreach $i (0..$#original_students){
        print "~~score[$i][1] is: $score[$i][1]<br>\n";
        print "~~score[$i][0] is: $score[$i][0]<br>\n";
    }
=cut
    # Do sorting.
    @score = sort {$b->[1] <=> $a->[1] || $a->[0] <=> $b->[0]} @score;
    #@score = sort {$b->[1] <=> $a->[1]} @score;
=pod
    foreach $i (0..$#original_students){
        print "score[$i][1] is: $score[$i][1]<br>\n";
        print "score[$i][0] is: $score[$i][0]<br>\n";
    }
=cut
    my @students;
    foreach $i (0..$#original_students){
        my $student_name = $original_students[$score[$i][0]];
        $student_name =~ s/$students_dir\///;
        $students[$i][0] = $student_name;
        $students[$i][1] = $score[$i][1];
    }
	#print "@students\n";
	$n = min(max($n, 0), $#students);


	print "<center>",
	    p,
		start_form, "\n";
		if (defined param('Next '.$range.' users')) {
		    my $min_num = min($n + $range, $#students);
		    # If not reaching the last page.
		    if ($min_num != $#students) {
		        $n = $min_num;
		    }
		    param('n', $n);
		}
		elsif(defined param('Previous '.$range.' users')){
		    $n = max($n - $range, 0);
		    param('n', $n);
		}
		foreach $i (0..$range - 1){
		    if ($students[$n + $i][0]) {
		        my $id = $n + $i;
		        print "<a href=\"./detail.cgi?username=$students[$n + $i][0]\">$students[$n + $i][0]</a>\n",
		        " Matching index = $students[$n + $i][1]<br><br>\n"
	        }
		}
	print hidden('n', $n),"\n",
	    hidden('input', $input), "\n",
	    submit('Previous '.$range.' users'),"\n",
		submit('Next '.$range.' users'),"\n",
		end_form, "\n",
		p, "\n",
		"</center>";
}

sub load_self_interests() {
    @user_favourite_bands = split ('&&&', $self_data{"favourite_bands"});
    @user_favourite_books = split ('&&&', $self_data{"favourite_books"});
    @user_favourite_hobbies = split ('&&&', $self_data{"favourite_hobbies"});
    @user_favourite_movies = split ('&&&', $self_data{"favourite_movies"});
    @user_favourite_TV_shows = split ('&&&', $self_data{"favourite_TV_shows"});
    @user_courses = split ('&&&', $self_data{"courses"});
    #print "Loaded user favourite_bands is: @user_favourite_bands<br>\n";
    #print "Loaded user favourite_books is: @user_favourite_books<br>\n";
    #print "Loaded user favourite_hobbies is: @user_favourite_hobbies<br>\n";
    #print "Loaded user favourite_movies is: @user_favourite_movies<br>\n";
    #print "Loaded user favourite_TV_shows is: @user_favourite_TV_shows<br>\n";
    #print "Loaded user courses is: @user_courses<br>\n";
    
}

sub load_preferences(){
    my $profile_filename = "$students_dir/$username/preferences.txt";
	open my $p, "$profile_filename" or die "can not open $profile_filename: $!";
	my @user_preference = <$p>;
	
	my $i = 0;
	while ($i < @user_preference) {
	    if ($user_preference[$i] =~ /^gender:/) {
	        my $gender = $user_preference[$i + 1];
	        $gender =~ s/\s*//g;
	        $prefer{"gender"} = $gender;
	        $i += 2;
	        next;
	    }
	    elsif ($user_preference[$i] =~ /^weight:/) {
	        ++$i;
	        while ($user_preference[$i] =~ /^\s/) {
	            if ($user_preference[$i] =~ /^\s*min:/){
	                my $weight = $user_preference[$i + 1];
	                $weight =~ s/\s*//g;
	                $weight =~ s/kg$//;
	                $prefer{"weight_min"} = $weight;
	            }
	            elsif ($user_preference[$i] =~ /^\s*max:/){
	                my $weight = $user_preference[$i + 1];
	                $weight =~ s/\s*//g;
	                $weight =~ s/kg$//;
	                $prefer{"weight_max"} = $weight;
	            }
	            ++$i;
	        }
	        next;
	    }
	    elsif ($user_preference[$i] =~ /^height:/) {
	        ++$i;
	        while ($user_preference[$i] =~ /^\s/) {
	            if ($user_preference[$i] =~ /^\s*min:/){
	                my $height = $user_preference[$i + 1];
	                $height =~ s/\s*//g;
	                $height =~ s/m$//;
	                $prefer{"height_min"} = $height;
	            }
	            elsif ($user_preference[$i] =~ /^\s*max:/){
	                my $height = $user_preference[$i + 1];
	                $height =~ s/\s*//g;
	                $height =~ s/m$//;
	                $prefer{"height_max"} = $height;
	            }
	            ++$i;
	        }
	        next;
	    }
	    elsif ($user_preference[$i] =~ /^age:/) {
	        ++$i;
	        while ($user_preference[$i] =~ /^\s/) {
	            if ($user_preference[$i] =~ /^\s*min:/){
	                my $age = $user_preference[$i + 1];
	                $age =~ s/\s*//g;
	                $prefer{"age_min"} = $age;
	            }
	            elsif ($user_preference[$i] =~ /^\s*max:/){
	                my $age = $user_preference[$i + 1];
	                $age =~ s/\s*//g;
	                $prefer{"age_max"} = $age;
	            }
	            ++$i;
	        }
	        next;
	    }
	    elsif ($user_preference[$i] =~ /^hair_colours:/) {
	        ++$i;
	        my $hair_colours;
	        while ($i < @user_preference && $user_preference[$i] =~ /^\s/) {
                my $hair = $user_preference[$i];
                $hair =~ s/\s*//g;
                if (defined $hair_colours) {
                    $hair_colours .= "&&&$hair";
                }
                else {
                    $hair_colours = $hair;
                }
	            ++$i;
	        }
	        $prefer{"hair_colour"} = $hair_colours;
	        next;
	    }
	    ++$i;
	}
}

sub load_self_data() {
    my $username = $_[0];
    my $profile_filename = "$students_dir/$username/profile.txt";
	open my $p, "$profile_filename" or die "can not open $profile_filename: $!";
	my @self_data = <$p>;
	my %self_data = ();
	
	my $i = 0;
	while ($i < @self_data) {
	    if ($self_data[$i] =~ /gender:/) {
	        my $gender = $self_data[$i + 1];
	        $gender =~ s/\s*//g;
	        $self_data{"gender"} = $gender;
	        $i += 2;
	        next;
	    }
	    elsif ($self_data[$i] =~ /birthdate:/) {
	        my $birthdate = $self_data[$i + 1];
	        $birthdate =~ s/\s*//g;
	        $birthdate =~ /(\d{4})/;
	        $birthdate = $1;
	        $self_data{"birthdate"} = $birthdate;
	        #print "$birthdate<br>\n";
	        $i += 2;
	        next;
	    }
	    elsif ($self_data[$i] =~ /height:/) {
	        my $height = $self_data[$i + 1];
	        $height =~ s/\s*//g;
	        $height =~ s/m$//;
	        $self_data{"height"} = $height;
	        $i += 2;
	        next;
	    }
	    elsif ($self_data[$i] =~ /weight:/) {
	        my $weight = $self_data[$i + 1];
	        $weight =~ s/\s*//g;
	        $weight =~ s/kg$//;
	        $self_data{"weight"} = $weight;
	        $i += 2;
	        next;
	    }
	    elsif ($self_data[$i] =~ /hair_colour:/) {
	        my $hair_colour = $self_data[$i + 1];
	        $hair_colour =~ s/\s*//g;
	        $self_data{"hair_colour"} = $hair_colour;
	        $i += 2;
	        next;
	    }
	    elsif ($self_data[$i] =~ /degree:/) {
	        my $degree = $self_data[$i + 1];
	        $degree =~ s/\s*//g;
	        $self_data{"degree"} = $degree;
	        $i += 2;
	        next;
	    }
	    elsif ($self_data[$i] =~ /courses:/) {
	        ++$i;
	        my $courses_list;
	        while ($self_data[$i] =~ /^\s/) {
                my $courses = $self_data[$i];
                chomp $courses;
                $courses =~ s/^\s*//;
                if (defined $courses_list) {
                    $courses_list .= "&&&$courses";
                }
                else {
                    $courses_list = "$courses";
                }
	            ++$i;
	        }
	        $self_data{"courses"} = $courses_list;
	        next;
	    }
	    elsif ($self_data[$i] =~ /favourite_bands:/) {
	        ++$i;
	        my $favourite_bands_list;
	        while ($i < @self_data && $self_data[$i] =~ /^\s/) {
                my $favourite_bands = $self_data[$i];
                chomp $favourite_bands;
                $favourite_bands =~ s/^\s*//;
                if (defined $favourite_bands_list) {
                    $favourite_bands_list .= "&&&$favourite_bands";
                }
                else {
                    $favourite_bands_list = "$favourite_bands";
                }
	            ++$i;
	        }
	        $self_data{"favourite_bands"} = $favourite_bands_list;
	        next;
	    }
	    elsif ($self_data[$i] =~ /favourite_books:/) {
	        ++$i;
	        my $favourite_books_list;
	        while ($i < @self_data && $self_data[$i] =~ /^\s/) {
                my $favourite_books = $self_data[$i];
                chomp $favourite_books;
                $favourite_books =~ s/^\s*//;
                if (defined $favourite_books_list) {
                    $favourite_books_list .= "&&&$favourite_books";
                }
                else {
                    $favourite_books_list = "$favourite_books";
                }
	            ++$i;
	        }
	        $self_data{"favourite_books"} = $favourite_books_list;
	        next;
	    }
	    elsif ($self_data[$i] =~ /favourite_hobbies:/) {
	        ++$i;
	        my $favourite_hobbies_list;
	        while ($i < @self_data && $self_data[$i] =~ /^\s/) {
                my $favourite_hobbies = $self_data[$i];
                chomp $favourite_hobbies;
                $favourite_hobbies =~ s/^\s*//;
                if (defined $favourite_hobbies_list) {
                    $favourite_hobbies_list .= "&&&$favourite_hobbies";
                }
                else {
                    $favourite_hobbies_list = "$favourite_hobbies";
                }
	            ++$i;
	        }
	        $self_data{"favourite_hobbies"} = $favourite_hobbies_list;
	        next;
	    }
	    elsif ($self_data[$i] =~ /favourite_movies:/) {
	        ++$i;
	        my $favourite_movies_list;
	        while ($i < @self_data && $self_data[$i] =~ /^\s/) {
                my $favourite_movies = $self_data[$i];
                chomp $favourite_movies;
                $favourite_movies =~ s/^\s*//;
                if (defined $favourite_movies_list) {
                    $favourite_movies_list .= "&&&$favourite_movies";
                }
                else {
                    $favourite_movies_list = "$favourite_movies";
                }
	            ++$i;
	        }
	        $self_data{"favourite_movies"} = $favourite_movies_list;
	        next;
	    }
	    elsif ($self_data[$i] =~ /favourite_TV_shows:/) {
	        ++$i;
	        my $favourite_TV_shows_list;
	        while ($i < @self_data && $self_data[$i] =~ /^\s/) {
                my $favourite_TV_shows = $self_data[$i];
                chomp $favourite_TV_shows;
                $favourite_TV_shows =~ s/^\s*//;
                if (defined $favourite_TV_shows_list) {
                    $favourite_TV_shows_list .= "&&&$favourite_TV_shows";
                }
                else {
                    $favourite_TV_shows_list = "$favourite_TV_shows";
                }
	            ++$i;
	        }
	        $self_data{"favourite_TV_shows"} = $favourite_TV_shows_list;
	        next;
	    }
	    
	    ++$i;
	}
	return %self_data;
}


sub rating() {
    my $student = $_[0];
    my $index_i = $_[1];
    $student =~ s/$students_dir\///;
	my %student_profile = &load_self_data($student);
	
    my $rating = 0;
    # $score is for interests counting.
    my $score = 0;
    foreach $key (keys %student_profile) {
        if ($key eq "gender") {
            #print "student gender is: $student_profile{$key}<br>\n";
            #print "user gender is: $self_data{$key}<br>\n";
            #print "prefer gender is: $prefer{$key}<br>\n";
            if (defined $prefer{$key} && $prefer{$key} ne $student_profile{$key}) {
                #print "Should return 0, student_profile is ^^^$student_profile{$key}^^^<br>\n";
                #print "Should return 0, prefer is ^^^$prefer{$key}^^^<br>\n";
                return 0;
            }
            # No homosexual as default unless user required.
            elsif ($self_data{$key} eq $student_profile{$key}) {
                return 0;
            }
            # No score plus for gender.
        }
        elsif ($key eq "birthdate") {
            my $age = 2014 - $student_profile{$key};
            #my $temp = $rating;
            #print "student[$index_i] age is: $age<br>\n";
            if (defined $prefer{"age_min"}) {
                if ($age >= $prefer{"age_min"} && $age <= $prefer{"age_max"}){
                    $rating += 30 * $match_para;
                }
                elsif (abs($prefer{"age_min"} - $age) <= 5 || abs($age - $prefer{"age_max"}) <= 5){
                    $rating += 15 * $match_para;
                }
                # No score plus if the age difference is too large.
            }
            else {
                # If age preference is not defined.
                if (abs($student_profile{$key} - $self_data{$key}) <= 5){
                    $rating += 30;
                }
                elsif(abs($student_profile{$key} - $self_data{$key}) <= 10){
                    $rating += 15;
                }
                # No score plus if the age difference is too large.
            }
            #$result = $rating - $temp;
            #print "student[$index_i] age rating is: $result<br>\n";
        }
        elsif ($key eq "height") {
            my $height = $student_profile{$key};
            if (defined $prefer{"height_min"}) {
                if ($height >= $prefer{"height_min"} && $height <= $prefer{"height_max"}){
                    $rating += 17.5 * $match_para;
                }
                elsif ($prefer{"height_min"} - $height <= 3 || $height - $prefer{"height_max"} <= 3){
                    $rating += 8.75 * $match_para;
                }
                # No score plus if the height difference is too large.
            }
            else {
                # If height preference is not defined.
                $rating += 17.5;
            }
        }
        elsif ($key eq "weight") {
            my $weight = $student_profile{$key};
            if (defined $prefer{"weight_min"}) {
                if ($weight >= $prefer{"weight_min"} && $weight <= $prefer{"weight_max"}){
                    $rating += 10 * $match_para;
                }
                elsif ($prefer{"weight_min"} - $weight <= 5 || $weight - $prefer{"weight_max"} <= 5){
                    $rating += 5 * $match_para;
                }
                # No score plus if the weight difference is too large.
            }
            else {
                # If weight preference is not defined.
                $rating += 10;
            }
        }
        elsif ($key eq "hair_colour") {
            my $hair_colour = $student_profile{$key};
            #print "student hair_colour = $hair_colour<br>\n";
            #print "user prefer hair_colour = ", $prefer{"hair_colour"}, "<br>\n";
            if (defined $prefer{"hair_colour"}) {
                if ($prefer{"hair_colour"} =~ /$hair_colour/){
                    #print "student[$index_i] hair color matches!!!<br>\n";
                    $rating += 7.5 * $match_para;
                }
            }
            else {
                # If hair_colours preference is not defined.
                $rating += 7.5;
            }
        }
        # The following are interests, which will not be in the preferences.txt
        # but the system should calculate the score according to the profile of user.
        # If a student's particular interest matches the user's one, system will score the student 1.
        elsif ($key eq "favourite_bands") {
            $score += &get_score(\@user_favourite_bands, $student_profile{$key}, $key);
        }
        elsif ($key eq "favourite_books") {
            $score += &get_score(\@user_favourite_books, $student_profile{$key}, $key);
        }
        elsif ($key eq "favourite_hobbies") {
            $score += &get_score(\@user_favourite_hobbies, $student_profile{$key}, $key);
        }
        elsif ($key eq "favourite_movies") {
            $score += &get_score(\@user_favourite_movies, $student_profile{$key}, $key);
        }
        elsif ($key eq "favourite_TV_shows") {
            $score += &get_score(\@user_favourite_TV_shows, $student_profile{$key}, $key);
        }
        # Followings are some other features which are not so ralavent
        # but constitute a little extra rating
        elsif ($key eq "degree") {
            my $degree = $student_profile{$key};
            if ($self_data{$key} eq $degree) {
                $rating += 10;
                #print "Same degree!!!<br>\n";
            }
        }
        elsif ($key eq "courses") {
            my @courses = split ('&&&', $student_profile{$key});
            my $hits = 0;
            foreach my $c (@courses) {
                foreach my $uc (@user_courses) {
                    if ($c eq $uc) {
                        ++$hits;
                    }
                }
            }
            $rating += 5 if $hits == 1;
            $rating += 7 if $hits > 1;
            #print "Same course~~~<br>\n" if $hits > 0;
        }
    }
    # If score = 3 (out of 5 interests), rating += 30, if score = 2, rating += 25, score = 1
    # rating += 20, else, rating += 10.
    $rating += 30 if $score == 3;
    $rating += 25 if $score == 2;
    $rating += 20 if $score == 1;
    $rating += 10 if $score == 0;
    return $rating;
}

sub get_score() {
    my ($user_interest, $target_interest, $key) = @_;
    #print "user $key = @$user_interest<br>\n";
    my @target_interest = split ('&&&', $target_interest);
    my $hits = 0;
    foreach my $f (@target_interest) {
        foreach my $uf (@$user_interest) {
            if ($f eq $uf) {
                ++$hits;
            }
        }
    }
    #print "student $key hits = $hits<br>\n";
    #print "student $key = @target_interest<br>\n";
    if ($hits > 0) {
        return 1;
    }
    return 0;
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














