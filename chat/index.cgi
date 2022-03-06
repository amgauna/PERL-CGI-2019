#!/usr/local/bin/perl -U

  read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'}); 
  @pairs = split(/&/, $buffer); 
  foreach $pair (@pairs)  {
    ($name, $value) = split(/=/, $pair);
    $value =~ tr/+/ /; 
    $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

  ### "|" Filtering
    $value =~ s/\|/\&\#124\;/g; 
    $FORM{$name} = $value;      }

   $FORM{'message'} =~ s/<([^>]|\n)*>//g; 
   $FORM{'name'} =~ s/\ /_/g;
   $FORM{'name'} =~ s/\.|\,|\:|\;|\|<|\>|\"|\^|\$|\@|\{|\}|\]|\~|\`|\[|\%|\?|\*/_/g;

  $date = `date +"%a,%m/%d %I:%M:%S"`; chop ($date);
  $cgi_url = "./index.cgi";
######################## Delete some old rooms #################
system ("find ./Rooms/* -ctime +1 -exec rm -r \{\} \\;");
#####################################################

&waiting_room if ($FORM{'name'});

#########################################################
  print "Content-type: text/html\n\n";
  print "<HTML><HEAD><TITLE>WWWChat 3.0</TITLE></HEAD>";
  print "<BODY BGCOLOR=C9CABD text=444444>\n";
  print "<CENTER><font size=+2>WWWChat 3.0 created by Dae-hyun Paik</font><br><br>\n";
  print "You should use Netscape 3.0 or later version.<br><br>\n";

  $C_room = `ls ./Rooms/`; if ($C_room)  {
  print "Current Users<br>\n";
  print "<table border=2 cellpadding=4>\n";
  print "<tr align=center bgcolor=white><td>Room</td><td>User</td></tr>\n";
  @Num = split (/\n/, $C_room); 
  foreach $room_name(@Num) {
  print "<tr><td>$room_name</td><td>\n"; 
  $user_name = `ls ./Rooms/$room_name/Users/`; 
  @MMM = split (/\n/, $user_name); 
  foreach $user(@MMM) { 
  print "$user  ";   }
  print "</td></tr>\n";  }     
  print "</table><br><br>\n";   }
  else { print "No one is here.<br><br>\n";  }

  print "Choose your Nickname and color.<BR>\n";
  print "<table border=0 cellpadding=3 cellspacing=4><tr align=center>";
  print "<td><form method=post action=$cgi_url target=_self>\n";
  print "<input type=hidden name=command value=new>";
  print "Nickname : <input method=text name=\"name\" size=12 maxlength=15></td>\n";
  print "
<td><select name=color><option selected value=black>Black<option value=green>
Green<option value=blue>Blue<option value=magenta>Magenta
<option value=8B6508>Gold<option value=A020F0>Purple<option value=8B4513>Brown
<option value=404040>Grey<option value=EE1289>Pink<option value=FF4500>Orange
<option value=2F4F4F>Indian Grey</select></td>
<td><BR><INPUT TYPE=\"submit\" VALUE=\"Join\"></FORM></td></tr></table>
</BODY></HTML>\n";

  exit;

####### SUB WAIT ROOM #######
sub waiting_room  {

  print "Content-type: text/html\n\n";
  print "<HTML><HEAD><TITLE>WWWChat 3.0 [Room List]</TITLE></HEAD>";
  print "<body bgcolor=black text=907030 link=yellow vlink=F0A0A0>\n";
  print "<CENTER><font size=+2>Room List</font><hr>\n";
  print "<table border=2><tr align=center><td>Room</td><td>Users</td><td>Topic</td></tr>\n";

 $room_d = `ls ./Rooms/`; 
  @Num = split (/\n/, $room_d); 
  foreach $room_name(@Num) {
  $HOW_MANY = `ls ./Rooms/$room_name/Users`;
   @people = split (/\n/, $HOW_MANY);
  $USERS = @people;
  $topic = `cat ./Rooms/$room_name/topic.txt`;
print "<tr align=center><td><a 
href=chat.cgi?$room_name\&$FORM{'name'}\&$FORM{'color'}>$room_name</a></td><td>$USERS</td><td>$topic</td><tr>\n";
                   }

print "</table><br>\n";

print "<hr><br><font size=+2>Make a new room</font><br><br>\n";
print "If the owner leave the room, the room will be deleted.<br>
Just give the ownership to another user when you leave the room.<br>
<table><tr><td>
<form method=post action=make.cgi>
Room Name :</td><td> <input type=text size=10 maxlength=20 name=room_name></td></tr><tr><td>
Topic :</td><td> <input type=text size=30 maxlength=40 name=topic></td></tr><tr><td>
<input type=hidden name=color value=$FORM{'color'}>
<input type=hidden name=name value=$FORM{'name'}></td><td>
<input type=submit value=\"Make a new room\"></form></td></tr></table>
<br><hr>
<br><br>
\n";

exit;   }


