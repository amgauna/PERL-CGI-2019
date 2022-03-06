#!/usr/local/bin/perl -U

  $date = `date +"%a,%m/%d %I:%M:%S"`; chop ($date);


  print "Content-type: text/html\n\n";
  print "<HTML><HEAD>\n";
  print "<TITLE>User Info</TITLE></HEAD>\n";
  print "<BODY bgcolor=C9CABD><center><FONT size=-1>\n";
  print "Current users Info ($date)<br><br></center>\n";

  $ROOMS = `ls ./Rooms/`; 
  @Num = split (/\n/, $ROOMS); 
  foreach $room_name(@Num) {
  $owner = `cat ./Rooms/$room_name/owner.info`;
  
  print "[Room: $room_name] [Owner: <font color=green>$owner</font>]<br>\n";
  
  $USERS = `ls ./Rooms/$room_name/Users/`;
  @GOGO = split (/\n/, $USERS);
  foreach $user_name(@GOGO)  {
  $U_DATA = `cat ./Rooms/$room_name/User_info/$user_name.info`;
  print "$user_name$U_DATA<br>\n";   }
  print "<HR>\n";   }

  print "<BR><center>
<form method=post action=./user.cgi>
<input type=submit value=\"Update\">
</form>
<br>
This information is not automatically updated.<br> 
You can push the \"Update\" button to see the new users.<br><br>
</font>
</center></body></html>\n";

  exit;
############################ THE END #######################

