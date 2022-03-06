#!/usr/local/bin/perl -U

################ GET QUERY SRTING #################################
 if ($ENV{'QUERY_STRING'})  {
 $INFO = $ENV{'QUERY_STRING'};
 ($QDATA1, $QDATA2, $QDATA3) = split (/\&/, $INFO, 3);
 $FORM{'name'} = $QDATA2;
 $FORM{'color'} = $QDATA3;
 $FORM{'room'} = $QDATA1;
 $FORM{'message'} = "Hello there?";
 $FORM{'user'} = "all";
                            }
######################################################
 else {
  read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'}); 
  @pairs = split(/&/, $buffer); 
  foreach $pair (@pairs)  {
    ($name, $value) = split(/=/, $pair);
    $value =~ tr/+/ /; 
    $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

  ### "|" Filtering
    $value =~ s/\|/\&\#124\;/g; 
    $FORM{$name} = $value;        }       }
  
   $FORM{'message'} =~ s/<([^>]|\n)*>//g; 
   $FORM{'name'} =~ s/\ /_/g;
   $FORM{'name'} =~ s/\.|\,|\:|\;|\|<|\>|\"|\^|\$|\@|\{|\}|\]|\~|\`|\[|\%|\?|\*/_/g;

  $date = `date +"%a,%m/%d %I:%M:%S"`; chop ($date);
  $USER_DIR = $FORM{'name'};
  $window = "./Rooms/$FORM{'room'}/Users/$USER_DIR/msg.txt";
  $cgi_url = "./tool.cgi";
  $MY_DIR = "./Rooms/$FORM{'room'}";

  if (!$FORM{'owner'}) {  $OWNER = `cat ./Rooms/$FORM{'room'}/owner.info`;
  $FORM{'owner'} = $OWNER if ($FORM{'name'} eq $OWNER);  }

&go_out if ($FORM{'command'} eq 'go_out');
&kick_out if ($FORM{'command'} eq 'kick_out'); 
&change_owner if ($FORM{'change_owner'});  
&main_work;

############## Start Main Work ############################

sub main_work {

  if ($FORM{'message'})  {

 if ($FORM{'user'} eq 'all')  {
  $user_d = `ls $MY_DIR/Users/`;
  @Num = split (/\n/, $user_d); 
  foreach $users_name(@Num) {

  $target_file = "$MY_DIR/Users/$users_name/msg.txt";
  open (MSG_DATA,">>$target_file"); 
  print MSG_DATA "<font color=$FORM{'color'}>$FORM{'name'}: $FORM{'message'}</font><br>\n"; 
  close (MSG_DATA);  }      }

  else { $target_file = "$MY_DIR/Users/$FORM{'user'}/msg.txt";
  open (MSG_DATA,">>$target_file"); 
  print MSG_DATA "<font color=$FORM{'color'}>\#Whisper! $FORM{'name'} : $FORM{'message'}</font><br>\n"; 
  close (MSG_DATA);

  $self_file = "$MY_DIR/Users/$FORM{'name'}/msg.txt"; 
  open (MSG_DATA,">>$self_file"); 
  print MSG_DATA "<font color=$FORM{'color'}>\#To $FORM{'user'} : $FORM{'message'}</font><br>\n";
  close (MSG_DATA); 
    }          }

  print "Content-type: text/html\n\n";
  print "<HTML><HEAD><TITLE>WWW Chat 2.0</TITLE>\n";
  print "<SCRIPT>\n";
  if (!$FORM{'message'}) {
  print "<!--  Copyright\(C\) 1997 DAE-HYUN PAIK All Rights Reserved\n";
  print "function openWin\(\)\n";
  print "\{\n";
  print "window.open\(\'window.cgi?$FORM{'room'}\&$FORM{'name'}\',\'MSG\');\n";
  print "\}\n";
  print "\/\/ Copyright\(C\) 1997 DAE-HYUN PAIK All Rights Reserved-->\n";
  print "openWin\(\)\;\n";
                          }
  print " <\!-- \n";
  print "function Pointer\(\) \{\n";
  print "document.chat.message.focus\(\)\;\n";
  print "return\;\n";
  print "\}\n";
  print "\/\/-->\n";
  print "</SCRIPT></HEAD>\n";
  print "<BODY BGCOLOR=C9CABD onLoad=\"Pointer\(\)\"><center>";
  print "<form name=\"chat\" method=post action=$cgi_url><input type=text name=message size=60 maxlength=100>";
  print "<input type=hidden name=name value=$FORM{'name'}>\n";
  print "<input type=hidden name=room value=$FORM{'room'}>\n";
  print "<input type=hidden name=color value=$FORM{'color'}>\n";
  print "<input type=hidden name=owner value=$FORM{'owner'}>\n" if ($FORM{'owner'}); 
  print "<select name=user><option selected value=all>Say to all\n";

  $user_d = `ls $MY_DIR/Users/`; 
  @Num = split (/\n/, $user_d); 
  foreach $users_name(@Num) {
  print "<option value=$users_name>$users_name\n";        }
  print "</select>\n";
  print "<input type=submit value=\"Chat\"></form>\n";
  print "You are the owner of this room.<br>\n" if ($FORM{'owner'});

 if ($FORM{'owner'})  {
 print "<form method=post action=$cgi_url>\n";
 print "<input type=hidden name=command value=kick_out>\n";
 print "<input type=hidden name=name value=$FORM{'name'}>\n";
 print "<input type=hidden name=room value=$FORM{'room'}>\n";
 print "<input type=hidden name=color value=$FORM{'color'}>\n";
 print "<input type=hidden name=owner value=$FORM{'owner'}>\n"; 
 print "<select name=user><option selected value=\"\">Kick someone out\n"; 
 
  $user_d = `ls $MY_DIR/Users/`; 
  @Num = split (/\n/, $user_d); 
  foreach $users_name(@Num) {
  print "<option value=$users_name>$users_name\n";  }
  print "</select>\n";
  print "<input type=submit value=\"Kick out!\"></form>\n"; 
  print "<form method=post action=$cgi_url>";
  print "<input type=hidden name=name value=$FORM{'name'}>"; 
  print "<input type=hidden name=color value=$FORM{'color'}>"; 
  print "<input type=hidden name=room value=$FORM{'room'}>"; 
  print "<select name=change_owner><option selected value=\"\">Give someone the ownership\n"; 

  $user_d = `ls $MY_DIR/Users/`; 
  @Num = split (/\n/, $user_d); 
  foreach $users_name(@Num) {
  print "<option value=$users_name>$users_name\n";  }
  print "</select>\n"; 
  print "<input type=submit value=\"Give it!\"></form>\n"; 


                           }  
  print "If you leave this room, this room will be destroyed.<br><br>\n" if ($FORM{'owner'});
  print "<form method=post action=$cgi_url>";
  print "<input type=hidden name=name value=$FORM{'name'}>";
  print "<input type=hidden name=color value=$FORM{'color'}>";
  print "<input type=hidden name=room value=$FORM{'room'}>";
  print "<input type=hidden name=owner value=$FORM{'owner'}>\n" if ($FORM{'owner'}); 
  print "<input type=hidden name=command value=go_out><input type=submit value=";
  print "\"Leave this room\"></form><BR>\n";
  print "<br>

<form method=post action=$cgi_url>
<input type=hidden name=name value=$FORM{'name'}>
<input type=hidden name=room value=$FORM{'room'}>
<input type=hidden name=color value=$FORM{'color'}>\n";
  print "<input type=hidden name=owner value=$FORM{'owner'}>\n" if ($FORM{'owner'}); 
  print "
<select name=color><option selected value=black>Black<option value=green>
Green<option value=blue>Blue<option value=magenta>Magenta 
<option value=8B6508>Gold<option value=A020F0>Purple 
<option value=8B4513>Brown<option value=404040>Grey
<option value=EE1289>Pink<option value=FF4500>
Orange <option value=2F4F4F>Indian Grey</select>
<BR><INPUT TYPE=\"submit\" VALUE=\"Change the text color\"></FORM>

<br>\n";
  print "</CENTER></BODY></HTML>\n";
   &cut_tale;
   exit;        }

########################## SUB ROUTINE ###########################
sub cut_tale {

  $user_d = `ls $MY_DIR/Users/`; 
  @Num = split (/\n/, $user_d); 
  foreach $users_name(@Num) {
  $window_data = "$MY_DIR/Users/$users_name/msg.txt";

  open (FILE,"$window_data");  @LINES=<FILE>;  close(FILE); 
  $SIZE=@LINES; 
  if ($SIZE > 11) {
  open (MSGS,">$window_data"); 
  for ($i=0;$i<=$SIZE;$i++) {
  $_=$LINES[$i]; 
 ($Q1,$Q2) = split (/\:/, $LINES[0], 2); 
  if (/$Q1/) {
  print MSGS " ";    } 
  else { 
  print MSGS $_; } }
  close (MSGS);  } 
                          }
    }

############### GO OUT ###########
sub go_out     { 

  $user_d = `ls $MY_DIR/Users/`;
  @Member = split (/\n/, $user_d); 
  foreach $users_name(@Member) {
  $target_data = "$MY_DIR/Users/$users_name/msg.txt";
  open (MSG_DATA,">>$target_data");
  print MSG_DATA "<font color=red>SYSTEM</font>: \"$FORM{'name'} went out.\"<br>\n";
  close (MSG_DATA);  }

  system ("rm -r $MY_DIR/Users/$FORM{'name'}");
  system ("rm -r $MY_DIR/User_info/$FORM{'name'}.info");
  system ("rm -r $MY_DIR") if ($FORM{'owner'});

  &End_MSG;

      exit;  }

################################################################
sub kick_out {

  &ERROR if (!$FORM{'user'});

  $user_d = `ls $MY_DIR/Users/`; 
  @Member = split (/\n/, $user_d); 
  foreach $users_name(@Member) {
  $target_data = "$MY_DIR/Users/$users_name/msg.txt";
  open (MSG_DATA,">>$target_data");
  print MSG_DATA "<font color=red>SYSTEM
</font>: \"$FORM{'name'} kicked $FORM{'user'} out.\"<br>\n"; 
  close (MSG_DATA);        } 

  $kicked_user = "$MY_DIR/Users/$FORM{'user'}/msg.txt";

  open (KICKED_DATA, ">>$kicked_user");
  print KICKED_DATA "<font color=red>SYSTEM</font>: \"$FORM{'name'} kick you out.\"<br>\n"; 
  close (KICKED_DATA);

  sleep 5;

  system ("rm -r $MY_DIR/Users/$FORM{'user'}");
system ("rm -r $MY_DIR/User_info/$FORM{'user'}.info");

$FORM{'message'} = "\"You kicked $FORM{'user'} out!\"";
$FORM{'user'} = $FORM{'name'};
&main_work; exit; 

 }
##########################################################
 sub change_owner  {

$user_d = `ls $MY_DIR/Users/`; 
  @Member = split (/\n/, $user_d); 
  foreach $users_name(@Member) {
  $target_data = "$MY_DIR/Users/$users_name/msg.txt"; 
  open (MSG_DATA,">>$target_data"); 
  print MSG_DATA "<font color=red>SYSTEM</font>: \"$FORM{'name'} gave 
$FORM{'change_owner'} the ownership.<br>\n";
  close (MSG_DATA);  }

  $owner_data = "$MY_DIR/owner.info";

  open (OWNER_DATA, ">$owner_data");
  print OWNER_DATA "$FORM{'change_owner'}";
  close (OWNER_DATA);

$FORM{'message'} = "\"Gave the ownership!\"";  
$FORM{'user'} = $FORM{'name'};
$FORM{'owner'} = ""; 
&main_work; exit; 

     }
########################################
 sub End_MSG {
  print "Content-type: text/html\n\n";
  print "<HTML><HEAD>\n";
  print "<TITLE>Good bye!</TITLE></HEAD>\n";
  print "<script>\n";
  print "<!-- Copyright\(C\) 1997 DAE-HYUN PAIK All Rights Reserved\n"; 
  print "function openWin\(\)\n"; 
  print "\{\n"; 
  print "window.open\(\'out.html\',\'MSG\');\n"; 
  print "\}\n"; 
  print "\/\/ Copyright\(C\) 1997 DAE-HYUN PAIK All Rights Reserved-->\n"; 
  print "openWin\(\)\;\n"; 
  print "</script>\n";
  print "<body bgcolor=black text=806030><center>\n";
  print "You [ $FORM{'name'} ] are out of the room.[$FORM{'room'}]<br><br>\n";
  print "<form method=post action=\"index.cgi\" target=_parent>"; 
  print "<input type=hidden name=name value=$FORM{'name'}>"; 
  print "<input type=hidden name=color value=$FORM{'color'}>"; 
  print "<input type=hidden name=room value=$FORM{'room'}>"; 
  print "<input type=hidden name=command value=go_out><input type=submit value="; 
  print "\"Go back to the room list\"></form><BR>\n"; 
  print "<br></body></html>\n";

  exit;  }
###########################################
 sub ERROR {

  print "Content-type: text/html\n\n"; 
  print "<HTML><HEAD>\n"; 
  print "<TITLE>ERROR</TITLE></HEAD>\n"; 
  print "<H1>ERROR!</H1><br>\n";
  print "</HTML>\n";

  exit;  }
############################ THE END #######################
