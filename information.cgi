#! /usr/local/bin/tclsh
set size_of_form_information $env(CONTENT_LENGTH)
set form_info [read stdin $size_of_form_information]
set par [split $form_info = ]
set field_name [lindex $par 0]
set command [lindex $par 1]

puts "Content-type: text/plain", "\n\n"
if {$command == "guest"} {
puts "usr/local/bin/guest"
} elsif {$command == "mgi"} {
puts "usr/ucb/mgi"
} else {
puts "usr/local/bin/outro";
}
exit(0);
