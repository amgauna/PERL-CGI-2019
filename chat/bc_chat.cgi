#!/usr/bin/perl

############# Begin Setup ###############

# complete url or path to directory images are located
# this is all you are required to change, rest is optional.
$imagedir = 'http://www.yourdomain.com/bluechat';

# if you have to place all the cgi files in
# your cgi-bin directory, then the chat directory
# must be placed outside the cgi-bin directory.
# change chatpath to the absolute path to the chat
# directory and chaturl to the http://whatever url.
# Leave as is for most installations.
$chatpath = './chat';
$chaturl = './chat';

# Chat refresh time, in seconds
$ChatRefresh = 10;
# Time to leave messages
$ChatMessageTime = 180;

# Enable chat logging? 0 is false, 1 is true.
# If you enable logging, be sure to check the
# log file often, it can grow in size quickly.
$chatLogging = '0';
$logFileName = 'chat_history.htm';

# bad words will be filtered out of chat.
# Notice you can use Perl regular expressions too.
# Comment out the entire line to remove all of them.
@badwords = ("fuck", "shit", "damn", " ass ", "asshole", "f`?.?u`?.?c`?.?k");

# You can exclude one channel from badwords filtering.
# If you want all channels to be excluded, comment
# out the @badwords variable instead.
$exclude_channel = 'adult';

############### End Setup #################

print "Content-type: text/html\nPragma: no-cache\n\n";

# get the form data.
&get_form_data;

# check for room, and read the old message file
$formdata{'room'} =~ s/\W//g;
$formdata{'room'} = lc($formdata{'room'});

&lock($chatpath . '/' . $formdata{'room'} . '.lck');

# create room if not exist.
if (!(-e "$chatpath/$formdata{'room'}\.htm")) {
  open(CREATE, ">$chatpath/$formdata{'room'}\.htm");
  close(CREATE);
}

open(HTMLOLD, "$chatpath/$formdata{'room'}\.htm") ||
  &myerror("Unable to open room: $formdata{'room'}");
@lines=<HTMLOLD>;
close(HTMLOLD);

# time message printed.
my $thetime = time;

# write and output new messages file
          $newmessage = '';
	      if (($formdata{'cname'} ne '') && ($formdata{'message'} ne '')){
		    # remove all badwords
			$exclude_channel = lc($exclude_channel);
			if ($exclude_channel ne $formdata{'room'}) {
              if (@badwords > 0) {
    			  foreach $curse (@badwords) {
	    		    $formdata{'message'} =~ s/$curse/\<font color=red\>\%\&\#\%\<\/font\>/ig;
		    	    $formdata{'cname'} =~ s/$curse/\<font color=red\>\%\&\#\%\<\/font\>/ig;
                  }
			  }
			}
			# format the message
			$ColoredName = $formdata{'cname'};
            $ColoredMessage = $formdata{'message'};
			# replace smilely faces
			$ColoredMessage =~ s/\:\)/\<img src=\"$imagedir\/smile1.gif\" width=\"16\" height=\"12\" border=\"0\"\>/g;
			$ColoredMessage =~ s/\:\(/\<img src=\"$imagedir\/smile2.gif\" width=\"16\" height=\"12\" border=\"0\"\>/g;
			$ColoredMessage =~ s/\;\)/\<img src=\"$imagedir\/smile3.gif\" width=\"16\" height=\"12\" border=\"0\"\>/g;
			# check for me action
            if ($ColoredMessage =~ s/^\.me//i) {
              $ColoredName = &Make_Color('`1|||`4|||`1|||`% ' . $ColoredName);
			  $ColoredMessage = &Make_Color('<b>`2' . $ColoredMessage . '</b>');
            } else {
			   $ColoredName = &Make_Color($ColoredName . '`%:');
			   $ColoredMessage = &Make_Color($ColoredMessage);
			  }

			$newmessage = "<FONT SIZE=\"-1\"><B>$ColoredName</B> $ColoredMessage<!--$thetime//--></FONT><BR>\n";
          }
		
		open (NEW, ">$chatpath/$formdata{'room'}\.htm");
		print NEW "<HTML><HEAD><META HTTP-EQUIV=\"Refresh\" CONTENT=\"$ChatRefresh\">\n";
		print NEW '<META HTTP-EQUIV="Expires" CONTENT="Fri, Jun 12 1981 08:20:00 GMT">' . "\n";
        print NEW '<META HTTP-EQUIV="Pragma" CONTENT="no-cache">' . "\n";
        print NEW '<META HTTP-EQUIV="Cache-Control" CONTENT="no-cache">' . "\n";
		print NEW "</HEAD><BODY BGCOLOR=\"#F0F0F0\">\n";
		print "<HTML><HEAD><META HTTP-EQUIV=\"Refresh\" CONTENT=\"$ChatRefresh;URL=$chaturl/$formdata{'room'}\.htm\">\n";
		print '<META HTTP-EQUIV="Expires" CONTENT="Fri, Jun 12 1981 08:20:00 GMT">' . "\n";
        print '<META HTTP-EQUIV="Pragma" CONTENT="no-cache">' . "\n";
        print '<META HTTP-EQUIV="Cache-Control" CONTENT="no-cache">' . "\n";
		print "</HEAD><BODY BGCOLOR=\"#F0F0F0\">\n";
			
			if ($newmessage ne '') {
			  print NEW $newmessage;
			  print $newmessage;
			  if ($chatLogging) {
			    my $now_string = gmtime;
			    if (open(CHATLOG, ">>$chatpath/$logFileName")) {
				  print CHATLOG '<small>' . $now_string . '-' . $formdata{'room'} . '-</small>' . $newmessage;
				  close(CHATLOG);
			    }
			  }
			}

			for ($i = 1; $i < @lines; $i++)
			{
			    $lines[$i] =~ m/<!--(\d*)\/\/-->/;
				if ((time - $1) <= $ChatMessageTime)
				{
				  if ($lines[$i] ne "</BODY></HTML>\n") {
			        print NEW "$lines[$i]";
			        print "$lines[$i]";
				  }
				}
			}

			print NEW "</BODY></HTML>\n";
			print "</BODY></HTML>\n";
		close(NEW);

&unlock($chatpath . '/' . $formdata{'room'} . '.lck');
exit;

# Gets Form data, also removes html formatting.
sub get_form_data {
	if ($ENV{'REQUEST_METHOD'} eq 'GET') {
      @pairs = split(/&/, $ENV{'QUERY_STRING'});
    }
	else
	{	
	$buffer = "";
	read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
	@pairs=split(/&/,$buffer);
    }

	foreach $pair (@pairs)
	{
		@a = split(/=/,$pair);
		$name=$a[0];
		$value=$a[1];
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
		$value =~ s/~!/ ~!/g;
		$value =~ s/\+/ /g;
		$value =~ s/\</\&lt\;/g;  # remove to enable html tags in messages.
		$value =~ s/\>/\&gt\;/g;  # remove to enable html tags in messages.
		$value =~ s/\r//g;
		push (@data,$name);
		push (@data, $value);
	}
	%formdata=@data;
	%formdata;
}

sub myerror {
   my $msg = shift;
   &unlock($chatpath . '/' . $formdata{'room'} . '.lck');
   print $msg;
   exit;
}

sub Make_Color {
my $st = shift;
my $result = '';
my $colors = 0;
my $i;
my $ch;

for ($i=0; $i < length($st); $i++) {
  if (substr($st,$i,1) eq '`') {
    $i++;
	if ($i > length($st)) { next; }
	$ch = substr($st,$i,1);
	if ($ch eq '1') {$result .= '<font color="#0000A8">'; $colors++;}
	elsif ($ch eq '2') {$result .= '<font color="#007000">'; $colors++;}
	elsif ($ch eq '3') {$result .= '<font color="#008080">'; $colors++;}
	elsif ($ch eq '4') {$result .= '<font color="#A80000">'; $colors++;}
	elsif ($ch eq '5') {$result .= '<font color="#A800A8">'; $colors++;}
	elsif ($ch eq '6') {$result .= '<font color="#A85400">'; $colors++;}
	elsif ($ch eq '7') {$result .= '<font color="#808080">'; $colors++;}
	elsif ($ch eq '8') {$result .= '<font color="#505050">'; $colors++;}
	elsif ($ch eq '9') {$result .= '<font color="#5454FC">'; $colors++;}
	elsif ($ch eq '0') {$result .= '<font color="#00B000">'; $colors++;}
	elsif ($ch eq '!') {$result .= '<font color="#00A0A0">'; $colors++;}
	elsif ($ch eq '@') {$result .= '<font color="#FC5454">'; $colors++;}
	elsif ($ch eq '#') {$result .= '<font color="#FC54FC">'; $colors++;}
	elsif ($ch eq 'A') {$result .= '<font color="#FC54FC">'; $colors++;}
	elsif ($ch eq '$') {$result .= '<font color="#AAAA00">'; $colors++;}
	elsif ($ch eq '%') {$result .= '<font color="#000000">'; $colors++;}
  } else {
     $result .= substr($st,$i,1);
	 }
}

while ($colors--) { $result .= '</font>'; }

return ($result);
}

sub lock
{
$mylockfile = shift;
   my $endtime = time + 7;
   if (-e $mylockfile) {
      open (LOCKFILE, $mylockfile);
      my $temp = <LOCKFILE>;
      close (LOCKFILE);
      if ($temp < time) {
         unlink ($mylockfile);
      }
   }
   while (-e $mylockfile && time < $endtime) {
      sleep(1);
   }
   if (-e $mylockfile) {
      &error("Can't obtain file lock for $mylockfile");
   } else {
      open (LOCKFILE, ">$mylockfile") or &error ("Can't obtain file lock for $mylockfile");
      print LOCKFILE (time + 10);
	  close(LOCKFILE);
   }
}

sub unlock
{
$mylockfile = shift;
   # close (LOCKFILE);
   unlink ($mylockfile);
}

sub error
{
   my $msg = shift;
   print "<html><head><title>File Lock Error</title></head><body>\n";
   print '<p><a href="javascript:window.location.reload(1);">Click Here</a> to try again.</p>';
   print "\n<p>$msg</p>\n";
   print '<p>This may be caused by an incorrectly set variable.</p>';
   print '<p>The $chatpath variable must be the path, not the URL to the chat directory.</p>';
   print '<p>Also make sure the chat directory exists and is chmod 777</p>';
   print '</body></html>';
   exit;
}
