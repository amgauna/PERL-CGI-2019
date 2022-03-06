#!/usr/local/bin/perl -U

  $date = `date +"%a,%m/%d %I:%M:%S"`; chop ($date); 

  $INFO = "$ENV{'QUERY_STRING'}";

  ($QDATA1, $QDATA2, $QDATA3) = split(/\&/, $INFO, 3);
  
  system ("mkdir ./Rooms/$QDATA1/Users/$QDATA2");
  system ("chmod a+wrx ./Rooms/$QDATA1/Users/$QDATA2"); 

  $FIRST_MSG = "./Rooms/$QDATA1/Users/$QDATA2/msg.txt"; 
  open (M_DATA,">$FIRST_MSG"); 
  print M_DATA "  "; 
  close (M_DATA);
  system ("chmod a+wrx $FIRST_MSG");

  $user_info = "./Rooms/$QDATA1/User_info/$QDATA2.info";
  $CHECK = `cat $user_info`;
  if (!$CHECK)   {
  open (USER_DATA,">$user_info"); 
  print USER_DATA ":$QDATA2 [$date]:$ENV{'REMOTE_HOST'}<br>\n"; 
  close (USER_DATA);   }




$user_d = `ls ./Rooms/$QDATA1/Users/`; 
  @Num = split (/\n/, $user_d); 
  foreach $users_name(@Num) {
 
  $greeting = "./Rooms/$QDATA1/Users/$users_name/msg.txt";


 open (MSG_DATA,">>$greeting"); 
 print MSG_DATA "<font color=red>SYSTEM</font>: \"$QDATA2 has joined.\"($ENV{'REMOTE_HOST'}) $date<br>\n";
 close (MSG_DATA);  }

 system ("chmod a+rwx $greeting"); 

print "Content-type: text/html\n\n";
print "
<HTML> <HEAD> 
<TITLE>WWWChat 3.0 : Room [ $QDATA1 ]</TITLE>
</HEAD>
<FRAMESET rows=\"*, 100, 100\" BORDER=\"3\" BORDERCOLOR=black>
<FRAME Name=\"MSG\" SRC=\"window.cgi?$QDATA1&$QDATA2\" Scrolling=Auto>
<FRAME Name=\"tool\" SRC=\"tool.cgi?$INFO\" Scrolling=Auto>
<FRAME Name=\"INFO\" SRC=\"user.cgi\" Scrolling=Auto>
</FRAMESET>
</HTML>
\n";
exit;
