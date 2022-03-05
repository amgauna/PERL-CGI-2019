#! /usr/local/bin/tclsh
set request_method $env(REQUEST_METHOD)
if {$request_method =="GET"}{
et form_info $env(QUERY_STRING)
} else {
set size_of_form_information $env(CONTENT_LENGTH)
set form_info [read stdin $size_of_form_information]
}
