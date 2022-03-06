#!/usr/local/bin/perl -U

###########TIME for LOG File#############
  $date = `date +"%a,%m/%d %I:%M:%S"`; chop ($date);
#####################
read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
  @pairs = split(/&/, $buffer);
  foreach $pair (@pairs)
  {
    ($name, $value) = split(/=/, $pair);
    $value =~ tr/+/ /;
    $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
    
### "|" Filtering
    $value =~ s/\|/\&\#124\;/g;
    $FORM{$name} = $value;
      }

### HTML TAG Filtering for name, subject and email.
  $FORM{'room_name'} =~ s/<([^>]|\n)*>//g;
  $FORM{'name'} =~ s/<([^>]|\n)*>//g;
  $FORM{'room_name'} =~ s/\ /_/g;
  $FORM{'room_name'} =~ s/\.|\,|\:|\;|\|<|\>|\"|\^|\$|\@|\{|\}|\]|\~|\`|\[|\%|\?|\*/_/g; 
  $FORM{'name'} =~ s/\ /_/g;
  $FORM{'name'} =~ s/\.|\,|\:|\;|\|<|\>|\"|\^|\$|\@|\{|\}|\]|\~|\`|\[|\%|\?|\*/_/g;
###########################################
  &no_input unless $FORM{'name'};
  &no_input unless $FORM{'room_name'};
  &no_input unless $FORM{'topic'};

##################
  $ROOM_DIR = "./Rooms/$FORM{'room_name'}";
  system ("mkdir $ROOM_DIR");
  system ("chmod a+wrx $ROOM_DIR");
  system ("mkdir $ROOM_DIR/Users");
  system ("chmod a+wrx $ROOM_DIR/Users");
  system ("mkdir $ROOM_DIR/User_info");
  system ("chmod a+wrx $ROOM_DIR/User_info");
  system ("mkdir $ROOM_DIR/Users/$FORM{'name'}");
  system ("chmod a+wrx $ROOM_DIR/Users/$FORM{'name'}");
###################################################
  $msg_file = "$ROOM_DIR/Users/$FORM{'name'}/msg.txt";
  open (MSG_DATA,">$msg_file"); 
  print MSG_DATA "<font color=red>SYSTEM</font>: $FORM{'name'} made a room.<br>\n"; 
  close (MSG_DATA);
  system ("chmod a+wrx $msg_file");
###################################################
  $target_file = "$ROOM_DIR/owner.info";
  open (OWNER_DATA,">$target_file"); 
  print OWNER_DATA "$FORM{'name'}"; 
  close (OWNER_DATA);
##################################################
 $user_info = "$ROOM_DIR/User_info/$FORM{'name'}.info";
  open (USER_DATA,">$user_info"); 
  print USER_DATA "$FORM{'name'}:[$date]:$ENV{'REMOTE_HOST'}<br>"; 
  close (USER_DATA);
##########################################################
 $topic_file = "$ROOM_DIR/topic.txt"; 
  open (T_DATA,">$topic_file"); 
  print T_DATA "$FORM{'topic'}"; 
  close (T_DATA); 

###################################################################
  sub no_input
   {
    print "Content-type: text/html\n\n";
    print "<HTML><HEAD><TITLE>Error!</TITLE></HEAD>\n";
    print "<BODY BGCOLOR=FFFFFF><center><h1>You didn't fill all out.</h1>\n";
    print "<BR><BR><BR>Please get back and enter all of them.\n";
    print "</center></BODY></HTML>\n";

    exit;   }
################################################
    print "Content-type: text/html\n\n";
    print "<HTML><HEAD>
<TITLE>A room was created</TITLE></HEAD>
<body bgcolor=C9CABD><br><br><br><center>
You have created a room [$FORM{'room_name'}]<br><br><BR><BR>
<a href=chat.cgi?$FORM{'room_name'}\&$FORM{'name'}\&$FORM{'color'}>[ Join the room ]</a><br>

\n";
exit;
########################## END #####
