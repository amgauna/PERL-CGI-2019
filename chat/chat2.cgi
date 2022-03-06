#!/usr/bin/perl

require config; 

# HTML Part
########################


#REGISTER.HTML - Printed when user registers new nick
sub register_html {
    print <<"[END]";
<HTML>
<HEAD><TITLE>$html_title - registrar novo apelido</TITLE></HEAD>
$html_bodytag
<CENTER>
<H1><I>Registrar novo apelido</I></H1>
<FORM METHOD=POST ACTION="$script2_name">
<INPUT TYPE=HIDDEN NAME="action" VALUE="create_nick">
<TABLE><TR><TD>
<B>Novo apelido: </B></TD><TD><INPUT NAME="name"><BR></TD></TR>
<TR><TD><B>Senha:</B> </TD><TD><INPUT TYPE=PASSWORD NAME="password"><BR></TD></TR>
<TR><TD><B>Confirme a senha:</B> </TD><TD><INPUT TYPE=PASSWORD NAME="password2"><BR></TD></TR>
<TR><TD><B>eMail:<BR> (somente para administra��o)</B> </TD><TD><INPUT NAME="email"><BR>
</TD></TR></TABLE>
<INPUT TYPE=SUBMIT VALUE="registrar">
</FORM>
</CENTER>
</BODY>
</HTML>
[END]
}

#BANNER.HTML - the banner on the top - You may change or remove it!
sub banner_html {
    print <<"[END]";
<HTML>$html_bodytag
<CENTER>
<A HREF="$banner_link"><IMG SRC="$banner_picture" BORDER=0></A>
</CENTER>
</BODY></HTML>
[END]
}

#OPTIONS.HTML - the options page
sub options_html {
    print <<"[END]";
<HTML><HEAD><TITLE>$html_title - Op��es</TITLE></HEAD>
$html_bodytag
<CENTER>
<H1><I>Op��es</I></H1>
<FORM METHOD=POST ACTION="$script2_name">
<INPUT TYPE=HIDDEN NAME="action" VALUE="setoptions">
<INPUT TYPE=HIDDEN NAME="name" VALUE="$query{'name'}">
<INPUT TYPE=HIDDEN NAME="password" VALUE="$query{'password'}">
<TABLE>
<TR><TD>Atualiza��o em X segundos: </TD><TD><INPUT SIZE="10" NAME="updatefrequency" VALUE=$query{'updatefrequency'}></TD></TR>
<TR><TD>Cor da Fonte:</TD><TD><SELECT NAME="color">
<OPTION SELECTED VALUE="$query{'color'}">atual</OPTION>
<OPTION VALUE="standard">padr�o</OPTION>
<OPTION VALUE="standard">--------</OPTION>
<OPTION VALUE="0000FF">azul</OPTION>
<OPTION VALUE="008000">verde</OPTION>
<OPTION VALUE="FF0000">vermelho</OPTION>
<OPTION VALUE="000000">preto</OPTION>
<OPTION VALUE="FFFFFF">branco</OPTION>
<OPTION VALUE="800000">maroon</OPTION>
<OPTION VALUE="808000">olive</OPTION>
<OPTION VALUE="000080">navy</OPTION>
<OPTION VALUE="800080">purple</OPTION>
<OPTION VALUE="808080">cinza</OPTION>
<OPTION VALUE="C0C0C0">prata</OPTION>
<OPTION VALUE="00FF00">lime</OPTION>
<OPTION VALUE="FFFF00">amarelo</OPTION>
<OPTION VALUE="FF00FF">fuchsia</OPTION>
<OPTION VALUE="00FFFF">aqua</OPTION>
<OPTION VALUE="008080">teal</OPTION>
</SELECT></TD></TR>
<TR><TD>Ordem das mensagens</TD><TD><SELECT NAME="new_msg_on_top">
<OPTION VALUE="$query{'new_msg_on_top'}" SELECTED>atual</OPTION>
<OPTION VALUE="1">novas no topo</OPTION>
<OPTION VALUE="0">novas no final</OPTION>
</SELECT></TD></TR>
<TR><TD><H3>Trocar a Senha</H3></TR></TD>
<TR><TD>Senha antiga: </TD><TD><INPUT TYPE=PASSWORD NAME="change_pwd_old"></TD></TR>
<TR><TD>Nova senha: </TD><TD><INPUT TYPE=PASSWORD NAME="change_pwd_new"></TD></TR>
<TR><TD>Confirme nova senha : </TD><TD><INPUT TYPE=PASSWORD NAME="change_pwd_new2"></TD></TR>
</TABLE>
<INPUT TYPE=SUBMIT VALUE="configurar">
</FORM>
</CENTER></BODY></HTML>
[END]
}


#USERINFO.HTML - informations about the users, click on user in online list
sub userinfo_html {
    print <<"[END]";
<HTML>
<HEAD><TITLE>$html_title - Informa��es de usu�rio</TITLE>
</HEAD>
$html_bodytag
<CENTER>
<H1><I>Informa��es do usu�rio</I></H1>
[END]

    print "<TABLE><TR><TD VALIGN=top><IMG SRC=\"$userinfo{'photo_url'}\"></TD><TD VALIGN=top>" if ($userinfo{'photo_url'} ne "");
    print "<TABLE>";
    print "<TR><TD><B>apelido</B>:</TD><TD>$query{'infoabout'}</TD></TR>";
    print "<TR><TD><B>nome real</B>:</TD><TD>$userinfo{'realname'}</TD></TR>";
    print "<TR><TD><B>email</B>:</TD><TD><A HREF=\"mailto:$userinfo{'email'}\">$userinfo{'email'}</A></TD></TR>";
    print "<TR><TD><B>idade</B>:</TD><TD>$userinfo{'age'}</TD></TR>";
    print "<TR><TD><B>cidade</B>:</TD><TD>$userinfo{'city'}</TD></TR>";
    print "<TR><TD><B>pais</B>:</TD><TD>$userinfo{'country'}</TD></TR>";
    print "<TR><TD><B>homepage url</B>:</TD><TD><A HREF=\"$userinfo{'url'}\">$userinfo{'url'}</A></TD></TR>";
    print "<TR><TD><B>ICQ uin</B>:</TD><TD>$userinfo{'icq_uin'}</TD></TR>";
    print "<TR><TD VALIGN=top><B>Outras informa��es</B>:</TD><TD>$userinfo{'stuff'}</TD></TR>";
    print "</TABLE>";
    print "</TD></TR></TABLE>" if ($userinfo{'photo_url'} ne "");

    print <<"[END]";
</CENTER>
</BODY>
</HTML>
[END]
}

#CHANGEUSERINFO.HTML - change user informations
sub changeuserinfo_html {
    print <<"[END]";
<HTML>
<HEAD><TITLE>$html_title - Informa��es do usu�rio</TITLE>
</HEAD>
$html_bodytag
<CENTER>
<H1><I>Informa��es do usu�rio</I></H1>
<TABLE>
<FORM METHOD=POST ACTION="$script2_name">
<INPUT TYPE=hidden NAME="action" VALUE="setuserinfo">
<INPUT TYPE=HIDDEN NAME="name" VALUE="$query{'name'}">
<INPUT TYPE=HIDDEN NAME="password" VALUE="$query{'password'}">
<INPUT TYPE=HIDDEN NAME="color" VALUE="$query{'color'}">
<INPUT TYPE=HIDDEN NAME="new_msg_on_top" VALUE="$query{'new_msg_on_top'}">
<INPUT TYPE=HIDDEN NAME="updatefrequency" VALUE="$query{'updatefrequency'}">
<TR><TD><B>Nome completo</B>:</TD><TD><INPUT NAME="realname" VALUE="$userinfo{'realname'}"></TD></TR>
<TR><TD><B>email</B>:</TD><TD><INPUT NAME="email" VALUE="$userinfo{'email'}"></TD></TR>
<TR><TD><B>Pais</B>:</TD><TD><INPUT NAME="country" VALUE="$userinfo{'country'}"></TD></TR>
<TR><TD><B>Cidade</B>:</TD><TD><INPUT NAME="city" VALUE="$userinfo{'city'}"></TD></TR>
<TR><TD><B>Idade</B>:</TD><TD><INPUT NAME="age" VALUE="$userinfo{'age'}"></TD></TR>
<TR><TD><B>Homepage(url)</B>:</TD><TD><INPUT NAME="url" VALUE="$userinfo{'url'}"></TD></TR>
<TR><TD><B>Foto(url) </B>:</TD><TD><INPUT NAME="photo_url" VALUE="$userinfo{'photo_url'}"></TD></TR>
<TR><TD><B>ICQ uin</B>:</TD><TD><INPUT NAME="icq_uin" VALUE="$userinfo{'icq_uin'}"></TD></TR>
<TR><TD VALIGN=top><B>Outras informa��es</B>:</TD><TD><TEXTAREA ROWS=10 COLS=50 NAME="stuff">$userinfo{'stuff'}</TEXTAREA></A></TD></TR>
</TABLE>
<INPUT TYPE=SUBMIT VALUE="entrar informa��es"></FORM>
</CENTER>
</BODY>
</HTML>
[END]
}

#SCRIPTLINKS.HTML - Links to other chatscripts
sub scriptlinks_html {
    print <<"[END]";
<HTML>$html_bodytag
<A HREF="chat2.cgi?action=login&name=$query{'name'}&password=$query{'password'}" TARGET="_top">chat 2</A>
</BODY></HTML>
[END]
}

#ILLEGAL_NICK.HTML - when nick containing illegal characters is created
sub illegal_nick_html {
    print <<"[END]";
<HTML><HEAD><TITLE>Apelido ilegal</TITLE></HEAD>
$html_bodytag
<CENTER>
<H1><I>Apelido Ilegal</I></H1>
<B>Seu apelido "$query{'name'}" contem caracteres ilegais<BR>A Nick may contain only letters, numbers and the underdash "_".</B>
<BR><B><A HREF="$script2_name?action=register">tentar novamente</A></B>
</CENTER></BODY></HTML>
[END]
}

#ILLEGAL_PASS.HTML - when nick with password containing illegal characters is created
sub illegal_pass_html {
    print <<"[END]";
<HTML>
<HEAD><TITLE>$html_title - Senha ilegal</TITLE>
</HEAD>
$html_bodytag
<CENTER>
<H1><I>Senha ilegal</I></H1>
<B>A senha n�o pode conter ";"</B><BR>
<B><A HREF="$script2_name?action=register">tentar novamente</A></B>
</CENTER>
</BODY>
</HTML>
[END]
}

#PASS_CHECK_FAILED_HTML - when password is different from password 2
sub pass_check_failed_html {
    print <<"[END]";
<HTML>
<HEAD><TITLE>$html_title - Password Check Falhou</TITLE>
</HEAD>
$html_bodytag
<CENTER>
<H1><I>A verifica��o de senha Falhou</I></H1>
<B>As senhas que voc� entrou n�o s�o iguais</B><BR>
<B><A HREF="$script2_name?action=register">tentar novamente</A></B>
</CENTER>
</BODY>
</HTML>
[END]
}

#EXISTINGNICK.HTML - Nick already exists
sub existingnick_html {
    print <<"[END]";
<HTML>
<HEAD><TITLE>$html_title - Este apelido j� existe</TITLE>
</HEAD>
$html_bodytag
<CENTER>
<H1><I>Este apelido j� existe</I></H1>
<A HREF="$script2_name?action=register"><B>tente outro apelido</B></A>
</CENTER>
</BODY>
</HTML>
[END]
}

#NICKCREATED.HTML - after nick is registered
sub nickcreated_html {
    print <<"[END]";
<HTML>
<HEAD><TITLE>$html_title - Seu apelido agora est� registrado</TITLE>
</HEAD>
$html_bodytag
<CENTER>
<H1><I>Seu apelido agora est� registrado</I></H1>
<B><A HREF="$script_name">ENTRAR</A></B>
</CENTER>
</BODY>
</HTML>
[END]
}

#CHATFRAMES.HTML
sub chatframes_html {
	print "<HTML><HEAD><TITLE>$html_title</TITLE></HEAD>\n";
	if ($banner_picture) {
		print " <FRAMESET ROWS=\"65,*,60\" BORDER=0 FRAMEBORDER=0 FRAMESPACING=0>\n"
	} else {
		print " <FRAMESET ROWS=\"*,60\" BORDER=0 FRAMEBORDER=0 FRAMESPACING=0>\n"
	}
	print "  <FRAME SRC=\"$script2_name?action=banner\" SCROLLING=NO>\n" if ($banner_picture);
	print "  <FRAMESET COLS=\"*,150\" BORDER=0 FRAMEBORDER=0 FRAMESPACING=0>\n";
	print "   <FRAME NAME=\"main\" SRC=\"$script_name?action=chat&name=$query{'name'}&password=$query{'password'}&updatefrequency=$query{'updatefrequency'}&color=$query{'color'}&new_msg_on_top=$query{'new_msg_on_top'}#end\">  \n";
#	print "	   <FRAMESET ROWS=\"*,100\" BORDER=0 FRAMEBORDER=0 FRAMESPACING=0> \n"; #UNCOMMENT IF YOU WANT MULTIPLE SCRIPT SUPPORT
	print "    <FRAME SRC=\"$script_name?action=stillalive&name=$query{'name'}&password=$query{'password'}&updatefrequency=$query{'updatefrequency'}&color=$query{'color'}&new_msg_on_top=$query{'new_msg_on_top'}\">    \n";
#	print "    <FRAME SRC=\"$script2_name?action=scriptlinks&name=$query{'name'}&password=$query{'password'}\" scrolling=auto>\n"; #UNCOMMENT IF YOU WANT MULTIPLE SCRIPT SUPPORT
	print "   </FRAMESET>\n";
#	print "  </FRAMESET>\n"; #UNCOMMENT IF YOU WANT MULTIPLE SCRIPT SUPPORT
	print "  <FRAME SRC=\"$script_name?action=chatinput_html&name=$query{'name'}&password=$query{'password'}&updatefrequency=$query{'updatefrequency'}&color=$query{'color'}&new_msg_on_top=$query{'new_msg_on_top'}\" scrolling=no>\n";
	print "</FRAMESET>\n";
	print "</HTML>\n";
}

#CHAT_IS_FULL.HTML - when chat room is full
sub chat_is_full_html {
    print <<"[END]";
<HTML>
<HEAD><TITLE>$html_title - Chat cheio</TITLE>
</HEAD>
$html_bodytag
<CENTER>
<H1><I>o Chat est� cheio</I></H1>
Sorry, the chat room is full, please try another room or come back another time.
You can login anyway if you login with the password "yourpassword masterpassword".
<BR><A HREF="$script_name">back</A></B>
</CENTER>
</BODY>
</HTML>
[END]
}

sub send_pwd_html {
    print <<"[END]";
<HTML>
<HEAD><TITLE>$html_title - Lost Password</TITLE>
</HEAD>
$html_bodytag
<CENTER>
<H1><I>Send Password</I></H1>
A senha foi enviada para voc� ($query{'email'}).<BR>
<BR><A HREF="$script_name">voltar</A></B>
</CENTER>
</BODY>
</HTML>
[END]
}

# Main Part - DON'T CHANGE ANYTHING HERE!
#
#######################



&action;    # Fuehrt je nach action variable gegebene sub aus
	    # action im FORM definieren!

exit;

sub action {
    if ($qs eq "") { # Wenn query_string leer sprung zum
    	&error("dont't execute this file, run chat.cgi instead");
    } 
    elsif ($query{'action'} eq "register") {
        &header;
        &register_html;
    }
    elsif ($query{'action'} eq "login") {
    	&login;
    }
    elsif ($query{'action'} eq "create_nick") {
    	&create_nick;
    }
    elsif ($query{'action'} eq "banner") {
        &header;
        &banner_html;
    }
    elsif ($query{'action'} eq "options_html") {
        &header;
        &options_html;
    }
    elsif ($query{'action'} eq "setoptions") {
        &setoptions;
    }
    elsif ($query{'action'} eq "gotourl") {
        &gotourl;
    }
    elsif ($query{'action'} eq "userinfo") {
        &userinfo;
    }
    elsif ($query{'action'} eq "changeuserinfo") {
        &changeuserinfo;
    }
    elsif ($query{'action'} eq "setuserinfo") {
        &setuserinfo;
    }
    elsif ($query{'action'} eq "show_users") {
        &show_users;
    }
    elsif ($query{'action'} eq "scriptlinks") {
        &header;
        &scriptlinks_html;
    }
    elsif ($query{'action'} eq "send_pwd") {
        &send_pwd;
    }
    else {
    	&error;
    } 
}


sub login { # Loginprozedur 
    # check login name+password
    if (-e "$data_dir/$data_nicks_file") {  # wenn nickfile existiert dann oeffnen
    	open (NICKFILE, "<$data_dir/$data_nicks_file") || &error("::open $data_dir/$data_nicks_file failed::");
    } 
    else {  # sonst nonick_html
    	&header;
    	&nonick_html;
	    exit;
    }

    # check if ip is banned
    {
    open (BANFILE, "<$data_dir/$data_banned_file");
    my $banfile = <BANFILE>;
    my @banfiletemp = split(/;;/, $banfile);
    for (@banfiletemp){
        if ("ip:".$ENV{'REMOTE_ADDR'} eq $_) {
            &header;
            &banned_html;
            exit;
        }
    }
    }

    &max_user_limit; # check if chat is full

    my @nickfile = <NICKFILE>; # Daten aus nickfile an @nickfile uebergeben
    close NICKFILE; # nickfile schliessen
    
    &make_matrix(@nickfile); # nickfile -> matrix
    
    for ($i=0; $i<=$#matrix; $i++) {
        if (uc($matrix[$i][0]) eq uc($query{'name'})) { # compare nicks with uppercases
            $query{'name'} = $matrix[$i][0] if ($matrix[$i][0] ne $query{'name'}); # if nicks are different, because of some upper cases use the version in the nickfile

            if ($matrix[$i][1] eq $query{'password'}) {
                # update last visited var
                $matrix[$i][4] = time;
                # set ip
                $matrix[$i][11] = $ENV{'REMOTE_ADDR'};                            

                #set unkicked if user was kicked
                $matrix[$i][10] = 0 if ($matrix[$i][10] == 1);

                #check if user is banned
                if ($matrix[$i][10] == 2) {
                    close NICKFILE;
                    &header;
                    &banned_html;
                    exit;
                }

                if ($clear_old_msgs == 1) {
                    &clear_old_msgs_sub;
                }

                if ($matrix[$i][5] ne "") {
                    $query{'updatefrequency'} = $matrix[$i][5];
                    $query{'color'} = $matrix[$i][6];
                    $query{'new_msg_on_top'} = $matrix[$i][9];
                } else {
                    $query{'updatefrequency'} = $updatefrequency;
                    $query{'color'} = "standard";
                    $query{'new_msg_on_top'} = $new_msg_on_top;
                }

				#post welcome msg
                if ($welcome_msg ne "") {
                    &postprivatemsg($query{'name'}, "BEM-VINDO", $welcome_msg);
                    #print login msg
                    open (CHATFILE, ">>$data_dir/$data_msg_file");
                    flock(CHATFILE,2);
                    print CHATFILE "<B>".$query{'name'}." ".$login_msg."</B>\n";
                    close CHATFILE;
                }

				# check memos
				&check_for_memo($matrix[$i][12]) if ($matrix[$i][12] > 0);
				$matrix[$i][12] = 0;

                open (NICKFILE, ">$data_dir/$data_nicks_file");
                flock(NICKFILE,2);
                
                for ($i2=0; $i2<=$#matrix; $i2++) {
                    print NICKFILE &join_matrix."\n";
                }

#                flock(NICKFILE,8);
                close NICKFILE;

                &enterchat;    # wenn beides richtig goto chat
                exit;	       # danach prozedur verlassen
            } else {
                &header;
                &wrongpass_html;
                exit;
            }
        }
    }
    
    # falls nick falsch nonick_html
    &header;
    &nonick_html;
}

sub enterchat {
    # LOG ACTION
    if ($logtype >= 2) {
        open (LOGFILE, ">>$log_dir/$log_file") || &error("::open $log_dir/$log_file failed::");
        flock(LOGFILE,2);
        print LOGFILE localtime(time)." $ENV{'REMOTE_ADDR'} [LOGIN] $query{'name'}\n";
        close LOGFILE;
    }
    &header;
    &chatframes_html;
}

sub validate_string { # params: 0: string to validate
    # alle strings die spaces, semikolons oder steuerzeichen enthalten
    if ($_[0] =~ /[\W]/ || $_[0] eq "") { 
        return 1; # illegal string
    } else {
        return 0; # legal string
    }
}

sub create_nick { # neuen nick anlegen + weiterleiten zum chat
    if (&validate_string($query{'name'}) == 1) { # ueberpruefen ob nick illegale Zeichen enthaelt
        &header;
        &illegal_nick_html;
        exit;
    };
    if ($query{'password'} =~ /;/ || !$query{'password'}) { # ueberpruefen ob password illegale Zeichen enthaelt
        &header;
        &illegal_pass_html;
        exit;
    };

    if ($query{'password'} ne $query{'password2'}) {
        &header;
        &pass_check_failed_html;
        exit;
    };

    if (-e "$data_dir/$data_nicks_file") {  # wenn nickfile existiert dann oeffnen
    	open (NICKFILE, "<$data_dir/$data_nicks_file") || &error("::open $data_dir/$data_nicks_file failed::");
    } 
    else {  # sonst erstellen
    	&create_file("$data_dir/$data_nicks_file");    
    	open (NICKFILE, "<$data_dir/$data_nicks_file") || &error("::open Nickfile failed::"); # und dann oeffnen
    }
    my @nickfile = <NICKFILE>; # Daten aus nickfile an @nickfile uebergeben
    close NICKFILE; # nickfile schliessen

    &make_matrix(@nickfile);

    # does nick already exist?
	for ($i=0; $i<=$#matrix; $i++) {
	    if (uc($matrix[$i][0]) eq uc($query{'name'})) {
		    &header;		 # wenn ja dann ausgabe existingnick.htm
		    &existingnick_html;
		    exit;
	    }
    }		# sonst fortfuehren der prozedur
            

    open (NICKFILE, ">>$data_dir/$data_nicks_file") || &error("open nickfile failed");
    flock(NICKFILE,2);

    $nickdata[0] = $query{'name'};	# nickdaten zusammenfuehren
    $nickdata[1] = $query{'password'};    
    $nickdata[2] = $query{'email'};
    $zeit = time();
    $nickdata[3] = localtime($zeit);
    $nickdata[4] = time;
    $nickdata[5] = $updatefrequency;
    $nickdata[6] = "standard";
    $nickdata[9] = $new_msg_on_top;
    $nickentry = join(';;', @nickdata);
    print NICKFILE "$nickentry\n";
                
#    flock(NICKFILE,8);
    close NICKFILE;

    if (-e "$data_dir/$data_private_file.$query{'name'}") {
    } else {
        &create_file("$data_dir/$data_private_file.$query{'name'}");
    }
    
    #MAIL TO ADMIN
    if ($mail_on_new_registration == 1) {
        open(MAIL,"|$mailprogramme -t");
        print MAIL "To: $admin_email_addresse\n";
        print MAIL "From: $admin_email_addresse (Ralfs Chat Script)\n";
        print MAIL "Subject: [CHAT] Novo apelido registrado\n\n";
        print MAIL "Um novo usu�rio foi registrado\n";
        print MAIL "Apelido: $query{'name'}\n";
        print MAIL "eMail: $query{'email'}\n";
        print MAIL "HTTP User Agent: ".$ENV{'HTTP_USER_AGENT'}."\n";
        print MAIL "Remote Addresse: ".$ENV{'REMOTE_ADDR'}."\n";
    }

    # LOG ACTION
    if ($logtype >= 1) {
        open (LOGFILE, ">>$log_dir/$log_file") || &error("::open $log_dir/$log_file failed::");
        flock(LOGFILE,2);
        print LOGFILE localtime(time)." $ENV{'REMOTE_ADDR'} [NEW USER] $query{'name'} <$query{'email'}>\n";
        close LOGFILE;
    }

    &header;
    &nickcreated_html;
}

sub clear_old_msgs_sub {
    # safile einlesen
    if (-e "$data_dir/$data_stillalive_file") { # SAfile oeffnen                
        open (SAFILE, "<$data_dir/$data_stillalive_file") || &error("opening safile failed");
        my $safile = <SAFILE>; # Daten aus safile an $safile uebergeben
        close SAFILE;
        @sa = split (/;;/, $safile);

        # Eintraege nach ueberfaelligen (> 50) durchsuchen und diese entfernen    
        my $coms_i = 0;
        for ($coms_i=1; $coms_i<=$#sa; $coms_i+=2) { 
            if ($sa[$coms_i] < (time - 50)) { # ist zeitstempel schon aelter als 50s?
                $sa[$coms_i] = "//2delete";
                $sa[$coms_i-1] = "//2delete";  # zu loeschende eintraege mit //2delete ersetzten
            }  
        }
        # alle Felder mit //2delete entfernen
    
        $templsa = $#sa; # Laenge von @sa wird in templsa gespeichert;
        for ($coms_i=0; $coms_i<=$templsa; $coms_i++) {
            $temp = shift(@sa);
            if ($temp ne "//2delete") {
                push(@sa,$temp);
            }
        }

        # wenn laenge von safile < 0 (chat empty) dann chatfile leeren
        if ($#sa < 0) {
            if (-e "$data_dir/$data_msg_file") { # CHATFILE oeffnen
                open (CHATFILE, ">$data_dir/$data_msg_file") || &error("opening chatfile failed");
                print CHATFILE "";
                close CHATFILE;
            }
        }
    }
}

sub setoptions {
    if ($query{'updatefrequency'}<$min_update_freq || $query{'updatefrequency'} eq "") {
        $query{'updatefrequency'}=$min_update_freq;
    }

	$change_password_ok = 0;
    if ($query{'change_pwd_old'} && $query{'change_pwd_new'}) {
		if ($query{'change_pwd_old'} eq $query{'password'}) {
	        if ($query{'change_pwd_new'} eq $query{'change_pwd_new2'}) {
			    if ($query{'change_pwd_new'} !~ /[;\n]/ || !$query{'change_pwd_new'}) { 
					$change_password_ok = 1;
			    	$cpw_msg="Password changed";
			   	} else {
			    	$cpw_msg="The new password may not contain \";\"";
				}
			} else {
		    	$cpw_msg="New password check failed, probably mistyped";
			}
		} else {
		    $cpw_msg="Wrong password";
		}
		&postprivatemsg("$query{'name'}","CHANGE_PWD",$cpw_msg) if ($cpw_msg);
		$query{'password'} = $query{'change_pwd_new'} if ($change_password_ok == 1);
    }

    open (NICKFILE, "<$data_dir/$data_nicks_file") || &error("::open $data_dir/$data_nicks_file failed::");
    my @nickfile = <NICKFILE>; # Daten aus nickfile an @nickfile uebergeben
    close NICKFILE; # nickfile schliessen
    
    &make_matrix(@nickfile);

    for ($i=0; $i<=$#matrix; $i++) {
        if ($matrix[$i][0] eq $query{'name'}) {
            $matrix[$i][1] = $query{'password'};
            $matrix[$i][5] = $query{'updatefrequency'};
            $matrix[$i][6] = $query{'color'};
            $matrix[$i][9] = $query{'new_msg_on_top'};
            open (NICKFILE, ">$data_dir/$data_nicks_file");
            flock(NICKFILE,2); 

            for ($i2=0; $i2<=$#matrix; $i2++) {
                print NICKFILE &join_matrix."\n";
            }
#            flock(NICKFILE,8);
            close NICKFILE;
        }
    }


    &header;
    &chatframes_html;
}

sub setuserinfo {
    &checkpass;

    open (UIFILE, "<$data_dir/$data_userinfo_file") || &error("::open $data_dir/$data_userinfo_file failed::");
    my @uifile = <UIFILE>;
    close UIFILE;
    
    &make_matrix(@uifile);
    for ($i=0; $i<=$#matrix; $i++) {
        if ($matrix[$i][0] eq $query{'name'}) {
            $info_exists=1;
        }
    }

    if ($info_exists != 1) { 
        $matrix[$#matrix+1][0] = $query{'name'}; 
    }


    for ($i=0; $i<=$#matrix; $i++) {
        if ($matrix[$i][0] eq $query{'name'}) {
            $matrix[$i][1] = $query{'realname'};
            $matrix[$i][2] = $query{'email'};
            $matrix[$i][3] = $query{'age'};
            $matrix[$i][4] = $query{'city'};
            $matrix[$i][5] = $query{'country'};
            $matrix[$i][6] = $query{'url'};
            $matrix[$i][7] = $query{'stuff'};
            $matrix[$i][8] = $query{'photo_url'};
            $matrix[$i][9] = $query{'icq_uin'};
            for ($i2=0; $i2<=9; $i2++) { 
                $matrix[$i][$i2] =~ s/;/&#59;/g;
                $matrix[$i][$i2] =~ s/</\&lt\;/g;
                $matrix[$i][$i2] =~ s/\n/<BR>/g;
            }
            open (UIFILE, ">$data_dir/$data_userinfo_file");
            flock(UIFILE,2); 

            for ($i2=0; $i2<=$#matrix; $i2++) {
                print UIFILE &join_matrix."\n";
            }
#            flock(UIFILE,8);
            close UIFILE;
        }
    }


    &header;
    &chatframes_html;
}


sub changeuserinfo {
    &checkpass;
    open (UIFILE, "<$data_dir/$data_userinfo_file") || &create_file("$data_dir/$data_userinfo_file");
    my @uifile = <UIFILE>; 
    close UIFILE;

    &make_matrix(@uifile);

    for ($i=0; $i<=$#matrix; $i++) {
        if ($matrix[$i][0] eq $query{'name'}) {
            for ($i2=0; $i2<=9; $i2++) { 
                $matrix[$i][$i2] =~ s/&#59;/;/g;
                $matrix[$i][$i2] =~ s/<BR>/\n/g;
            }
            $userinfo{'realname'}=$matrix[$i][1];
            $userinfo{'email'}=$matrix[$i][2];
            $userinfo{'age'}=$matrix[$i][3];
            $userinfo{'city'}=$matrix[$i][4];
            $userinfo{'country'}=$matrix[$i][5];
            $userinfo{'url'}=$matrix[$i][6];
            $userinfo{'stuff'}=$matrix[$i][7];
            $userinfo{'photo_url'}=$matrix[$i][8];
            $userinfo{'icq_uin'}=$matrix[$i][9];
        }
    }

    &header;
    &changeuserinfo_html;
}

sub show_users {
    &header;
    print &number_of_users;
}

sub number_of_users {
    open (SAFILE, "<$data_dir/$data_stillalive_file");
    flock(SAFILE,2); 
    my $safile = <SAFILE>; # Daten aus safile an $safile uebergeben
#    flock(SAFILE,8);
    close SAFILE;

    @sa = split (/;;/, $safile);

    @sa = &repair_safile(@sa) if (($#sa+1) % 2 == 1); # wenn safile fehlerhaft -> repair

    # Eintraege nach ueberfaelligen (aelter als 50s) durchsuchen und diese entfernen    
    for ($i=1; $i<=$#sa; $i+=2) { 
        if ($sa[$i] < (time - 50)) { # ist zeitstempel schon aelter als 50s?
            $sa[$i] = "//2delete";
            $sa[$i-1] = "//2delete";  # zu loeschende eintraege mit //2delete ersetzten
        }  
    }
    # alle Felder mit //2delete entfernen
    $templsa = $#sa; # Laenge von @sa wird in templsa gespeichert;
    for ($i=0; $i<=$templsa; $i++) {
        $temp = shift(@sa);
        if ($temp ne "//2delete") {
            push(@sa,$temp);
        }
    }

    $safile = join(';;', @sa);
    
    open (SAFILE, ">$data_dir/$data_stillalive_file");
    flock(SAFILE,2);

    print SAFILE $safile;

#    flock(SAFILE,8);
    close SAFILE;
    
    $nrusers = ($#sa+1) / 2;
    return $nrusers;
}

sub gotourl {
    &header;
    print "<HTML>";
    print "<meta http-equiv=\"refresh\" content=\"0; URL=$query{'url'}\">";
    print "<BODY>please wait</BODY>";
    print "</HTML>";
}

sub max_user_limit {
    if (&number_of_users >= $max_users && $max_users >= 0) {
        if ($query{'password'} =~ / $masterpassword$/) {
            $query{'password'} = substr($query{'password'}, 0, index($query{'password'}, " "));
        } else {
            &header;
            &chat_is_full_html;
            exit;
        }
    }
}

sub check_for_memo {
    &create_file("$data_dir/$data_memo_file") if (!-e "$data_dir/$data_memo_file");
    open (MEMOFILE, "<$data_dir/$data_memo_file") || &error("opening memofile failed");
    flock(MEMOFILE,2); 
    my @memofile = <MEMOFILE>; 
    close MEMOFILE;

	@cfmsave_matrix = @matrix;
	$save_i = $i;
    &make_matrix(@memofile);


    # Eintraege nach ueberfaelligen (aelter als $days_to_keep_memos) durchsuchen und diese entfernen    
    for ($i=0; $i<=$#matrix; $i++) { 
        if ($matrix[$i][3] < (time - $days_to_keep_memos*60*60*24)) { # ist zeitstempel schon aelter als 50s?
            $matrix[$i] = "//2delete";
        }  
    }

    for ($cfm_i=0; $cfm_i<=$#matrix; $cfm_i++) {
		if ($matrix[$cfm_i][0] eq $query{'name'}) {
		    &postprivatemsg($query{'name'},"MEMO","<B>Memo from $matrix[$cfm_i][1] (".localtime($matrix[$cfm_i][3])."): $matrix[$cfm_i][2]</B>");
            $matrix[$cfm_i] = "//2delete";
		}
	}

    # alle Felder mit //2delete entfernen
    $templ = $#matrix; # Laenge von @sa wird in templsa gespeichert;
    for ($i=0; $i<=$templ; $i++) {
        $temp = shift(@matrix);
        if ($temp ne "//2delete") {
            push(@matrix,$temp);
        }
    }

	open (MEMOFILE, ">$data_dir/$data_memo_file");
	flock(MEMOFILE,2); 
	for ($i2=0; $i2<=$#matrix; $i2++) {
		print MEMOFILE &join_matrix."\n";
	}
	close MEMOFILE;

	@matrix = @cfmsave_matrix;
	$i = $save_i;
}

sub send_pwd {
    open (NICKFILE, "<$data_dir/$data_nicks_file") || &error("::open $data_dir/$data_nicks_file failed::");
    my @nickfile = <NICKFILE>; # Daten aus nickfile an @nickfile uebergeben
    close NICKFILE; # nickfile schliessen
    
    &make_matrix(@nickfile);

    for ($i=0; $i<=$#matrix; $i++) {
        if ($matrix[$i][0] eq $query{'name'}) {
			$query{'email'} = $matrix[$i][2];
			$query{'password'} = $matrix[$i][1]
		}
	}

	# mail to user
    open(MAIL,"|$mailprogramme -t");
	print MAIL "To: $query{'email'}\n";
    print MAIL "From: $admin_email_addresse ($html_title)\n";
    print MAIL "Subject: [CHAT] Sua Senha\n\n";
    print MAIL "Sua senha � $query{'password'} (Nick: $query{'name'})\n\n";
	print MAIL "- the admin";
	close MAIL;

	&header;
	&send_pwd_html;
}
