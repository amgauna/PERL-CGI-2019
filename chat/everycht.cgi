#!/usr/bin/perl

#############################################################
# CONFIGURATION (MODIFY THIS SECTION)
# place the absolute path to your chat room message files
# here (include a trailing slash).

	$filepath='/home/hahnfld/public_html/messages/';

# place the file extention of your chat room message files
# here, including the dot.  It is probably .htm or .html

	$filext='.html';

# setting this flag will make messages scroll from top to
# bottom, making the script compatible with EVERY browser.
# See the readme.txt file under OPTIONS for more details!

	$iecompatible=0;

#############################################################
# Section 1: read in the form data and initialize page

	print "Content-type: text/html\nPragma: no-cache\n\n";
	&get_form_data;

#############################################################
# Section 2: check if [room].html exists and if so, read in
# the old message file

	$formdata{'room'} =~ s/\W//g;
	unless (open(HTMLOLD, "$filepath$formdata{'room'}$filext"))
	{
		die 'The following room does not exist on this server: ';
	}
	@lines=<HTMLOLD>;
	close(HTMLOLD);

#############################################################
# Section 3: get the time and format to look nice

	$now_string = localtime;
	@thetime = split(/ +/,$now_string);
	@theclock = split(/:/,$thetime[3]);
	$ampm = 'am';
	if ($theclock[0] > 11)
	{ $ampm = 'pm'; }
	if ($theclock[0] == 0)
	{ $theclock[0] = 12; }
	if ($theclock[0] > 12)
	{ $theclock[0] -= 12; }
	else
	{ $theclock[0] += 0; }

#############################################################
# Section 4: initialize the message form after logon and
# write new messages file

	print "<html><title></title><BODY BGCOLOR=\#000080 TEXT=\#FFFFFF>\n";
	if ($formdata{'logoff'} eq '1')
	{
		print "<CENTER>Thank you for using EveryChat 3.5\!</CENTER><BR><HR><FONT SIZE=-1>\n";
	}
	else
	{
		print "<CENTER><TABLE CELLSPACING=0 CELLPADDING=0>\n<TR>\n<TD>\n";
		print "<nobr><FORM ACTION=\"$ENV{'SCRIPT_NAME'}\" METHOD=\"POST\">Your message\:\n\<input name=username type=hidden value=\"$formdata{'username'}\">\n";
		print "<input name=room type=hidden value=\"$formdata{'room'}\"\>\n";
		print "<input type=text name=message size=35>\n";
		print "<input type=submit value=\"Post This\">";
		print "</form></nobr>\n</TD>\n<TD>\n";
		print "<nobr><FORM ACTION=\"$ENV{'SCRIPT_NAME'}\" METHOD=\"POST\"><input name=username type=hidden value=\"$formdata{'username'}\">\n";
		print "<input name=room type=hidden value=\"$formdata{'room'}\">\n";
		print "<input name=logoff type=hidden value=1>\n";
		print "<input type=hidden name=message value=\"Buh\-Bye\! I just logged off\!\">\n";
		print "<input type=submit value=\"Logoff\">";
		print "</form></nobr>\n</TD>\n</TR>\n</TABLE></CENTER><BR><HR>\n";
		print "<FONT SIZE=\-2>Hit \"post\" without entering a message to refresh the screen\.\.\.</FONT><FONT SIZE=-1>\n";
	}

#############################################################
# Section 5: output the new message page

	if ($formdata{'message'} ne "") {
		$newmessage = "\<P\>\<B\>$formdata{'username'}\</B\> says\,\"$formdata{'message'}\" \($thetime[0] $theclock[0]\:$theclock[1]$ampm\)\n";
		open (NEW, ">$filepath$formdata{'room'}$filext");
		print NEW '<HTML><HEAD><META HTTP-EQUIV="Refresh" CONTENT="5"></HEAD><BODY BGCOLOR="#FFFFFF">';
		print NEW "\n";
		if ($iecompatible) {
			print NEW $newmessage;
			print $newmessage;
			for ($i = 1; $i < 15; $i++)
			{
			    print NEW "$lines[$i]";
			    print "$lines[$i]";
			}
			print NEW '<BR><FONT COLOR=#FFFFFF>EveryChat (c) 1997 Matt Hahnfeld</FONT></BODY>';
		}
		else {
			for ($i = 2; $i < 16; $i++)
			{
			    print NEW "$lines[$i]";
			    print "$lines[$i]";
			}
			print NEW $newmessage;
			print $newmessage;
			print NEW '<BR><FONT COLOR=#FFFFFF><A NAME="END">EveryChat (c) 1997 Matt Hahnfeld</A></FONT></BODY>';
		}
		print NEW "\n";
		close(NEW);
	}
	else {
		for ($i = 1; $i < 16; $i++)
			{
			    print "$lines[$i]";
			}
	}
        print "</font></body></html>\n";
	exit 0;

#############################################################
# Section 6: subprograms to perform useful tasks

sub get_form_data {
	$buffer = "";
	read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
	@pairs=split(/&/,$buffer);
	foreach $pair (@pairs)
	{
		@a = split(/=/,$pair);
		$name=$a[0];
		$value=$a[1];
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
		$value =~ s/~!/ ~!/g;
		$value =~ s/\+/ /g;
		$value =~ s/\</\&lt\;/g;  # html tag removal (remove these lines to enable HTML tags in messages)
		$value =~ s/\>/\&gt\;/g;  # html tag removal (remove these lines to enable HTML tags in messages)
		$value =~ s/\r//g;
		push (@data,$name);
		push (@data, $value);
	}
	%formdata=@data;
	%formdata;
}