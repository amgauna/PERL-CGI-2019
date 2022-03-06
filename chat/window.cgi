#!/usr/local/bin/perl -U

 &warning unless ($ENV{'QUERY_STRING'});

$TEMP_DATA = $ENV{'QUERY_STRING'};
($N_R, $USER_DIR) = split (/\&/, $TEMP_DATA, 2);
$ROOM = "./Rooms/$N_R";

  $window_data = "$ROOM/Users/$USER_DIR/msg.txt";
  $user_data = `cat $ROOM/User_info/$USER_DIR.info`;

  &warning unless ($window_data); 
  &warning if (!$user_data);

#####################
  if ($user_data)  {

  print "Content-type: text/html\n\n";
  print "<META HTTP-EQUIV=\"Refresh\" CONTENT=\"5\;\n";
  print "URL=./window.cgi?$ENV{'QUERY_STRING'}\">\n"; 

  print "<HTML><HEAD><TITLE>WWWChat 3.0</TITLE></HEAD>\n";
  print "<BODY bgcolor=C9CABD><DL><DD>\n";

  $HTML_OUT = `cat $window_data`;

  print "$HTML_OUT\n";
  print "<HR><font size=-1>
If it doesn't update the messages every 5 seconds, just push the \"Chat\" button.
<br>\n";
############# Don't remove following lines! ################
print "
Powerd by <A HREF=\"http://soback.kornet.nm.kr/~photoboy/CGI/\" target=\"_blank\">
WWWChat 3.0</a>
<br>\n";
  print "</CENTER></BODY></HTML>\n";
  
  exit;         }

  else { &warning;  exit; }

#################### Warning Message ######################
sub warning {
 print "Content-type: text/html\n\n";
 print "<HTML><HEAD><TITLE>$N_R</TITLE></HEAD>\n";
 print "<BODY bgcolor=black text=yellow><center>\n";
 print "<BR><BR><H2>You [$USER_DIR] are out of room.</H2><br>\n";
 print "<br><br>\n";
 print "Have a nice day!<br><br>\n";
 print "</CENTER></BODY></HTML>\n";

 exit;   }

######################## The end of window.cgi ################
